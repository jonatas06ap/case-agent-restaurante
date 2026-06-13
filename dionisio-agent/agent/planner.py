"""Planner — system prompt, montagem das tools a partir do retrieval e das messages.

Decisao-chave (ver History/dia_1.md §3.5): o texto EMBEDADO de cada operacao e so uma
frase curta de intencao. Os parametros/body para montar uma chamada valida NAO vem do
`full_text`; vem do OpenAPI spec local. Aqui carregamos o spec uma vez e, por operationId,
montamos um JSON Schema tipado (query + path params + campos de body).

As tools sao montadas UMA vez por turno a partir do retrieval inicial; as iteracoes do
loop ReAct reaproveitam essas tools.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from rag.indexer import _deref  # resolve um nivel de $ref no spec
from rag.retriever import OperationDoc, RetrievalResult

from . import calculator

logger = logging.getLogger("dionisio.agent.planner")

# Expansao de dominio (Dia 6): teto de operacoes-irmas injetadas alem do top-k.
_DOMAIN_EXPANSION_CAP = 15

_SPEC_PATH = Path(__file__).resolve().parent.parent / "rag" / "openapi_spec.json"
_HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


# ===========================================================================
# Helpers de data/tempo (timestamps da API sao em MILISSEGUNDOS)
# ===========================================================================
def today_str() -> str:
    """Data local de hoje no formato YYYY-MM-DD (usado em `?date=`)."""
    return datetime.now().strftime("%Y-%m-%d")


def day_bounds_ms(date: str | None = None) -> tuple[int, int]:
    """Inicio (00:00) e fim (23:59:59.999) do dia, em ms epoch. `date`=YYYY-MM-DD."""
    base = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    start = base.replace(hour=0, minute=0, second=0, microsecond=0)
    end = base.replace(hour=23, minute=59, second=59, microsecond=999000)
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000)


# ===========================================================================
# System prompt
# ===========================================================================
SYSTEM_PROMPT = """Voce e o assistente interno do Dionisio, um CRM de restaurantes. \
Operadores humanos te fazem pedidos em linguagem natural e voce opera a API REST do \
Dionisio para responde-los.

REGRAS (inviolaveis):
- Use SOMENTE os dados retornados pela API. NUNCA invente IDs, nomes, numeros ou campos.
- Quando precisar de um dado (ex: o ID de uma reserva), descubra-o chamando a operacao \
adequada antes — nunca chute.
- Se faltar informacao para atender o pedido, diga claramente o que falta em vez de adivinhar.
- Voce so tem acesso as ferramentas (operacoes da API) que foram fornecidas neste turno. \
Se nenhuma serve, explique a limitacao.
- Ao montar argumentos, respeite os tipos do schema da ferramenta.
- Se voce chamar uma ferramenta e receber "ferramenta desconhecida"/"nao existe", voce ERROU \
o NOME — a capacidade pode existir com outro nome. Olhe a lista de ferramentas deste turno (e \
as sugestoes que a observacao trouxer) e chame o nome correto. NUNCA conclua que algo e \
impossivel so porque um nome de ferramenta falhou: so declare impossivel depois de conferir \
a lista fornecida.
- CALCULO: para QUALQUER conta — soma, media, percentual, contagem, ordenacao/ranking — use a \
ferramenta `calcular`. NUNCA calcule "de cabeca" no texto (erra conta e ordem). Cite o numero \
que a ferramenta devolveu, igual a um dado da API.

