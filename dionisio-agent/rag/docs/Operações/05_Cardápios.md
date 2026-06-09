# Cardápios

O módulo **Cardápios** é onde você monta o cardápio digital do restaurante: cria as categorias, cadastra os itens com preço e foto, configura pizzas e monta os complementos. É esse cardápio que aparece no link público de pedidos, no QR Code e que a Assistente IA consulta para responder os clientes.

Você pode ter **mais de um cardápio** na mesma loja. O uso mais comum é separar **salão** e **delivery**, ou manter uma **carta de vinhos** ou de drinks à parte — embora também dê para atender salão e delivery com um cardápio só, definindo preços diferentes por canal.

> ℹ️ **Observação:** no menu o módulo se chama **Cardápios**, mas a tela ainda aparece com o título **Gerenciamento de Catálogos** e usa "catálogo" em alguns botões. É o mesmo lugar.

## Para quem é

* **Dono** e **Administrador** — montam e mantêm o cardápio: categorias, itens, preços, fotos e complementos.
* **Membro** — acessa o módulo apenas com a permissão de cardápio habilitada.

## O que você pode fazer

* Criar um cardápio
* Criar e organizar categorias
* Cadastrar itens
* Configurar pizzas
* Montar complementos

## Principais conceitos

* **Cardápio** — conjunto de categorias e itens publicado para o cliente. Tem link público, QR Code e canais próprios (salão e delivery).
* **Categoria** — agrupa os itens dentro do cardápio (Entradas, Pizzas, Vinhos). Cada categoria tem um **Tipo de Item** que define como os itens dela funcionam.
* **Item** — produto individual de uma categoria, com preço para salão e para delivery.
* **Complemento** — grupo de opções extras que você vincula a um ou mais itens (ponto da carne, adicionais, bordas).

## Como acessar

No menu lateral, clique em **Cardápios**. A tela lista todos os cardápios da loja. Clique em um cardápio para abrir o detalhe, dividido em quatro abas:

| Aba                    | O que faz                                      |
| ---------------------- | ---------------------------------------------- |
| **Visualização geral** | Mostra o cardápio como o cliente o vê.         |
| **Categorias**         | Cria e organiza as seções, e configura pizzas. |
| **Itens**              | Cadastra os produtos de cada categoria.        |
| **Complementos**       | Cria os grupos de opções extras.               |

## Onde o cardápio aparece

* **Link público de pedidos e QR Code** — o cardápio ativo é o que o cliente vê e usa para pedir.
* **Pedidos manuais** — ao criar um pedido pela equipe, os itens vêm dos cardápios ativos.
* **Assistente IA** — lê nome, descrição e preço dos itens para responder sobre o cardápio.
* **Cupons** — os cupons de delivery podem ser aplicados aos itens do cardápio.
* **Integrações** — a sincronização com iFood, Saipos e outros sistemas é configurada em Integrações, não aqui.

## Problemas comuns

* Um item não aparece no link do cardápio

## Começando

Se você está montando o cardápio do zero, siga nesta ordem:

1. Crie um cardápio
2. Crie as categorias
3. Cadastre os itens
4. Monte os complementos

# Criar um cardápio

Um cardápio reúne as categorias e os itens que o cliente vê no link público de pedidos. Crie um cardápio quando for montar o menu do zero ou quando quiser um menu separado — por exemplo, um para o **salão** e outro para o **delivery**, ou uma **carta de vinhos** à parte.

> ℹ️ **Observação:** no menu o módulo se chama **Cardápios**, mas a tela usa **catálogo** nos botões e campos (**Criar Catálogo**, **Nome do Catálogo**). É o mesmo lugar.

## Antes de começar

Você precisa da **permissão de cardápio** (Dono e Administrador têm por padrão). Sem a permissão de **pedidos**, os toggles de canal (**Aceitar Pedidos de Delivery** e **Aceitar Pedidos de Salão**) ficam desligados.

