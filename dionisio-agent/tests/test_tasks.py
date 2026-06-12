"""Suíte das 6 tarefas do case (Dia 4).

Núcleo OFFLINE e DETERMINÍSTICO: o LLM (`StubLLM`) e a API (`FakeClient`) são
mockados, mas o loop ReAct, o executor, a barreira de confirmação e o fluxo de
estado (`discovered_entities`/`actions_taken`) são os reais — é o encadeamento
multi-step que está sob teste, não a criatividade do modelo.

Princípio anti-alucinação: os passos do roteiro que dependem de um ID/horário são
CALLABLES que leem a observação real já no histórico — se o dado não viesse da
API, o passo produziria lixo e o teste quebraria. Assim provamos "nenhum ID
inventado" de verdade, não por construção.

Variantes @pytest.mark.live (LLM + API reais) ao final, puladas por default.
"""

from __future__ import annotations

import os

import pytest

from agent import Agent, ConversationState
from tests.conftest import (
    DionisioAPIError,
    FakeClient,
    FakeRetriever,
    StubLLM,
    final_msg,
    find_observation,
    load_fixture,
    tool_msg,
    tool_observations,
)

# Δ entre quinta e sábado, em ms — preserva o time-of-day ("mesmo horário").
TWO_DAYS_MS = 2 * 24 * 60 * 60 * 1000


# ===========================================================================
# helpers locais
# ===========================================================================
def record_for(state: ConversationState, operation_id: str):
    """Primeiro ToolCallRecord de uma operação (ou None)."""
    for r in state.actions_taken:
        if r.operation_id == operation_id:
            return r
    return None


def _reschedule_was_blocked(messages) -> bool:
    """True se a observação do reschedule indica cancelamento por falta de confirmação."""
    return any(
        m.get("role") == "tool" and "NAO executada" in (m.get("content") or "")
        for m in messages
    )


def make_agent(stub, op_ids, client, confirm_callback=None):
    return Agent(
        llm=stub,
        retriever=FakeRetriever(op_ids),
        client=client,
        confirm_callback=confirm_callback,
    )


# ===========================================================================
# Tarefa 1 — contar reservas de hoje (regressão Dia 2)
# ===========================================================================
async def test_tarefa1_conta_reservas_de_hoje():
    stub = StubLLM(script=[
        tool_msg([("reservations_list", {"date": "2023-11-21"})]),
        final_msg("Há 1 reserva confirmada para hoje."),
    ])
    client = FakeClient({"reservations.list": load_fixture("reservations_list_today")})
    agent = make_agent(stub, ["reservations.list"], client)

    answer = await agent.run_turn("quantas reservas temos pra hoje?", ConversationState())

    assert client.called_ops() == ["reservations.list"]
    assert "1" in answer
    assert stub.ambiguity_calls == 1  # pré-check rodou


# ===========================================================================
# Tarefa 2 — remarcar reserva (multi-step + estado + confirmação)
# ===========================================================================
_T2_OPS = [
    "clients.search", "reservations.list",
    "reservations.availability", "reservations.reschedule",
]


def _t2_script():
    """search -> list (usa clientId) -> availability -> reschedule (usa reservationId+start)."""
    def step_list(messages):
        cli = find_observation(messages, lambda o: o["items"][0]["id"].startswith("cli"))
        client_id = cli["items"][0]["id"]
        return tool_msg([("reservations_list", {"clientId": client_id, "date": "2023-11-23"})])

    def step_reschedule(messages):
        resv = find_observation(messages, lambda o: "duration" in o["items"][0])
        item = resv["items"][0]
        new_start = item["duration"]["start"] + TWO_DAYS_MS  # sábado, mesmo horário
        return tool_msg([("reservations_reschedule", {"id": item["id"], "start": new_start})])

    def step_final(messages):
        if _reschedule_was_blocked(messages):
            return final_msg(
                "Não remarquei a reserva do João: a confirmação foi negada, então "
                "nenhuma alteração foi feita. Não há como avisá-la pela API — avise manualmente."
            )
        return final_msg(
            "Remarquei a reserva do João para sábado no mesmo horário. Não consigo "
            "avisá-la pela API (não há canal de comunicação); avise-a manualmente."
        )

    return [
        tool_msg([("clients_search", {"name": "João"})]),
        step_list,
        tool_msg([("reservations_availability", {"date": "2023-11-25"})]),
        step_reschedule,
        step_final,
    ]


def _t2_client():
    return FakeClient({
        "clients.search": load_fixture("clients_search_joao"),
        "reservations.list": load_fixture("reservations_list_joao"),
        "reservations.availability": load_fixture("reservations_availability_sat"),
        "reservations.reschedule": load_fixture("reservations_reschedule"),
    })


