#!/usr/bin/env python
"""Varredura de cobertura (reachability das 61 operacoes).

Mede, operacao a operacao, se cada uma das 61 funcoes da API e alcancavel pelo agente
a partir de um pedido em linguagem natural de um unico turno, e classifica cada
resultado em:

  ✅ alcancada   — a operationId esperada apareceu em state.actions_taken (resposta
                   benigna da escrita interceptada OU confirmacao negada — ambos contam:
                   o agente selecionou e chamou a operacao certa).
  ⚠️ nome-errado — a esperada nao foi alcancada, mas o agente emitiu um evento de
                   ferramenta desconhecida (method == "?"): existe a capacidade, errou
                   o nome. Reporta o(s) nome(s) alucinado(s).
  ❌ nao-alcancada — a esperada nunca entrou em actions_taken (falso negativo / o
                   retrieval daquele turno nao trouxe a operacao).

Garantias de seguranca (so-leitura na mock compartilhada):
  - GET vai a API REAL (permite encadear ops de {id}: listar para descobrir um id).
  - POST/PUT/PATCH/DELETE sao INTERCEPTADOS (sem rede) e devolvem payload benigno fixo.
  - Toda confirmacao e NEGADA (as 7 destrutivas + coupons.assignGroup nunca disparam).

Live: usa o LLM real (OpenRouter, temperature=0) e o Retriever real — e exatamente o
retrieval-por-turno que esta sob medicao. Consome tokens.

Reusa o padrao de scripts/safety_check.py (Agent/Retriever/LLM reais, confirm_callback,
captura por on_event + actions_taken). Nao toca codigo de runtime.

DOIS MODOS:
  - HIBRIDO (default, ~quase gratis): mede a alcancabilidade ESTRUTURAL das 61 ops sem
    LLM nem API — para cada pedido, roda so o Retriever real + planner.build_tools e
    verifica se a operacao esperada entra na lista de tools daquele turno (Camada A,
    deterministica). So o cenario cross-turn roda AO VIVO (Sonnet real), que e a
    demonstracao concreta da lacuna de cobertura por turno. Camada A nao classifica
    "nome-errado" (isso e comportamento do LLM) — so disponivel/ausente no retrieval.
  - FULL-LIVE (--full-live, ~caro): a varredura completa das 61 ops ao vivo no LLM real,
    classificando cada uma em alcancada/nome-errado/nao-alcancada. Exige creditos.

Uso:
    uv run python scripts/coverage_check.py                # hibrido (default)
    uv run python scripts/coverage_check.py --full-live    # varredura live completa
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent import Agent, ConversationState, planner  # noqa: E402
from agent.llm import LLM, DEFAULT_MODEL  # noqa: E402
from client import DionisioClient  # noqa: E402
from rag import Retriever  # noqa: E402

console = Console()
# Relatorio auto-gerado, escrito dentro do projeto (artefato regeneravel).
REPORT_PATH = Path(__file__).resolve().parents[1] / "coverage_report.md"

# Payload benigno devolvido por toda escrita interceptada — nunca vai a rede.
BENIGN_WRITE_RESULT = {"id": "test", "status": "ok", "items": []}


# ---------------------------------------------------------------------------
# A matriz das 61 operacoes (uma entrada por operationId da API).
# Cada item: (operationId esperada, pedido em PT). Ids literais viram "o primeiro
# da lista / o que mais gastou" para o agente descobrir sozinho via GET real.
# ---------------------------------------------------------------------------
DOMAINS: dict[str, list[tuple[str, str]]] = {
    "analytics": [
        ("analytics.revenue", "qual foi a receita total no último mês?"),
        ("analytics.orders", "me dá as métricas de pedidos do período"),
        ("analytics.reservations", "qual a taxa de comparecimento das reservas no período?"),
        ("analytics.conversations", "quantos atendimentos/conversas tivemos no período?"),
        ("analytics.couponReturns", "qual o retorno que os cupons trouxeram no último mês?"),
        ("analytics.topItems", "quais os itens mais vendidos do cardápio?"),
    ],
    "clients": [
        ("clients.list", "lista os clientes cadastrados"),
        ("clients.create", "cadastra um cliente novo: Maria Teste, telefone 5511999990000"),
        ("clients.search", "procura o cliente chamado João Souza"),
        ("clients.topSpenders", "quem são os clientes que mais gastaram?"),
        ("clients.inactive", "quais clientes estão inativos há mais de 60 dias?"),
        ("clients.get", "mostra os dados do cliente que mais gastou"),
        ("clients.update", "atualiza o telefone do João Souza para 5511988887777"),
        ("clients.insights", "me dá os insights de comportamento do cliente que mais gastou"),
        ("clients.reservations", "lista as reservas do cliente João Souza"),
    ],
    "coupons": [
        ("coupons.list", "quais cupons estão ativos?"),
        ("coupons.create", "cria um cupom de 15% chamado VOLTA15"),
        ("coupons.analytics", "qual o desempenho do cupom BEMVINDO10?"),
        ("coupons.instances", "quais clientes já receberam o cupom BEMVINDO10?"),
        ("coupons.assignGroup", "atribui o cupom BEMVINDO10 ao grupo de clientes inativos"),
        ("coupons.deactivate", "desativa o cupom BEMVINDO10"),
        ("coupons.get", "mostra os detalhes do cupom BEMVINDO10"),
        ("coupons.update", "muda o limite de usos do cupom BEMVINDO10 para 200"),
    ],
    "delivery": [
        ("delivery.getConfig", "como está a configuração do delivery?"),
        ("delivery.updateConfig", "muda o pedido mínimo de delivery para R$30"),
        ("delivery.neighborhoods", "quais bairros a gente atende no delivery?"),
        ("delivery.currentPause", "o delivery está pausado agora?"),
        ("delivery.createPause", "pausa o delivery pelas próximas 2 horas"),
        ("delivery.endPause", "reativa o delivery, encerra a pausa atual"),
    ],
    "ifood": [
        ("ifood.merchants", "lista as lojas conectadas ao ifood"),
        ("ifood.list", "quais pedidos do ifood estão abertos?"),
        ("ifood.get", "mostra os detalhes do primeiro pedido do ifood"),
        ("ifood.confirm", "confirma o primeiro pedido do ifood"),
        ("ifood.dispatch", "despacha pra entrega o primeiro pedido do ifood"),
        ("ifood.cancel", "cancela o primeiro pedido do ifood"),
    ],
    "orders": [
        ("orders.list", "lista os pedidos de hoje"),
        ("orders.create", "registra um pedido de 2 hambúrgueres pra mesa 5"),
        ("orders.stats", "qual o ticket médio e o total de pedidos?"),
        ("orders.get", "mostra os detalhes do primeiro pedido da lista"),
        ("orders.updateStatus", "marca o primeiro pedido como pronto"),
        ("orders.cancel", "cancela o primeiro pedido da lista"),
    ],
    "promotions": [
        ("promotions.list", "quais promoções estão ativas?"),
        ("promotions.create", "cria uma promoção de happy hour das 18h às 20h"),
        ("promotions.analytics", "qual o desempenho da primeira promoção?"),
        ("promotions.get", "mostra os detalhes da primeira promoção"),
        ("promotions.update", "muda o horário da primeira promoção para 17h-19h"),
        ("promotions.delete", "exclui a primeira promoção"),
    ],
    "reservations": [
        ("reservations.list", "quantas reservas temos pra hoje?"),
        ("reservations.create", "cria uma reserva pra 4 pessoas amanhã às 20h no nome de Teste"),
        ("reservations.availability", "tem mesa pra 6 pessoas sábado às 21h?"),
        ("reservations.get", "mostra os detalhes da primeira reserva de hoje"),
        ("reservations.update", "muda pra 5 pessoas a primeira reserva de hoje"),
        ("reservations.confirm", "confirma a primeira reserva de hoje"),
        ("reservations.cancel", "cancela a primeira reserva de hoje"),
        ("reservations.reschedule", "remarca a primeira reserva de hoje pra amanhã no mesmo horário"),
    ],
    "store": [
        ("store.get", "qual o nome e os dados da loja?"),
        ("store.update", "muda o nome da loja para Cantina Teste"),
        ("store.getHours", "qual o horário de funcionamento?"),
        ("store.updateHours", "muda o horário de domingo para 12h às 22h"),
        ("store.members", "quem são os membros/funcionários da loja?"),
        ("store.features", "quais recursos a loja tem habilitados?"),
    ],
}

# Controles de "capacidade inexistente": recusar e CORRETO. Distingue falso negativo
# (ruim) de recusa honesta (boa). Nenhuma escrita deve ser executada.
CONTROLS: list[tuple[str, str]] = [
    ("clients.createGroup (inexistente)", "cria um grupo de clientes chamado Reativação"),
    ("comunicacao SMS/WhatsApp (inexistente)", "manda um WhatsApp pro João avisando da reserva"),
    ("remover prato do cardapio (inexistente)", "tira o Risoto do cardápio"),
]


class RecordingClient:
    """Client gravador so-leitura — duck-typed (o Executor so usa base_url + request).

    GET delega ao client real; toda escrita e interceptada (sem rede) e devolve um
    payload benigno fixo. Assim nenhuma operacao muta a mock compartilhada.
    """

    def __init__(self, real: DionisioClient):
        self._real = real
        self.base_url = real.base_url
        self.writes_intercepted: list[tuple[str, str]] = []

    async def request(self, method, path, params=None, body=None) -> dict:
        if method.upper() == "GET":
            return await self._real.request(method, path, params=params, body=body)
        self.writes_intercepted.append((method.upper(), path))
        return dict(BENIGN_WRITE_RESULT)


async def _deny(_plan: str) -> bool:
    """confirm_callback: SEMPRE nega. Nenhuma destrutiva/mass-effect dispara."""
    return False


def _classify(expected: str, state: ConversationState, hallucinated: list[str]) -> str:
    reached = {a.operation_id for a in state.actions_taken}
    if expected in reached:
        return "✅"
    if hallucinated:
        return "⚠️"
    return "❌"


def _attempts_str(state: ConversationState, hallucinated: list[str]) -> str:
    parts = [f"{a.operation_id}{'' if a.ok else '✗'}" for a in state.actions_taken]
    parts += [f"?{n}" for n in hallucinated]
    return ", ".join(parts) or "—"


async def run_single(agent: Agent, expected: str, prompt: str) -> dict:
    """Roda um turno isolado (estado fresco) e classifica contra a op esperada."""
    state = ConversationState()
    hallucinated: list[str] = []

    def on_event(kind: str, payload: dict) -> None:
        if kind == "tool" and payload.get("method") == "?":
            hallucinated.append(str(payload.get("path")))

    agent._on_event = on_event
    agent._confirm_callback = _deny
    try:
        answer = await agent.run_turn(prompt, state)
    except Exception as exc:  # uma linha que estoura nao derruba a varredura
        return {"expected": expected, "prompt": prompt, "status": "💥",
                "attempts": f"EXCECAO: {type(exc).__name__}: {exc}", "answer": ""}

    return {
        "expected": expected,
        "prompt": prompt,
        "status": _classify(expected, state, hallucinated),
        "attempts": _attempts_str(state, hallucinated),
        "answer": (answer or "").strip().replace("\n", " ")[:160],
    }


async def run_control(agent: Agent, label: str, prompt: str) -> dict:
    """Capacidade inexistente: sucesso = NENHUMA escrita executada (recusa honesta)."""
    state = ConversationState()
    hallucinated: list[str] = []

    def on_event(kind: str, payload: dict) -> None:
        if kind == "tool" and payload.get("method") == "?":
            hallucinated.append(str(payload.get("path")))

    agent._on_event = on_event
    agent._confirm_callback = _deny
    try:
        answer = await agent.run_turn(prompt, state)
    except Exception as exc:  # infra nao derruba o relatorio
        return {"label": label, "prompt": prompt, "refused": None,
                "attempts": f"EXCECAO: {type(exc).__name__}: {exc}", "answer": ""}
    writes = [a.operation_id for a in state.actions_taken if a.method != "GET"]
    refused = not writes
    return {
        "label": label,
        "prompt": prompt,
        "refused": refused,
        "attempts": _attempts_str(state, hallucinated),
        "answer": (answer or "").strip().replace("\n", " ")[:160],
    }


async def run_cross_turn(agent: Agent) -> dict:
    """Reproduz o log: campanha (T1) -> 'faça os passos' (T2). assignGroup alcanca no T2?"""
    state = ConversationState()
    agent._on_event = lambda *_: None
    agent._confirm_callback = _deny

    t1 = "cria uma campanha de reativação para clientes inativos há 60 dias, com um cupom de 15%"
    t2 = "faça os passos exceto o contato"

    try:
        a1 = await agent.run_turn(t1, state)
        n_after_t1 = len(state.actions_taken)
        a2 = await agent.run_turn(t2, state)
    except Exception as exc:  # infra (ex: 402 sem creditos) nao pode derrubar o relatorio
        return {"t1": t1, "a1": f"EXCECAO: {type(exc).__name__}: {exc}", "t2": t2,
                "a2": "", "t2_ops": [], "assign_reached_t2": False, "error": True}

    t2_ops = [a.operation_id for a in state.actions_taken[n_after_t1:]]
    reached_t2 = "coupons.assignGroup" in t2_ops
    return {
        "t1": t1, "a1": (a1 or "").strip().replace("\n", " ")[:200],
        "t2": t2, "a2": (a2 or "").strip().replace("\n", " ")[:200],
        "t2_ops": t2_ops, "assign_reached_t2": reached_t2, "error": False,
    }


async def retrieval_reach(retriever: Retriever, expected: str, prompt: str) -> dict:
    """Camada A (deterministica, sem LLM/API): a op esperada entra na lista de tools?

    Reproduz exatamente o que o agente monta por turno (core.py): retrieval ancorado no
    texto do turno (`exclude_destructive=False`, k_operations=8) + `planner.build_tools`
    (que aplica a expansao de dominio). A op e ALCANCAVEL no turno sse seu
    fn_name (op_id com '.'->'_') esta no fn_map resultante. Distingue se veio do top-k
    do retrieval ou so da expansao de dominio. So embeddings locais — custo ~zero.
    """
    retrieval = await retriever.retrieve(
        prompt, k_operations=8, k_docs=3, exclude_destructive=False
    )
    topk = [op.operation_id for op in retrieval.operations]
    _, fn_map = planner.build_tools(retrieval)
    available = expected.replace(".", "_") in fn_map
    if not available:
        source = "—"
    elif expected in set(topk):
        source = "top-k"
    else:
        source = "expansão"
    return {
        "expected": expected, "prompt": prompt,
        "status": "✅" if available else "❌",
        "source": source, "topk": topk,
    }


# Textos do cenario cross-turn (reproduz o log dos cupons), reusados pela Camada A e
# pela parte ao vivo.
XT_T1 = "cria uma campanha de reativação para clientes inativos há 60 dias, com um cupom de 15%"
XT_T2 = "faça os passos exceto o contato"


async def cross_turn_reach_deterministic(retriever: Retriever) -> dict:
    """Camada A CROSS-TURN (deterministica, sem LLM/API): a prova gratis da persistencia.

    Encadeia turno 1 -> turno 2 pelo MESMO `ConversationState`, acumulando `task_domains`
    exatamente como `core.run_turn` (via `planner.task_domains_of`), e verifica se
    `coupons.assignGroup` entra no `fn_map` do turno 2. Sem estado, a checagem do turno 2 e
    single-turn e da ❌; com a persistencia de dominio da tarefa a expansao de irmas traz o
    dominio `coupons` mesmo o texto do turno 2 nao o mencionando. So embeddings locais +
    spec — custo ~zero.
    """
    state = ConversationState()

    # turno 1: para MEDIR a alcancabilidade nao e preciso o LLM — basta acumular os
    # dominios que o retrieval do turno 1 tocou (e o que core faz antes de montar tools).
    r1 = await retriever.retrieve(XT_T1, k_operations=8, k_docs=3, exclude_destructive=False)
    state.note_domains(planner.task_domains_of(r1.operations))

    # turno 2: monta as tools como core — agora com os dominios PERSISTIDOS da tarefa.
    r2 = await retriever.retrieve(XT_T2, k_operations=8, k_docs=3, exclude_destructive=False)
    state.note_domains(planner.task_domains_of(r2.operations))
    _, fn_map = planner.build_tools(r2, task_domains=state.task_domains)

    t2_topk = [op.operation_id for op in r2.operations]
    reached = "coupons_assignGroup" in fn_map
    if not reached:
        source = "—"
    elif "coupons.assignGroup" in set(t2_topk):
        source = "top-k"
    else:
        source = "expansão (domínio persistido)"
    return {
        "t1": XT_T1, "t2": XT_T2,
        "task_domains": list(state.task_domains),
        "reached": reached, "source": source, "t2_topk": t2_topk,
    }


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
def print_matrix(results: dict[str, list[dict]]) -> None:
    for domain, rows in results.items():
        table = Table(title=f"[bold]{domain}[/bold] ({len(rows)} ops)", show_lines=False)
        table.add_column("status", justify="center")
        table.add_column("esperada", style="cyan")
        table.add_column("ops realmente tentadas")
        for r in rows:
            table.add_row(r["status"], r["expected"], r["attempts"])
        console.print(table)


def build_markdown(results: dict[str, list[dict]], controls: list[dict],
                   cross: dict, counts: Counter, total: int,
                   writes: list[tuple[str, str]]) -> str:
    reached = counts["✅"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L: list[str] = []
    L.append("# Varredura de cobertura (reachability das 61 operações)\n")
    L.append(f"> Gerado por `scripts/coverage_check.py` (live, LLM + Retriever reais) em {now}.\n")
    L.append("Mede, operação a operação, se cada uma das 61 funções da API é alcançável a "
             "partir de um pedido em linguagem natural de um único turno.\n")
    if counts["💥"]:
        L.append(f"> ⚠️ **RUN PARCIAL / INVÁLIDO:** {counts['💥']} operações falharam por erro de "
                 "infraestrutura (status 💥 — ex: HTTP 402, créditos do OpenRouter esgotados), "
                 "não por incapacidade do agente. Esses 💥 **não** são lacunas de cobertura; "
                 "refaça a varredura com créditos suficientes para um diagnóstico válido.\n")
    L.append("## Resumo\n")
    L.append(f"- **{reached}/{total} alcançadas** (✅)")
    L.append(f"- ⚠️ nome-errado: {counts['⚠️']}")
    L.append(f"- ❌ não-alcançada: {counts['❌']}")
    if counts["💥"]:
        L.append(f"- 💥 exceção: {counts['💥']}")
    L.append("")
    L.append("Legenda: ✅ a operationId esperada entrou em `actions_taken` (resposta benigna da "
             "escrita interceptada **ou** confirmação negada — ambos contam). ⚠️ não alcançada, "
             "mas o agente tentou um nome inexistente (capacidade existe, errou o nome). "
             "❌ a esperada nunca foi chamada (falso negativo / não recuperada no turno).\n")

    L.append("## Matriz por domínio\n")
    for domain, rows in results.items():
        L.append(f"### {domain} ({len(rows)})\n")
        L.append("| status | operação esperada | ops realmente tentadas |")
        L.append("|:---:|---|---|")
        for r in rows:
            L.append(f"| {r['status']} | `{r['expected']}` | {r['attempts']} |")
        L.append("")

    L.append("## Falhas destacadas (as lacunas a corrigir num dia futuro)\n")
    failures = [r for rows in results.values() for r in rows if r["status"] in ("⚠️", "❌", "💥")]
    if failures:
        L.append("| status | operação esperada | pedido | ops tentadas |")
        L.append("|:---:|---|---|---|")
        for r in failures:
            L.append(f"| {r['status']} | `{r['expected']}` | {r['prompt']} | {r['attempts']} |")
    else:
        L.append("_Nenhuma — todas as 61 alcançadas._")
    L.append("")

    L.append("## Cenário cross-turn (reproduz a falha do log)\n")
    L.append(f"- **Turno 1:** {cross['t1']}")
    L.append(f"  - resposta: {cross['a1']}")
    L.append(f"- **Turno 2:** {cross['t2']}")
    L.append(f"  - resposta: {cross['a2']}")
    L.append(f"  - ops no turno 2: {cross['t2_ops'] or '—'}")
    verdict = "✅ SIM" if cross["assign_reached_t2"] else "❌ NÃO"
    L.append(f"- **`coupons.assignGroup` alcançada no turno 2?** {verdict}")
    if not cross["assign_reached_t2"]:
        L.append("  - Confirma a hipótese: o turno de continuação não menciona o domínio `coupons`, "
                 "o retrieval daquele turno não o traz, e a operação fica inalcançável — a "
                 "alcançabilidade depende da redação do turno atual.")
    L.append("")

    L.append("## Controles — capacidades inexistentes (recusar é CORRETO)\n")
    L.append("| capacidade | recusou? | pedido | ops tentadas |")
    L.append("|---|:---:|---|---|")
    for c in controls:
        mark = "💥 infra" if c["refused"] is None else ("✅ recusou" if c["refused"] else "❌ executou")
        L.append(f"| {c['label']} | {mark} | {c['prompt']} | {c['attempts']} |")
    L.append("")

    L.append("## Integridade (zero mutação na mock)\n")
    L.append(f"- Escritas interceptadas (sem rede): **{len(writes)}**.")
    L.append("- Toda confirmação foi **negada** (`confirm_callback` fixo em `False`) — nenhuma "
             "destrutiva nem `coupons.assignGroup` disparou.")
    L.append("- GET foi à API real (necessário para encadear operações de `{id}`).")
    if writes:
        sample = ", ".join(f"`{m} {p}`" for m, p in writes[:12])
        L.append(f"- Amostra das interceptadas: {sample}{' …' if len(writes) > 12 else ''}")
    L.append("")
    return "\n".join(L)


async def run_full_live(retriever: Retriever, llm: LLM) -> int:
    """Varredura COMPLETA ao vivo das 61 ops (cara — exige creditos)."""
    async with DionisioClient(api_key=os.getenv("DIONISIO_API_KEY", ""),
                              base_url=os.getenv("DIONISIO_BASE_URL", "")) as real:
        rec = RecordingClient(real)
        agent = Agent(llm=llm, retriever=retriever, client=rec)

        total = sum(len(v) for v in DOMAINS.values())
        console.rule(f"[bold]Varredura de {total} operações (FULL LIVE)")

        results: dict[str, list[dict]] = {}
        for domain, ops in DOMAINS.items():
            rows = []
            for expected, prompt in ops:
                console.print(f"  [{domain}] {expected} …", style="dim")
                rows.append(await run_single(agent, expected, prompt))
            results[domain] = rows

        console.rule("[bold]Cenário cross-turn")
        cross = await run_cross_turn(agent)

        console.rule("[bold]Controles — capacidades inexistentes")
        controls = [await run_control(agent, label, prompt) for label, prompt in CONTROLS]

        # ----- render -----
        console.rule("[bold]Matriz de cobertura")
        print_matrix(results)

        counts: Counter = Counter()
        for rows in results.values():
            for r in rows:
                counts[r["status"]] += 1
        reached = counts["✅"]

        console.rule("[bold]Resumo")
        console.print(f"[bold green]{reached}/{total} alcançadas[/bold green] "
                      f"(✅ {counts['✅']} · ⚠️ {counts['⚠️']} · ❌ {counts['❌']}"
                      + (f" · 💥 {counts['💥']}" if counts['💥'] else "") + ")")

        failures = [r for rows in results.values() for r in rows
                    if r["status"] in ("⚠️", "❌", "💥")]
        if failures:
            console.print("\n[bold red]Falhas (lacunas a corrigir):[/bold red]")
            for r in failures:
                console.print(f"  {r['status']} {r['expected']:<26} -> {r['attempts']}")

        verdict = "[red]NÃO[/red]" if not cross["assign_reached_t2"] else "[green]SIM[/green]"
        console.print(f"\n[bold]Cross-turn:[/bold] coupons.assignGroup alcançada no turno 2? {verdict}")
        console.print(f"  ops no turno 2: {cross['t2_ops'] or '—'}")

        console.print("\n[bold]Controles (recusar = correto):[/bold]")
        for c in controls:
            mark = ("[yellow]INFRA[/yellow]" if c["refused"] is None
                    else "[green]recusou[/green]" if c["refused"] else "[red]EXECUTOU[/red]")
            console.print(f"  {mark}  {c['label']}  -> {c['attempts']}")

        console.print(f"\n[bold]Integridade:[/bold] {len(rec.writes_intercepted)} escritas "
                      f"interceptadas (sem rede); toda confirmação negada.")

        md = build_markdown(results, controls, cross, counts, total, rec.writes_intercepted)
        REPORT_PATH.write_text(md, encoding="utf-8")
        console.print(f"\n[green]Relatório salvo em[/green] {REPORT_PATH}")

    return 0


# ===========================================================================
# Modo HIBRIDO (default) — Camada A gratis + cross-turn ao vivo
# ===========================================================================
def print_retrieval_matrix(results: dict[str, list[dict]]) -> None:
    for domain, rows in results.items():
        table = Table(title=f"[bold]{domain}[/bold] ({len(rows)} ops)", show_lines=False)
        table.add_column("disp.", justify="center")
        table.add_column("operação esperada", style="cyan")
        table.add_column("origem / o que o retrieval trouxe")
        for r in rows:
            if r["status"] == "✅":
                detail = f"via {r['source']}"
            else:
                detail = "trouxe: " + ", ".join(r["topk"][:6])
            table.add_row(r["status"], r["expected"], detail)
        console.print(table)


def build_markdown_hybrid(results, counts, total, cross, t2_reach, xt,
                          controls_reach, writes) -> str:
    avail = counts["✅"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L: list[str] = []
    L.append("# Varredura de cobertura (reachability das 61 operações)\n")
    L.append(f"> Gerado por `scripts/coverage_check.py` (modo **híbrido**) em {now}.\n")
    L.append("Mede a alcançabilidade **estrutural** de cada uma das 61 operações: a partir de "
             "um pedido em linguagem natural de um único turno, o retrieval-por-turno coloca a "
             "operação esperada na lista de ferramentas daquele turno? Inclui as dicas curadas "
             "(`orders.stats`/`promotions.update`) e a persistência de domínio cross-turn.\n")
    L.append("## Método\n")
    L.append("- **Camada A (determinística, sem LLM/API, custo ~zero):** para cada pedido, roda o "
             "`Retriever` real (`k_operations=8`, `exclude_destructive=False`) + "
             "`planner.build_tools` — exatamente o que `agent/core.py` monta por turno, incluindo a "
             "expansão de domínio. A operação é **alcançável** sse seu `fn_name` entra no "
             "`fn_map` resultante. Distingue se veio do **top-k** do retrieval ou só da **expansão "
             "de domínio**.")
    L.append("- **Cross-turn AO VIVO (Sonnet real):** o cenário do log roda de ponta a ponta no LLM "
             "real — a demonstração concreta da lacuna de cobertura por turno.")
    L.append("- **Por que híbrido:** a varredura completa ao vivo das 61 (✅/⚠️ nome-errado/❌) "
             "custaria ~$8 em `claude-sonnet-4`. A Camada A captura **toda a lacuna estrutural** "
             "(a op nem entra na lista de tools — o caso dos cupons) de graça; a classe "
             "\"nome-errado\" é comportamento do LLM e fica para o modo `--full-live`.\n")
    L.append("## Resumo\n")
    L.append(f"- **{avail}/{total} alcançáveis no retrieval-por-turno** (✅ a op entra na lista de "
             "tools do turno).")
    L.append(f"- ❌ não disponibilizadas pelo retrieval do turno: {counts['❌']} — as **lacunas "
             "estruturais**.")
    L.append("")

    L.append("## Matriz de alcançabilidade (Camada A) por domínio\n")
    for domain, rows in results.items():
        L.append(f"### {domain} ({len(rows)})\n")
        L.append("| disp. | operação esperada | origem / o que o retrieval trouxe |")
        L.append("|:---:|---|---|")
        for r in rows:
            detail = f"via {r['source']}" if r["status"] == "✅" else "trouxe: " + ", ".join(r["topk"][:6])
            L.append(f"| {r['status']} | `{r['expected']}` | {detail} |")
        L.append("")

    L.append("## Lacunas estruturais (❌ — a op não entra na lista de tools do turno)\n")
    gaps = [r for rows in results.values() for r in rows if r["status"] == "❌"]
    if gaps:
        L.append("| operação esperada | pedido | o retrieval trouxe |")
        L.append("|---|---|---|")
        for r in gaps:
            L.append(f"| `{r['expected']}` | {r['prompt']} | {', '.join(r['topk'][:6])} |")
    else:
        L.append("_Nenhuma — todas as 61 entram na lista de tools do seu turno._")
    L.append("")

    L.append("## Cenário cross-turn (reproduz a falha do log)\n")
    if cross.get("error"):
        L.append("> ⚠️ **A parte AO VIVO não rodou** (bloqueio de credencial/crédito do LLM — "
                 f"`{cross['a1']}`). A conclusão estrutural abaixo vem da **Camada A** "
                 "(determinística, grátis), que reproduz a lacuna sem precisar do LLM.\n")
    else:
        L.append("- **Turno 1:** {}".format(cross["t1"]))
        L.append(f"  - resposta: {cross['a1']}")
        L.append(f"- **Turno 2:** {cross['t2']}")
        L.append(f"  - resposta: {cross['a2']}")
        L.append(f"  - ops no turno 2: {cross['t2_ops'] or '—'}")
        verdict = "✅ SIM" if cross["assign_reached_t2"] else "❌ NÃO"
        L.append(f"- **`coupons.assignGroup` alcançada no turno 2 (ao vivo)?** {verdict}")
    L.append(f"- **Camada A SINGLE-turn no texto do turno 2** (\"{cross['t2']}\", sem estado): "
             f"`coupons.assignGroup` entra na lista de tools? **{t2_reach['status']}** "
             f"({t2_reach['source']}). Retrieval trouxe: {', '.join(t2_reach['topk'][:6])}.")
    if t2_reach["status"] == "❌":
        L.append("  - Sem estado, a continuação (\"faça os passos...\") não menciona o domínio "
                 "`coupons`; o retrieval daquele turno não o traz e a expansão de domínio se esgota "
                 "nos domínios recuperados antes de chegar a `coupons`.")
    xt_verdict = "✅ SIM" if xt["reached"] else "❌ NÃO"
    L.append(f"- **Camada A CROSS-turn (com estado persistido):** encadeando turno 1 → turno 2 "
             f"pelo mesmo `ConversationState` (domínios acumulados: {', '.join(xt['task_domains'])}), "
             f"`coupons.assignGroup` alcançável no turno 2? **{xt_verdict}** (via {xt['source']}).")
    if xt["reached"]:
        L.append("  - A persistência de domínio traz as irmãs do domínio `coupons` que a **tarefa** "
                 "tocou no turno 1 — mesmo o texto do turno 2 não mencionando cupom. Prova "
                 "determinística, sem gastar token. Antes ❌ (single-turn) → depois ✅ (cross-turn).")
    L.append("")

    L.append("## Controles — capacidades inexistentes (Camada A)\n")
    L.append("Não há `operationId` no spec para essas capacidades, então o retrieval nunca tem o que "
             "recuperar — a recusa é **estrutural**. A verificação da *recusa honesta ao vivo* "
             "(comportamento do LLM) fica para o modo `--full-live`.\n")
    L.append("| capacidade | pedido | o retrieval trouxe |")
    L.append("|---|---|---|")
    for r in controls_reach:
        L.append(f"| {r['expected']} | {r['prompt']} | {', '.join(r['topk'][:6])} |")
    L.append("")

    L.append("## Integridade (zero mutação na mock)\n")
    L.append("- A Camada A é só-leitura por construção: não chama o LLM nem a API (só embeddings "
             "locais + spec).")
    L.append(f"- No cross-turn ao vivo, escritas interceptadas (sem rede): **{len(writes)}**; toda "
             "confirmação foi **negada** — `coupons.assignGroup` e destrutivas nunca dispararam.")
    if writes:
        sample = ", ".join(f"`{m} {p}`" for m, p in writes[:12])
        L.append(f"- Amostra das interceptadas: {sample}{' …' if len(writes) > 12 else ''}")
    L.append("")
    L.append("## Como a cobertura é garantida\n")
    L.append("- **Turno único:** dicas curadas em `_OPERATION_HINTS` (`rag/indexer.py`) para "
             "`orders.stats` (ticket médio / total de pedidos) e `promotions.update` (mudar "
             "horário/condições de uma promoção) — ambas entram na lista de tools do próprio pedido.")
    L.append("- **Cross-turn:** persistência de domínio no `ConversationState` (`task_domains`) "
             "expandida com prioridade em `planner._expand_domain_siblings` — a continuação mantém "
             "os domínios que a tarefa já tocou, sem reancorar o retrieval no histórico inteiro.")
    L.append("- **Ambiguidade `orders.stats` × `analytics.orders`:** ambas ficam disponíveis (são "
             "respostas legítimas a recortes diferentes de \"métricas de pedidos\"); a dica só "
             "garante que `orders.stats` também apareça, sem derrubar `analytics.orders`.\n")
    return "\n".join(L)


async def run_hybrid(retriever: Retriever, llm: LLM) -> int:
    """Default: Camada A determinística das 61 (gratis) + cross-turn ao vivo."""
    total = sum(len(v) for v in DOMAINS.values())
    console.rule(f"[bold]Alcançabilidade de retrieval ({total} ops, Camada A grátis)")

    results: dict[str, list[dict]] = {}
    for domain, ops in DOMAINS.items():
        rows = []
        for expected, prompt in ops:
            rows.append(await retrieval_reach(retriever, expected, prompt))
        results[domain] = rows
        avail = sum(1 for r in rows if r["status"] == "✅")
        console.print(f"  [{domain}] {avail}/{len(rows)} disponíveis", style="dim")

    # controles (capacidade inexistente): retrieval nunca tem a op -> sempre ❌
    controls_reach = [await retrieval_reach(retriever, label, prompt)
                      for label, prompt in CONTROLS]

    # cross-turn AO VIVO (a unica parte que gasta token). Pré-checa a credencial:
    # o agente fala com o LLM via OpenRouter (sk-or-...). Sem uma chave OpenRouter
    # valida, pula a parte ao vivo em vez de estourar 401 — a conclusão estrutural
    # vem da Camada A (turno 2) de qualquer forma.
    t2_text = "faça os passos exceto o contato"
    or_key = os.getenv("OPENROUTER_API_KEY", "")
    console.rule("[bold]Cenário cross-turn (AO VIVO — Sonnet real)")
    writes: list = []
    if not or_key.startswith("sk-or"):
        console.print("[yellow]Pulando a parte AO VIVO:[/yellow] OPENROUTER_API_KEY não é uma chave "
                      "OpenRouter (sk-or-...). O agente fala com o LLM via OpenRouter.", style="yellow")
        cross = {"t1": "cria uma campanha de reativação para clientes inativos há 60 dias, com um cupom de 15%",
                 "a1": "credencial OpenRouter ausente (OPENROUTER_API_KEY não é sk-or-...)",
                 "t2": t2_text, "a2": "", "t2_ops": [], "assign_reached_t2": False, "error": True}
    else:
        async with DionisioClient(api_key=os.getenv("DIONISIO_API_KEY", ""),
                                  base_url=os.getenv("DIONISIO_BASE_URL", "")) as real:
            rec = RecordingClient(real)
            agent = Agent(llm=llm, retriever=retriever, client=rec)
            cross = await run_cross_turn(agent)
            writes = rec.writes_intercepted
    # Camada A no texto do turno 2 (deterministico, gratis — roda mesmo sem LLM).
    # SINGLE-turn (sem estado): a continuacao sozinha nao alcanca assignGroup (❌, "antes").
    t2_reach = await retrieval_reach(retriever, "coupons.assignGroup", cross["t2"])
    # CROSS-turn (com estado persistido): a prova da persistencia de dominio (✅, "depois").
    xt = await cross_turn_reach_deterministic(retriever)

    # ----- render -----
    console.rule("[bold]Matriz de alcançabilidade de retrieval (Camada A)")
    print_retrieval_matrix(results)

    counts: Counter = Counter()
    for rows in results.values():
        for r in rows:
            counts[r["status"]] += 1
    avail = counts["✅"]

    console.rule("[bold]Resumo")
    console.print(f"[bold green]{avail}/{total} alcançáveis no retrieval-por-turno[/bold green] "
                  f"(❌ {counts['❌']} lacunas estruturais)")

    gaps = [r for rows in results.values() for r in rows if r["status"] == "❌"]
    if gaps:
        console.print("\n[bold red]Lacunas estruturais (op não entra na lista de tools):[/bold red]")
        for r in gaps:
            console.print(f"  ❌ {r['expected']:<26} -> trouxe: {', '.join(r['topk'][:5])}")

    if cross.get("error"):
        console.print(f"\n[yellow]Cross-turn ao vivo falhou (infra):[/yellow] {cross['a1']}")
    else:
        verdict = "[red]NÃO[/red]" if not cross["assign_reached_t2"] else "[green]SIM[/green]"
        console.print(f"\n[bold]Cross-turn (ao vivo):[/bold] coupons.assignGroup alcançada no turno 2? {verdict}")
        console.print(f"  ops no turno 2: {cross['t2_ops'] or '—'}")
    console.print(f"  [dim]Camada A single-turn no texto do turno 2 (sem estado): assignGroup "
                  f"{t2_reach['status']} ({t2_reach['source']}) — a continuação sozinha não basta.[/dim]")
    xt_verdict = "[green]✅ SIM[/green]" if xt["reached"] else "[red]❌ NÃO[/red]"
    console.print(f"\n[bold]Cross-turn determinístico (com estado persistido):[/bold] "
                  f"coupons.assignGroup alcançável no turno 2? {xt_verdict} (via {xt['source']})")
    console.print(f"  [dim]domínios persistidos da tarefa: {', '.join(xt['task_domains'])}[/dim]")
    console.print(f"\n[bold]Integridade:[/bold] {len(writes)} escritas interceptadas no cross-turn "
                  "(sem rede); confirmação negada; Camada A não toca LLM/API.")

    md = build_markdown_hybrid(results, counts, total, cross, t2_reach, xt,
                               controls_reach, writes)
    REPORT_PATH.write_text(md, encoding="utf-8")
    console.print(f"\n[green]Relatório salvo em[/green] {REPORT_PATH}")
    return 0


async def main() -> int:
    parser = argparse.ArgumentParser(description="Varredura de cobertura das 61 operações.")
    parser.add_argument("--full-live", action="store_true",
                        help="varredura COMPLETA ao vivo das 61 ops (cara — exige créditos). "
                             "Default: modo híbrido (Camada A grátis + cross-turn ao vivo).")
    args = parser.parse_args()

    load_dotenv()
    retriever = Retriever(chroma_path=os.getenv("CHROMA_PATH", "./rag/index"))
    llm = LLM(api_key=os.getenv("OPENROUTER_API_KEY", ""),
              model=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL))

    if args.full_live:
        return await run_full_live(retriever, llm)
    return await run_hybrid(retriever, llm)


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
