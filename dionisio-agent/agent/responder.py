"""Responder — sintese da resposta final ao operador.

O loop ReAct (core.py) sai quando o LLM responde texto puro (sem tool_calls): esse texto
JA e a resposta final, sintetizada pelo proprio modelo com grounding (o system prompt
instrui a citar os dados reais). Aqui apenas extraimos esse texto — "formatacao direta",
conforme o prompt do Dia 2 permite. Se, por algum motivo, o ultimo turno do LLM nao trouxe
texto, fazemos uma ultima chamada de sintese explicita como fallback.

`partial_failure` produz uma mensagem honesta quando o loop estoura o limite de iteracoes.
"""

from __future__ import annotations

from .state import ConversationState

_SYNTH_INSTRUCTION = (
    "Com base nas observacoes acima, responda agora ao operador em portugues, de forma "
    "direta e pratica, no tom de quem trabalha no restaurante. Cite SO os dados que vieram "
    "das observacoes (numeros, nomes, telefones, horarios) — nao invente nem aproxime. Nao "
    "use jargao de API na resposta: nada de nomes de operacoes, campos do JSON, status HTTP "
    "ou 'a API'. Nao chame mais ferramentas."
)


async def synthesize(state: ConversationState, llm=None, messages: list[dict] | None = None) -> str:
    """Retorna a resposta final. Usa o ultimo texto do assistant; senao sintetiza."""
    text = state.last_assistant_text()
    if text:
        return text

    if llm is None or messages is None:
        return "Concluido, mas nao consegui formular um resumo da resposta."

    synth_messages = [*messages, {"role": "user", "content": _SYNTH_INSTRUCTION}]
    msg = await llm.complete(messages=synth_messages, tools=None)
    final = msg.content or "Concluido."
    state.messages.append({"role": "assistant", "content": final})
    return final


def partial_failure(state: ConversationState) -> str:
    """Mensagem honesta de falha parcial ao estourar o limite de iteracoes."""
    tried = ", ".join(
        f"{a.operation_id} ({'ok' if a.ok else 'falhou'})" for a in state.actions_taken
    )
    detail = f" Tentei: {tried}." if tried else ""
    return (
        "Nao consegui concluir o pedido dentro do limite de passos."
        f"{detail} Pode reformular ou detalhar melhor o que precisa?"
    )
