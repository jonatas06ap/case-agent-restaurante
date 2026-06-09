"""DionisioClient — wrapper HTTP assincrono da API Case Mock do Dionisio.

Caracteristicas:
- httpx.AsyncClient (o agente roda em loop async).
- Auth Bearer em toda chamada.
- Retry com backoff exponencial (1s -> 2s -> 4s, 3 tentativas) apenas para 429 e 5xx.
- Erros HTTP levantam DionisioAPIError — nunca retorna None silenciosamente.
- Log estruturado por chamada: metodo, path, status, latencia (ms).
- Async context manager.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger("dionisio.client")

# Status que justificam retry: rate limit + erros transitorios de servidor.
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class DionisioAPIError(Exception):
    """Erro retornado pela API (4xx nao-retryable, ou falha apos os retries)."""

    def __init__(self, status_code: int, error_body: Any):
        self.status_code = status_code
        self.error_body = error_body
        super().__init__(f"Dionisio API error {status_code}: {error_body}")


class _RetryableStatus(Exception):
    """Sinal interno: status retryable recebido — dispara nova tentativa."""

    def __init__(self, status_code: int, error_body: Any):
        self.status_code = status_code
        self.error_body = error_body
        super().__init__(f"retryable status {status_code}")


class DionisioClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float = 15.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    # ----- ciclo de vida ----------------------------------------------------
    async def __aenter__(self) -> "DionisioClient":
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        return self

    async def __aexit__(self, *exc) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    # ----- nucleo -----------------------------------------------------------
    async def request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        body: dict | None = None,
    ) -> dict:
        """Executa uma chamada HTTP. Retorna o JSON parseado ou levanta DionisioAPIError."""
        if self._client is None:
            # Permite uso sem `async with` (cria client efemero por chamada).
            async with DionisioClient(self.api_key, self.base_url, self.timeout) as c:
                return await c.request(method, path, params=params, body=body)

        try:
            return await self._request_with_retry(method, path, params, body)
        except _RetryableStatus as exc:
            # Esgotou os retries num status retryable -> erro definitivo.
            raise DionisioAPIError(exc.status_code, exc.error_body) from exc

    @retry(
        retry=retry_if_exception_type(_RetryableStatus),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def _request_with_retry(
        self,
        method: str,
        path: str,
        params: dict | None,
        body: dict | None,
    ) -> dict:
        assert self._client is not None
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        started = time.perf_counter()
        response = await self._client.request(
            method.upper(),
            path,
            params=clean_params or None,
            json=body,
        )
        elapsed_ms = (time.perf_counter() - started) * 1000

        logger.info(
            "%s %s -> %s (%.0fms)",
            method.upper(),
            path,
            response.status_code,
            elapsed_ms,
        )

        error_body = self._safe_json(response)

        if response.status_code in _RETRYABLE_STATUS:
            logger.warning(
                "status retryable %s em %s %s — tentando novamente",
                response.status_code,
                method.upper(),
                path,
            )
            raise _RetryableStatus(response.status_code, error_body)

        if response.status_code >= 400:
            raise DionisioAPIError(response.status_code, error_body)

        return error_body if isinstance(error_body, dict) else {"data": error_body}

    @staticmethod
    def _safe_json(response: httpx.Response) -> Any:
        try:
            return response.json()
        except Exception:
            return {"raw": response.text}

    # ----- conveniencia: Clientes ------------------------------------------
    async def list_clients(self, q=None, group_id=None, limit=50, offset=0) -> dict:
        return await self.request(
            "GET", "/clients",
            params={"q": q, "groupId": group_id, "limit": limit, "offset": offset},
        )

    async def get_client(self, client_id: str) -> dict:
        return await self.request("GET", f"/clients/{client_id}")

    async def search_clients(self, phone=None, name=None) -> dict:
        return await self.request("GET", "/clients/search", params={"phone": phone, "name": name})

    async def get_inactive_clients(self, days=60) -> dict:
        return await self.request("GET", "/clients/inactive", params={"days": days})

    async def get_top_spenders(self, period="month", min_spent=None, limit=20) -> dict:
        return await self.request(
            "GET", "/clients/top-spenders",
            params={"period": period, "minSpent": min_spent, "limit": limit},
        )

    async def get_client_insights(self, client_id: str) -> dict:
        return await self.request("GET", f"/clients/{client_id}/insights")

    # ----- conveniencia: Reservas ------------------------------------------
    async def list_reservations(self, date=None, status=None, client_id=None) -> dict:
        return await self.request(
            "GET", "/reservations",
            params={"date": date, "status": status, "clientId": client_id},
        )

    async def get_availability(self, date=None) -> dict:
        return await self.request("GET", "/reservations/availability", params={"date": date})

    async def create_reservation(self, client_id, start_ms, adults, **kwargs) -> dict:
        body = {"clientId": client_id, "start": start_ms, "adults": adults}
        body.update({k: v for k, v in kwargs.items() if v is not None})
        return await self.request("POST", "/reservations", body=body)

    async def reschedule_reservation(self, reservation_id, new_start_ms) -> dict:
        # DESTRUTIVO: o horario original e perdido.
        return await self.request(
            "POST", f"/reservations/{reservation_id}/reschedule",
            body={"start": new_start_ms},
        )

    async def cancel_reservation(self, reservation_id, reason_code=None, reason_text=None) -> dict:
        # DESTRUTIVO.
        return await self.request(
            "POST", f"/reservations/{reservation_id}/cancel",
            body={"reasonCode": reason_code, "reasonText": reason_text},
        )

    async def confirm_reservation(self, reservation_id) -> dict:
        return await self.request("POST", f"/reservations/{reservation_id}/confirm")

    # ----- conveniencia: Pedidos -------------------------------------------
    async def list_orders(self, date=None, status=None, client_id=None, limit=50) -> dict:
        return await self.request(
            "GET", "/orders",
            params={"date": date, "status": status, "clientId": client_id, "limit": limit},
        )

    async def cancel_order(self, order_id) -> dict:
        # DESTRUTIVO.
        return await self.request("POST", f"/orders/{order_id}/cancel")

    # ----- conveniencia: Cupons --------------------------------------------
    async def list_coupons(self, status=None) -> dict:
        return await self.request("GET", "/coupons", params={"status": status})

    async def create_coupon(self, name, type_, benefit_text) -> dict:
        return await self.request(
            "POST", "/coupons",
            body={"name": name, "type": type_, "benefitText": benefit_text},
        )

    async def assign_coupon_to_group(self, coupon_id, group_id) -> dict:
        return await self.request(
            "POST", f"/coupons/{coupon_id}/assign-group",
            body={"groupId": group_id},
        )

    async def deactivate_coupon(self, coupon_id) -> dict:
        # DESTRUTIVO.
        return await self.request("POST", f"/coupons/{coupon_id}/deactivate")

    # ----- conveniencia: Loja / Analytics ----------------------------------
    async def get_store(self) -> dict:
        return await self.request("GET", "/store")

    async def get_analytics_revenue(self, period_start_ms, period_end_ms) -> dict:
        return await self.request(
            "GET", "/analytics/revenue",
            params={"periodStart": period_start_ms, "periodEnd": period_end_ms},
        )

    async def get_top_items(self, limit=10) -> dict:
        return await self.request("GET", "/analytics/top-items", params={"limit": limit})
