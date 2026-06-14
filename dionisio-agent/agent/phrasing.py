"""Phrasing — traduz o plano de confirmacao para LINGUAGEM DE OPERADOR.

Motivo (observado em uso real): antes, a confirmacao de uma acao destrutiva mostrava
`reservations.reschedule (POST /reservations/{id}/reschedule). Parametros: start=178...`
— ininteligivel para um dono de restaurante. Aqui mapeamos as **8 operacoes que exigem
confirmacao** (7 `x-destructive` + `coupons.assignGroup`) para uma frase de restaurante,
e humanizamos os argumentos uteis (timestamp em ms -> data/hora). O conjunto e fechado:
so essas operacoes chegam ao `_build_plan`, entao o mapa nao precisa cobrir as 61.

Nao expomos IDs crus nem campos JSON ao operador — ele acabou de pedir a acao e tem o
contexto; mostramos O QUE sera feito, o detalhe relevante (ex: novo horario) e o aviso
de irreversibilidade (vindo ja humanizado de `confirmation_reason`).
"""

from __future__ import annotations

from datetime import datetime

# operationId -> acao em linguagem de operador (verbo + alvo).
_OP_PHRASES: dict[str, str] = {
    "reservations.cancel": "cancelar a reserva",
    "reservations.reschedule": "remarcar a reserva",
    "orders.cancel": "cancelar o pedido",
    "coupons.deactivate": "desativar o cupom",
    "coupons.assignGroup": "aplicar o cupom a todos os clientes do grupo",
    "promotions.delete": "excluir a promocao",
    "delivery.createPause": "pausar o delivery",
    "ifood.cancel": "cancelar o pedido do iFood",
}

# Campos de tempo (epoch ms) que vale a pena mostrar como data/hora.
_TIME_FIELDS = ("start", "end", "periodStart", "periodEnd")


def _fmt_ms(value) -> str | None:
    """Timestamp em ms -> 'dd/mm às HHhMM'. None se nao parecer um epoch em ms."""
    try:
        ms = int(value)
    except (TypeError, ValueError):
        return None
    if ms < 10_000_000_000:  # provavelmente nao e epoch em milissegundos
        return None
    dt = datetime.fromtimestamp(ms / 1000)
    return dt.strftime("%d/%m as %Hh%M")


def _detail(operation_id: str, args: dict) -> str:
    """Detalhe humano relevante para a acao (ex: novo horario da remarcacao)."""
    if operation_id == "reservations.reschedule":
        when = _fmt_ms(args.get("start"))
        return f" para {when}" if when else ""
    if operation_id == "delivery.createPause":
        ini, fim = _fmt_ms(args.get("start")), _fmt_ms(args.get("end"))
        if ini and fim:
            return f" de {ini} ate {fim}"
        return ""
    return ""


def humanize_plan(operation_id: str, args: dict, reason: str) -> str:
    """Plano de confirmacao em linguagem de restaurante (sem jargao tecnico)."""
    acao = _OP_PHRASES.get(operation_id, "fazer esta alteracao")
    detalhe = _detail(operation_id, args or {})
    aviso = reason.strip()
    aviso = f" {aviso[0].upper()}{aviso[1:]}." if aviso else ""
    return f"Vou {acao}{detalhe}.{aviso}\nPosso confirmar?"
