# Clientes

O módulo **Clientes** é a base de contatos do seu estabelecimento no Dionísio. É onde você visualiza, cadastra, importa, organiza e exporta os clientes, além de abrir o perfil de cada um com o histórico de relacionamento. A tela é dividida em duas abas: **Clientes** (a lista geral de contatos) e **Grupos de Clientes** (segmentação da base).

## Para quem é

* **Dono e Administrador** — definem quais campos são obrigatórios em cada contexto de atendimento (**Configurações Avançadas**), importam bases existentes e exportam dados para análise.
* **Membro** — no dia a dia, cadastra clientes, busca contatos, abre o perfil e inicia conversas no WhatsApp a partir da lista.

> ℹ️ **Observação:** "cliente" aqui é um contato do restaurante (quem reserva, pede ou entra na fila) — não confunda com **usuário** do sistema (Dono, Administrador, Membro), que é quem opera o Dionísio.

## Como acessar

No menu lateral, clique em **Clientes**. A tela abre na aba **Clientes**.

## O que você pode fazer

* **Cadastrar um cliente** — botão **Novo Cliente**. O formulário pede **Nome Completo** e **Telefone** (obrigatórios) e, opcionalmente, **Email**, **CPF**, **Gênero**, **Data de Nascimento** e **Observações**.
* **Ver o** **Perfil do Cliente** — ícone de visualizar (ou clique na linha) abre o perfil com o histórico completo.
* **Editar um cliente** — ícone de editar abre o cadastro; salvar não apaga o histórico.
* **Conversar pelo WhatsApp** — ícone de mensagem inicia uma conversa com o cliente.
* **Buscar e filtrar** — campo de busca por nome ou telefone, e **Filtros Avançados** (nome, telefone, CPF, gênero, email e faixa de idade).
* **Importar clientes em massa** — botão **Importar Clientes**, a partir de uma planilha CSV ou Excel.
* **Exportar a base** — **Exportar PDF** (lista para impressão) ou **Exportar Excel** (planilha com opções de campos, ordenação e limite).
* **Organizar em** **Grupos de Clientes** — na aba **Grupos de Clientes**, segmente a base (criar um grupo, gerenciar grupos) para usar como público dos disparos no WhatsApp.

## Principais conceitos

### A lista de clientes

A aba **Clientes** lista os contatos em uma tabela com as colunas **Nome**, **Telefone**, **CPF**, **Idade** e **Gênero**, além de uma coluna de ações por linha. A **Idade** é calculada a partir da data de nascimento; quando o dado não existe, a célula mostra `—`. A lista é ordenada por **completude de perfil** (clientes com mais campos preenchidos aparecem primeiro) e, em empate, por nome.

### Campos obrigatórios por contexto (Configurações Avançadas)

Em **Configurações Avançadas** (na barra de ferramentas, ícone de engrenagem; título da janela: **Configurações Avançadas de Clientes**), você define quais campos são exigidos do cliente em cada contexto de atendimento: **Reservas Pagas**, **Reservas Gratuitas**, **Eventos**, **Fila**, **Pedidos** e **NPS**. Os campos configuráveis são **Telefone**, **Nome**, **CPF**, **Data de Nascimento**, **Gênero**, **Email** e **Endereço**. **Nome** e **Telefone** são sempre obrigatórios em todos os contextos e não podem ser desmarcados; em **Reservas Pagas**, o **CPF** também é obrigatório.

### Grupo de Clientes

Um **Grupo de Clientes** é um segmento da base, usado como público dos Disparos no WhatsApp. Os grupos ficam na segunda aba e podem ser **Manual** ou **Automático**. Veja a página Grupos de Clientes para detalhes.

> 💡 **Dica:** manter a base completa e organizada é o que torna a comunicação no WhatsApp certeira. Quanto mais campos preenchidos (telefone, data de nascimento, gênero), melhor você segmenta — e um disparo para o grupo certo (aniversariantes do mês, quem sumiu, clientes recorrentes) rende muito mais do que uma mensagem para todo mundo.

## Integrações e canais

* **WhatsApp** — a partir de qualquer cliente na lista você inicia uma conversa; os **Grupos de Clientes** viram o público dos Disparos (mensagens pontuais). As Campanhas (Sistema de Marketing IA) são automáticas e disparam pelo comportamento do cliente — não dependem de grupos.
* **Reservas, Eventos, Fila, Pedidos e NPS** — cada um desses contextos pode exigir campos diferentes do cliente, conforme você configurar em **Configurações Avançadas**.

