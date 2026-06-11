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
from rag.retriever import RetrievalResult

logger = logging.getLogger("dionisio.agent.planner")

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

PEDIDO IMPOSSIVEL (perguntar ou recusar — nunca fingir):
- A API do Dionisio cobre clientes, reservas, pedidos, cupons, promocoes, delivery, iFood, \
loja e analytics. NAO existe nenhum endpoint de comunicacao/notificacao: nao da pra \
enviar SMS, WhatsApp, e-mail ou "avisar" um cliente. Se o pedido depender disso, diga \
claramente que essa parte nao e executavel pela API — execute o que for possivel e seja \
honesto sobre o que ficou de fora. NUNCA diga que notificou/avisou alguem.
- Se uma operacao retornar erro ou nao encontrar dados, explique o que voce tentou, o que \
encontrou e o que faltaria. Nunca afirme que executou uma acao que falhou ou foi cancelada.
- Se uma acao foi CANCELADA por falta de confirmacao do operador, reporte que ela NAO foi \
realizada — nao a descreva como concluida.

TIMESTAMPS:
- Todos os campos de tempo da API sao timestamp em MILISSEGUNDOS (epoch Unix): campos \
*At, start, end, periodStart, periodEnd.
- Endpoints de listagem usam `date=YYYY-MM-DD`. Para "hoje", use a data de hoje informada abaixo.

QUANDO TERMINAR:
- Apos coletar os dados necessarios, responda ao operador em portugues, de forma direta e \
sem jargao tecnico, CITANDO os numeros/dados reais retornados pela API (ex: "Ha 7 reservas \
para hoje"). Essa resposta final e texto puro (sem chamar mais ferramentas)."""


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


def build_tools(retrieval: RetrievalResult) -> tuple[list[dict], dict]:
    """Monta as tools (formato OpenAI) e o mapa reverso para o executor.

    fn_map[fn_name] = {operation_id, method, path, locations}
    `path` e o path do spec (com prefixo /api/case-mock); o executor remove o prefixo
    que ja esta no base_url do client.
    """
    tools: list[dict] = []
    fn_map: dict[str, dict] = {}

    for op in retrieval.operations:
        op_id = op.operation_id
        fn_name = op_id.replace(".", "_")  # OpenAI exige ^[a-zA-Z0-9_-]+$
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

    return tools, fn_map


def build_messages(state, retrieval: RetrievalResult) -> list[dict]:
    """Monta a lista de mensagens: system (prompt + data + docs) + historico do estado."""
    return [{"role": "system", "content": build_system_content(retrieval)}, *state.messages]
