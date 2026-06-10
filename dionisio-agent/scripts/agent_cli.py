#!/usr/bin/env python
"""CLI interativo do agente do Dionisio (Dia 2).

Loop de input/output no terminal, mantendo UM ConversationState ao longo da sessao
(multi-turno). Mostra de forma enxuta o que o agente fez (retrieval + tool calls) — util
para a demo e para debugging.

Uso:
    uv run python scripts/agent_cli.py
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent import Agent, ConversationState  # noqa: E402
from agent.llm import LLM, DEFAULT_MODEL  # noqa: E402
from client import DionisioClient  # noqa: E402
from rag import Retriever  # noqa: E402

console = Console()
EXIT_WORDS = {"sair", "exit", "quit", "q"}


def _make_observer(console: Console):
    """Callback que imprime retrieval e tool calls de forma enxuta."""

    def on_event(kind: str, payload: dict) -> None:
        if kind == "retrieve":
            ops = payload["operations"]
            shown = ", ".join(f"{o.operation_id} ({o.score:.2f})" for o in ops[:5])
            console.print(f"  [dim][retrieve][/dim] {shown}")
        elif kind == "tool":
            color = "green" if payload["ok"] else "red"
            console.print(
                f"  [{color}][tool][/{color}]     {payload['method']} {payload['path']} "
                f"-> {payload['summary']}"
            )

    return on_event


async def main() -> int:
    load_dotenv()
    api_key = os.getenv("DIONISIO_API_KEY", "")
    base_url = os.getenv("DIONISIO_BASE_URL", "")
    chroma_path = os.getenv("CHROMA_PATH", "./rag/index")
    or_key = os.getenv("OPENROUTER_API_KEY", "")
    or_model = os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)

    if not or_key:
        console.print("[red]OPENROUTER_API_KEY ausente no .env — necessario para o LLM.[/red]")
        return 1

    retriever = Retriever(chroma_path=chroma_path)
    llm = LLM(api_key=or_key, model=or_model)
    state = ConversationState()

    console.print("[bold]Dionisio[/bold] — assistente do operador. "
                  "Digite seu pedido (ou 'sair').")
    console.print(f"[dim]modelo: {or_model}[/dim]\n")

    async with DionisioClient(api_key=api_key, base_url=base_url) as client:
        agent = Agent(llm=llm, retriever=retriever, client=client,
                      on_event=_make_observer(console))

        while True:
            try:
                user_input = console.input("[bold cyan]> [/bold cyan]").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\nAte logo.")
                break

            if not user_input:
                continue
            if user_input.lower() in EXIT_WORDS:
                console.print("Ate logo.")
                break

            try:
                answer = await agent.run_turn(user_input, state)
            except Exception as e:  # rede/LLM fora do controle do loop ReAct
                console.print(f"  [red]Erro inesperado: {e}[/red]")
                logging.getLogger("dionisio").exception("erro no turno")
                continue

            console.print(f"  [bold]{answer}[/bold]\n")

    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    raise SystemExit(asyncio.run(main()))
