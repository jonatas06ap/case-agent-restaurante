"""Estado da conversa — Pydantic v2.

O estado vive em memoria durante a sessao do CLI (persistencia entre sessoes e
melhoria futura). Tres papeis:

- `messages`: historico no formato do chat (system/user/assistant/tool). Carrega o
  contexto multi-turno — permite resolver "cancela a reserva dele" por referencia.
- `discovered_entities`: mecanismo anti-alucinacao. IDs achados num passo (ex:
  reservationId) ficam disponiveis nos passos seguintes, em vez de o LLM reinventa-los.
- `actions_taken`: trilha de auditoria das operacoes executadas no turno.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ToolCallRecord(BaseModel):
    """Registro de uma operacao despachada para a API (auditoria)."""

    operation_id: str           # ex: "reservations.list"
    method: str                 # "GET"
    path: str                   # "/reservations" (path params ja resolvidos)
    arguments: dict             # args enviados pelo LLM
    ok: bool                    # True em 2xx; False em erro de API
    summary: str                # resumo curto do retorno ou do erro
    confirmed: bool | None = None  # None=nao exigia confirmacao; True/False=exigia e foi/nao foi confirmada


class ConversationState(BaseModel):
    """Estado acumulado da conversa (multi-turno)."""

    messages: list[dict] = Field(default_factory=list)
    discovered_entities: dict[str, str] = Field(default_factory=dict)
    actions_taken: list[ToolCallRecord] = Field(default_factory=list)
    iterations: int = 0         # contador do loop ReAct no turno atual

    def last_assistant_text(self) -> str | None:
        """Ultimo texto produzido pelo assistant (resposta final do loop)."""
        for msg in reversed(self.messages):
            if msg.get("role") == "assistant" and msg.get("content"):
                return msg["content"]
        return None
