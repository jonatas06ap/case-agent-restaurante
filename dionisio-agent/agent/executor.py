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
from urllib.parse import urlparse

from client import DionisioAPIError, DionisioClient

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

    async def run(self, tool_call, fn_map: dict, state: ConversationState) -> str:
        """Executa um tool_call e devolve a observacao textual (mensagem role:tool)."""
        fn_name = tool_call.function.name
        entry = fn_map.get(fn_name)
        if entry is None:
            return f"Erro: ferramenta desconhecida '{fn_name}'. Use apenas as ferramentas fornecidas."

        # --- parse dos argumentos ---
        raw_args = tool_call.function.arguments or "{}"
        try:
            args = json.loads(raw_args) if isinstance(raw_args, str) else dict(raw_args)
        except json.JSONDecodeError as e:
            return f"Erro: argumentos invalidos para {fn_name} (JSON malformado: {e})."

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
                operation_id=entry["operation_id"],
                method=method,
                path=rel_path,
                arguments=args,
                ok=ok,
                summary=summary,
            )
        )
        return observation

    # ----- helpers ----------------------------------------------------------
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