ENCADEAMENTO (pedidos multi-step):
- DECOMPONHA o pedido em passos e execute-os EM ORDEM, esperando a observacao (resposta da \
API) de cada passo ANTES de montar o proximo. Ex: para remarcar a reserva "do Joao", \
primeiro descubra o clientId (clients.search), depois a reserva dele (reservations.list), \
depois confirme a disponibilidade (reservations.availability) e so entao remarque.
- USE os IDs e valores que a API JA retornou nos passos anteriores (clientId, reservationId, \
horarios, datas) — eles estao no historico desta conversa. NUNCA invente um ID, horario ou \
campo: se faltar um dado, BUSQUE-o com a operacao adequada antes de prosseguir.
- NAO dispare em paralelo passos que dependem um do outro: nao chame uma remarcacao/atribuicao \
antes de ter, vindo da API, o ID alvo e a verificacao necessaria (ex: "tem mesa?").
- Ao preservar "o mesmo horario" numa remarcacao, reaproveite o horario (time-of-day) da \
reserva original (campo start, em ms) — nao reinvente o horario.
- Para descobrir QUEM pediu um prato/item num periodo (ex: "quem pediu o prato X nos ultimos 7 \
dias"), liste o historico de pedidos de UMA vez — use um limite alto (ex: limit=200, com \
offset se houver mais paginas), SEM filtrar por dia. Depois filtre LOCALMENTE: olhe os itens \
de cada pedido pra achar o prato e use a data (campo em ms) pra checar a janela do periodo. \
NUNCA liste dia a dia (uma chamada por data gasta um passo por dia e estoura o limite de \
iteracoes antes de voce responder). Junte os clientes (nome/telefone) dos pedidos que tinham \
o item — essa e a lista a entregar. Se NENHUM pedido do periodo tiver o item, a resposta \
correta e dizer que ninguem pediu aquele prato no periodo: lista vazia e um resultado honesto \
e completo, nao motivo pra continuar tentando.

PEDIDO IMPOSSIVEL (perguntar ou recusar — nunca fingir):
- Voce cuida de clientes, reservas, pedidos, cupons, promocoes, delivery, iFood, loja e \
relatorios. Voce NAO consegue ENVIAR MENSAGENS/AVISOS aos clientes (SMS, WhatsApp, e-mail, \
ligacao): nao da pra "avisar", "comunicar" ou "notificar" alguem por aqui. Se o pedido pedir \
isso, faca o que for possivel e diga, em linguagem simples, que o aviso ao cliente precisa ser \
feito por fora (no sistema do restaurante / direto com o cliente). NUNCA diga que avisou ou \
notificou alguem.
- Voce tambem NAO mexe no CARDAPIO: nao da pra adicionar, remover ou desativar um prato/item. \
Voce so consegue CONSULTAR o que foi pedido (historico de pedidos, itens mais vendidos). Se \
pedirem para tirar um prato do cardapio, diga em linguagem simples que isso e feito no sistema \
do restaurante, nao por aqui — NUNCA diga que removeu ou desativou um prato.
- Quando um pedido MISTURA o que da e o que nao da (ex: "remove o prato X e avisa quem pediu"), \
FACA a parte possivel (ex: levante quem pediu o prato) e seja honesto sobre a parte que nao da \
— entregue o resultado ao operador para ele agir. Nunca finja ter feito o que voce nao consegue.
- IMPORTANTE — antes de dizer "nao consigo": confira a lista de ferramentas deste turno. Se a \
operacao existe (listar, atribuir cupom a um grupo, remarcar, cancelar...), USE-A — nao recuse \
algo que e possivel. So e impossivel comunicacao com cliente e mexer no cardapio; o resto, se \
estiver na lista, da pra fazer.
- Se uma operacao der erro ou nao achar dados, explique em linguagem simples o que voce tentou, \
o que achou e o que faltou. Nunca afirme ter feito uma acao que falhou ou foi cancelada.
- Se uma acao foi CANCELADA por falta de confirmacao do operador, diga que ela NAO foi feita — \
nao a descreva como concluida.
- AO FALAR DE UMA LIMITACAO, fale como operador, nunca como sistema: diga "nao consigo enviar \
o aviso aos clientes por aqui", NAO "a API nao tem endpoint de notificacao". Nada de "API", \
"endpoint", "ferramenta", "operacao" ou nome tecnico na fala ao operador.

TIMESTAMPS:
- Todos os campos de tempo da API sao timestamp em MILISSEGUNDOS (epoch Unix): campos \
*At, start, end, periodStart, periodEnd.
- Endpoints de listagem usam `date=YYYY-MM-DD`. Para "hoje", use a data de hoje informada abaixo.