## Como acessar

No menu lateral, clique em **Cardápios**. A tela lista os cardápios já criados.

## Passos

1. Clique em **Criar Catálogo**.
2. Preencha o **Nome do Catálogo**.
3. Confira o **Slug** — ele é gerado a partir do nome, mas você pode editar.
4. Ajuste os toggles de status e de canais.
5. Clique em **Criar Catálogo**.

## Configurações

| Campo                               | Obrigatório | Descrição                                                                                                                                                   |
| ----------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nome do Catálogo**                | Sim         | Nome do cardápio. Aparece para você e na navegação.                                                                                                         |
| **Slug**                            | Sim         | Identificador na URL pública (ex: `m.odionisio.com/sua-loja/cardapio-principal`). Só aceita **letras minúsculas, números e hífens**.                        |
| **Descrição**                       | Não         | Texto interno para você diferenciar os cardápios.                                                                                                           |
| **Catálogo Ativo**                  | Não         | Liga ou desliga o cardápio. Vem **ligado**. Desligado, ele some do link público sem ser excluído.                                                           |
| **Aceitar Pedidos de Delivery**     | Não         | Define se o cardápio vende por delivery. Vem ligado se você tem permissão de pedidos.                                                                       |
| **Aceitar Pedidos de Salão**        | Não         | Define se o cardápio vende no salão. Vem ligado se você tem permissão de pedidos.                                                                           |
| **Banners e Promoções do Catálogo** | Não         | Imagens no topo do cardápio, proporção **16:6** (JPG ou PNG, até 5 MB). Cada banner pode ter **Turnos de exibição** para aparecer só em horários definidos. |

## Dicas e observações

> ⚠️ **Atenção:** o slug **`delivery` é reservado** e não pode ser usado — o sistema troca por **`delivery-menu`**. Depois de compartilhar o link, evite mudar o slug: links e QR Codes antigos deixam de funcionar.

> 💡 **Dica:** dá para atender salão e delivery com **um cardápio só**, definindo preços diferentes por canal em cada item. Use vários cardápios quando os menus forem realmente distintos.

## Próximos passos

* Criar e organizar categorias
* Cadastrar itens

# Categorias

As **categorias** agrupam os itens do cardápio em seções — Entradas, Pizzas, Vinhos, Bebidas. Cada item pertence a uma categoria, e é a categoria que define o **Tipo de Item**: se ali entram produtos de preço fixo, pizzas, vinhos ou combos.

## Antes de começar

Você precisa de um cardápio já criado.

## Como acessar

No menu lateral, clique em **Cardápios**, abra o cardápio e vá na aba **Categorias**.

## Criar uma categoria

1. Clique em **Adicionar categoria**.
2. Em **Tipo**, escolha **Categoria** (seção principal) ou **Subcategoria** (divisão dentro de outra).
3. Preencha o **Nome da categoria** e, se quiser, a **Descrição**.
4. Escolha o **Tipo de Item**.
5. Clique em **Criar**.

## Configurações

| Campo                      | Obrigatório | Descrição                                                                              |
| -------------------------- | ----------- | -------------------------------------------------------------------------------------- |
| **Tipo**                   | Sim         | **Categoria** (seção principal) ou **Subcategoria** (divisão dentro de uma categoria). |
| **Nome da categoria**      | Sim         | Nome exibido como seção no cardápio.                                                   |
| **Descrição da categoria** | Não         | Texto explicativo da seção.                                                            |
| **Tipo de Item**           | Sim         | Define o tipo de produto da categoria (veja abaixo). **Não pode ser alterado depois.** |

### Tipos de Item

| Tipo de Item     | Quando usar                                                                                                                   |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Item Simples** | Produtos de preço fixo: pratos, hambúrgueres, bebidas, sobremesas.                                                            |
| **Pizza**        | Pizzas com tamanhos, massas, bordas e sabores. Veja Configurar pizzas. |
| **Vinho**        | Vinhos com preço por volume (ex: taça, garrafa).                                                                              |
| **Combo**        | Combos formados por vários itens, com preço configurável.                                                                     |

