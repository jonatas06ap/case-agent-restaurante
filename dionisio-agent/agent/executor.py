"""Executor — despacha tool_calls do LLM para o DionisioClient.

Para cada tool_call:
1. Resolve nome_funcao -> (operation_id, method, path, locations) pelo fn_map.
2. Parseia os argumentos (string JSON) para dict.
3. Separa path params (preenche {id}), query params (GET) e body (POST/PATCH).
4. Chama o `request()` generico do client (uma rota cobre as 61 operacoes).
5. Sucesso -> observacao = JSON retornado. DionisioAPIError -> observacao textual legivel
   (o loop continua; o LLM decide). NUNCA propaga exception que derruba o turno.
6. Grava ToolCallRecord em state.actions_taken e promove IDs a state.discovered_entities.
"""

from __future__ import annotations

import json
import logging
from typing import Awaitable, Callable
from urllib.parse import urlparse

from client import DionisioAPIError, DionisioClient
from safety.destructive import confirmation_reason, requires_confirmation

from . import calculator
from .phrasing import humanize_plan
from .state import ConversationState, ToolCallRecord

logger = logging.getLogger("dionisio.agent.executor")

# Limite defensivo do tamanho da observacao devolvida ao LLM (evita estourar contexto).
_MAX_OBSERVATION_CHARS = 6000