QUANDO TERMINAR:
- Apos coletar os dados necessarios, responda ao operador em portugues, de forma direta e \
pratica, no tom de quem trabalha no salao de um restaurante — nao de quem opera uma API.
- GROUNDING: cite SO os numeros, nomes, telefones, IDs e horarios que VIERAM de uma \
observacao (resposta da API). Se um dado nao apareceu numa observacao, NAO o afirme. Nada \
de valores aproximados, arredondados ou "provaveis": ou veio da API, ou voce nao sabe.
- SEM JARGAO DE API na fala final: nao mencione nomes de operacoes/endpoints \
(reservations.reschedule, orders.list), nomes de campos do JSON (couponsUsed, clientId, \
start em ms), metodos HTTP, status codes nem "a API". Traduza para a linguagem do operador \
(ex: "remarquei a reserva da Ana para sabado as 20h" — nao "executei reservations.reschedule \
com start=..."; "11 clientes gastaram mais de R$500 e nunca usaram cupom" — nao "filtrei por \
couponsUsed=0"). Os detalhes tecnicos ficam no log, nao na resposta ao operador.
- Essa resposta final e texto puro (sem chamar mais ferramentas)."""


def build_system_content(retrieval: RetrievalResult) -> str:
    """System prompt + data de hoje + docs de negocio recuperados (contexto auxiliar)."""
    parts = [SYSTEM_PROMPT, f"\nDATA DE HOJE: {today_str()}"]
    if retrieval.docs:
        parts.append(
            "\nDOCUMENTACAO DE NEGOCIO (contexto auxiliar — traduz linguagem de negocio "
            "para filtros da API):"
        )
        for d in retrieval.docs:
            parts.append(f"\n## {d.section}\n{d.text}")
    return "\n".join(parts)


# ===========================================================================
# Spec -> JSON Schema das tools
# ===========================================================================
@lru_cache(maxsize=1)
def _load_spec() -> dict:
    return json.loads(_SPEC_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _operations_by_id() -> dict[str, dict]:
    """Mapa operationId -> {method, path, operation} a partir do spec."""
    spec = _load_spec()
    out: dict[str, dict] = {}
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if method.lower() not in _HTTP_METHODS:
                continue
            op_id = op.get("operationId")
            if op_id:
                out[op_id] = {"method": method.upper(), "path": path, "op": op}
    return out


def _schema_property(spec: dict, schema: dict) -> dict:
    """Converte um schema do OpenAPI numa propriedade JSON Schema enxuta."""
    schema = _deref(spec, schema or {})
    prop: dict = {"type": schema.get("type", "string")}
    if "enum" in schema:
        prop["enum"] = schema["enum"]
    if schema.get("description"):
        prop["description"] = schema["description"]
    if "example" in schema:
        prop.setdefault("description", "")
        prop["description"] = (prop["description"] + f" (ex: {schema['example']})").strip()
    return prop


def _build_parameters_schema(op_id: str) -> tuple[dict, dict]:
    """Retorna (json_schema, locations).

    json_schema: {"type":"object","properties":{...},"required":[...]} para a tool.
    locations: {param_name: "path"|"query"|"body"} para o executor rotear os args.
    """
    spec = _load_spec()
    entry = _operations_by_id().get(op_id)
    properties: dict[str, dict] = {}
    required: list[str] = []
    locations: dict[str, str] = {}

    if not entry:
        return {"type": "object", "properties": {}}, locations

    op = entry["op"]

    # --- path & query params ---
    for p in op.get("parameters", []):
        p = _deref(spec, p)
        name = p.get("name")
        loc = p.get("in")
        if not name or loc not in ("path", "query"):
            continue
        prop = _schema_property(spec, p.get("schema", {}))
        pdesc = p.get("description")
        if pdesc:  # descricao do parametro tem prioridade sobre a do schema/exemplo
            existing = prop.get("description")
            prop["description"] = f"{pdesc} {existing}".strip() if existing else pdesc
        properties[name] = prop
        locations[name] = loc
        # path params sao sempre obrigatorios; query so se marcado
        if loc == "path" or p.get("required"):
            required.append(name)

    # --- request body (application/json) ---
    request_body = _deref(spec, op.get("requestBody", {}))
    content = request_body.get("content", {})
    body_schema = _deref(spec, (content.get("application/json") or {}).get("schema", {}))
    body_props = body_schema.get("properties", {})
    body_required = set(body_schema.get("required", []))
    for field, fschema in body_props.items():
        properties[field] = _schema_property(spec, fschema)
        locations[field] = "body"
        if field in body_required:
            required.append(field)

    json_schema: dict = {"type": "object", "properties": properties}
    if required:
        json_schema["required"] = required
    return json_schema, locations


def _expand_domain_siblings(operations: list[OperationDoc]) -> list[OperationDoc]:
    """Injeta operacoes-irmas dos dominios tocados, fora do top-k (Dia 6).

    Falso negativo medido (`Context/simulacao.md`): o retrieval roda UMA vez por
    turno, ancorado no texto ORIGINAL do usuario, e congela a lista de tools. Num
    pedido multi-step ("desmarque as reservas do dia 19") ele traz `reservations.cancel`
    mas nao `reservations.list` — a operacao que o agente precisa para *encontrar*
    as reservas. O LLM emite o nome certo, recebe "ferramenta desconhecida" e conclui
    que a capacidade nao existe. Aqui garantimos que, tocando um dominio, TODAS as
    operacoes dele fiquem disponiveis como tool (inclui `reservations.list` e o
    `coupons.assignGroup` da campanha). Em memoria, a partir do spec local — sem rede,
    sem reindex. A barreira de confirmacao no executor segue valendo para as destrutivas.
    """
    retrieved = {op.operation_id for op in operations}
    # dominios na ordem de relevancia (operations ja vem ordenado por score)
    domains: list[str] = []
    for op in operations:
        d = op.operation_id.split(".")[0]
        if d not in domains:
            domains.append(d)

    by_id = _operations_by_id()
    extra: list[OperationDoc] = []
    for domain in domains:
        for op_id, entry in by_id.items():
            if len(extra) >= _DOMAIN_EXPANSION_CAP:
                return extra
            if op_id in retrieved or op_id.split(".")[0] != domain:
                continue
            op = entry["op"]
            summary = op.get("summary", op_id)
            extra.append(
                OperationDoc(
                    operation_id=op_id,
                    method=entry["method"],
                    path=entry["path"],
                    domain=domain,
                    destructive=bool(op.get("x-destructive", False)),
                    summary=summary,
                    full_text=summary,
                    score=0.0,
                )
            )
    return extra


def build_tools(retrieval: RetrievalResult) -> tuple[list[dict], dict]:
    """Monta as tools (formato OpenAI) e o mapa reverso para o executor.

    fn_map[fn_name] = {operation_id, method, path, locations}
    `path` e o path do spec (com prefixo /api/case-mock); o executor remove o prefixo
    que ja esta no base_url do client.

    Alem do top-k recuperado, injeta (a) as operacoes-irmas dos dominios tocados
    (anti-falso-negativo) e (b) a calculadora local (sempre disponivel).
    """
    tools: list[dict] = []
    fn_map: dict[str, dict] = {}

    operations = list(retrieval.operations) + _expand_domain_siblings(retrieval.operations)
    for op in operations:
        op_id = op.operation_id
        fn_name = op_id.replace(".", "_")  # OpenAI exige ^[a-zA-Z0-9_-]+$
        if fn_name in fn_map:  # irma ja presente no top-k; nao duplica
            continue
        parameters, locations = _build_parameters_schema(op_id)
        description = (op.summary or op.full_text or op_id).lstrip("⚠️ ").strip()

        tools.append(
            {
                "type": "function",
                "function": {
                    "name": fn_name,
                    "description": description,
                    "parameters": parameters,
                },
            }
        )
        fn_map[fn_name] = {
            "operation_id": op_id,
            "method": op.method,
            "path": op.path,
            "locations": locations,
        }

    # Calculadora local: tool deterministica, sempre presente, despachada sem API.
    tools.append(calculator.build_tool())
    fn_map[calculator.TOOL_NAME] = dict(calculator.FN_MAP_ENTRY)

    return tools, fn_map


def build_messages(state, retrieval: RetrievalResult) -> list[dict]:
    """Monta a lista de mensagens: system (prompt + data + docs) + historico do estado."""
    return [{"role": "system", "content": build_system_content(retrieval)}, *state.messages]
