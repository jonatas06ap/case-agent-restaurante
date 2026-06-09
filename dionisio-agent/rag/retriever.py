"""Retriever — retrieval semantico sobre os namespaces do ChromaDB.

Usa a MESMA embedding function do indexer (via rag/embeddings.py). Interface
async como exige o agente; o Chroma e sincrono, entao as queries rodam em
thread separada (asyncio.to_thread) para nao bloquear o loop.

Score = 1 - cosine_distance (collections criadas com hnsw:space=cosine).
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import chromadb

from .embeddings import (
    DOCS_COLLECTION,
    OPERATIONS_COLLECTION,
    get_embedding_function,
)


@dataclass
class OperationDoc:
    operation_id: str
    method: str
    path: str
    domain: str
    destructive: bool
    summary: str
    full_text: str
    score: float


@dataclass
class BusinessDoc:
    section: str
    text: str
    score: float


@dataclass
class RetrievalResult:
    operations: list[OperationDoc]
    docs: list[BusinessDoc]
    query: str


class Retriever:
    def __init__(self, chroma_path: str, embedding_model: str = "text-embedding-3-small"):
        self._embedding_fn = get_embedding_function(embedding_model)
        self._client = chromadb.PersistentClient(path=chroma_path)
        self._operations = self._client.get_collection(
            OPERATIONS_COLLECTION, embedding_function=self._embedding_fn
        )
        self._docs = self._client.get_collection(
            DOCS_COLLECTION, embedding_function=self._embedding_fn
        )

    # ----- helpers ----------------------------------------------------------
    @staticmethod
    def _score(distance: float) -> float:
        return round(1.0 - distance, 4)

    def _query_operations(self, query: str, k: int, exclude_destructive: bool) -> list[OperationDoc]:
        where = {"destructive": False} if exclude_destructive else None
        res = self._operations.query(
            query_texts=[query],
            n_results=k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        out: list[OperationDoc] = []
        metas = res["metadatas"][0]
        docs = res["documents"][0]
        dists = res["distances"][0]
        for meta, doc, dist in zip(metas, docs, dists):
            out.append(
                OperationDoc(
                    operation_id=meta.get("operation_id", ""),
                    method=meta.get("method", ""),
                    path=meta.get("path", ""),
                    domain=meta.get("domain", ""),
                    destructive=bool(meta.get("destructive", False)),
                    summary=meta.get("summary", ""),
                    full_text=doc,
                    score=self._score(dist),
                )
            )
        return out

    def _query_docs(self, query: str, k: int) -> list[BusinessDoc]:
        res = self._docs.query(
            query_texts=[query],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )
        out: list[BusinessDoc] = []
        for meta, doc, dist in zip(res["metadatas"][0], res["documents"][0], res["distances"][0]):
            out.append(
                BusinessDoc(
                    section=meta.get("section", ""),
                    text=doc,
                    score=self._score(dist),
                )
            )
        return out

    # ----- API publica ------------------------------------------------------
    async def retrieve(
        self,
        query: str,
        k_operations: int = 5,
        k_docs: int = 3,
        exclude_destructive: bool = False,
    ) -> RetrievalResult:
        """Retorna as k operacoes e k chunks de docs mais relevantes.

        Com exclude_destructive=True, filtra operacoes destructive=True.
        """
        operations, docs = await asyncio.gather(
            asyncio.to_thread(self._query_operations, query, k_operations, exclude_destructive),
            asyncio.to_thread(self._query_docs, query, k_docs),
        )
        return RetrievalResult(operations=operations, docs=docs, query=query)

    async def retrieve_operations_only(self, query: str, k: int = 8) -> list[OperationDoc]:
        """Para quando so precisamos de endpoints, sem docs de negocio."""
        return await asyncio.to_thread(self._query_operations, query, k, False)