> ℹ️ **Observação:** você não precisa cadastrar todo mundo à mão. Um contato vira cliente automaticamente quando faz uma reserva, entra na fila, faz um pedido, entra na lista de um evento, responde uma pesquisa ou fala com a Assistente IA — por isso a coluna **Origem** do perfil mostra de onde cada cliente veio. O cadastro usa o **telefone** como chave: se o número já existe na base, os dados são atualizados no cadastro existente em vez de criar um cliente duplicado.

## Começando

Se você está começando agora, siga nesta ordem:

1. Cadastre seus primeiros clientes com **Novo Cliente**, ou traga sua base existente com **Importar Clientes**.
2. Defina os campos obrigatórios por contexto em **Configurações Avançadas**.
3. Organize a base em Grupos de Clientes para usar como público dos disparos no WhatsApp.

# Perfil do Cliente

O **Perfil do Cliente** é a tela que reúne, em um só lugar, os dados cadastrais de um cliente, suas estatísticas de relacionamento e o histórico completo de atividades dele com o restaurante. É uma tela de gestão interna — só o operador acessa, o cliente final não vê esse perfil.

## Como funciona

### Como abrir o perfil

Na lista de **Clientes**, clique no ícone de **visualizar** (olho), com a dica **Ver detalhes**, na linha do cliente.

A tela abre no endereço `/home/clients/:clientId/history` e tem o título **Perfil do Cliente** no topo.

No topo ainda há os botões **arrow\_back** (voltar para a lista de Clientes) e **refresh** (recarregar os dados do perfil).

### Cabeçalho

O cabeçalho mostra a identidade do cliente e as ações principais.

| Elemento            | O que mostra                                                                                                   |
| ------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Nome**            | Nome do cliente, em destaque, com um avatar gerado a partir das iniciais.                                      |
| **ID**              | Identificador curto no formato `#XXXXX` — os 5 primeiros caracteres do ID interno, em maiúsculas.              |
| **Origem**          | Como o cliente entrou na base (ver tabela abaixo). Só aparece quando há origem registrada.                     |
| **Grupos**          | Quantidade de grupos dos quais o cliente faz parte, ex.: `2 grupos`. Só aparece quando há pelo menos um grupo. |
| **Editar Perfil**   | Abre o formulário de edição dos dados cadastrais.                                                              |
| **Enviar Mensagem** | Abre o envio de mensagem por WhatsApp para esse cliente.                                                       |

> ℹ️ **Observação:** o botão **Enviar Mensagem** exige que o cliente tenha um telefone cadastrado. Sem telefone, aparece o aviso **Cliente não possui telefone cadastrado** e nada é aberto.

### Informações Detalhadas

O painel **Informações Detalhadas** lista os dados cadastrais do cliente. Campos sem valor exibem **Não informado**; o campo **Origem** usa **Não definido** quando não há origem registrada.

| Campo           | O que mostra                                                                                                                              |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Telefone**    | Número cadastrado, ou **Não informado**.                                                                                                  |
| **Email**       | E-mail cadastrado, ou **Não informado**.                                                                                                  |
| **CPF**         | CPF cadastrado, ou **Não informado**.                                                                                                     |
| **Aniversário** | Data de nascimento. Com ano, no formato `dia mês, ano` (ex.: `9 Junho, 1990`); sem ano, apenas `dia mês`. **Não informado** quando vazio. |
| **Gênero**      | **Masculino** ou **Feminino**; **Não informado** quando vazio.                                                                            |
| **Origem**      | Canal de entrada do cliente, ex.: **Cadastro Manual**, **Reserva**; **Não definido** quando vazio.                                        |
| **Criado em**   | Data de criação do cadastro, por extenso (ex.: `9 de junho de 2026`).                                                                     |
| **Grupos**      | Nome dos grupos dos quais o cliente faz parte, em etiquetas. Só aparece quando há pelo menos um grupo.                                    |

Quando o cliente tem endereços cadastrados, aparece abaixo uma seção **Endereços** com a lista dos endereços e, para os que têm coordenadas, um mapa com a localização.

#### Valores de Origem

A origem indica por qual canal o cliente entrou na base. Os valores exibidos são:

| Origem exibida      | Quando ocorre                                     |
| ------------------- | ------------------------------------------------- |
| **Reserva**         | Cliente criado a partir de uma reserva.           |
| **Lista de Evento** | Cliente adicionado pela lista de um evento.       |
| **Cadastro Manual** | Cliente cadastrado manualmente pelo operador.     |
| **Fila**            | Cliente que entrou pela fila de espera.           |
| **iFood**           | Cliente vindo de um pedido do iFood.              |
| **Pedido**          | Cliente vindo de um pedido.                       |
| **NPS**             | Cliente que respondeu uma Pesquisa de Satisfação. |

