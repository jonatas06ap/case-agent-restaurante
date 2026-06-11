"""Classificador DETERMINISTICO de operacoes que exigem confirmacao (Dia 3).

A regra do CLAUDE.md e inviolavel: destrutividade/alto impacto e decidida por
metadado do spec + allowlist explicita, NUNCA por LLM. Uma operacao exige
confirmacao se cair em qualquer uma das duas classes:

- Classe A — `x-destructive: true` no `rag/openapi_spec.json` (7 operacoes
  irreversiveis: cancelar/remarcar reserva, cancelar pedido, desativar cupom,
  deletar promocao, criar pausa de delivery, cancelar pedido iFood). Lemos do
  spec — a MESMA fonte de verdade do indexer/retriever — para nao duplicar uma
  lista hardcoded que poderia divergir se o spec mudar.

- Classe B — "efeito em massa": opera sobre um grupo/segmento de clientes, com
  consequencia real para muita gente, mas SEM marca `x-destructive`. Mantida como
  allowlist pequena e explicita, justificada por inspeccao do spec.

A barreira (Dia 3) migrou do retrieval para o executor: o retrieval volta a
incluir as destrutivas (senao a tool nem estaria disponivel) e a confirmacao
acontece no boundary da tool-call, imediatamente antes do `client.request`.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_SPEC_PATH = Path(__file__).resolve().parent.parent / "rag" / "openapi_spec.json"
_HTTP_METHODS = {"get", "post", "put", "patch", "delete"}

# ---------------------------------------------------------------------------
# Classe B — alto impacto / efeito em massa (NAO marcado x-destructive no spec).
#
# Inspecao do spec (POST/PUT/PATCH/DELETE): de todas as operacoes de escrita, a
# unica que age sobre um GRUPO INTEIRO de clientes e `coupons.assignGroup`
# (POST /coupons/{id}/assign-group, body: groupId) — gera uma instancia do cupom
# para cada cliente do grupo. E o "disparo" da campanha (Tarefa 4). As demais
# escritas ou ja sao Classe A, ou atuam sobre 1 registro (clients.update,
# reservations.create...) ou sobre a config da loja (store.update,
# delivery.updateConfig) — alto impacto operacional, mas nao "campanha para um
# segmento de clientes". Por isso a allowlist fica so com assignGroup; ampliar
# exige nova justificativa por leitura do spec.
# ---------------------------------------------------------------------------
MASS_EFFECT_OPS: frozenset[str] = frozenset(
    {
        "coupons.assignGroup",  # atribui o cupom a um grupo inteiro — disparo da campanha (Tarefa 4)
    }
)


@lru_cache(maxsize=1)
def _destructive_ops() -> frozenset[str]:
    """Classe A — operationIds com `x-destructive: true`, lidos do spec local."""
    spec = json.loads(_SPEC_PATH.read_text(encoding="utf-8"))
    out: set[str] = set()
    for methods in spec.get("paths", {}).values():
        for method, op in methods.items():
            if method.lower() not in _HTTP_METHODS:
                continue
            if op.get("x-destructive") is True:
                op_id = op.get("operationId")
                if op_id:
                    out.add(op_id)
    return frozenset(out)


def requires_confirmation(operation_id: str) -> bool:
    """True se a operacao exige confirmacao explicita (Classe A ou Classe B)."""
    return operation_id in _destructive_ops() or operation_id in MASS_EFFECT_OPS


def confirmation_reason(operation_id: str) -> str:
    """Frase curta sobre POR QUE confirma — compoe o plano apresentado ao operador."""
    if operation_id in _destructive_ops():
        return "operacao irreversivel (x-destructive)"
    if operation_id in MASS_EFFECT_OPS:
        return "afeta um grupo inteiro de clientes"
    return ""
