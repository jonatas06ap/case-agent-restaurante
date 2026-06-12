# Dionísio Agent

Assistente interno do **Dionísio** (CRM de restaurantes). Um operador humano faz um pedido em
linguagem natural ("quantas reservas temos pra hoje?", "remarca a reserva do João pra sábado")
e o agente **opera a API REST do Dionísio** para resolvê-lo: descobre os dados que faltam,
encadeia as chamadas necessárias, confirma antes de qualquer ação destrutiva, e responde
citando o dado real. A arquitetura é um **loop ReAct single-agent** (sem LangChain/CrewAI/
LlamaIndex) com **RAG** sobre o OpenAPI spec para escolher quais das 61 operações ficam
disponíveis em cada turno.

## Setup (4 comandos)

```bash
uv sync                                   # 1. dependências (usa uv — https://docs.astral.sh/uv)
cp .env.example .env                      # 2. preencha DIONISIO_API_KEY e OPENROUTER_API_KEY
uv run python scripts/build_index.py      # 3. constrói o índice RAG (ChromaDB em ./rag/index)
uv run python scripts/agent_cli.py        # 4. abre o CLI interativo do agente
```

> **1º build:** os pesos do embedder local (`paraphrase-multilingual-MiniLM-L12-v2`, ~470 MB)
> são baixados e cacheados. Requer rede uma vez; depois roda offline. Para validar a fundação
> antes do CLI: `uv run python scripts/smoke_test.py` (alvo: **7/7 checks** contra a API real).

## Variáveis de ambiente (`.env`)

| Variável | Obrigatória | Descrição |
|---|---|---|
| `DIONISIO_API_KEY` | sim | Bearer token da Case Mock API (`key-jonatas-augusto`). |
| `OPENROUTER_API_KEY` | sim | Chave do OpenRouter — o LLM do agente. |
| `DIONISIO_BASE_URL` | sim | `https://dionisio-crm.web.app/api/case-mock`. |
| `OPENROUTER_MODEL` | não | Slug do modelo (default `anthropic/claude-sonnet-4`). |
| `EMBEDDING_PROVIDER` | não | `local` (padrão) ou `openai`. |
| `OPENAI_API_KEY` | não | Só se `EMBEDDING_PROVIDER=openai`. |
| `CHROMA_PATH` | não | Onde o ChromaDB persiste (default `./rag/index`). |

O `.env.example` já vem com `DIONISIO_API_KEY`, a base URL e o modelo preenchidos — basta
colar sua `OPENROUTER_API_KEY`.

## Como usar — as 6 tarefas do case

Rode `uv run python scripts/agent_cli.py` e digite o pedido. O CLI mostra, em cinza, o
retrieval e cada tool call; em negrito, a resposta ao operador. A sessão mantém contexto
multi-turno (dá pra dizer "cancela a reserva **dele**" depois de falar do João).

| # | Pedido (digite no `>`) | O que esperar |
|---|---|---|
| **1** | `quantas reservas temos pra hoje?` | Conta as reservas do dia e cita o número real ("Temos 1 reserva para hoje…"). |
| **2** | `remarca a reserva do João de quinta pra sábado no mesmo horário e avisa ela` | Multi-step (acha o cliente → a reserva → confere mesa no sábado) → **pede confirmação** antes de remarcar; **recusa** "avisar" (a API não tem canal de notificação). |
| **3** | `lista os clientes que gastaram mais de R$500 no último mês e nunca usaram cupom` | Filtro composto: cruza gasto × uso de cupom e devolve a lista real (nome, telefone, gasto). |
| **4** | `cria uma campanha de reativação pra inativos há 60 dias com cupom de 15%` | Descobre os inativos → cria o cupom → **na hora de atribuir ao grupo, apresenta o plano e exige "confirmar"**. Um "ok"/"não" aborta sem chamar a API. |
| **5** | `o prato 'Risoto de Funghi' saiu do cardápio — remove ele e avisa quem pediu ele nos últimos 7 dias` | Separa o possível do impossível: **recusa** remover (sem domínio de cardápio na API) e **recusa** avisar, mas **entrega a lista** de quem pediu o prato no período (busca o histórico de pedidos e filtra pelo item). |
| **6** | `cancela o pedido do João` (com 2+ pedidos) | **Ambíguo** → faz **uma** pergunta de desambiguação e **não** toca a API antes de saber qual pedido. Variante impossível: `manda um SMS pro João` → recusa explicada (sem canal de comunicação). |

### Os dois comportamentos que o avaliador procura

**Confirmação de dois estágios** (Tarefas 2 e 4) — antes de uma ação com efeito real, o agente
imprime o plano e bloqueia até o operador digitar `confirmar`:

