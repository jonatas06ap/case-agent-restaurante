"""Detector de ambiguidade por LLM (Dia 3) — resposta JSON estruturada.

Roda UMA vez por turno, ANTES do loop ReAct (design doc §5 passo 2). Objetivo:
quando o pedido ja nasce ambiguo (multiplas interpretacoes que mudam a acao) ou
falta um dado essencial que so o operador pode dar, devolver UMA pergunta de
esclarecimento e encerrar o turno — em vez de gastar tool calls para descobrir,
no meio do loop, que nao da pra decidir.

Decisoes de robustez:
- Conservador: so marca ambiguo quando a ambiguidade MUDA A ACAO. Pedir
  confirmacao de coisas obvias deixa o agente chato e lento.
- Usa o historico (`state.messages`) para resolver referencias: "cancela a
  reserva dele" nao e ambiguo se o turno anterior ja fixou quem e "ele".
- Parse JSON tolerante: o modelo pode embrulhar o JSON em texto ou ```json. Em
  qualquer falha de parse, degrada para NAO ambiguo (comportamento do Dia 2) —
  nunca derruba o turno.
- temperatura 0, SEM tools nesta chamada.

A pre-classificacao aqui coexiste com a ambiguidade que so aparece nos dados (o
LLM do loop, vendo 2 resultados, pergunta). Esta pega o enunciado; o loop pega o
resto.
"""

from __future__ import annotations

import json
import logging
import re

logger = logging.getLogger("dionisio.safety.ambiguity")

_SYSTEM = """Voce e um classificador de ambiguidade para um agente que opera a API \
de um CRM de restaurantes (o Dionisio). Sua UNICA tarefa e decidir se o pedido do \
operador pode ser executado sem perguntar nada, ou se ha uma ambiguidade que MUDA A \
ACAO e exige esclarecimento antes de agir.

Marque ambiguous=true SOMENTE quando:
- o pedido tem 2+ interpretacoes que levariam a acoes diferentes (ex: "cancela o \
pedido do Joao" quando nao da pra saber qual pedido/cliente), OU
- falta um dado essencial que o operador deveria fornecer e que o sistema nao tem \
como descobrir sozinho (ex: um valor, uma data, um nome que nao foi dito).

Marque ambiguous=false (seja CONSERVADOR — este e o caso comum) quando:
- o pedido e claro, mesmo que exija varios passos para executar;
- o dado que falta pode ser DESCOBERTO via API (ex: "quantas reservas pra hoje" — \
a data e hoje, o numero vem da API; NAO e ambiguo);
- uma referencia ("ela", "esse cliente", "a reserva dele") ja foi fixada no \
historico da conversa.

NAO marque ambiguo so porque o pedido e destrutivo ou de alto impacto — isso e \
tratado por outro mecanismo (confirmacao), nao por voce.

NAO marque ambiguo um pedido IMPOSSIVEL. A API do Dionisio NAO tem nenhum canal de \
comunicacao/notificacao (nada de SMS, WhatsApp, e-mail, "avisar" cliente). Se o pedido \
for enviar mensagem/notificar alguem, ele e impossivel — NAO peca telefone, e-mail ou \
canal (seria pedir um dado inutil). Deixe passar (ambiguous=false): o agente vai explicar \
a limitacao adiante. Sua tarefa nao e julgar impossibilidade, e so ambiguidade.

Responda SOMENTE com um objeto JSON, sem texto ao redor, neste formato exato:
{"ambiguous": true|false, "clarifying_question": "<uma unica pergunta especifica>" ou null}
Se ambiguous=false, clarifying_question deve ser null."""


def _recent_history(state, max_msgs: int = 6) -> list[dict]:
    """Ultimas mensagens user/assistant (texto) para resolver referencias."""
    out: list[dict] = []
    for msg in state.messages:
        role = msg.get("role")
        content = msg.get("content")
        if role in ("user", "assistant") and isinstance(content, str) and content:
            out.append({"role": role, "content": content})
    return out[-max_msgs:]


def _parse_verdict(text: str) -> dict:
    """Extrai {ambiguous, clarifying_question} tolerando texto/```json ao redor."""
    if not text:
        return {"ambiguous": False, "clarifying_question": None}
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"ambiguous": False, "clarifying_question": None}
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        logger.debug("verdict JSON malformado, tratando como nao ambiguo: %r", text)
        return {"ambiguous": False, "clarifying_question": None}

    ambiguous = bool(data.get("ambiguous"))
    question = data.get("clarifying_question")
    if not ambiguous or not isinstance(question, str) or not question.strip():
        # sem pergunta valida -> nao trava o turno
        return {"ambiguous": False, "clarifying_question": None}
    return {"ambiguous": True, "clarifying_question": question.strip()}


async def detect_ambiguity(user_input: str, state, llm) -> dict:
    """Classifica o pedido. Retorna {"ambiguous": bool, "clarifying_question": str|None}.

    Falha graciosa: qualquer erro (LLM/rede/parse) -> nao ambiguo (degrada para o
    comportamento do Dia 2), nunca derruba o turno.
    """
    messages = [
        {"role": "system", "content": _SYSTEM},
        *_recent_history(state),
        {"role": "user", "content": f"Pedido a classificar:\n{user_input}"},
    ]
    try:
        msg = await llm.complete(messages=messages, tools=None)
    except Exception:  # rede/LLM fora do controle — nao trava o turno
        logger.warning("detect_ambiguity: chamada LLM falhou, seguindo como nao ambiguo", exc_info=True)
        return {"ambiguous": False, "clarifying_question": None}
    return _parse_verdict(msg.content or "")