> ⚠️ **Atenção:** o **Tipo de Item não pode ser alterado** depois que a categoria é criada. Se errar o tipo, será preciso **criar uma nova categoria** e recadastrar os itens. Escolha com cuidado.

## Subcategorias

Subcategorias criam divisões dentro de uma categoria — por exemplo, "Pizzas" com as subcategorias "Salgadas" e "Doces". A subcategoria **herda o Tipo de Item** da categoria pai.

> ℹ️ **Observação:** só categorias do tipo **Item Simples** e **Combo** aceitam subcategorias. **Pizza** e **Vinho** não têm subcategorias.

## Pausar, reordenar e excluir

* **Pausar** (ícone de pausar na categoria) tira a seção do ar sem apagá-la — os itens dela somem do cardápio até você reativar. É a forma recomendada de esconder uma seção temporariamente.
* **Reordenar Categorias** (no menu de ações da aba) define a ordem em que as seções aparecem para o cliente. A ordem **não** segue a data de criação.
* **Excluir** remove a categoria e os itens vinculados. A ação é **irreversível** e não tem desfazer.

## Próximos passos

* Cadastrar itens
* Configurar pizzas

# Itens

Os **itens** são os produtos que aparecem no cardápio — com nome, descrição, preço, foto e complementos. Cada item pertence a uma categoria, e o formato do cadastro muda conforme o **Tipo de Item** dessa categoria.

## Antes de começar

Você precisa de uma categoria já criada. O Tipo de Item da categoria (Simples, Pizza, Vinho ou Combo) define quais campos aparecem no item.

## Como acessar

No menu lateral, clique em **Cardápios**, abra o cardápio e vá na aba **Itens**. Use a busca para encontrar um produto pelo nome.

## Cadastrar um item

Clique em **Adicionar item**. O cadastro tem três passos:

1. **Categoria** — escolha a categoria do item em **Categoria do Item**.
2. **Detalhes** — preencha os dados do produto (os campos variam por tipo).
3. **Revisão** — confira o resumo e finalize.

Para **Pizza**, você define o preço por tamanho — veja Configurar pizzas. Para **Vinho**, define o preço por volume. Para **Combo**, escolhe os itens que compõem o combo e o preço.

## Campos do item

Campos do passo **Detalhes** para um **Item Simples**:

| Campo                          | Obrigatório | Descrição                                             |
| ------------------------------ | ----------- | ----------------------------------------------------- |
| **Nome do Produto**            | Sim         | Nome exibido no cardápio.                             |
| **Descrição**                  | Não         | Ingredientes, preparo ou diferenciais.                |
| **Preço Interno**              | Sim         | Preço para o **salão** (balcão).                      |
| **Preço Delivery**             | Não         | Preço para **delivery**. Pode ser diferente do salão. |
| **Disponível para Balcão**     | Não         | Se o item é vendido no salão.                         |
| **Disponível para Delivery**   | Não         | Se o item é vendido no delivery.                      |
| **Status do Item**             | Não         | **Disponível** ou **Indisponível** para o cliente.    |
| **Imagens do Produto**         | Não         | Foto do item. Itens com foto vendem melhor.           |
| **Tempo de Preparo (minutos)** | Não         | Tempo estimado de preparo. Padrão 30.                 |
| **Porções**                    | Não         | Quantas pessoas o item serve. Padrão 1.               |
| **Produto em Destaque**        | Não         | Destaca o item no cardápio.                           |

No mesmo passo, em **Grupos de Opções**, você vincula os complementos do item (ponto da carne, adicionais, acompanhamentos).

> ℹ️ **Observação:** os preços são separados por canal. Deixar **Preço Delivery** zerado e **Disponível para Delivery** desligado tira o item do delivery, mas ele continua no salão.

