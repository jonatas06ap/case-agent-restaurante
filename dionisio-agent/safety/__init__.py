"""Camada de seguranca do agente.

Dois mecanismos, com responsabilidades separadas:

- `destructive.py`  decide DETERMINISTICAMENTE (sem LLM) quais operacoes exigem
  confirmacao explicita antes de ir para a API: Classe A (x-destructive, lido do
  spec) + Classe B (allowlist de alto impacto / efeito em massa).
- `ambiguity.py`    detecta ambiguidade no enunciado do operador (uma chamada LLM,
  resposta JSON) ANTES do loop ReAct — perguntar antes de agir.

Invariante: destrutividade/alto impacto NUNCA e decidida por LLM; o LLM so opina
sobre ambiguidade.
"""

from .destructive import (
    MASS_EFFECT_OPS,
    confirmation_reason,
    requires_confirmation,
)
from .ambiguity import detect_ambiguity

__all__ = [
    "requires_confirmation",
    "confirmation_reason",
    "MASS_EFFECT_OPS",
    "detect_ambiguity",
]