async def test_tarefa2_remarca_apos_confirmacao(approve):
    client = _t2_client()
    stub = StubLLM(script=_t2_script())
    agent = make_agent(stub, _T2_OPS, client, confirm_callback=approve)
    state = ConversationState()

    answer = await agent.run_turn(
        "remarca a reserva do João de quinta pra sábado no mesmo horário e confirma se tem mesa, e avisa ela",
        state,
    )

    # ordem dos passos encadeados
    assert client.called_ops() == [
        "clients.search", "reservations.list",
        "reservations.availability", "reservations.reschedule",
    ]
    # a confirmação foi exigida e aprovada
    assert approve.state["asked"] is True
    resched = record_for(state, "reservations.reschedule")
    assert resched.ok is True and resched.confirmed is True

    # ANTI-ALUCINAÇÃO: o reservationId veio do passo 2 (fixture), não foi inventado
    fixture_resv = load_fixture("reservations_list_joao")["items"][0]
    assert resched.arguments["id"] == fixture_resv["id"]
    # "mesmo horário": start de sábado = start original + 2 dias (preserva time-of-day)
    assert resched.arguments["start"] == fixture_resv["duration"]["start"] + TWO_DAYS_MS

    # "avisa ela" é recusado honestamente (sem fingir notificação)
    assert "avis" in answer.lower()


async def test_tarefa2_confirmacao_negada_nao_remarca(deny):
    client = _t2_client()
    stub = StubLLM(script=_t2_script())
    agent = make_agent(stub, _T2_OPS, client, confirm_callback=deny)
    state = ConversationState()

    answer = await agent.run_turn(
        "remarca a reserva do João de quinta pra sábado no mesmo horário e avisa ela", state
    )

    assert deny.state["asked"] is True
    # confirmação NEGADA -> a API de reschedule NÃO foi chamada
    assert "reservations.reschedule" not in client.called_ops()
    resched = record_for(state, "reservations.reschedule")
    assert resched is not None and resched.ok is False and resched.confirmed is False
    # texto honesto: não afirma que remarcou
    assert "negada" in answer.lower() or "não remarquei" in answer.lower()


# ===========================================================================
# Tarefa 3 — filtro composto (gasto > R$500 no último mês E nunca usou cupom)
# ===========================================================================
async def test_tarefa3_filtro_composto_intersecao():
    def step_insights(messages):
        top = find_observation(messages, lambda o: o.get("period") == "month")
        ids = [it["client"]["id"] for it in top["items"]]
        return tool_msg([("clients_insights", {"clientId": cid}) for cid in ids])

    def step_final(messages):
        obs = tool_observations(messages)
        top = next(o for o in obs if o.get("period") == "month")
        coupons = {o["clientId"]: o["couponsUsed"] for o in obs if "couponsUsed" in o and "clientId" in o}
        keep = [
            (it["client"]["name"], it["spent"])
            for it in top["items"]
            if coupons.get(it["client"]["id"], 1) == 0  # nunca usou cupom
        ]
        listado = ", ".join(f"{name} (R${spent})" for name, spent in keep)
        return final_msg(
            f"Clientes que gastaram mais de R$500 no último mês e nunca usaram cupom: {listado}."
        )

    def insights_router(method, path, params, body):
        cid = path.split("/")[2]  # /clients/<id>/insights
        return load_fixture(f"clients_insights_{cid.split('_')[1]}")

    client = FakeClient({
        "clients.topSpenders": load_fixture("clients_topspenders"),
        "clients.insights": insights_router,
    })
    stub = StubLLM(script=[
        tool_msg([("clients_topSpenders", {"period": "month", "minSpent": 500})]),
        step_insights,
        step_final,
    ])
    agent = make_agent(stub, ["clients.topSpenders", "clients.insights"], client)
    state = ConversationState()

    answer = await agent.run_turn(
        "lista os clientes que gastaram mais de R$500 no último mês e nunca usaram cupom", state
    )

    # cruzou os dois endpoints, nessa ordem
    assert client.called_ops() == [
        "clients.topSpenders", "clients.insights", "clients.insights", "clients.insights",
    ]
    # ANTI-ALUCINAÇÃO: insights foi pedido para os clientIds que vieram do topSpenders
    insights_ids = {c["path"].split("/")[2] for c in client.calls if c["operation_id"] == "clients.insights"}
    assert insights_ids == {"cli_ana", "cli_bruno", "cli_carla"}
    # interseção correta: Ana e Carla (couponsUsed=0); Bruno (couponsUsed=2) fica de fora
    assert "Ana Souza" in answer and "Carla Dias" in answer
    assert "Bruno" not in answer


# ===========================================================================
# Tarefa 4 — campanha (assignGroup) só dispara após confirmação (reuso Dia 3)
# ===========================================================================
_T4_OPS = ["clients.inactive", "coupons.create", "coupons.assignGroup"]


