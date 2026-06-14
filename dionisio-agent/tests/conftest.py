"""Fixtures e dublês de teste.

O objetivo é tornar o multi-step DETERMINÍSTICO e OFFLINE: mockamos as duas
fronteiras não-determinísticas do agente — o LLM (OpenRouter) e a API (rede) —
mantendo intacto TUDO que está em teste: o loop ReAct (`agent/core.py`), o
roteamento de tool-calls (`agent/executor.py`), a barreira de confirmação
(`safety/`), e o fluxo de estado (`discovered_entities`/`actions_taken`).

Três dublês:

- `StubLLM`  — devolve uma sequência fixa (ou dinâmica) de mensagens. Na
  pré-checagem de ambiguidade (chamada SEM tools) devolve um veredito JSON
  configurável; no loop (chamada COM tools) consome o `script` passo a passo.
  Passos podem ser CALLABLES que leem as observações reais já no histórico — é
  assim que provamos que um ID veio da API, não foi inventado.
- `FakeClient` — mesma interface async de `DionisioClient.request`, roteando
  `(method, path)` de volta ao `operationId` pelos templates do spec local e
  devolvendo a fixture configurada (ou levantando `DionisioAPIError`). Grava
  todas as chamadas para asserção.
- `FakeRetriever` — devolve um `RetrievalResult` fixo. Os parâmetros das tools
  ainda saem do spec local (via `agent.planner`), então as tools são reais.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from agent.planner import _operations_by_id
from client import DionisioAPIError
from rag.retriever import BusinessDoc, OperationDoc, RetrievalResult
from safety.destructive import _destructive_ops

_FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
_BASE_PATH = "/api/case-mock"


# ===========================================================================
# Carregamento de fixtures JSON
# ===========================================================================
def load_fixture(name: str) -> dict:
    """Carrega tests/fixtures/<name>.json como dict."""
    path = _FIXTURES_DIR / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


# ===========================================================================
# Dublês de mensagem do LLM (mimetizam o objeto da OpenAI)
# ===========================================================================
class _Fn:
    def __init__(self, name: str, arguments: str):
        self.name = name
        self.arguments = arguments


class _ToolCall:
    def __init__(self, call_id: str, name: str, arguments: dict):
        self.id = call_id
        self.function = _Fn(name, json.dumps(arguments))


class _Msg:
    def __init__(self, content: str | None = None, tool_calls: list | None = None):
        self.content = content
        self.tool_calls = tool_calls


def tool_msg(calls: list[tuple[str, dict]]) -> _Msg:
    """Mensagem do assistant com tool_calls. `calls` = [(fn_name, args_dict), ...]."""
    tcs = [_ToolCall(f"call_{i}", name, args) for i, (name, args) in enumerate(calls)]
    return _Msg(content=None, tool_calls=tcs)


def final_msg(text: str) -> _Msg:
    """Mensagem final de texto puro (encerra o loop)."""
    return _Msg(content=text, tool_calls=None)


# ===========================================================================
# Helpers para passos dinâmicos: ler as OBSERVAÇÕES já no histórico
# (é o que o LLM real faz — prova que o dado veio da API, não foi inventado)
# ===========================================================================
def tool_observations(messages: list[dict]) -> list[dict]:
    """Todos os retornos de tool (role:tool) já parseados como dict/JSON."""
    out: list[dict] = []
    for m in messages:
        if m.get("role") == "tool" and isinstance(m.get("content"), str):
            try:
                out.append(json.loads(m["content"]))
            except (json.JSONDecodeError, ValueError):
                out.append({"_raw": m["content"]})
    return out


def find_observation(messages: list[dict], predicate) -> dict | None:
    """A observação mais recente que satisfaz `predicate(dict) -> bool`."""
    for obs in reversed(tool_observations(messages)):
        try:
            if predicate(obs):
                return obs
        except (KeyError, TypeError, IndexError):
            continue
    return None


# ===========================================================================
# StubLLM
# ===========================================================================
_NOT_AMBIGUOUS = '{"ambiguous": false, "clarifying_question": null}'


class StubLLM:
    """LLM determinístico. `script`: lista de _Msg ou callables(messages)->_Msg."""

    def __init__(self, script: list | None = None, ambiguity: str = _NOT_AMBIGUOUS):
        self._script = list(script or [])
        self._ambiguity = ambiguity
        self._i = 0
        self.tool_iterations = 0  # nº de chamadas COM tools (passos do loop)
        self.ambiguity_calls = 0  # nº de pré-checagens de ambiguidade

    async def complete(self, messages: list[dict], tools: list[dict] | None = None):
        if tools is None:
            # Pré-checagem de ambiguidade (ou fallback de síntese — não usado aqui).
            self.ambiguity_calls += 1
            return _Msg(content=self._ambiguity, tool_calls=None)

        if self._i >= len(self._script):
            # Roteiro esgotou sem mensagem final — encerra honestamente o loop.
            return final_msg("Concluído.")
        step = self._script[self._i]
        self._i += 1
        self.tool_iterations += 1
        if callable(step):
            step = step(messages)
        return step


# ===========================================================================
# FakeClient — roteia (method, path) -> operationId pelos templates do spec
# ===========================================================================
def _route_table() -> list[tuple[str, re.Pattern, str]]:
    """[(METHOD, regex_do_path_relativo, operationId)] a partir do spec local."""
    table: list[tuple[str, re.Pattern, str]] = []
    for op_id, entry in _operations_by_id().items():
        method = entry["method"].upper()
        path = entry["path"]
        if path.startswith(_BASE_PATH):
            path = path[len(_BASE_PATH):]
        # {param} -> segmento sem barra
        regex = re.sub(r"\{[^}]+\}", r"[^/]+", path)
        table.append((method, re.compile(f"^{regex}$"), op_id))
    return table


_ROUTES = _route_table()


class FakeClient:
    """Dublê de DionisioClient: roteia para `responses[operationId]`.

    `responses[op_id]` pode ser:
      - dict      -> retornado como resposta 2xx
      - Exception -> levantada (ex: DionisioAPIError para testar erro)
      - callable(method, rel_path, params, body) -> dict (pode levantar)
    """

    def __init__(self, responses: dict, base_url: str = "https://fake.local/api/case-mock"):
        self.responses = responses
        self.base_url = base_url
        self.calls: list[dict] = []

    @staticmethod
    def _resolve(method: str, path: str) -> str | None:
        for m, regex, op_id in _ROUTES:
            if m == method.upper() and regex.match(path):
                return op_id
        return None

    async def request(self, method, path, params=None, body=None) -> dict:
        op_id = self._resolve(method, path)
        self.calls.append(
            {"operation_id": op_id, "method": method.upper(), "path": path,
             "params": params, "body": body}
        )
        if op_id is None:
            raise AssertionError(f"FakeClient: rota não mapeada para {method} {path}")
        if op_id not in self.responses:
            raise AssertionError(f"FakeClient: sem resposta configurada para {op_id} ({method} {path})")
        resp = self.responses[op_id]
        if isinstance(resp, Exception):
            raise resp
        if callable(resp):
            return resp(method, path, params, body)
        return resp

    def called_ops(self) -> list[str]:
        return [c["operation_id"] for c in self.calls]


# ===========================================================================
# FakeRetriever — RetrievalResult fixo; tools reais (params vêm do spec)
# ===========================================================================
def make_operation_docs(op_ids: list[str]) -> list[OperationDoc]:
    """OperationDoc para cada operationId, com method/path reais do spec."""
    destructive = _destructive_ops()
    ops = _operations_by_id()
    out: list[OperationDoc] = []
    for i, op_id in enumerate(op_ids):
        entry = ops.get(op_id)
        if entry is None:
            raise KeyError(f"operationId desconhecido no spec: {op_id}")
        op = entry["op"]
        out.append(
            OperationDoc(
                operation_id=op_id,
                method=entry["method"],
                path=entry["path"],
                domain=op_id.split(".")[0],
                destructive=op_id in destructive,
                summary=op.get("summary", op_id),
                full_text=op.get("summary", op_id),
                score=round(0.9 - i * 0.01, 4),
            )
        )
    return out


class FakeRetriever:
    """Retriever determinístico: sempre devolve o mesmo conjunto de operações."""

    def __init__(self, op_ids: list[str], docs: list[BusinessDoc] | None = None):
        self._operations = make_operation_docs(op_ids)
        self._docs = docs or []

    async def retrieve(self, query, k_operations=5, k_docs=3, exclude_destructive=False):
        ops = self._operations
        if exclude_destructive:
            ops = [o for o in ops if not o.destructive]
        return RetrievalResult(operations=ops, docs=self._docs, query=query)

    async def retrieve_operations_only(self, query, k=8):
        return self._operations[:k]


# ===========================================================================
# confirm_callbacks de teste
# ===========================================================================
@pytest.fixture
def approve():
    """confirm_callback que sempre aprova; grava se foi acionado."""
    state = {"asked": False}

    async def _cb(plan: str) -> bool:
        state["asked"] = True
        return True

    _cb.state = state
    return _cb


@pytest.fixture
def deny():
    """confirm_callback que sempre nega; grava se foi acionado."""
    state = {"asked": False}

    async def _cb(plan: str) -> bool:
        state["asked"] = True
        return False

    _cb.state = state
    return _cb


# Reexporta para os testes
__all__ = [
    "load_fixture", "tool_msg", "final_msg", "tool_observations", "find_observation",
    "StubLLM", "FakeClient", "FakeRetriever", "make_operation_docs", "DionisioAPIError",
]
