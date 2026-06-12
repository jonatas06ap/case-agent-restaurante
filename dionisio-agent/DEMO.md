# Demonstração — Dionísio Agent

Roteiro **reproduzível** de 4 tarefas + 1 recusa, com os comandos exatos e a saída esperada.
Pré-requisitos: setup do `README.md` feito (`uv sync`, `.env` preenchido,
`scripts/build_index.py` rodado). Tudo abaixo usa **API + LLM reais**.

> As saídas são do modelo `anthropic/claude-sonnet-4` (temperature=0) contra a Case Mock API
> em 2026-06-12. O fraseado da resposta pode variar levemente entre execuções; os **dados**
> (números, nomes, comportamento de confirmação/recusa) são estáveis.

---

## Opção A — sessão interativa (mostra retrieval + tool calls)

```bash
uv run python scripts/agent_cli.py
```

### 1. Tarefa 1 — leitura simples (grounding)

```
> quantas reservas temos pra hoje?
  [retrieve] reservations.list (0.65), reservations.reschedule (0.65), ...
  [tool]     GET /reservations -> 200 — 1 itens em 'items'
  Temos 1 reserva para hoje (12/06/2026). Está confirmada, é para 6 adultos e
  3 crianças (9 pessoas), na área da varanda, mesa 28.
```

### 2. Tarefa 3 — filtro composto

```
> lista os clientes que gastaram mais de R$500 no último mês e nunca usaram cupom
  [tool]     GET /clients/top-spenders -> 200 — 14 itens
  11 clientes gastaram mais de R$500 no último mês e nunca usaram cupom:
  1. Gabriela Gomes — (55) 81 92212-4384 — R$ 1.200
  2. Henrique Pereira — (55) 31 93166-1941 — R$ 1.000
  ... (mais 9) ...
  Total: 11 clientes, R$ 9.800 em gasto somado.
```

Cruzamento real (gasto > 500 ∩ cupons usados = 0); ninguém fora do critério entra na lista.

### 3. Tarefa 5 — possível vs. impossível (o caso completo)

```
> o prato 'Risoto de Funghi' saiu do cardápio — remove ele e avisa quem pediu ele nos últimos 7 dias
  [tool]     GET /orders -> 200 — itens do histórico
  Procurei nos pedidos dos últimos 7 dias: ninguém pediu "Risoto de Funghi"
  nesse período. Sobre o resto: não consigo remover o prato do cardápio nem
  avisar clientes por aqui — isso você faz direto no painel do Dionísio.
```

Três coisas de uma vez: **entrega** o resultado da busca (lista vazia — ninguém pediu o prato
no período, dado real do histórico) e **recusa** as duas partes que a API não cobre (remover do
cardápio, notificar) — sem nunca fingir. *(O agente faz a busca em **uma** passada do histórico
e filtra localmente; não varre dia a dia.)*

### 4. Tarefa 6 — ambíguo (uma pergunta, zero chamadas)

```
> cancela o pedido do João
  [ambiguidade] pedido ambiguo -> pedindo esclarecimento
  O João tem mais de um pedido ativo. Qual deles você quer cancelar — me passa
  o número do pedido ou mais um detalhe?
```

Nenhuma chamada destrutiva antes de saber qual pedido. Variante impossível:

```
> manda um SMS pro João avisando que a reserva foi confirmada
  Não consigo enviar SMS/WhatsApp por aqui — o Dionísio não tem canal de
  comunicação na minha caixa de ferramentas. Posso confirmar a reserva no
  sistema, mas o aviso ao cliente você faz por fora.
```

### 5. Confirmação de dois estágios — Tarefa 4

```
> cria uma campanha de reativação pra inativos há 60 dias com cupom de 15%
  [tool]     GET /clients/inactive -> 200, 13 clientes
  [tool]     POST /coupons -> 201, cupom VOLTA15 criado
  ⚠️  Confirmacao necessaria
  Vou executar: coupons.assignGroup (POST /coupons/cpn_.../assign-group).
  Motivo da confirmacao: atribui o cupom a um grupo inteiro de clientes.
  Digite 'confirmar' para prosseguir: nao
  Cancelado. Não atribuí o cupom a ninguém — a campanha não foi disparada.
```

Digite `confirmar` em vez de `nao` para ver o disparo real. Só `confirmar`/`confirmo`/
`sim, confirmo` prosseguem.

Para sair: `sair`.

---

## Opção B — scripts não interativos (1 comando cada)

```bash
uv run python scripts/safety_check.py    # Tarefa 4 (confirmação) + Tarefa 6 (ambíguo/impossível)
uv run python scripts/tasks_check.py     # Tarefas 2, 3 e 5 ponta a ponta (multi-step)
```

`tasks_check.py` roda a Tarefa 2 com a confirmação **negada** (prova que o `reschedule` não é
chamado), a Tarefa 3 (lista real) e a Tarefa 5 (duas recusas honestas + lista entregue).

## Opção C — suíte de testes (offline, determinística)

```bash
uv run pytest            # 9/9, mocks — prova o comportamento das 6 tarefas sem rede
uv run pytest -m live    # variantes com LLM + API reais
```