```
> cria uma campanha de reativação pra inativos há 60 dias com cupom de 15%
  [tool]     GET /clients/inactive -> 200, 13 clientes
  [tool]     POST /coupons -> 201, cupom VOLTA15 criado
  ⚠️  Confirmacao necessaria
  Vou executar: coupons.assignGroup (POST /coupons/cpn_.../assign-group).
  Parametros: groupId=grp_inativos, ...
  Motivo da confirmacao: atribui o cupom a um grupo inteiro de clientes.
  Digite 'confirmar' para prosseguir: confirmar
  Campanha disparada: cupom VOLTA15 (15%) atribuído a 13 clientes inativos.
```

Só `confirmar`/`confirmo`/`sim, confirmo` prosseguem — "ok"/"sim"/"pode ser" **abortam**.

**Recusa honesta** (Tarefas 5 e 6) — quando a API não cobre o pedido, o agente diz isso em vez
de fingir. Nunca afirma que enviou uma mensagem, removeu um prato ou executou algo que falhou.

## Testes

```bash
uv run pytest            # suíte offline: 9 testes, LLM + API mockados (determinístico)
uv run pytest -m live    # variantes ao vivo: LLM + API reais (lê o .env)
```

A suíte offline cobre as 6 tarefas sem rede (dublês `StubLLM`/`FakeClient`); as variantes
`live` exercitam o caminho real. Checagens ao vivo prontas para demo:
`scripts/safety_check.py` (confirmação/ambiguidade, Dia 3) e `scripts/tasks_check.py`
(multi-step das Tarefas 2/3/5, Dia 4).

## Arquitetura

```
client/
  dionisio.py    DionisioClient: httpx async, auth Bearer, retry (429/5xx), logging, DionisioAPIError
  schemas.py     Pydantic v2 dos retornos principais
rag/
  embeddings.py  embedding function COMPARTILHADA por indexer e retriever (local | openai)
  indexer.py     OpenAPI spec + docs GitBook -> ChromaDB (2 namespaces); _OPERATION_HINTS curados
  retriever.py   retrieval semântico async (operações + docs de negócio)
  openapi_spec.json / docs/ / index/   spec local · GitBook em markdown · Chroma persistido (gitignored)
agent/
  core.py        loop ReAct (reason → act → observe → repeat), máx. 8 iterações
  planner.py     system prompt + monta as tools (JSON Schema do spec) a partir do retrieval
  executor.py    despacha tool calls → DionisioClient; erro vira observação textual; promove IDs
  responder.py   sintetiza a resposta final (grounding) e a falha parcial honesta
  state.py       ConversationState (messages, discovered_entities, actions_taken)
  llm.py         wrapper OpenRouter (openai.AsyncOpenAI, formato function-calling, temperature=0)
safety/
  destructive.py confirmação determinística (x-destructive + allowlist coupons.assignGroup)
  ambiguity.py   detector de ambiguidade pré-loop (1 chamada LLM, resposta JSON)
scripts/         build_index · smoke_test · agent_cli · safety_check · tasks_check
tests/           test_tasks.py (6 tarefas) + conftest (dublês) + fixtures/
```

Um turno: **ambiguidade?** (pré-loop, 1 LLM) → **retrieval** (top-5 operações + top-3 docs,
inclui destrutivas) → **loop ReAct** (LLM escolhe tool tipada → executor chama a API →
observação volta → repete) → **confirmação** no boundary de toda op destrutiva/de massa →
**resposta** citando o dado real. `DionisioAPIError` nunca é silenciado: vira observação e o
loop replaneja.

## Decisões de design (uma linha cada)

- **Single-agent ReAct, sem framework** — menor latência e superfície de bug que orquestração multi-agente para 61 operações. (`Context/design-document-dionisio.md` §2.1)
- **RAG sobre o OpenAPI spec** — o LLM nunca vê as 61 (logo, nem as 600) operações, só o top-k recuperado; é a resposta de escalabilidade. (design doc §2.2, §6)
- **Embeddings locais multilíngues por padrão** — o OpenRouter não tem endpoint de embeddings e o corpus/queries são em PT; `openai` é opt-in. (`History/dia_1.md` §3)
- **Texto embedado = uma frase curta de intenção** ("Use when"); detalhes técnicos ficam no metadado `detail`. O embedder local dilui textos longos. (`History/dia_1.md` §3.5)
- **Destrutividade por metadado do spec** (`x-destructive`), nunca por LLM; a barreira é a confirmação no executor. (`History/dia_3.md`)
- **Multi-step é emergente** — reusa `discovered_entities` + histórico; sem planner-JSON nem sub-agentes. (`History/dia_4.md`)

Histórico dia a dia em `History/dia_N.md`; arquitetura e trade-offs completos em
`Context/design-document-dionisio.md`.

## Convenções (não violar)

- Gerência de pacotes por **uv** (não pip direto). Sem LangChain/LlamaIndex/CrewAI.
- Tudo **async**; LLM via OpenRouter (`temperature=0`). `build_index.py` é **idempotente**.
- Indexer e retriever **compartilham** a embedding function — vetores em espaços diferentes
  quebram o retrieval. Ao trocar `EMBEDDING_PROVIDER`, **reconstrua o índice**.
- **Nunca commitar `.env`** nem chaves. Score do retrieval = `1 - cosine_distance`.
```
