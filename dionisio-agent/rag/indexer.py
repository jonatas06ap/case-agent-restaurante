"""Indexador do RAG: OpenAPI spec + docs de negocio -> ChromaDB (persistido).

Dois namespaces:
- `api_operations`: 1 documento por operacao da API (texto rico + metadados).
- `business_docs`: chunks dos docs do GitBook (por secao `##`).

Fonte LOCAL-FIRST: usa os arquivos ja baixados (rag/openapi_spec.json e rag/docs/*.md);
faz fetch de rede so como fallback se o arquivo local faltar.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

import chromadb
import httpx

from .embeddings import (
    DOCS_COLLECTION,
    OPERATIONS_COLLECTION,
    get_embedding_function,
)

logger = logging.getLogger("dionisio.rag.indexer")

_HTTP_METHODS = {"get", "post", "put", "patch", "delete"}

# "Use when" curado: uma frase CURTA e liderada pela acao, em linguagem de
# negocio (PT). Decisao empirica (ver README/notas): o embedder local multilingue
# faz mean-pooling, entao documentos longos diluem o sinal e empatam o ranking —
# frases curtas e distintas discriminam muito melhor. Quando nao ha dica, cai no
# summary do spec (ja curto). Nao altera a chamada HTTP, so o texto embedado.
_OPERATION_HINTS = {
    "clients.inactive": "Clientes inativos; disparar campanha de reativacao com cupom.",
    "clients.reservations": "Reservas feitas por um cliente especifico.",
    "reservations.reschedule": "Remarcar a reserva para sabado ou outro dia.",
    "coupons.create": "Criar cupom de desconto para campanha de reativacao.",
    "coupons.assignGroup": "Distribuir cupons da campanha para um grupo de clientes; "
        "disparar campanha com cupom.",
    "delivery.createPause": "Pausar o delivery e interromper novos pedidos de entrega.",
    "orders.list":
        "Pedidos feitos pelos clientes; quem pediu um prato/item num periodo recente.",
    "analytics.topItems":
        "Pratos/itens mais pedidos do cardapio; ranking de itens vendidos.",
    "orders.stats":
        "Ticket medio e valor medio por pedido; total/contagem de pedidos; "
        "faturamento por pedido; estatisticas resumidas dos pedidos.",
    "promotions.update":
        "Mudar o horario, as condicoes ou os dados de uma promocao que ja existe; "
        "editar/ajustar uma promocao.",
}
_RAG_DIR = Path(__file__).resolve().parent
_SPEC_PATH = _RAG_DIR / "openapi_spec.json"
_DOCS_DIR = _RAG_DIR / "docs"

# Markdown minimo do prompt — fallback final se nao houver docs locais nem GitBook.
_FALLBACK_DOCS = """## Clientes e grupos
- Cliente inativo: cliente que nao realizou visita (reserva completed) nos ultimos N dias (padrao: 60)
- Top spenders: clientes rankeados por gasto total no periodo
- Grupo de clientes: segmento criado manualmente para campanhas direcionadas

## Reservas
- Status pipeline: pending -> confirmed -> seated -> completed
- Cancelamento: irreversivel; requer reasonCode
- Remarcacao: irreversivel no sentido de que o horario original e perdido; requer novo start em timestamp ms
- Disponibilidade: consulte /reservations/availability?date=YYYY-MM-DD para saber slots livres antes de criar ou remarcar
- Areas disponiveis: area_salao, area_varanda, area_mezanino

## Campanhas e cupons
- Campanha de reativacao: fluxo tipico = (1) buscar clientes inativos, (2) criar cupom com beneficio, (3) assign-group para gerar instancias por cliente
- Cupom desativado e irreversivel
- Instancias de cupom: cada cliente recebe um codigo unico gerado pelo assign-group

## Pedidos
- Cancelamento de pedido e irreversivel
- Status possiveis: pending, confirmed, preparing, ready, delivered, cancelled

## Delivery
- Pausa de delivery interrompe recebimento de pedidos novos
- Para encerrar uma pausa: DELETE /delivery/pauses/{id}

