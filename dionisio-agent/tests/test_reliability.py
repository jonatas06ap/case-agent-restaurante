"""Confiabilidade: cálculo determinístico, falsos negativos e linguagem.

Offline e determinístico (mesmo princípio do `test_tasks.py`): o loop, o executor,
o planner e a safety são os reais; só o LLM (`StubLLM`) e a API (`FakeClient`) são
dublês. Cobre três frentes:

- Fix A: a tool `calcular` é local, sempre presente, e dá o número exato.
- Fix B: a expansão de domínio traz a operação-irmã que o retrieval não trouxe;
  o erro de nome vira sugestão de recuperação.
- Fix C: confirmação/recusa em linguagem de operador, sem jargão técnico.
"""

from __future__ import annotations

import json

import pytest

from agent import Agent, ConversationState, calculator
from agent.executor import Executor
from agent.phrasing import humanize_plan
from agent.planner import build_tools
from rag.retriever import RetrievalResult
from safety.destructive import confirmation_reason
from tests.conftest import (
    FakeClient,
    FakeRetriever,
    StubLLM,
    final_msg,
    make_operation_docs,
    tool_msg,
)


# ===========================================================================
# Fix A — calculadora determinística
# ===========================================================================
def test_calculadora_percentual_corrige_erro_do_llm():
    # Em uso real o LLM disse 53%; o correto é 55%.
    out = json.loads(calculator.execute({"op": "percentual", "parte": 71, "total": 129}))
    assert out["resultado_pct"] == 55.0


def test_calculadora_ordenar_ranking_decrescente():
    out = json.loads(calculator.execute({"op": "ordenar", "itens": [
        {"rotulo": "sexta", "valor": 506.67},
        {"rotulo": "domingo", "valor": 796},
        {"rotulo": "quarta", "valor": 459.5},
    ]}))
    assert [r["rotulo"] for r in out["ranking"]] == ["domingo", "sexta", "quarta"]


def test_calculadora_soma_media():
    assert json.loads(calculator.execute({"op": "soma", "valores": [799, 536, 185]}))["resultado"] == 1520.0
    assert json.loads(calculator.execute({"op": "media", "valores": [2, 4]}))["resultado"] == 3.0


def test_calculadora_erro_nao_levanta():
    out = json.loads(calculator.execute({"op": "media", "valores": []}))
    assert "erro" in out and "operacoes_validas" in out


def test_calculadora_sempre_presente_como_tool_local():
    r = RetrievalResult(operations=make_operation_docs(["reservations.list"]), docs=[], query="x")
    tools, fn_map = build_tools(r)
    assert any(t["function"]["name"] == calculator.TOOL_NAME for t in tools)
    assert fn_map[calculator.TOOL_NAME].get("local") is True


async def test_calculadora_no_loop_nao_chama_api():
    stub = StubLLM(script=[
        tool_msg([("calcular", {"op": "percentual", "parte": 71, "total": 129})]),
        final_msg("Presencial é 55% dos pedidos."),
    ])
    client = FakeClient({})  # nenhuma resposta de API configurada: calc não pode tocar a API
    agent = Agent(llm=stub, retriever=FakeRetriever(["analytics.orders"]), client=client)

    answer = await agent.run_turn("qual o percentual de 71 em 129?", ConversationState())

    assert client.called_ops() == []  # nenhuma chamada HTTP
    assert "55" in answer


# ===========================================================================
# Fix B — falsos negativos: expansão de domínio + dica de recuperação
# ===========================================================================
def test_expansao_dominio_traz_reservations_list():
    # 'desmarque as reservas do dia 19' -> retrieval traz cancel, não list.
    r = RetrievalResult(
        operations=make_operation_docs(
            ["reservations.cancel", "orders.cancel", "reservations.reschedule"]
        ),
        docs=[], query="x",
    )
    _, fn_map = build_tools(r)
    assert "reservations_list" in fn_map  # a irmã de navegação ficou disponível


def test_expansao_dominio_traz_coupons_assigngroup():
    # 'dê um cupom para cada um' -> coupons tocado via coupons.get.
    r = RetrievalResult(
        operations=make_operation_docs(["promotions.get", "coupons.get", "ifood.get"]),
        docs=[], query="x",
    )
    _, fn_map = build_tools(r)
    assert "coupons_assignGroup" in fn_map  # a operação que o agente negava existir


async def test_nome_errado_vira_sugestao_de_recuperacao():
    r = RetrievalResult(operations=make_operation_docs(["coupons.get"]), docs=[], query="x")
    _, fn_map = build_tools(r)
    executor = Executor(FakeClient({}))
    call = tool_msg([("coupons_assign", {})]).tool_calls[0]  # nome errado

    obs = await executor.run(call, fn_map, ConversationState())

    assert "nao existe" in obs
    assert "coupons_assignGroup" in obs  # sugere o nome certo do mesmo domínio


# ===========================================================================
# Fix C — linguagem de operador (sem jargão técnico)
# ===========================================================================
# Termos técnicos que NÃO podem vazar na fala ao operador. ('/' não entra: é
# separador de data legítimo — '19/06'; caminhos HTTP vazariam como '/reservations',
# já coberto pela dot-notation e pelos métodos.)
_JARGON = ("reservations.", "coupons.", "/reservations", "/coupons", "POST ", "GET ",
           "PATCH ", "x-destructive", "endpoint", "operationId", "operation_id")


@pytest.mark.parametrize("op_id,args", [
    ("reservations.reschedule", {"id": "res_x", "start": 1781897400000}),
    ("reservations.cancel", {"id": "res_x"}),
    ("coupons.assignGroup", {"id": "cpn_x", "groupId": "grp_1"}),
])
def test_plano_de_confirmacao_sem_jargao(op_id, args):
    plano = humanize_plan(op_id, args, confirmation_reason(op_id))
    for termo in _JARGON:
        assert termo not in plano, f"jargão '{termo}' vazou no plano: {plano!r}"
    assert "Posso confirmar?" in plano


def test_confirmation_reason_sem_x_destructive():
    assert "x-destructive" not in confirmation_reason("reservations.cancel")
    assert "nao pode ser desfeita" in confirmation_reason("reservations.cancel")


async def test_confirmacao_destrutiva_ainda_dispara_em_linguagem_humana():
    # A barreira determinística segue valendo; só a redação mudou.
    seen: dict = {}

    async def capture(plan: str) -> bool:
        seen["plan"] = plan
        return True

    stub = StubLLM(script=[
        tool_msg([("reservations_cancel", {"id": "res_1"})]),
        final_msg("Reserva cancelada."),
    ])
    client = FakeClient({"reservations.cancel": {"id": "res_1", "status": "cancelled"}})
    agent = Agent(
        llm=stub, retriever=FakeRetriever(["reservations.cancel"]),
        client=client, confirm_callback=capture,
    )

    await agent.run_turn("cancela a reserva res_1", ConversationState())

    assert "plan" in seen  # confirmação foi pedida (barreira intacta)
    for termo in _JARGON:
        assert termo not in seen["plan"], f"jargão '{termo}' no plano: {seen['plan']!r}"
