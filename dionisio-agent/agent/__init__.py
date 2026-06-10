"""Agente assistente do Dionisio — loop ReAct single-agent (Dia 2).

Componentes:
- state.py     ConversationState (historico, entidades, acoes)
- llm.py       wrapper OpenRouter via openai.AsyncOpenAI
- planner.py   system prompt + montagem de tools a partir do retrieval
- executor.py  despacha tool_calls -> DionisioClient
- core.py      o loop ReAct (reason -> act -> observe -> repeat)
- responder.py sintese da resposta final em PT
"""

from .state import ConversationState, ToolCallRecord
from .core import Agent

__all__ = ["ConversationState", "ToolCallRecord", "Agent"]
