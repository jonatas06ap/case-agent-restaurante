"""Schema das tools de escrita a partir do spec minimalista do case-mock.

Regressão para um bug observado em uso real: `coupons.create` chegava ao LLM com schema
VAZIO — o spec não declara `requestBody` para várias operações de escrita (os campos vivem
só no `summary`). O modelo chamava a ferramenta sem `name` e a API devolvia
`400 Campo obrigatorio: name`. A suíte antiga não pegava: o `StubLLM` cravava args válidos
e o `FakeClient` não validava obrigatórios. Aqui:

- validamos que o schema expõe os campos (path do template + body curado/permissivo);
- exercitamos o executor com um cliente que VALIDA o corpo, como a API real faz.
"""

from __future__ import annotations

import pytest

from agent import ConversationState
from agent.executor import Executor
from agent.planner import _build_parameters_schema, build_tools
from client import DionisioAPIError
from rag.retriever import RetrievalResult
from tests.conftest import FakeClient, make_operation_docs, tool_msg


def _fn_map(op_ids: list[str]) -> dict:
    r = RetrievalResult(operations=make_operation_docs(op_ids), docs=[], query="x")
    _, fn_map = build_tools(r)
    return fn_map


# ===========================================================================
# Schema — campos de body que o spec OMITE (a causa raiz do bug)
# ===========================================================================
def test_coupons_create_expoe_name_obrigatorio():
    # O bug: schema vazio -> LLM chama sem name -> 400. Agora `name` é um slot obrigatório.
    sch, loc = _build_parameters_schema("coupons.create")
    assert "name" in sch["properties"]
    assert "name" in sch.get("required", [])
    assert loc["name"] == "body"
    # corpo permissivo: o LLM pode acrescentar campos guiado pela descrição
    assert sch.get("additionalProperties") is True


@pytest.mark.parametrize("op_id, campo", [
    ("orders.create", "items"),
    ("promotions.create", "discountType"),
    ("orders.updateStatus", "status"),
    ("store.updateHours", "workingHours"),
    ("coupons.assignGroup", "groupId"),
])
def test_corpo_curado_da_slots_ao_llm(op_id, campo):
    sch, loc = _build_parameters_schema(op_id)
    assert campo in sch["properties"]
    assert loc[campo] == "body"


# ===========================================================================
# Schema — path params extraídos do TEMPLATE {id} (não declarados no spec)
# ===========================================================================
@pytest.mark.parametrize(
    "op_id", ["coupons.deactivate", "ifood.confirm", "ifood.dispatch", "orders.cancel", "orders.updateStatus"]
)
def test_path_param_do_template_extraido(op_id):
    sch, loc = _build_parameters_schema(op_id)
    assert loc.get("id") == "path"
    assert "id" in sch.get("required", [])


# ===========================================================================
# Não regressão — ops com body declarado no spec e GETs ficam intactos
# ===========================================================================
def test_op_com_body_no_spec_nao_vira_permissiva():
    sch, loc = _build_parameters_schema("reservations.reschedule")
    assert "additionalProperties" not in sch  # schema fechado, respeita o contrato do spec
    assert set(sch["required"]) == {"id", "start"}
    assert loc["id"] == "path" and loc["start"] == "body"


def test_get_nao_ganha_additionalProperties_nem_id_espurio():
    sch, _ = _build_parameters_schema("reservations.list")
    assert "additionalProperties" not in sch
    assert "id" not in sch["properties"]  # /reservations não tem {id} no template


# ===========================================================================
# Executor — o que teria pegado o bug ao vivo: cliente que valida o obrigatório
# ===========================================================================
async def test_coupons_create_chega_com_name_ao_cliente_validador():
    # Cliente que valida `name`, como a API real (400 "Campo obrigatorio: name").
    def validate_create(method, path, params, body):
        if not body or "name" not in body:
            raise DionisioAPIError(400, {"message": "Campo obrigatorio: name"})
        return {"id": "cup_new", "name": body["name"], "status": "ACTIVE"}

    fn_map = _fn_map(["coupons.create"])
    client = FakeClient({"coupons.create": validate_create})
    executor = Executor(client)
    call = tool_msg([(
        "coupons_create",
        {"name": "REATIVA15", "type": "percent", "benefitText": "15% de volta"},
    )]).tool_calls[0]
    state = ConversationState()

    obs = await executor.run(call, fn_map, state)

    assert "cup_new" in obs  # criou — não tomou 400
    assert state.actions_taken[-1].ok is True
    # `name` foi roteado para o BODY (não query/path)
    assert client.calls[-1]["body"]["name"] == "REATIVA15"
    assert client.calls[-1]["params"] is None


async def test_executor_substitui_id_do_template_no_path(approve):
    # coupons.deactivate é destrutiva -> exige confirmação (fixture approve).
    fn_map = _fn_map(["coupons.deactivate"])
    client = FakeClient({"coupons.deactivate": {"id": "cup_x", "status": "INACTIVE"}})
    executor = Executor(client)
    call = tool_msg([("coupons_deactivate", {"id": "cup_x"})]).tool_calls[0]
    state = ConversationState()

    await executor.run(call, fn_map, state, confirm_callback=approve)

    sent_path = client.calls[-1]["path"]
    assert sent_path == "/coupons/cup_x/deactivate"  # {id} foi substituído
    assert "{id}" not in sent_path
    assert state.actions_taken[-1].ok is True
