#!/usr/bin/env python
"""Constroi (do zero) o indice RAG no ChromaDB. Idempotente.

Uso:
    uv run python scripts/build_index.py
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

# Permite rodar o script direto (sem instalar o pacote).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rag.indexer import build_index  # noqa: E402

console = Console()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    load_dotenv()

    chroma_path = os.getenv("CHROMA_PATH", "./rag/index")
    base_url = os.getenv("DIONISIO_BASE_URL")

    console.print(f"[bold]Construindo indice RAG[/bold] em [cyan]{chroma_path}[/cyan] ...")
    summary = build_index(chroma_path=chroma_path, base_url=base_url)

    table = Table(title="Indice RAG construido", show_header=True, header_style="bold green")
    table.add_column("Namespace")
    table.add_column("Itens", justify="right")
    table.add_row("api_operations (operacoes)", str(summary["operations"]))
    table.add_row("  └ destrutivas", str(summary["destructive"]))
    table.add_row("business_docs (chunks)", str(summary["doc_chunks"]))
    console.print(table)
    console.print("[bold green]OK[/bold green] — indice persistido em disco.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
