"""Embedding function compartilhada entre indexer e retriever.

CRITICO: indexer e retriever DEVEM usar exatamente a mesma embedding function,
senao os vetores ficam em espacos diferentes e o retrieval retorna lixo.

Default = embeddings locais (all-MiniLM via ChromaDB): offline, gratis, sem key.
Opt-in = OpenAI text-embedding-3-small (requer EMBEDDING_PROVIDER=openai + OPENAI_API_KEY).
OpenRouter NAO oferece endpoint de embeddings — serve apenas ao LLM (Dia 2+).
"""

from __future__ import annotations

import logging
import os

from chromadb.utils import embedding_functions

logger = logging.getLogger("dionisio.rag.embeddings")

# Identificadores das collections no Chroma (namespaces do RAG).
OPERATIONS_COLLECTION = "api_operations"
DOCS_COLLECTION = "business_docs"

DEFAULT_OPENAI_MODEL = "text-embedding-3-small"
# Modelo local multilingue — o corpus e as queries sao em portugues, entao o
# all-MiniLM (ingles) discrimina mal. Este modelo cobre PT muito melhor.
DEFAULT_LOCAL_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


def resolve_provider() -> str:
    """Retorna 'openai' ou 'local' com base no ambiente.

    So usa OpenAI se explicitamente pedido E houver key — caso contrario cai
    para local silenciosamente (com aviso), para o smoke test sempre rodar.
    """
    provider = os.getenv("EMBEDDING_PROVIDER", "local").strip().lower()
    if provider == "openai":
        if os.getenv("OPENAI_API_KEY"):
            return "openai"
        logger.warning(
            "EMBEDDING_PROVIDER=openai mas OPENAI_API_KEY ausente — usando embeddings locais."
        )
    return "local"


def get_embedding_function(model: str | None = None):
    """Constroi a embedding function de acordo com o provider resolvido."""
    provider = resolve_provider()
    if provider == "openai":
        model_name = model or os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_OPENAI_MODEL)
        logger.info("Embeddings: OpenAI (%s)", model_name)
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name=model_name,
        )

    model_name = model_local()
    logger.info("Embeddings: local multilingue (%s via SentenceTransformer)", model_name)
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)


def model_local() -> str:
    return os.getenv("LOCAL_EMBEDDING_MODEL", DEFAULT_LOCAL_MODEL)