## Turnos de Funcionamento

Em **Turnos de Funcionamento** (no passo Detalhes) você define **horários e dias** em que o item aparece no cardápio. É útil para itens que só existem no almoço ou em dias específicos.

Cada turno tem **Nome do Turno**, **Horário de Início**, **Horário de Fim**, os dias da semana (**Segunda** a **Domingo**) e o toggle **Turno ativo**. Clique em **Adicionar Turno** para criar.

> ⚠️ **Atenção:** com um turno configurado, o item **só aparece dentro daquela janela**. Fora do horário ou dos dias marcados, ele some do link — sem turno, fica sempre visível. Se um item sumiu sem explicação, veja Um item não aparece no link do cardápio.

## Pausar e reordenar itens

* **Pausar** o item (ou deixar o status **Indisponível**) o esconde do cardápio e dos pedidos manuais, sem apagar o cadastro. É a forma recomendada de tirar um prato do ar temporariamente.
* **Reordenar Itens** (no menu de ações da aba) define a ordem dos itens dentro da categoria. A ordem **não** segue a data de criação.
* **Excluir** é irreversível e não tem desfazer.

## Próximos passos

* Montar complementos
* Configurar pizzas
* Um item não aparece no link do cardápio

# Pizzas

Pizza é um **Tipo de Item** de categoria. Diferente de um item simples, a pizza tem **tamanhos**, **massas**, **bordas** e **sabores** — e o preço de uma pizza com vários sabores depende de uma regra que você escolhe. Toda a configuração fica na aba **Categorias**.

## Antes de começar

Você precisa de uma categoria do tipo **Pizza**. Ao criar essa categoria, você define o **Método de Preço** (Soma, Máximo ou Média), usado no cálculo da pizza com vários sabores.

## Como acessar

No menu lateral, clique em **Cardápios**, abra o cardápio e vá na aba **Categorias**. Clique na categoria de pizza para **expandir** o card — as seções **TAMANHOS**, **MASSAS** e **BORDAS** aparecem dentro dela.

## Tamanhos

Em **TAMANHOS**, clique em **+** para adicionar um tamanho:

| Campo                 | Obrigatório | Descrição                                                                                           |
| --------------------- | ----------- | --------------------------------------------------------------------------------------------------- |
| **Nome do Tamanho**   | Sim         | Ex: "Média 25 cm", "Grande 35 cm".                                                                  |
| **Número de Fatias**  | Sim         | Quantas fatias o tamanho tem.                                                                       |
| **Frações Aceitas**   | Sim         | Em quantas partes a pizza pode ser dividida: **1/1** (inteira), **1/2** (meio a meio), **1/4** etc. |
| **Ordem de Exibição** | Não         | Posição do tamanho na lista.                                                                        |

As **Frações Aceitas** definem quantos sabores cabem numa pizza daquele tamanho: `1/2` permite meio a meio, `1/4` permite até quatro sabores.

## Massas e bordas

Em **MASSAS** e **BORDAS**, clique em **+** para adicionar. Massas e bordas têm os mesmos campos:

| Campo                                 | Obrigatório | Descrição                                                        |
| ------------------------------------- | ----------- | ---------------------------------------------------------------- |
| **Nome da Massa** / **Nome da Borda** | Sim         | Ex: "Tradicional", "Integral"; "Catupiry", "Cheddar".            |
| **Preço Interno**                     | Sim         | Acréscimo no salão. Use `0,00` para sem acréscimo.               |
| **Preço Delivery**                    | Não         | Acréscimo no delivery. Use `0,00` se não disponível no delivery. |
| **Ordem de Exibição**                 | Não         | Posição na lista.                                                |

## Sabores