> ℹ️ **Observação:** quando o contato veio por um canal de mensagem, a origem ganha um sufixo, ex.: **Reserva • WhatsApp** ou **Cadastro Manual • Instagram**. Se houver mais de um canal, eles aparecem juntos, separados por vírgula: **Reserva • WhatsApp, Instagram**.

### Estatísticas

Quando há dados de resumo, o perfil mostra cartões com a contagem **total** (acumulada) de atividades do cliente.

| Métrica                | O que conta                                         |
| ---------------------- | --------------------------------------------------- |
| **Reservas Criadas**   | Total de reservas feitas pelo cliente.              |
| **Grupos Adicionados** | Total de grupos aos quais o cliente foi adicionado. |

### Histórico de Atividades

A coluna **Histórico de Atividades** mostra uma linha do tempo dos eventos do cliente, do mais recente para o mais antigo. Cada entrada traz a **data e hora**, um **ícone** do tipo de evento, um **título** e uma **descrição**.

Os eventos são carregados em blocos: o botão **Carregar Mais Atividades** exibe mais entradas. Quando o cliente não tem nenhum evento, aparece **Nenhuma atividade registrada**; quando há eventos, mas todos foram filtrados (ver observação abaixo), a linha do tempo mostra **Nenhum histórico encontrado**.

Tipos de evento exibidos na linha do tempo:

| Evento                           | O que registra                                                            |
| -------------------------------- | ------------------------------------------------------------------------- |
| **Cliente Criado**               | Criação do perfil, com a data da última atualização quando houver.        |
| **Reserva Criada**               | Reserva feita pelo cliente, com número de pessoas e status.               |
| **Pagamento Realizado**          | Pagamento, com tipo de serviço, forma de pagamento, valor e status.       |
| **Adicionado à Lista de Evento** | Entrada na lista de um evento, com o nome da lista.                       |
| **Adicionado ao Grupo**          | Entrada em um Grupo de Clientes, com o nome do grupo.                     |
| **Entrou na Fila**               | Entrada na fila de espera, com o nome da fila e o status.                 |
| **Conversa WhatsApp**            | Atendimento por WhatsApp.                                                 |
| **Pedido Criado**                | Pedido, com número, tipo, status e valor.                                 |
| **Pedido iFood**                 | Pedido do iFood (exibe **Concluído** ou **Cancelado** conforme o status). |
| **Pesquisa NPS Respondida**      | Resposta a uma Pesquisa de Satisfação, com o nome da pesquisa.            |

> ℹ️ **Observação:** nem todo evento aparece. Conversas de WhatsApp marcadas como notificação automática e pedidos do iFood ainda não finalizados ficam de fora da linha do tempo.

## Quando usar

* Para conferir os dados cadastrais completos de um cliente antes de atendê-lo.
* Para ver o relacionamento dele com o restaurante: reservas, pedidos, filas, conversas e participação em grupos.
* Para iniciar uma conversa por WhatsApp ou corrigir/atualizar os dados do cliente sem sair da tela.

## Limitações

* O perfil é uma tela interna do operador; o cliente final não tem acesso a ela.
* O botão **Enviar Mensagem** depende de o cliente ter telefone cadastrado.
* A linha do tempo omite conversas automáticas de notificação e pedidos iFood não finalizados.
* O **Histórico de Atividades** é permanente e auditável: ele só pode ser carregado e atualizado, não há ação para apagar ou editar os eventos. Mesmo ao editar os dados cadastrais do cliente, o histórico é preservado.

## Relacionado

* Grupos de Clientes

# Grupos de Clientes

Um **Grupo de Clientes** é um segmento da sua base de contatos no Dionísio, usado como público dos Disparos no WhatsApp. Os grupos ficam na aba **Grupos de Clientes**, dentro de **Clientes**, e podem ser **Manual** (você escolhe quem entra) ou **Automático** (o sistema recalcula os membros sozinho, a partir de regras de comportamento).

## Como funciona

| Tipo           | Como funciona                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------- |
| **Manual**     | Você adiciona e remove os clientes. Ideal para listas fixas (ex: "Clientes VIP", "Parceiros"). |
| **Automático** | O sistema adiciona e remove clientes automaticamente, com base nas regras que você define.     |

### O que você vê em cada grupo

Os grupos aparecem em uma grade de cards. Cada card mostra:

