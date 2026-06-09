#!/usr/bin/env python
"""Smoke test do Dia 1 — valida DionisioClient + Retriever de ponta a ponta.

Criterio de conclusao do Dia 1: 7/7 checks passando contra a API real.

Uso:
    uv run python scripts/smoke_test.py
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from client import DionisioClient  # noqa: E402
from rag import Retriever  # noqa: E402

console = Console()


def _ok(msg: str) -> bool:
    console.print(f"  [green]→ {msg} ✓[/green]")
    return True


def _fail(msg: str) -> bool:
    console.print(f"  [red]→ {msg} ✗[/red]")
    return False


def _fmt_ops(ops, n=3) -> str:
    return ", ".join(f"{o.operation_id} ({o.score:.2f})" for o in ops[:n])


async def run() -> int:
    load_dotenv()
    api_key = os.getenv("DIONISIO_API_KEY", "")
    base_url = os.getenv("DIONISIO_BASE_URL", "")
    chroma_path = os.getenv("CHROMA_PATH", "./rag/index")

    results: list[bool] = []
    retriever = Retriever(chroma_path=chroma_path)

    async with DionisioClient(api_key=api_key, base_url=base_url) as client:
        # CHECK 1
        console.print("[bold][CHECK 1][/bold] DionisioClient — GET /clients/inactive?days=60")
        try:
            data = await client.get_inactive_clients(days=60)
            items = data.get("clients") or data.get("data") or data.get("items") or []
            results.append(_ok(f"status 200, {len(items)} clientes retornados"))
        except Exception as e:
            results.append(_fail(f"erro: {e}"))

        # CHECK 2
        today = datetime.now().strftime("%Y-%m-%d")
        console.print(f"[bold][CHECK 2][/bold] DionisioClient — GET /reservations/availability?date={today}")
        try:
            data = await client.get_availability(date=today)
            slots = data.get("slots", [])
            total = data.get("totalCapacity", "?")
            results.append(_ok(f"status 200, {len(slots)} slots, capacidade total {total}"))
        except Exception as e:
            results.append(_fail(f"erro: {e}"))

        # CHECK 3
        console.print("[bold][CHECK 3][/bold] DionisioClient — GET /store")
        try:
            data = await client.get_store()
            results.append(_ok(f'status 200, loja: "{data.get("name", "?")}"'))
        except Exception as e:
            results.append(_fail(f"erro: {e}"))

    # CHECK 4
    console.print('[bold][CHECK 4][/bold] Retriever — query: "clientes inativos ha 60 dias"')
    r = await retriever.retrieve("clientes inativos ha 60 dias", k_operations=3, k_docs=2)
    console.print(f"  top-3 operacoes: {_fmt_ops(r.operations)}")
    console.print(f"  top-2 docs: {', '.join(f'{d.section} ({d.score:.2f})' for d in r.docs)}")
    ids4 = [o.operation_id for o in r.operations]
    if "clients.inactive" in ids4:
        results.append(_ok("clients.inactive presente no top-3"))
    else:
        results.append(_fail(f"clients.inactive ausente (veio: {ids4})"))

    # CHECK 5
    console.print('[bold][CHECK 5][/bold] Retriever — query: "remarcar reserva para sabado"')
    r = await retriever.retrieve("remarcar reserva para sabado", k_operations=3, k_docs=2)
    console.print(f"  top-3 operacoes: {_fmt_ops(r.operations)}")
    top = r.operations[0] if r.operations else None
    if top and top.operation_id == "reservations.reschedule" and top.destructive:
        results.append(_ok("reservations.reschedule no topo, destrutiva=True"))
    else:
        results.append(_fail(f"esperado reservations.reschedule destrutiva no topo (veio: {top.operation_id if top else None})"))

    # CHECK 6
    console.print('[bold][CHECK 6][/bold] Retriever — query: "disparar campanha de reativacao com cupom"')
    ops6 = await retriever.retrieve_operations_only("disparar campanha de reativacao com cupom", k=5)
    ids6 = [o.operation_id for o in ops6]
    console.print(f"  top-5 operacoes: {', '.join(ids6)}")
    expected6 = {"clients.inactive", "coupons.create", "coupons.assignGroup"}
    missing6 = expected6 - set(ids6)
    if not missing6:
        results.append(_ok("inclui clients.inactive, coupons.create, coupons.assignGroup"))
    else:
        results.append(_fail(f"faltando no top-5: {missing6}"))

    # CHECK 7
    console.print('[bold][CHECK 7][/bold] Retriever exclude_destructive=True — query: "cancelar reserva"')
    r = await retriever.retrieve("cancelar reserva", k_operations=5, exclude_destructive=True)
    ids7 = [o.operation_id for o in r.operations]
    console.print(f"  operacoes: {', '.join(ids7)}")
    if "reservations.cancel" not in ids7:
        results.append(_ok("reservations.cancel corretamente excluida"))
    else:
        results.append(_fail("reservations.cancel apareceu apesar de exclude_destructive"))

    passed = sum(results)
    total = len(results)
    color = "green" if passed == total else "red"
    console.print(f"\n[bold {color}]RESULTADO: {passed}/{total} checks passaram[/bold {color}]")
    return 0 if passed == total else 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    raise SystemExit(asyncio.run(run()))