def _t4_script():
    def step_assign(messages):
        inact = find_observation(messages, lambda o: "groupId" in o)
        coupon = find_observation(messages, lambda o: o.get("id", "").startswith("cup"))
        return tool_msg([("coupons_assignGroup", {"id": coupon["id"], "groupId": inact["groupId"]})])

    def step_final(messages):
        if _reschedule_was_blocked(messages):  # mesma marca de "NAO executada"
            return final_msg(
                "Campanha NÃO disparada: a confirmação foi negada, nenhum cupom foi atribuído."
            )
        return final_msg("Campanha disparada: cupom VOLTA15 atribuído ao grupo de inativos.")

    return [
        tool_msg([("clients_inactive", {"days": 60})]),
        tool_msg([("coupons_create", {"name": "VOLTA15", "type": "percent", "benefitText": "15%"})]),
        step_assign,
        step_final,
    ]


def _t4_client():
    return FakeClient({
        "clients.inactive": load_fixture("clients_inactive"),
        "coupons.create": load_fixture("coupons_create"),
        "coupons.assignGroup": load_fixture("coupons_assigngroup"),
    })


async def test_tarefa4_assign_group_apos_confirmacao(approve):
    client = _t4_client()
    stub = StubLLM(script=_t4_script())
    agent = make_agent(stub, _T4_OPS, client, confirm_callback=approve)
    state = ConversationState()

    await agent.run_turn(
        "cria uma campanha de reativação para clientes inativos há 60 dias, com um cupom de 15%", state
    )

    assert approve.state["asked"] is True
    assert "coupons.assignGroup" in client.called_ops()
    assign = record_for(state, "coupons.assignGroup")
    assert assign.ok is True and assign.confirmed is True
    # provenance: couponId veio do create, groupId veio do inactive
    assert assign.arguments["id"] == load_fixture("coupons_create")["id"]
    assert assign.arguments["groupId"] == load_fixture("clients_inactive")["groupId"]


async def test_tarefa4_confirmacao_negada_nao_dispara(deny):
    client = _t4_client()
    stub = StubLLM(script=_t4_script())
    agent = make_agent(stub, _T4_OPS, client, confirm_callback=deny)
    state = ConversationState()

    answer = await agent.run_turn(
        "cria uma campanha de reativação para clientes inativos há 60 dias, com um cupom de 15%", state
    )

    assert deny.state["asked"] is True
    assert "coupons.assignGroup" not in client.called_ops()
    assign = record_for(state, "coupons.assignGroup")
    assert assign is not None and assign.ok is False and assign.confirmed is False
    assert "não disparada" in answer.lower() or "nenhum cupom" in answer.lower()


# ===========================================================================
# Tarefa 5 — possível vs impossível (remover prato/notificar = sem endpoint)
# ===========================================================================
async def test_tarefa5_separa_possivel_do_impossivel():
    def step_final(messages):
        orders = find_observation(messages, lambda o: "client" in o["items"][0])
        nomes = ", ".join(it["client"]["name"] for it in orders["items"])
        return final_msg(
            "Não consigo remover o 'Risoto de Funghi' do cardápio (a API não tem domínio de "
            "cardápio/menu) nem notificar os clientes (não há canal de comunicação). Mas aqui "
            f"estão os clientes que pediram o prato nos últimos 7 dias, para avisar manualmente: {nomes}."
        )

    client = FakeClient({
        "analytics.topItems": load_fixture("analytics_topitems"),
        "orders.list": load_fixture("orders_list_risoto"),
    })
    stub = StubLLM(script=[
        tool_msg([("analytics_topItems", {})]),
        tool_msg([("orders_list", {})]),
        step_final,
    ])
    agent = make_agent(stub, ["analytics.topItems", "orders.list"], client)
    state = ConversationState()

    answer = await agent.run_turn(
        "o prato 'Risoto de Funghi' saiu do cardápio — remove ele e avisa quem pediu nos últimos 7 dias",
        state,
    )

    # só fez leitura (nenhuma escrita/mutação — não existe endpoint pra isso mesmo)
    assert all(c["method"] == "GET" for c in client.calls)
    assert client.called_ops() == ["analytics.topItems", "orders.list"]
    # recusa explícita das duas partes impossíveis
    low = answer.lower()
    assert "cardápio" in low and ("não consigo remover" in low or "não" in low)
    assert "comunicação" in low or "notificar" in low
    # entrega a parte possível: a lista de quem pediu (da fixture de orders.list)
    assert "Marina Alves" in answer and "Pedro Rocha" in answer