Os **sabores** são cadastrados como **itens** da categoria de pizza. Na aba **Itens**, clique em **Adicionar item**, escolha a categoria de pizza e defina o **preço por tamanho** (Preço Interno e Preço Delivery em cada tamanho criado). Por isso a categoria de pizza conta os cadastros em **sabores**, não em itens.

## Preço da pizza com vários sabores

Quando o cliente monta uma pizza meio a meio (ou em mais partes), o preço final vem do **Método de Preço** definido na categoria:

| Método de Preço | Como calcula                                                                        |
| --------------- | ----------------------------------------------------------------------------------- |
| **Soma**        | Soma a parte proporcional de cada sabor. Meia de R$ 50 + meia de R$ 40 = **R$ 45**. |
| **Máximo**      | Cobra o sabor **mais caro**. Meia de R$ 50 + meia de R$ 40 = **R$ 50**.             |
| **Média**       | Cobra a **média** dos sabores. Meia de R$ 50 + meia de R$ 40 = **R$ 45**.           |

> ℹ️ **Observação:** **Soma** e **Média** dão o mesmo valor numa pizza meio a meio, mas mudam quando há frações diferentes (ex: 1/4 + 3/4). **Máximo** é o mais usado por quem não quer cobrar barato pela metade mais cara.

## Próximos passos

* Criar e organizar categorias
* Cadastrar itens
* Montar complementos

# Complementos

Os **complementos** são grupos de opções extras que você vincula a um ou mais itens — ponto da carne, adicionais, bordas, acompanhamentos. Cada grupo reúne as opções, e cada opção pode ter um preço próprio.

## Antes de começar

Você precisa de um cardápio criado. Para usar o complemento, é preciso ter pelo menos um item ao qual vinculá-lo.

## Como acessar

No menu lateral, clique em **Cardápios**, abra o cardápio e vá na aba **Complementos**.

## Criar um grupo de opções

Clique em **Adicionar complemento**. O cadastro tem três passos:

1. **Informações Básicas** — nome do grupo, tipo e regras de seleção.
2. **Configurar Opções** — as opções e seus preços.
3. **Revisão** — confira e finalize.

### Informações Básicas

| Campo                       | Obrigatório | Descrição                                                                          |
| --------------------------- | ----------- | ---------------------------------------------------------------------------------- |
| **Nome do Grupo de Opções** | Sim         | Nome exibido ao cliente (ex: "Ponto da carne", "Adicionais").                      |
| **Tipo de Grupo de Opções** | Sim         | Como o cliente escolhe (veja abaixo).                                              |
| **Mínimo Permitido**        | Não         | Quantas opções o cliente deve escolher. **0** torna o grupo opcional.              |
| **Máximo Permitido**        | Não         | Quantas opções o cliente pode escolher no total.                                   |
| **Método de Preço**         | Não         | Como somar o preço quando há mais de uma opção: **Soma**, **Máximo** ou **Média**. |
| **Status**                  | Não         | **Disponível** ou **Indisponível** para o cliente.                                 |

### Tipos de Grupo de Opções

| Tipo                 | Como funciona                                | Exemplo                                             |
| -------------------- | -------------------------------------------- | --------------------------------------------------- |
| **Opção única**      | O cliente escolhe exatamente uma opção.      | Ponto da carne: Mal passado, Ao ponto, Bem passado. |
| **Opções múltiplas** | O cliente marca quantas opções quiser.       | Adicionais: Queijo, Bacon, Ovo.                     |
| **Com quantidade**   | O cliente define a quantidade de cada opção. | Molhos: 2 de barbecue, 1 de alho.                   |

## Configurar as opções

No passo **Configurar Opções**, clique em **Adicionar Opção** e preencha:

| Campo                 | Obrigatório | Descrição                                                |
| --------------------- | ----------- | -------------------------------------------------------- |
| **Nome da Opção**     | Sim         | Nome exibido (ex: "Mussarela Extra").                    |
| **Descrição**         | Não         | Detalhe opcional da opção.                               |
| **Preço (Balcão)**    | Não         | Acréscimo no **salão**. Use `0,00` para opção sem custo. |
| **Preço (Delivery)**  | Não         | Acréscimo no **delivery**. Pode diferir do salão.        |
| **Quantidade Máxima** | Não         | Quantas unidades dessa opção o cliente pode pedir.       |
| **Status**            | Não         | **Disponível** ou **Indisponível** por opção.            |

## Vincular o complemento aos itens

O grupo de opções é vinculado ao item **na aba Itens**, em **Grupos de Opções** (no passo Detalhes do item). Um mesmo grupo pode ser reutilizado em vários itens — útil para "Ponto da carne" ou "Adicionais".

> ℹ️ **Observação:** em categorias de **Pizza**, os grupos de opções são vinculados na própria categoria, não item a item. Veja Configurar pizzas.

## Dicas e observações

> 💡 **Dica:** para tornar um complemento **obrigatório**, defina **Mínimo Permitido** como **1** ou mais — o cliente precisa escolher antes de continuar.

> ⚠️ **Atenção:** **excluir** um grupo o desvincula de todos os itens associados e é irreversível. Para tirá-lo do ar temporariamente, deixe o **Status** como **Indisponível**.

## Próximos passos

* Cadastrar itens
* Configurar pizzas

# Item não aparece no link do cardápio

Você cadastrou um item, mas ele não aparece para o cliente no link público do cardápio. Quase sempre é uma configuração de visibilidade, não um erro. Verifique as causas abaixo na ordem.

## Sintomas

* O item está cadastrado na aba **Itens**, mas não aparece no link público.
* O item aparecia antes e sumiu sozinho, sem ninguém excluí-lo.
* O item aparece no salão mas não no delivery (ou o contrário).

## Causas comuns

### 1. Item pausado ou indisponível

**Como verificar:** em **Cardápios** → aba **Itens**, confira se o item está **pausado** ou com **Status do Item** em **Indisponível**.

**Solução:** reative o item (despause ou mude o status para **Disponível**). A mudança vale na hora.

### 2. Categoria pausada

**Como verificar:** na aba **Categorias**, veja se a categoria do item está **pausada**. Uma categoria pausada esconde **todos** os itens dela.

**Solução:** reative a categoria. Os itens voltam a aparecer.

### 3. Fora do Turno de Funcionamento

**Como verificar:** abra o item e veja a seção **Turnos de Funcionamento**. Se houver um turno, confira **Horário de Início**, **Horário de Fim** e os dias marcados. Compare com o horário e o dia atuais.

**Solução:** ajuste a janela do turno, marque os dias certos, ou **remova o turno** para o item ficar sempre visível. Sem turno configurado, o item aparece o tempo todo.

### 4. Item desligado para o canal

**Como verificar:** abra o item e veja **Disponível para Balcão** e **Disponível para Delivery**. Um item com **Disponível para Delivery** desligado não aparece no link de delivery, mesmo ativo no salão. Confira também se o cardápio aceita aquele canal em **Aceitar Pedidos de Delivery** / **Aceitar Pedidos de Salão**.

**Solução:** ligue o canal no item e confirme que o cardápio aceita pedidos desse canal.

### 5. Cardápio inativo ou cliente em outro cardápio

**Como verificar:** confira se o **Catálogo Ativo** está ligado no cardápio. Se a loja tem mais de um cardápio, confirme que o cliente está no cardápio onde o item foi cadastrado (o slug na URL identifica qual é).

**Solução:** ative o cardápio, ou envie ao cliente o link do cardápio correto.

## Se nada disso resolver

* Anote o nome do item, o cardápio (slug) e o horário em que o cliente tentou ver.
* Abra o link público você mesmo, no horário do problema, para confirmar o sintoma.
* Abra um chamado pelo canal de suporte com essas informações.

## Relacionado

* Cadastrar itens
* Criar e organizar categorias
