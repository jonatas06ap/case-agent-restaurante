# Dionisio Agent — Dia 1 (Fundação, Client e RAG)

Agente assistente interno do **Dionísio** (CRM de restaurantes). Recebe pedidos em
linguagem natural e executa operações na API REST do Dionísio, usando um loop ReAct
single-agent com **RAG** sobre o OpenAPI spec para seleção de ferramentas.

Este repositório cobre o **Dia 1**: estrutura do projeto, o client HTTP (`DionisioClient`)
e o pipeline de RAG (indexação + retrieval). Critério de conclusão: `scripts/smoke_test.py`
passa **7/7 checks** contra a API real.

## Setup (poucos comandos)

```bash
# 1. Dependências (usa uv — https://docs.astral.sh/uv/)
uv sync

# 2. Variáveis de ambiente
cp .env.example .env        # preencha DIONISIO_API_KEY e (opcional) OPENAI_API_KEY

# 3. Construir o índice RAG (ChromaDB persistido em ./rag/index)
uv run python scripts/build_index.py

# 4. Validar tudo contra a API real
uv run python scripts/smoke_test.py     # objetivo: RESULTADO: 7/7 checks passaram
```

> No 1º build, os pesos do modelo de embeddings local (~470 MB) são baixados e cacheados.
> Requer rede uma única vez; depois roda offline.

## Variáveis de ambiente (`.env`)

| Variável | Descrição |
|---|---|
| `DIONISIO_API_KEY` | Bearer token da Case Mock API (`key-jonatas-augusto`). |
| `DIONISIO_BASE_URL` | `https://dionisio-crm.web.app/api/case-mock`. |
| `EMBEDDING_PROVIDER` | `local` (padrão) ou `openai`. |
| `OPENAI_API_KEY` | Só necessário se `EMBEDDING_PROVIDER=openai`. |
| `OPENROUTER_API_KEY` | LLM (usado a partir do Dia 2). |
| `CHROMA_PATH` | Onde o ChromaDB persiste (`./rag/index`). |

## Embeddings: local por padrão, OpenAI opt-in

O OpenRouter **não** oferece endpoint de embeddings (só chat/completions). Como o RAG
precisa de embeddings, o default é **local**:

- **`local`** (padrão): `paraphrase-multilingual-MiniLM-L12-v2` via `sentence-transformers`.
  Offline, grátis, sem key. Escolhido por ser **multilíngue** — o corpus e as queries são
  em português, e o `all-MiniLM` (inglês) do ChromaDB discrimina mal em PT.
- **`openai`**: `text-embedding-3-small` (como no design doc). Defina `EMBEDDING_PROVIDER=openai`
  e `OPENAI_API_KEY`. Após trocar o provider, **reconstrua o índice** (`build_index.py`).

O indexer e o retriever compartilham a mesma embedding function (`rag/embeddings.py`) —
isso é obrigatório: vetores em espaços diferentes quebram o retrieval.

## Estrutura

```
client/
  dionisio.py   # DionisioClient: httpx async, auth Bearer, retry (tenacity), logging
  schemas.py    # Pydantic models dos retornos principais
rag/
  embeddings.py # embedding function compartilhada (local | openai)
  indexer.py    # OpenAPI spec + docs GitBook -> ChromaDB (2 namespaces)
  retriever.py  # retrieval semântico async (operações + docs de negócio)
  openapi_spec.json   # spec local (fonte primária do indexer)
  docs/               # GitBook exportado em markdown (fonte dos business_docs)
  index/              # ChromaDB persistido (gitignored)
scripts/
  build_index.py # (re)constrói o índice — idempotente
  smoke_test.py  # 7 checks: client + retriever contra a API real
```

## Notas de design (RAG)

- **Dois namespaces** no Chroma: `api_operations` (1 doc por operação) e `business_docs`
  (chunks do GitBook por seção `##`).
- **`x-destructive`** do spec vira metadado booleano; o retriever filtra com
  `exclude_destructive=True` (`where={"destructive": False}`).
- **Documento de operação curto e liderado pela intenção** ("Use when"). Decisão empírica:
  o embedder local faz mean-pooling, então textos longos diluem o sinal e empatam o ranking
  entre operações do mesmo domínio. Frases curtas e distintas (vocabulário de negócio em PT)
  discriminam muito melhor. Detalhes técnicos (parâmetros, body, response) ficam no metadado
  `detail`, fora do texto embedado. Com `text-embedding-3-small` essa sensibilidade some.
- **Score = `1 - cosine_distance`**; collections criadas com `hnsw:space=cosine`.

## DionisioClient

- `httpx.AsyncClient` + context manager assíncrono.
- Header `Authorization: Bearer <key>` em todas as chamadas.
- Retry com backoff exponencial (1s → 2s → 4s, 3 tentativas) **só** para 429 e 5xx.
- Erros HTTP levantam `DionisioAPIError(status_code, error_body)` — nunca retorna `None`.
- Log estruturado por chamada: método, path, status, latência (ms).
- Métodos de conveniência para os endpoints principais (clients, reservations, orders,
  coupons, analytics).
