"""Wrapper fino do LLM via OpenRouter.

O OpenRouter e OpenAI-compatible, entao usamos o SDK `openai` apontado para a base
do OpenRouter. Tool use no formato function-calling da OpenAI (NAO o protocolo nativo
da Anthropic): `tools=[{"type":"function","function":{...}}]`, `tool_choice="auto"`,
le `response.choices[0].message.tool_calls`, devolve resultado como `role:"tool"`.

Nao adicionamos a dependencia `anthropic` — o modelo (Claude) e acessado via OpenRouter.
"""

from __future__ import annotations

import logging

from openai import AsyncOpenAI

logger = logging.getLogger("dionisio.agent.llm")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "anthropic/claude-sonnet-4"


class LLM:
    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        base_url: str = OPENROUTER_BASE_URL,
    ):
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    async def complete(self, messages: list[dict], tools: list[dict] | None = None):
        """Uma chamada de chat. Retorna a `message` (pode ter content e/ou tool_calls)."""
        logger.info("LLM call (%s): %d msgs, %d tools", self.model, len(messages), len(tools or []))
        resp = await self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools or None,
            tool_choice="auto" if tools else None,
            temperature=0,
        )
        return resp.choices[0].message
