"""Core — o loop ReAct (reason -> act -> observe -> repeat).

Um turno:
1. Retrieval (exclude_destructive=True no Dia 2 — destrutividade e do Dia 3).
2. Monta tools a partir do retrieval (uma vez por turno).
3. Loop (max 8 iteracoes): chama o LLM; se ha tool_calls, executa e devolve observacoes
   como mensagens role:tool; senao, o texto do LLM e a resposta -> sai do loop.
4. Estourou 8 iteracoes -> falha parcial honesta.

Erros de API viram observacoes textuais (no executor) — nunca derrubam o turno.
"""

from __future__ import annotations

import logging
from typing import Callable

from client import DionisioClient
from rag import Retriever

from . import planner, responder
from .executor import Executor
from .llm import LLM
from .state import ConversationState

logger = logging.getLogger("dionisio.agent.core")

MAX_ITERATIONS = 8


class Agent:
    """Agente single-agent ReAct. Reusa um DionisioClient ja aberto na sessao."""

    def __init__(
        self,
        llm: LLM,
        retriever: Retriever,
        client: DionisioClient,
        on_event: Callable[[str, dict], None] | None = None,
    ):
        self.llm = llm
        self.retriever = retriever
        self.executor = Executor(client)
        self._on_event = on_event or (lambda *_: None)

    def _emit(self, kind: str, payload: dict) -> None:
        try:
            self._on_event(kind, payload)
        except Exception:  # observador nunca quebra o turno
            logger.debug("on_event falhou", exc_info=True)

    @staticmethod
    def _msg_to_dict(msg) -> dict:
        d: dict = {"role": "assistant", "content": msg.content}
        if msg.tool_calls:
            d["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ]
        return d

    async def run_turn(self, user_input: str, state: ConversationState) -> str:
        state.iterations = 0

        retrieval = await self.retriever.retrieve(
            user_input, k_operations=5, k_docs=3, exclude_destructive=True
        )
        self._emit("retrieve", {"operations": retrieval.operations, "docs": retrieval.docs})
        tools, fn_map = planner.build_tools(retrieval)

        state.messages.append({"role": "user", "content": user_input})

        messages: list[dict] = []
        for i in range(MAX_ITERATIONS):
            state.iterations = i + 1
            messages = planner.build_messages(state, retrieval)
            msg = await self.llm.complete(messages=messages, tools=tools)
            state.messages.append(self._msg_to_dict(msg))

            if not msg.tool_calls:
                break  # texto puro = resposta final

            for call in msg.tool_calls:
                before = len(state.actions_taken)
                observation = await self.executor.run(call, fn_map, state)
                if len(state.actions_taken) > before:
                    rec = state.actions_taken[-1]
                    self._emit("tool", {
                        "method": rec.method, "path": rec.path,
                        "ok": rec.ok, "summary": rec.summary,
                    })
                else:
                    self._emit("tool", {"method": "?", "path": call.function.name,
                                         "ok": False, "summary": observation[:120]})
                state.messages.append(
                    {"role": "tool", "tool_call_id": call.id, "content": observation}
                )
        else:
            # estourou MAX_ITERATIONS sem resposta final
            logger.warning("limite de %d iteracoes atingido", MAX_ITERATIONS)
            return responder.partial_failure(state)

        return await responder.synthesize(state, self.llm, messages)