class Executor:
    def __init__(self, client: DionisioClient):
        self.client = client
        # Prefixo de path ja embutido no base_url (ex: "/api/case-mock"); os paths do
        # spec o incluem, entao removemos para nao duplicar.
        self._base_path = urlparse(client.base_url).path.rstrip("/")

    def _relative_path(self, spec_path: str, path_args: dict) -> str:
        path = spec_path
        if self._base_path and path.startswith(self._base_path):
            path = path[len(self._base_path):]
        for name, value in path_args.items():
            path = path.replace("{" + name + "}", str(value))
        return path or "/"

    async def run(
        self,
        tool_call,
        fn_map: dict,
        state: ConversationState,
        confirm_callback: Callable[[str], Awaitable[bool]] | None = None,
    ) -> str:
        """Executa um tool_call e devolve a observacao textual (mensagem role:tool).

        Se a operacao exige confirmacao (safety.requires_confirmation), monta o
        plano em linguagem natural e chama `confirm_callback(plano)` ANTES da
        chamada HTTP. Sem confirmacao (callback ausente ou negado), nao chama a
        API: devolve observacao de cancelamento e registra ToolCallRecord(ok=False).
        """
        fn_name = tool_call.function.name
        entry = fn_map.get(fn_name)
        if entry is None:
            # Nome errado != capacidade inexistente. Em vez do beco sem saida,
            # sugere os nomes do MESMO dominio disponiveis neste turno para o LLM
            # se autocorrigir no proprio turno (corrige falsos negativos observados
            # em uso real). Sem re-retrieval.
            return self._unknown_tool_hint(fn_name, fn_map)

        # --- parse dos argumentos ---
        raw_args = tool_call.function.arguments or "{}"
        try:
            args = json.loads(raw_args) if isinstance(raw_args, str) else dict(raw_args)
        except json.JSONDecodeError as e:
            return f"Erro: argumentos invalidos para {fn_name} (JSON malformado: {e})."

        # --- ferramenta LOCAL (calculadora): sem API, sem confirmacao ---
        if entry.get("local"):
            return calculator.execute(args)

        locations = entry["locations"]
        path_args = {k: v for k, v in args.items() if locations.get(k) == "path"}
        query_args = {k: v for k, v in args.items() if locations.get(k) == "query"}
        body_args = {k: v for k, v in args.items() if locations.get(k) == "body"}
        # args sem localizacao conhecida: trata como query em GET, body caso contrario.
        method = entry["method"].upper()
        for k, v in args.items():
            if k not in locations:
                (query_args if method == "GET" else body_args)[k] = v

        rel_path = self._relative_path(entry["path"], path_args)
        operation_id = entry["operation_id"]

        # --- barreira de confirmacao, no boundary da tool-call ---
        confirmed: bool | None = None
        if requires_confirmation(operation_id):
            plano = self._build_plan(operation_id, method, rel_path, args)
            approved = await confirm_callback(plano) if confirm_callback else False
            confirmed = bool(approved)
            if not approved:
                summary = "cancelada (sem confirmacao)"
                state.actions_taken.append(
                    ToolCallRecord(
                        operation_id=operation_id,
                        method=method,
                        path=rel_path,
                        arguments=args,
                        ok=False,
                        summary=summary,
                        confirmed=False,
                    )
                )
                logger.info("tool %s -> NAO confirmada, abortada", fn_name)
                return (
                    f"Acao NAO executada (operacao {operation_id}) — o operador nao "
                    f"confirmou. Nada foi alterado. Diga ao operador, em linguagem "
                    f"simples, que a acao foi cancelada e nao realizada."
                )

        # --- chamada HTTP (erro vira observacao, nunca derruba o turno) ---
        try:
            result = await self.client.request(
                method,
                rel_path,
                params=query_args or None,
                body=body_args or None,
            )
            ok = True
            summary = self._summarize_result(result)
            observation = self._truncate(json.dumps(result, ensure_ascii=False))
            self._promote_entities(result, state)
        except DionisioAPIError as e:
            ok = False
            summary = f"Erro {e.status_code}: {self._error_text(e.error_body)}"
            observation = f"Erro {e.status_code} em {method} {rel_path}: {self._error_text(e.error_body)}"
            logger.info("tool %s -> %s", fn_name, summary)

        state.actions_taken.append(
            ToolCallRecord(
                operation_id=operation_id,
                method=method,
                path=rel_path,
                arguments=args,
                ok=ok,
                summary=summary,
                confirmed=confirmed,
            )
        )
        return observation

    # ----- helpers ----------------------------------------------------------
    @staticmethod
    def _build_plan(operation_id: str, method: str, rel_path: str, args: dict) -> str:
        """Plano curto e honesto apresentado ao operador antes de executar.

        Em LINGUAGEM DE RESTAURANTE: nada de operationId, metodo/path HTTP
        ou nome de campo JSON — o operador leigo nao entende isso. A traducao mora
        em `agent/phrasing.py` (mapa das 8 operacoes confirmaveis). Cita SO dados ja
        conhecidos (os args, vindos do que a API ja retornou) — nao inventa nada.
        """
        return humanize_plan(operation_id, args, confirmation_reason(operation_id))

    @staticmethod
    def _unknown_tool_hint(fn_name: str, fn_map: dict) -> str:
        """Observacao de recuperacao quando o LLM erra o NOME da ferramenta.

        Sugere os nomes do mesmo dominio (prefixo antes do '_') disponiveis neste
        turno, para o LLM corrigir sem re-retrieval. Mensagem destinada ao LLM
        (observacao), nao ao operador.
        """
        prefix = fn_name.split("_", 1)[0]
        same_domain = sorted(
            name for name, e in fn_map.items()
            if not e.get("local") and name.split("_", 1)[0] == prefix and name != fn_name
        )
        if same_domain:
            return (
                f"A ferramenta '{fn_name}' nao existe. Disponiveis neste dominio: "
                f"{', '.join(same_domain)}. Use um destes nomes exatos — a capacidade "
                f"provavelmente existe, voce so errou o nome."
            )
        disponiveis = sorted(n for n, e in fn_map.items() if not e.get("local"))
        return (
            f"A ferramenta '{fn_name}' nao existe. Ferramentas deste turno: "
            f"{', '.join(disponiveis)}. Use um destes nomes exatos."
        )

    @staticmethod
    def _truncate(text: str) -> str:
        if len(text) <= _MAX_OBSERVATION_CHARS:
            return text
        return text[:_MAX_OBSERVATION_CHARS] + f"\n... (truncado, {len(text)} chars no total)"

    @staticmethod
    def _error_text(error_body) -> str:
        if isinstance(error_body, dict):
            return str(error_body.get("message") or error_body.get("error") or error_body)
        return str(error_body)

    @staticmethod
    def _summarize_result(result) -> str:
        """Resumo curto do retorno (para a auditoria em actions_taken)."""
        if isinstance(result, dict):
            for key in ("reservations", "clients", "orders", "coupons", "items", "slots", "data"):
                if isinstance(result.get(key), list):
                    return f"200 — {len(result[key])} itens em '{key}'"
            return f"200 — {len(result)} campos"
        if isinstance(result, list):
            return f"200 — {len(result)} itens"
        return "200"

    @staticmethod
    def _promote_entities(result, state: ConversationState) -> None:
        """Promove IDs do retorno para discovered_entities (anti-alucinacao)."""
        def scan(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (str, int)) and (k == "id" or k.endswith("Id")):
                        state.discovered_entities.setdefault(k, str(v))
                    elif isinstance(v, (dict, list)):
                        scan(v)
            elif isinstance(obj, list):
                for item in obj[:5]:  # so os primeiros, evita poluir
                    scan(item)

        scan(result)