## Timestamps
- Todos os campos *At, start, end, periodStart, periodEnd usam timestamp em milissegundos (ms) desde epoch Unix
- Para "hoje": use datetime.now() convertido para ms
- Para "proxima quinta": calcule o timestamp do inicio do dia (00:00 local) em ms
"""


# ===========================================================================
# Resolucao de $ref no OpenAPI
# ===========================================================================
def _resolve_ref(spec: dict, ref: str) -> dict:
    """Resolve um $ref local (#/components/...). Retorna {} se nao encontrado."""
    node: Any = spec
    for part in ref.lstrip("#/").split("/"):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return {}
    return node if isinstance(node, dict) else {}


def _deref(spec: dict, node: dict) -> dict:
    """Segue um unico nivel de $ref se presente."""
    if isinstance(node, dict) and "$ref" in node:
        return _resolve_ref(spec, node["$ref"])
    return node


# ===========================================================================
# api_operations
# ===========================================================================
def load_spec(base_url: str | None = None) -> dict:
    """Carrega o spec local; se ausente, faz fetch de docs.json."""
    if _SPEC_PATH.exists():
        logger.info("Spec local: %s", _SPEC_PATH)
        return json.loads(_SPEC_PATH.read_text(encoding="utf-8"))

    if not base_url:
        raise FileNotFoundError(f"Spec local ausente em {_SPEC_PATH} e base_url nao informado")

    root = base_url.replace("/api/case-mock", "").rstrip("/")
    url = f"{root}/api/case-mock/docs.json"
    logger.warning("Spec local ausente — fetch de %s", url)
    resp = httpx.get(url, timeout=30.0)
    resp.raise_for_status()
    return resp.json()


def _format_parameters(spec: dict, params: list[dict]) -> str:
    parts = []
    for p in params:
        p = _deref(spec, p)
        name = p.get("name", "?")
        loc = p.get("in", "?")
        desc = p.get("description", "")
        ptype = (p.get("schema") or {}).get("type", "")
        parts.append(f"{name} ({loc}): {desc} ({ptype})".strip())
    return ", ".join(parts) if parts else "nenhum"


def _format_body_fields(spec: dict, request_body: dict) -> str:
    request_body = _deref(spec, request_body)
    content = request_body.get("content", {})
    schema = (content.get("application/json") or {}).get("schema", {})
    schema = _deref(spec, schema)
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    if not props:
        return "nenhum"
    parts = []
    for field, fschema in props.items():
        fschema = _deref(spec, fschema)
        flag = "obrigatorio" if field in required else "opcional"
        ftype = fschema.get("type", "")
        fdesc = fschema.get("description", "")
        parts.append(f"{field} [{flag}] ({ftype}): {fdesc}".strip())
    return "; ".join(parts)


def _format_response(spec: dict, responses: dict) -> str:
    ok = responses.get("200") or responses.get("201") or {}
    ok = _deref(spec, ok)
    return ok.get("description", "")


def build_operation_documents(spec: dict) -> tuple[list[str], list[dict], list[str]]:
    """Constroi (documentos, metadados, ids) para o namespace api_operations."""
    documents: list[str] = []
    metadatas: list[dict] = []
    ids: list[str] = []

    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if method.lower() not in _HTTP_METHODS:
                continue
            operation_id = op.get("operationId") or f"{method}_{path}"
            summary = op.get("summary", "")
            tags = op.get("tags") or []
            domain = tags[0] if tags else "Geral"
            destructive = bool(op.get("x-destructive", False))
            params_text = _format_parameters(spec, op.get("parameters", []))
            body_text = _format_body_fields(spec, op.get("requestBody", {}))
            response_text = _format_response(spec, op.get("responses", {}))

            # "Use when" = intencao em linguagem de negocio (dicas curadas quando
            # existem; senao deriva do summary). Sinonimos do dominio reforcam.
            clean_summary = summary.lstrip("⚠️ ").strip()
            # Intencao em UMA frase curta: dica curada se existir, senao o summary.
            use_when = _OPERATION_HINTS.get(operation_id) or clean_summary

            # Documento EMBEDADO = so a frase de intencao (curta = sinal focado).
            # Os detalhes tecnicos (parametros/body/response) ficam no metadado
            # `detail`; embeda-los diluiria a intencao e degradaria o retrieval em PT.
            doc = use_when
            detail = (
                f"Parameters: {params_text}\n"
                f"Request body fields: {body_text}\n"
                f"Response: {response_text}"
            )

            documents.append(doc)
            metadatas.append(
                {
                    "operation_id": operation_id,
                    "method": method.upper(),
                    "path": path,
                    "domain": domain,
                    "destructive": destructive,
                    "summary": summary,
                    "detail": detail,
                }
            )
            ids.append(operation_id)

    return documents, metadatas, ids


# ===========================================================================
# business_docs
# ===========================================================================
def _approx_tokens(text: str) -> int:
    # Aproximacao sem dependencia extra: ~0.75 palavra/token -> tokens ~ palavras/0.75.
    return int(len(text.split()) / 0.75)


def _split_section_into_chunks(text: str, max_tokens: int = 400) -> list[str]:
    """Quebra uma secao em chunks <= max_tokens, respeitando paragrafos."""
    if _approx_tokens(text) <= max_tokens:
        return [text.strip()] if text.strip() else []

    chunks: list[str] = []
    current: list[str] = []
    for para in re.split(r"\n\s*\n", text):
        candidate = "\n\n".join(current + [para])
        if current and _approx_tokens(candidate) > max_tokens:
            chunks.append("\n\n".join(current).strip())
            current = [para]
        else:
            current.append(para)
    if current:
        tail = "\n\n".join(current).strip()
        if tail:
            chunks.append(tail)
    return chunks


def _chunk_markdown(md: str, doc_title: str, category: str) -> list[tuple[str, str]]:
    """Quebra um markdown por secoes `##`. Retorna [(section_title, chunk_text)]."""
    results: list[tuple[str, str]] = []
    # Divide mantendo o cabecalho de cada secao `##`.
    sections = re.split(r"(?m)^##\s+", md)
    intro = sections[0].strip()
    if intro:
        # Conteudo antes do primeiro ## (geralmente o titulo `#` + visao geral).
        for chunk in _split_section_into_chunks(intro):
            results.append((doc_title or category, chunk))
    for sec in sections[1:]:
        lines = sec.splitlines()
        title = lines[0].strip() if lines else doc_title
        body = sec.strip()
        for chunk in _split_section_into_chunks(body):
            results.append((title, chunk))
    return results


def build_doc_documents() -> tuple[list[str], list[dict], list[str]]:
    """Constroi (documentos, metadados, ids) para o namespace business_docs.

    Local-first: le rag/docs/**/*.md. Se nao houver nenhum, usa o fallback minimo.
    """
    documents: list[str] = []
    metadatas: list[dict] = []
    ids: list[str] = []

    md_files = sorted(_DOCS_DIR.rglob("*.md")) if _DOCS_DIR.exists() else []

    if not md_files:
        logger.warning("Sem docs locais em %s — usando markdown fallback minimo.", _DOCS_DIR)
        for i, (section, chunk) in enumerate(_chunk_markdown(_FALLBACK_DOCS, "Fallback", "Fallback")):
            documents.append(chunk)
            metadatas.append({"source": "fallback", "section": section})
            ids.append(f"fallback::{i}")
        return documents, metadatas, ids

    logger.info("Indexando %d arquivos de docs locais (GitBook).", len(md_files))
    for md_file in md_files:
        category = md_file.parent.name
        raw = md_file.read_text(encoding="utf-8")
        first_line = raw.lstrip().splitlines()[0] if raw.strip() else ""
        doc_title = first_line.lstrip("# ").strip() if first_line.startswith("#") else md_file.stem
        rel = md_file.relative_to(_DOCS_DIR).as_posix()
        for i, (section, chunk) in enumerate(_chunk_markdown(raw, doc_title, category)):
            documents.append(chunk)
            metadatas.append(
                {
                    "source": "gitbook",
                    "section": section,
                    "category": category,
                    "file": rel,
                }
            )
            ids.append(f"{rel}::{i}")

    return documents, metadatas, ids


# ===========================================================================
# Orquestracao
# ===========================================================================
def _reset_collection(client: chromadb.ClientAPI, name: str, embedding_fn):
    try:
        client.delete_collection(name)
    except Exception:
        pass  # idempotente: ok se nao existir
    return client.create_collection(
        name=name,
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"},
    )


def build_index(chroma_path: str, base_url: str | None = None) -> dict:
    """(Re)constroi o indice do zero. Idempotente. Retorna sumario."""
    embedding_fn = get_embedding_function()
    client = chromadb.PersistentClient(path=chroma_path)

    # --- api_operations ---
    op_docs, op_meta, op_ids = build_operation_documents(load_spec(base_url))
    op_collection = _reset_collection(client, OPERATIONS_COLLECTION, embedding_fn)
    if op_docs:
        op_collection.add(documents=op_docs, metadatas=op_meta, ids=op_ids)
    destructive_count = sum(1 for m in op_meta if m["destructive"])

    # --- business_docs ---
    doc_docs, doc_meta, doc_ids = build_doc_documents()
    doc_collection = _reset_collection(client, DOCS_COLLECTION, embedding_fn)
    if doc_docs:
        doc_collection.add(documents=doc_docs, metadatas=doc_meta, ids=doc_ids)

    return {
        "operations": len(op_docs),
        "destructive": destructive_count,
        "doc_chunks": len(doc_docs),
    }
