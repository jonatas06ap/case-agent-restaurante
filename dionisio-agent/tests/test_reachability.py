"""Cobertura por turno: persistência de domínio cross-turn + dicas curadas.

Offline e determinístico. A maioria dos casos exercita só `build_tools`/`ConversationState`
a partir do spec local (sem LLM, sem API, sem índice). Os dois casos de retrieval-quality
(`orders.stats`, `promotions.update`) usam o `Retriever` real + índice Chroma — ainda grátis
(embeddings locais), mas pulam se o índice não foi construído.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from agent import ConversationState, planner
from agent.planner import build_tools, domains_of, task_domains_of
from rag.retriever import RetrievalResult
from tests.conftest import make_operation_docs


def _result(op_ids: list[str], query: str = "x") -> RetrievalResult:
    return RetrievalResult(operations=make_operation_docs(op_ids), docs=[], query=query)


# ===========================================================================
# ConversationState.task_domains — acumulação ordenada e sem duplicar
# ===========================================================================
def test_note_domains_acumula_sem_duplicar_preservando_ordem():
    state = ConversationState()
    state.note_domains(["clients", "coupons"])
    state.note_domains(["coupons", "analytics"])  # coupons repetido, analytics novo
    assert state.task_domains == ["clients", "coupons", "analytics"]


def test_domains_of_distinto_em_ordem_de_relevancia():
    ops = make_operation_docs(["coupons.create", "coupons.assignGroup", "clients.inactive"])
    assert domains_of(ops) == ["coupons", "clients"]


# ===========================================================================
# (a) Lacuna cross-turn — domínio persistido traz a irmã num turno seguinte
#     cujo texto NÃO menciona aquele domínio.
# ===========================================================================
def test_dominio_persistido_traz_assigngroup_quando_coupons_nem_e_recuperado():
    # Turno de continuação onde o retrieval não toca `coupons` (texto sem "cupom").
    r2 = _result(
        ["promotions.get", "orders.get", "clients.get", "ifood.get"],
        query="faça os passos exceto o contato",
    )
    # Sem estado: a irmã do cupom não tem como entrar — reproduz a lacuna.
    _, sem_estado = build_tools(r2)
    assert "coupons_assignGroup" not in sem_estado
    # Com o domínio `coupons` persistido da tarefa: entra (prioridade, fora do teto).
    _, com_estado = build_tools(r2, task_domains=["clients", "coupons"])
    assert "coupons_assignGroup" in com_estado


def test_dominio_persistido_vence_o_teto_quando_coupons_cai_tarde_na_ordem():
    # Reproduz fielmente o caso real: o turno 2 RECUPERA `coupons.get`, mas a irmã
    # `assignGroup` cai atrás do teto porque `coupons` aparece tarde na ordem dos domínios
    # e o teto se esgota nos domínios anteriores (clients tem 9 ops).
    r2 = _result(
        ["promotions.get", "orders.get", "clients.get", "ifood.get",
         "coupons.get", "delivery.getConfig"],
        query="faça os passos exceto o contato",
    )
    _, sem_estado = build_tools(r2)
    assert "coupons_assignGroup" not in sem_estado  # cortada pelo teto (a lacuna)
    _, com_estado = build_tools(r2, task_domains=["clients", "coupons"])
    assert "coupons_assignGroup" in com_estado  # com persistência de domínio


async def test_cross_turn_pelo_estado_acumulado_alcanca_assigngroup():
    # Encadeamento turno1 -> turno2 como core.run_turn faz: acumula domínios e monta
    # as tools do turno 2 com os domínios persistidos.
    state = ConversationState()
    r1 = _result(["clients.inactive", "coupons.create", "coupons.assignGroup"],
                 query="cria uma campanha com cupom de 15%")
    state.note_domains(task_domains_of(r1.operations))  # top-3 -> {clients, coupons}

    r2 = _result(["promotions.get", "orders.get", "clients.get", "ifood.get",
                  "coupons.get", "delivery.getConfig"],
                 query="faça os passos exceto o contato")
    state.note_domains(task_domains_of(r2.operations))
    _, fn_map = build_tools(r2, task_domains=state.task_domains)
    assert "coupons_assignGroup" in fn_map


def test_task_domains_of_persiste_so_o_topo_nao_o_long_tail():
    # 8 ops do top-k espalhadas por muitos domínios; só os 3 primeiros viram task domains.
    ops = make_operation_docs([
        "clients.inactive", "coupons.create", "coupons.assignGroup",
        "clients.reservations", "reservations.availability", "orders.list",
        "clients.topSpenders", "analytics.orders",
    ])
    assert task_domains_of(ops) == ["clients", "coupons"]  # reservations/orders/analytics = ruído


# ===========================================================================
# (c) Sem regressão: turno único (task_domains vazio) é idêntico ao retrieval sem
#     estado, e persistir domínio só ADICIONA — nunca remove op recuperada no turno.
# ===========================================================================
def test_turno_unico_sem_task_domains_identico_ao_sem_estado():
    r = _result(["reservations.cancel", "orders.cancel", "reservations.reschedule"])
    _, base = build_tools(r)
    _, com_lista_vazia = build_tools(r, task_domains=[])
    assert set(base) == set(com_lista_vazia)
    assert "reservations_list" in base  # expansão de domínio segue valendo


def test_persistir_dominio_nunca_remove_op_recuperada_no_turno():
    # As ops RECUPERADAS no turno (top-k) entram sempre — independem da expansão/teto.
    # (Sob o teto, irmãs de navegação podem ser reordenadas; o que não pode sumir é o
    # que o retrieval do turno trouxe.)
    r = _result(["reservations.list", "reservations.cancel"])
    _, com = build_tools(r, task_domains=["coupons", "promotions"])
    assert "reservations_list" in com and "reservations_cancel" in com
    # e os domínios persistidos trouxeram suas irmãs
    assert "coupons_assignGroup" in com and "promotions_update" in com


def test_destrutivas_continuam_no_fn_map_mas_barreira_e_no_executor():
    # A alcançabilidade não pode "abrir" execução: assignGroup/destrutivas entram como
    # tool, mas a confirmação no executor é quem barra (ver test_reliability).
    r = _result(["coupons.get"], query="dá um cupom pra cada inativo")
    _, fn_map = build_tools(r, task_domains=["coupons"])
    assert "coupons_assignGroup" in fn_map
    assert "coupons_deactivate" in fn_map  # destrutiva-irmã também disponível


# ===========================================================================
# (b) Dicas curadas + reindex — orders.stats e promotions.update voltam à lista
#     de tools do próprio pedido. Usa o Retriever real (grátis, embeddings locais);
#     pula se o índice Chroma não foi construído.
# ===========================================================================
_INDEX_PATH = Path(__file__).resolve().parent.parent / "rag" / "index"
_needs_index = pytest.mark.skipif(
    not _INDEX_PATH.exists(),
    reason="índice Chroma ausente — rode `uv run python scripts/build_index.py`",
)


async def _reachable(expected: str, prompt: str) -> bool:
    from rag import Retriever

    retriever = Retriever(chroma_path=os.getenv("CHROMA_PATH", "./rag/index"))
    retrieval = await retriever.retrieve(
        prompt, k_operations=8, k_docs=3, exclude_destructive=False
    )
    _, fn_map = build_tools(retrieval)
    return expected.replace(".", "_") in fn_map


@_needs_index
async def test_orders_stats_alcancavel_no_proprio_pedido():
    assert await _reachable("orders.stats", "qual o ticket médio e o total de pedidos?")


@_needs_index
async def test_promotions_update_alcancavel_no_proprio_pedido():
    assert await _reachable("promotions.update", "muda o horário da primeira promoção para 17h-19h")


@_needs_index
async def test_analytics_orders_continua_alcancavel_caso_ambiguo():
    # Decisão documentada: a dica de orders.stats NÃO derruba analytics.orders — ambas
    # ficam disponíveis para "métricas de pedidos".
    assert await _reachable("analytics.orders", "me dá as métricas de pedidos do período")
