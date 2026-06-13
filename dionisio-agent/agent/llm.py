"""Wrapper fino do LLM via OpenRouter.

O OpenRouter e OpenAI-compatible, entao usamos o SDK `openai` apontado para a base
do OpenRouter. Tool use no formato function-calling da OpenAI (NAO o protocolo nativo
da Anthropic): `tools=[{"type":"function","function":{...}}]`, `tool_choice="auto"`,
le `response.choices[0].message.tool_calls`, devolve resultado como `role:"tool"`.

Nao adicionamos a dependencia `anthropic` — o modelo (Claude) e acessado via OpenRouter.
"""

from __future__ import annotations

import logging
import os

from openai import AsyncOpenAI

logger = logging.getLogger("dionisio.agent.llm")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "anthropic/claude-sonnet-4"
# Teto de saida por chamada. O agente so produz tool_calls curtas e respostas curtas
# ao operador, entao 4096 sobra. Tambem evita que o OpenRouter RESERVE o teto do modelo
# (~64k tokens) por requisicao — uma reserva que pode exceder o saldo da chave e devolver
# 402 mesmo com uso real baixo. Sobrescrevivel por env (ex: OPENROUTER_MAX_TOKENS=2048).
DEFAULT_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "4096"))


class LLM:
    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        base_url: str = OPENROUTER_BASE_URL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ):
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.max_tokens = max_tokens

    async def complete(self, messages: list[dict], tools: list[dict] | None = None):
        """Uma chamada de chat. Retorna a `message` (pode ter content e/ou tool_calls)."""
        logger.info("LLM call (%s): %d msgs, %d tools", self.model, len(messages), len(tools or []))
        resp = await self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools or None,
            tool_choice="auto" if tools else None,
            temperature=0,
            max_tokens=self.max_tokens,
        )
        return resp.choices[0].message