| Elemento                      | Descrição                                                                                                                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Status**                    | `ATIVO` ou `EM PAUSA` — indica se o grupo está em uso.                                                                          |
| **Nome do grupo**             | Título do grupo. Grupos padrão começam com `*` (asterisco e espaço), um prefixo reservado que só o sistema usa.                 |
| **Tipo**                      | **Automação Inteligente** (ícone `auto_awesome`) para grupos automáticos, ou **Manual** (ícone `settings`) para grupos manuais. |
| **Membros**                   | Quantidade de clientes que fazem parte do grupo no momento.                                                                     |
| **Atualizado / Editado há X** | Quando o grupo teve a última recalculação automática (**Atualizado**) ou a última edição (**Editado**).                         |

### Como os grupos são usados

* **WhatsApp →** **Disparos****:** num disparo, o passo **Pra quem vai?** deixa você escolher um ou mais grupos como público.
* **Perfil do cliente****:** os grupos do cliente aparecem no perfil dele.

> ℹ️ **Observação:** as Campanhas (Sistema de Marketing IA) são automáticas e disparam pelo comportamento do cliente — elas **não** usam Grupos de Clientes como público. Para escolher um grupo manualmente, use os Disparos.

## Quando usar

* Use um grupo **Manual** para listas fixas que você controla à mão (clientes VIP, parceiros).
* Use um grupo **Automático** para segmentos dinâmicos que mudam sozinhos (quem reservou nos últimos 30 dias, aniversariantes do mês).
* Use **Criar Grupos Padrão** para começar rápido com um conjunto de grupos prontos — veja Gerenciar grupos de clientes.

## Limitações

* Há um limite de **50 grupos por tipo** — até 50 manuais e até 50 automáticos por loja. Ao tentar criar além disso, o sistema avisa que o limite foi atingido.
* O prefixo `*` é reservado para grupos padrão criados pelo sistema. Se você tentar salvar um grupo manual com um nome que começa com `*` , o sistema recusa o nome ao salvar.
* Um grupo **EM PAUSA** congela os membros: a atualização automática para até você reativá-lo. Detalhes em Gerenciar grupos de clientes.

## Relacionado

* Criar um grupo de clientes
* Gerenciar grupos de clientes
* Disparos
* Perfil do Cliente

# Criar um grupo de clientes

Crie um **Grupo de Clientes** para segmentar sua base e usar como público dos Disparos no WhatsApp. Um grupo pode ser **Manual** (você escolhe quem entra) ou **Automático** (o sistema recalcula os membros por regras de comportamento). Para entender o que é um grupo e quando usar cada tipo, veja Grupos de Clientes.

## Como acessar

No menu lateral, abra **Clientes** e a aba **Grupos de Clientes**. Clique em **Novo Grupo** para abrir o assistente em 4 passos.

## Passos

1. **Informações Básicas** — preencha o **Nome do Grupo** (até 100 caracteres) e, se quiser, uma **Descrição** (até 200). Escolha o **Tipo do Grupo**: **Manual** ou **Automático**.
2. **Adicionar Regras** *(só Automático)* — crie pelo menos uma regra que define quem entra no grupo. Um grupo Manual pula este passo e vai direto à revisão.
3. **Construir Expressão Lógica** *(só Automático)* — combine as regras com os operadores **AND** (o cliente precisa atender a todas as regras ligadas) e **OR** (basta atender a uma delas). Você pode adicionar até 6 regras.
4. **Revisão** — confira as informações e confirme. O grupo recém-criado nasce **ATIVO**.

## Campos e regras

### Passo 1 — Informações Básicas

| Campo             | Obrigatório | Descrição                                                  |
| ----------------- | ----------- | ---------------------------------------------------------- |
| **Nome do Grupo** | Sim         | Nome do grupo. Limite de 100 caracteres.                   |
| **Descrição**     | Não         | Texto livre que explica o grupo. Limite de 200 caracteres. |
| **Tipo do Grupo** | Sim         | **Manual** ou **Automático** (ver abaixo).                 |

| Tipo           | Como funciona                                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| **Manual**     | Você adiciona e remove os clientes. Ideal para listas fixas (ex: "Clientes VIP", "Parceiros").                  |
| **Automático** | O sistema adiciona e remove clientes automaticamente, com base nas regras que você define nos passos seguintes. |

### Tipos de regra (grupos Automáticos)

No passo **Adicionar Regras**, cada regra tem **Nome da Regra** (obrigatório), **Descrição (opcional)** e um **Tipo de Regra**:

| Tipo de Regra              | Segmenta por                                                     |
| -------------------------- | ---------------------------------------------------------------- |
| **Contagem de Reservas**   | Número de reservas no período.                                   |
| **Interações de Conversa** | Clientes que interagiram via chat (IA, atendimento humano etc.). |
| **Inatividade no Chat**    | Clientes sem atividade no chat há um tempo.                      |
| **Aniversários**           | Aniversário em um período específico.                            |
| **Criação de Cliente**     | Data de cadastro do cliente.                                     |
| **Total Gasto**            | Valor total gasto pelo cliente.                                  |
| **Nome na Lista**          | Presença em listas de eventos.                                   |
| **Participação em Fila**   | Clientes que participaram de filas.                              |
| **Pedidos (Dionísio)**     | Pedidos no sistema de delivery do Dionísio.                      |
| **Pedidos (iFood)**        | Pedidos no iFood.                                                |

Cada tipo abre seus próprios filtros. Por exemplo, em **Contagem de Reservas** você configura:

* **Período de Análise:** o intervalo de tempo considerado.
* **Critérios de Contagem:** mínimo e máximo de reservas no período.
* **Status das Reservas:** quais status contam — **Pendente**, **Aguardando Pagamento**, **Confirmada** (padrão), **Sentados**, **Concluída**, **Cancelada** ou **Não Compareceu**.
* **Filtros de Localização (opcional):** restringir por área, mesa ou experiência.
* **Filtro de valor de pagamento (opcional):** faixa de valor da reserva.
* **Filtro de Capacidade (opcional):** quantidade de pessoas.

## Dicas e observações

> 💡 **Dica:** use grupos **Automáticos** para segmentos dinâmicos (ex: "quem reservou nos últimos 30 dias") e **Manuais** para listas fixas que você controla à mão.

## Próximos passos

* Gerenciar grupos de clientes
* Disparos

# Gerenciar grupos de clientes

Depois de criar seus grupos, é na aba **Grupos de Clientes** que você os organiza: busca, filtra, edita, pausa, atualiza, exclui — e cria de uma vez um conjunto de grupos prontos. Para entender o que é um grupo, veja Grupos de Clientes.

## Como acessar

No menu lateral, abra **Clientes** e clique na aba **Grupos de Clientes**.

## Filtrar e buscar grupos

No topo da aba você tem dois controles:

* **Buscar Grupos:** campo de texto que filtra por nome ou descrição do grupo.
* **Filtrar por Status:** botão que abre um seletor (rotulado **Filtrar por tipo**) para mostrar apenas grupos **Manual** ou **Automático**. Use **Limpar** para remover o filtro.

## Criar grupos prontos

O botão **Criar Grupos Padrão** gera de uma vez um conjunto de grupos automáticos prontos, com regras já configuradas (clientes novos, recorrentes, aniversariantes do mês, engajados no WhatsApp, ativos em filas, entre outros).

**Quais grupos são criados depende dos módulos ativos da sua loja.** Grupos baseados em reservas, filas, eventos, pedidos ou WhatsApp só são criados se a loja tiver o módulo correspondente habilitado.

Se os grupos padrão já existirem, o sistema avisa **Grupos padrão já existem** e não duplica nada. Caso contrário, mostra quantos foram criados.

> 💡 **Dica:** os grupos padrão continuam se atualizando sozinhos depois de criados — você não precisa recriá-los.

## Editar, pausar e excluir

No menu **⋮** (`more_vert`) de cada card, você tem:

| Ação                   | O que faz                                                                        |
| ---------------------- | -------------------------------------------------------------------------------- |
| **Ver membros**        | Abre a lista de clientes que fazem parte do grupo.                               |
| **Editar**             | Altera nome, descrição e — nos automáticos — o agendamento de atualização.       |
| **Ativar / Desativar** | Pausa ou retoma o grupo. Pede confirmação.                                       |
| **Atualizar grupo**    | Recalcula os membros na hora. Aparece só em grupos automáticos e ativos.         |
| **Excluir**            | Remove o grupo. Pede confirmação. Os clientes **não** são apagados — só o grupo. |

> ℹ️ **Observação:** colocar um grupo **EM PAUSA** congela os membros — a atualização automática para e a ação **Atualizar grupo** some, então a lista de clientes fica como estava. O grupo continua disponível para selecionar como público nos disparos; pausar não o tira da seleção.

> ⚠️ **Atenção:** enquanto um grupo automático está atualizando (ícone girando, "Atualizando..."), as ações de editar, ativar/desativar, atualizar e excluir ficam indisponíveis até a recalculação terminar.

## Dicas e observações

> ⚠️ **Atenção:** há um limite de **50 grupos por tipo** — até 50 manuais e até 50 automáticos por loja. Ao tentar criar além disso, o sistema avisa que o limite foi atingido.

## Próximos passos

* Criar um grupo de clientes
* Disparos