# ===========================================================================
# Tarefa 6 — pedido ambíguo: UMA pergunta, ZERO chamadas à API
# ===========================================================================
async def test_tarefa6_ambiguo_pergunta_sem_chamar_api():
    pergunta = "Qual pedido você quer cancelar? Me diga o cliente ou o número do pedido."
    stub = StubLLM(
        script=[],
        ambiguity=f'{{"ambiguous": true, "clarifying_question": "{pergunta}"}}',
    )
    client = FakeClient({})  # nenhuma resposta — não deve ser chamado
    agent = make_agent(stub, ["orders.cancel", "orders.list"], client)
    state = ConversationState()

    answer = await agent.run_turn("cancela o pedido", state)

    assert answer == pergunta
    assert client.calls == []          # zero chamadas à API
    assert stub.tool_iterations == 0   # o loop ReAct nem rodou
    assert stub.ambiguity_calls == 1


# ===========================================================================
# Regressão Dia 2 — DionisioAPIError vira observação textual e o loop se recupera
# ===========================================================================
async def test_erro_de_api_vira_observacao_e_loop_recupera():
    calls = {"n": 0}

    def flaky(method, path, params, body):
        calls["n"] += 1
        if calls["n"] == 1:
            raise DionisioAPIError(400, {"message": "date inválida"})
        return load_fixture("reservations_list_today")

    client = FakeClient({"reservations.list": flaky})
    stub = StubLLM(script=[
        tool_msg([("reservations_list", {"date": "ontem"})]),       # 1ª tentativa: 400
        tool_msg([("reservations_list", {"date": "2023-11-21"})]),  # corrige
        final_msg("Há 1 reserva para hoje."),
    ])
    agent = make_agent(stub, ["reservations.list"], client)
    state = ConversationState()

    answer = await agent.run_turn("quantas reservas pra hoje?", state)

    # o erro não derrubou o turno; o agente tentou de novo e respondeu
    assert client.called_ops() == ["reservations.list", "reservations.list"]
    assert any(
        m.get("role") == "tool" and "Erro 400" in (m.get("content") or "")
        for m in state.messages
    )
    primeiro = state.actions_taken[0]
    assert primeiro.ok is False
    assert state.actions_taken[-1].ok is True
    assert "1" in answer


# ===========================================================================
# @pytest.mark.live — LLM + API reais (≥4 tarefas). Puladas por default.
# Rodar com:  uv run pytest -m live
# ===========================================================================
def _live_deps():
    """Instancia (retriever, llm, client_factory) reais a partir do .env, ou pula."""
    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("DIONISIO_API_KEY"):
        pytest.skip("variáveis OPENROUTER_API_KEY/DIONISIO_API_KEY ausentes — pulando live")

    from agent.llm import LLM, DEFAULT_MODEL
    from client import DionisioClient
    from rag import Retriever

    retriever = Retriever(chroma_path=os.getenv("CHROMA_PATH", "./rag/index"))
    llm = LLM(api_key=os.getenv("OPENROUTER_API_KEY", ""),
              model=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL))

    def client_factory():
        return DionisioClient(api_key=os.getenv("DIONISIO_API_KEY", ""),
                              base_url=os.getenv("DIONISIO_BASE_URL", ""))

    return retriever, llm, client_factory


async def _run_live(prompt: str, confirm: bool = False) -> tuple[str, ConversationState]:
    retriever, llm, client_factory = _live_deps()

    async def confirm_cb(_plan: str) -> bool:
        return confirm

    state = ConversationState()
    async with client_factory() as client:
        agent = Agent(llm=llm, retriever=retriever, client=client, confirm_callback=confirm_cb)
        answer = await agent.run_turn(prompt, state)
    return answer, state


@pytest.mark.live
async def test_live_tarefa1():
    answer, state = await _run_live("quantas reservas temos pra hoje?")
    assert any(c.isdigit() for c in answer)
    assert any(a.ok for a in state.actions_taken)


@pytest.mark.live
async def test_live_tarefa2_negada():
    # confirmação NEGADA -> reschedule não pode ter sido executado
    _, state = await _run_live(
        "remarca a reserva do João de quinta pra sábado no mesmo horário e confirma se tem mesa",
        confirm=False,
    )
    assert not any(a.operation_id == "reservations.reschedule" and a.ok for a in state.actions_taken)


@pytest.mark.live
async def test_live_tarefa3():
    answer, state = await _run_live(
        "lista os clientes que gastaram mais de R$500 no último mês e nunca usaram cupom"
    )
    assert any(a.ok for a in state.actions_taken)
    assert answer.strip()


@pytest.mark.live
async def test_live_tarefa5_honesto():
    answer, _ = await _run_live(
        "o prato 'Risoto de Funghi' saiu do cardápio — remove ele e avisa quem pediu nos últimos 7 dias"
    )
    low = answer.lower()
    # não pode fingir que removeu o prato nem que notificou
    assert "cardápio" in low or "menu" in low or "não" in low
