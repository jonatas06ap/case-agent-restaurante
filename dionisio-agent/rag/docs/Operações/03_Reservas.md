# Reservas

O módulo **Reservas** gerencia todo o ciclo de reservas do seu restaurante — desde a captação (pelo Link de Reservas público ou pela IA via WhatsApp e Instagram) até a operação no dia (aprovar pendentes, acomodar o cliente, marcar no-show) e a análise posterior (Histórico, exportações). Configura áreas, horários, Experiências pagas, bloqueios, políticas de cobrança e notificações automáticas.

## Para quem é

* **Dono e Administrador** — configuram o módulo: criam Áreas, definem horários e capacidade, configuram cobrança e políticas, ativam notificações.
* **Membros** — operam o módulo no dia a dia: aprovam reservas pendentes, marcam Sentados/Não Compareceu, atendem clientes na recepção.

## O que você pode fazer

**Operação do dia a dia**

* Operar reservas pela Visão Geral — acompanhar próximas e pendentes em tempo real.
* Criar uma reserva manualmente — registrar reserva por telefone, balcão ou outro canal.
* Confirmar, sentar, cancelar e Não Compareceu — agir sobre uma reserva pelo cartão.
* Calendário de Reservas — visualizar por mês/semana/dia e exportar PDF.
* Histórico de Reservas — consultar reservas passadas e exportar para Excel.

**Configuração**

* Áreas e Mesas — criar Áreas, configurar horários e capacidade, definir regras globais.
* Link de Reservas — URL pública que o cliente usa para reservar sozinho.
* Experiências — eventos especiais pagos, com capacidade paralela à reserva padrão.
* Datas Especiais — horários diferentes em feriados e datas comemorativas.
* Bloqueios — impedir reservas em períodos específicos.
* Notificações automáticas para o cliente — lembretes e avisos por WhatsApp.
* Políticas e pagamentos — recebimento, políticas de cancelamento, no-show e reagendamento.

## Principais conceitos

* Ciclo de vida de uma reserva — os 10 status possíveis e as transições automáticas (1h/3h após o início).
* **Reserva padrão × Experiência:** Experiências são reservas pagas paralelas, com capacidade própria — criar uma aumenta a capacidade efetiva do dia. Veja Experiências.
* **Datas Especiais × Bloqueios:** Data Especial **altera** os horários do dia; Bloqueio **impede** reservas. Veja a matriz comparativa em Bloqueios.
* **Capacidade compartilhada:** opção que define como a capacidade total do horário se distribui entre os slots. Detalhada em Configurar horários e capacidade.

## Integrações e canais

* **Link de Reservas público** — captação direta pelo cliente final, sem intermediação.
* **IA (WhatsApp e Instagram)** — captação por conversa; reservas pagas usam o mesmo Link de Reservas na etapa de pagamento.
* **WhatsApp** — canal das notificações automáticas para o cliente.
* **Clientes (CRM)** — toda reserva nova cria ou atualiza o cliente; campos coletados configurados em **Clientes** → **Configurações Avançadas**.
* **Relatórios** — métricas consolidadas de reservas ficam no módulo **Relatórios** (não dentro de Reservas).
* **Satisfação** — pesquisa pós-visita disparada automaticamente quando a reserva vira **Concluída**.

## Por onde começar

Se você está habilitando o módulo Reservas pela primeira vez, siga esta ordem:

1. Crie pelo menos uma Área em Áreas e Mesas.
2. Configure os horários e capacidade da Área.
3. Ajuste as Configurações Avançadas (confirmação automática, dias de antecedência etc.).
4. Se for cobrar antecipadamente, configure o recebimento e as políticas.
5. Crie notificações automáticas para os clientes.
6. Compartilhe o seu Link de Reservas com os clientes.

# Ciclo de vida de uma reserva

Toda reserva no Dionísio tem um **status** que muda ao longo do tempo — desde o momento em que é criada até quando ela é concluída, cancelada ou tem o pagamento recusado. Entender esses status é essencial para acompanhar o que está acontecendo no salão e configurar corretamente as automações.

## Os 10 status

A reserva pode estar em um dos status abaixo a qualquer momento. A grafia oficial é a da tabela — use-a sempre nos relatórios, nas conversas com o cliente e ao configurar notificações.

| Status                          | Quando acontece                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Pendente**                    | Reserva aguardando aprovação manual. Só existe quando **Confirmação automática** está desligada. |
| **Confirmada**                  | Reserva aprovada, aguardando o dia.                                                              |
| **Sentados**                    | Cliente chegou e está acomodado.                                                                 |
| **Concluída**                   | Reserva encerrada (cliente foi embora).                                                          |
| **Não Compareceu**              | Cliente não apareceu (no-show).                                                                  |
| **Cancelada pelo Cliente**      | Cliente cancelou pelo Link de Gerenciamento da Reserva.                                          |
| **Cancelada pelo Restaurante**  | Equipe cancelou pelo painel.                                                                     |
| **Aguardando Pagamento**        | Reserva paga, aguardando confirmação do adquirente.                                              |
| **Erro ao Processar Pagamento** | Falha genérica no pagamento, geralmente por dados de cartão incorretos.                          |
| **Cartão Recusado**             | Cartão recusado pelo emissor.                                                                    |

## Como uma reserva avança

O caminho mais comum de uma reserva gratuita criada pelo cliente é:

1. A reserva é criada como **Pendente** (ou já como **Confirmada**, se **Confirmação automática** estiver ligada).
2. A equipe do restaurante aprova, levando a reserva para **Confirmada**.
3. No dia, quando o cliente chega, alguém clica em **Marcar como Sentados** no cartão da reserva.
4. Depois que o cliente vai embora, a reserva é encerrada como **Concluída**.

O Dionísio tem **duas regras automáticas** baseadas em tempo que atuam sobre esse caminho:

* **1h após o início da reserva**, se ela ainda está em **Confirmada**, o sistema muda o status sozinho. Para qual lado depende do toggle **Atualização automática de status** (em **Áreas e Mesas** → **Configurações Avançadas**):
  * Com o toggle **ligado**, vai para **Sentados** (assume que o cliente apareceu).
  * Com o toggle **desligado**, vai para **Não Compareceu** (assume no-show).
* **3h após o início**, se a reserva está em **Sentados**, ela vai automaticamente para **Concluída**. Essa transição acontece sempre, independente do toggle.

> ⚠️ **Atenção:** mesmo com **Atualização automática de status** desligado, o sistema continua atualizando — apenas muda o destino para **Não Compareceu** em vez de **Sentados**. Ele não desliga a automação, apenas escolhe o oposto.

Você pode trocar o status de qualquer reserva manualmente editando-a, mesmo depois das transições automáticas.

## Pagamento e o ciclo de status

Quando a reserva é **paga** — Experiência paga ou Área com **Habilitar cobrança** ativo no horário — o caminho é diferente:

1. A reserva é criada em **Aguardando Pagamento**, independente de **Confirmação automática**.
2. Quando o adquirente confirma o pagamento, ela vai para **Confirmada**. A partir daí o ciclo segue normalmente.
3. Se o pagamento falhar, ela vai para um destes dois status terminais — e **não pode ser recuperada**:
   * **Erro ao Processar Pagamento:** falha genérica, geralmente por dados de cartão incorretos.
   * **Cartão Recusado:** o emissor do cartão recusou a operação.

> ℹ️ **Observação:** uma reserva paga sempre vai para **Confirmada** depois do pagamento confirmado, mesmo que **Confirmação automática** esteja desligada. O pagamento é tratado como um sinal mais forte do que a aprovação manual.

## Cancelamento e reagendamento

Uma reserva pode ser cancelada por dois caminhos distintos, e o Dionísio guarda os dois separados — útil para análise e para disparar notificações diferentes:

* **Cancelada pelo Cliente:** o cliente cancela pelo **Link de Gerenciamento da Reserva** que recebeu. Esse caminho exige dois toggles ligados: **Permitir cancelamento pelo cliente** em **Áreas e Mesas** → **Configurações Avançadas** (que controla cancelamento e reagendamento ao mesmo tempo) **e** **Permitir cancelamento de reservas** em **Políticas**.
* **Cancelada pelo Restaurante:** alguém da equipe cancela pelo painel — na Visão Geral, no Calendário ou no Histórico.

Reagendar é diferente de cancelar e criar outra: o cliente (pelo mesmo Link de Gerenciamento, quando o toggle de **Configurações Avançadas** e o **Permitir reagendamento de reservas** em **Políticas** estão ligados) ou a equipe **edita** a reserva existente, mantendo o mesmo ID. O histórico da reserva guarda quem fez a alteração — administrador ou cliente — e o que mudou.

## Onde cada reserva aparece

A **Visão Geral** mostra apenas reservas com data igual ou posterior a hoje, e somente nos seguintes status:

* Na aba **Próximas Reservas:** reservas em **Confirmada** e **Sentados**.
* Na aba **Reservas Pendentes:** reservas em **Pendente** e **Aguardando Pagamento**.

Todo o resto aparece no **Histórico** — tanto reservas com data passada quanto reservas em status terminais: **Concluída**, **Não Compareceu**, ambas formas de **Cancelada**, **Erro ao Processar Pagamento** e **Cartão Recusado**.

## Relacionado

* Operar reservas pela Visão Geral
* Confirmar, sentar, cancelar e Não Compareceu
* Configurações Avançadas de Reserva
* Histórico de Reservas

# Operar reservas pela Visão Geral

A **Visão Geral** é o centro de operação do módulo Reservas — é onde a equipe acompanha as próximas reservas em tempo real, aprova as pendentes e age conforme o cliente vai chegando ou não. Esta página explica o que tem na tela e como navegar. Para criar reservas manualmente, veja Criar uma reserva manualmente. Para mudar o status de uma reserva, veja Confirmar, sentar, cancelar e Não Compareceu.

## Como acessar

No menu lateral, clique em **Reservas** → **Visão Geral**.

## Os dois grupos: Próximas Reservas e Reservas Pendentes

A tela divide as reservas em duas abas:

* **Próximas Reservas:** reservas em **Confirmada** e **Sentados** com data igual ou posterior a hoje. Ordenadas cronologicamente.
* **Reservas Pendentes:** reservas em **Pendente** e **Aguardando Pagamento** com data igual ou posterior a hoje. O número ao lado do nome da aba indica quantas existem.

Reservas em status terminais (**Concluída**, **Não Compareceu**, ambas formas de **Cancelada**, **Erro ao Processar Pagamento**, **Cartão Recusado**) ou com data passada aparecem no Histórico, não aqui.

## Como ler um cartão de reserva

Cada reserva aparece como um cartão com as seguintes informações:

| Informação             | Descrição                                                      |
| ---------------------- | -------------------------------------------------------------- |
| **Horário**            | Hora da reserva.                                               |
| **Nome do cliente**    | Quem fez a reserva.                                            |
| **Badge de status**    | **Pendente**, **Confirmada** ou outro status atual da reserva. |
| **Data e hora**        | Data e hora exatas.                                            |
| **Telefone**           | Número do cliente, usado para contato via WhatsApp.            |
| **Email**              | E-mail do cliente, quando informado.                           |
| **Criada em**          | Data e hora em que a reserva foi registrada.                   |
| **Adultos / Crianças** | Composição do grupo.                                           |
| **Área**               | Área onde a reserva foi feita (ex: "Salão Principal").         |

Para entender o significado de cada status e como passar de um para o outro, veja Ciclo de vida de uma reserva.

## Busca, filtros e visualização

A tela tem três recursos para encontrar e exibir reservas:

* **Barra de busca** no topo: digite parte do nome do cliente para filtrar a lista.
* **Filtros Hora e Data**: clique nos botões **Hora** ou **Data** para filtrar por horário ou data específica.
* **Alternância de visualização**: dois ícones no canto superior direito alternam entre:
  * **Lista** (padrão) — cartões com todos os detalhes.
  * **Grade** — visualização compacta para escanear mais reservas de uma vez.

> 💡 **Dica:** o botão **+ Nova Reserva** no canto superior direito abre o formulário de criação manual. Para o passo a passo, veja Criar uma reserva manualmente.

## Próximos passos

* Confirmar, sentar, cancelar e Não Compareceu
* Criar uma reserva manualmente
* Calendário de Reservas
* Histórico de Reservas

# Criar uma reserva manualmente

Use esta tarefa quando o cliente fala com você pessoalmente, por telefone ou em outro canal que não passa pela IA ou pelo Link de Reservas. Você preenche o formulário com os dados da reserva e do cliente em dois passos.

## Como acessar

O botão **+ Nova Reserva** existe em duas telas:

* **Reservas** → **Visão Geral**
* **Reservas** → **Calendário**

Em qualquer uma delas o formulário é o mesmo.

![No celular: tela Gerenciar Reservas. As abas Próximas Reservas e Reservas Pendentes ficam no topo; o botão + Nova Reserva, destacado com um contorno vermelho, fica fixo no rodapé.](/files/yVt5rL151qVfpg0K6WdW)

![No computador: tela de Reservas na Visão Geral. No menu lateral, Reservas está aberto com Visão Geral selecionada; o botão + Nova Reserva, destacado com um contorno vermelho, fica no topo, à direita do título Gerenciar Reservas. Abaixo dele, as abas Próximas Reservas e Reservas Pendentes e o campo Buscar por nome ou telefone.](/files/gYMW9Jju7XLp5eDL6FfT)

## Passo 1 — Dados da Reserva

| Campo                      | Obrigatório | Descrição                                                                                                                          |
| -------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Experiência (opcional)** | Não         | Experiência vinculada à reserva. Padrão: **Reserva padrão**.                                                                       |
| **Adultos**                | Não         | Já vem preenchido com **1** e não pode ser menor que 1 — ajuste se houver mais adultos. Como já tem valor, você não precisa mexer. |
| **Crianças**               | Não         | Já vem preenchido com **0** — ajuste se houver crianças. Como já tem valor, você não precisa mexer.                                |
| **Data**                   | Sim         | Data desejada.                                                                                                                     |
| **Horário**                | Sim         | Habilita após selecionar a data; as opções vêm dos horários disponíveis da loja.                                                   |
| **Selecione uma área**     | Sim         | Aparece após selecionar data e horário. Mostra apenas áreas com disponibilidade para o slot.                                       |
| **Motivo (opcional)**      | Não         | Ocasião da visita (ex: aniversário, comemoração de trabalho).                                                                      |
| **Observações**            | Não         | Anotações livres para a equipe. Máximo 200 caracteres.                                                                             |

> 💡 **Dica:** se nenhuma área ou nenhum horário aparece, é porque não há configuração de disponibilidade para a data escolhida. Veja Configurar horários e capacidade.

## Passo 2 — Dados do Cliente

Os campos aparecem nesta ordem; o **Telefone** é o primeiro do passo.

| Campo                             | Obrigatório                                      | Descrição                                                                                                                                                                       |
| --------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Telefone**                      | Sim                                              | Primeiro campo do passo. Número com DDD. Usado para contato via WhatsApp e para buscar um cliente já cadastrado (ver observação abaixo).                                        |
| **CPF**                           | Não na reserva gratuita; **Sim** na reserva paga | Documento do cliente. Também busca cliente cadastrado ao ser preenchido. Quando a reserva é paga, o CPF vira obrigatório e o rótulo muda de **CPF (opcional)** para **CPF \***. |
| **Nome**                          | Sim                                              | Primeiro nome do cliente.                                                                                                                                                       |
| **Sobrenome**                     | Sim                                              | Sobrenome do cliente.                                                                                                                                                           |
| **Email (opcional)**              | Não                                              | E-mail do cliente.                                                                                                                                                              |
| **Data de Nascimento (opcional)** | Não                                              | Dia, mês e ano de nascimento, em campos separados.                                                                                                                              |

Depois de preencher, clique em **Finalizar** para criar a reserva. Ela aparece imediatamente nas telas que mostram reservas dela em diante.

> ℹ️ **Observação:** se o cliente já tem cadastro no Dionísio, o sistema busca pelo **Telefone** ou pelo **CPF** e autopreenche os dados — nome, sobrenome, email, CPF e data de nascimento são preenchidos a partir do cadastro. Ao encontrar, mostra **"Cliente encontrado! Dados preenchidos automaticamente."**; quando não encontra, mostra **"Novo cliente será criado com estes dados."**

## Status inicial e dicas

Depois que você clica em **Finalizar**, a reserva nasce com um status que depende do tipo:

* **Reserva gratuita:** criada manualmente, nasce sempre como **Confirmada** — não passa por aprovação.
* **Reserva paga** (Experiência paga ou Área com **Habilitar cobrança** ligado): nasce em **Aguardando Pagamento**, e o sistema gera o link de pagamento para o cliente.

Veja Ciclo de vida de uma reserva para os detalhes de cada status.

> ⚠️ **Atenção:** ao criar uma reserva manual como administrador, o sistema **permite estourar a capacidade** do horário **sem aviso**. Se a capacidade configurada já está cheia, a nova reserva é criada mesmo assim — confira a capacidade antes de finalizar se isso for um problema.

> 💡 **Dica:** se o cliente quer reservar em uma data com **Data Especial** ou **Bloqueio** configurado, ajuste a configuração antes de tentar criar a reserva. O formulário respeita as mesmas regras de disponibilidade do Link de Reservas.

## Próximos passos

* Operar reservas pela Visão Geral
* Confirmar, sentar, cancelar e Não Compareceu
* Ciclo de vida de uma reserva
* Experiências

# Confirmar, sentar, cancelar e Não Compareceu

Cada cartão de reserva no Dionísio traz botões que permitem mudar o status, editar campos e ver o histórico de alterações. As ações disponíveis variam conforme o status atual.

## Onde encontrar essas ações

Os mesmos botões aparecem nos cartões de reserva em três telas:

* **Reservas** → **Visão Geral** (próximas e pendentes)
* **Reservas** → **Calendário** (modo Dia)
* **Reservas** → **Histórico** (reservas passadas)

Algumas ações só aparecem em determinados status — por exemplo, **Confirmar Reserva** só aparece em reservas **Pendente**. Veja Ciclo de vida de uma reserva para o detalhamento dos status.

## Mudar o status da reserva

Quatro botões mudam o status da reserva diretamente pelo cartão.

### Confirmar uma reserva pendente

O botão **Confirmar Reserva** aparece em reservas no status **Pendente**. Ao clicar, a reserva passa para **Confirmada** e o cliente passa a aparecer na aba **Próximas Reservas** da Visão Geral.

> 💡 **Dica:** se você quer que reservas novas já nasçam confirmadas, ligue **Confirmação automática** nas Configurações Avançadas.

### Marcar como Sentados

O botão **Marcar como Sentados** registra que o cliente chegou e está acomodado. Use no momento em que a equipe leva o cliente até a mesa.

A reserva também pode ir para **Sentados** automaticamente — 1h depois do início, se **Atualização automática de status** estiver ligada. Mas marcar manualmente assim que o cliente chega mantém o painel mais preciso para a equipe.

### Marcar como Não Compareceu

O botão **Marcar como Não Compareceu** registra o no-show: o cliente não apareceu. Use quando o tempo passou e ninguém apareceu (ou avisou cancelamento).

A reserva pode ir para **Não Compareceu** automaticamente — 1h depois do início, se **Atualização automática de status** estiver desligada.

> ⚠️ **Atenção:** se a reserva era paga e a sua **Taxa por Não Comparecimento** está configurada, marcar como Não Compareceu **dispara a cobrança** automaticamente. Veja Política de cancelamento e no-show.

### Cancelar uma reserva

O botão **Cancelar Reserva** envia a reserva para **Cancelada pelo Restaurante**.

Se for uma reserva paga com **Política de Cancelamento** configurada, o reembolso ao cliente acontece automaticamente conforme o nível definido para o prazo restante.

> ℹ️ **Observação:** quando o próprio cliente cancela pelo **Link de Gerenciamento da Reserva**, o status registrado é **Cancelada pelo Cliente** (não pelo Restaurante). Os dois caminhos são tratados separadamente para análise e para disparar notificações diferentes.

## Editar uma reserva

Clique no ícone ✏️ no cartão para abrir os **Detalhes da Reserva**. Você pode alterar:

* **Informações do Cliente:** Nome, Sobrenome, Telefone, Email, CPF.
* **Horário:** Data e hora de início e de término.
* **Quantidade de Pessoas:** Adultos e Crianças.
* **Localização:** Área da reserva.
* **Status:** qualquer um dos 10 status possíveis.

Toda alteração fica registrada no histórico da reserva.

## Ver o histórico de alterações da reserva

O botão **Histórico da Reserva** (🕐) abre uma cronologia com todas as alterações feitas na reserva — quando aconteceu, o que mudou e quem fez a mudança (**administrador** ou **cliente**). É a fonte de auditoria para entender o que aconteceu com uma reserva específica.

> 💡 **Dica:** esse histórico individual é diferente do **Histórico de Reservas** (a tela com a lista das reservas passadas). Aqui você vê as alterações de **uma reserva** específica; lá você vê o conjunto das reservas.

## Próximos passos

* Ciclo de vida de uma reserva
* Operar reservas pela Visão Geral
* Política de cancelamento e no-show
* Histórico de Reservas

# Link de Reservas

O **Link de Reservas** é a URL pública do seu restaurante onde clientes fazem reserva por conta própria, sem precisar conversar com a IA ou ligar para a equipe. Existe um único link por estabelecimento, no formato `r.odionisio.com/{slug}`, e ele aceita reservas comuns e Experiências disponíveis.

## Antes de começar

Para o Link de Reservas funcionar e mostrar opções ao cliente, é preciso ter:

* Pelo menos uma **Área ativa** com **horário configurado** para o dia que o cliente está tentando reservar. Veja Criar uma área e Configurar horários e capacidade.
* Capacidade disponível no slot escolhido. Se a capacidade está esgotada, o horário não aparece para o cliente.

## Onde encontrar o link

No menu lateral, clique em **Reservas** → **Áreas e Mesas**. O link aparece no topo da tela, dentro do card **Link de Reservas**, ao lado de um botão de copiar.

Clique no ícone de cópia para copiar o link inteiro. Você pode então enviá-lo pelo WhatsApp, Instagram, Google Meu Negócio, e-mail marketing ou qualquer outro canal.

> 💡 **Dica:** o link é único por estabelecimento — você não precisa criar variantes por área. As Áreas e Experiências disponíveis aparecem automaticamente na hora da reserva.

## Como o cliente faz uma reserva pelo link

Ao acessar o link, o cliente passa por estas etapas:

1. **Escolha o tipo de reserva.** O cliente seleciona entre **Reserva padrão** (mesa comum) ou uma das **Experiências** disponíveis no momento, como "Brunch Dominical" ou "Jantar de Dia dos Namorados". Cada Experiência mostra título, descrição, período e valor.
2. **Escolha data e horário.** O calendário exibe apenas os dias com disponibilidade. Dias sem horários abertos não aparecem no calendário. Da mesma forma, slots sem capacidade não são exibidos.
3. **Informe número de pessoas e dados pessoais.** Os campos pedidos são definidos em **Clientes** → **Configurações Avançadas** (cards "Reservas Gratuitas" e "Reservas Pagas"). **Telefone** e **Nome** são sempre obrigatórios.
4. **Pague (se for o caso).** Em reservas pagas — Experiências ou horários com **Habilitar cobrança** ligado — o cliente escolhe entre **PIX** ou **cartão de crédito** antes de confirmar.
5. **Receba a confirmação.** O cliente recebe o **Link de Gerenciamento da Reserva**, onde poderá depois cancelar ou reagendar (se as políticas e configurações permitirem).

> ℹ️ **Observação:** quando uma reserva é criada pela IA via WhatsApp ou Instagram, ela pré-preenche os dados na etapa de pagamento e envia este mesmo link ao cliente — o pagamento sempre acontece pelo Link de Reservas.

## Personalização visual

O Link de Reservas pode ser personalizado com **cores** e **imagens** que reflitam a identidade do seu estabelecimento. A configuração da identidade visual é feita em outras telas do Dionísio — esta página será atualizada com o caminho exato quando documentarmos a fundo o tema de identidade visual.

> ℹ️ **Observação:** o rastreamento de visitas e conversões do Link de Reservas pode ser integrado a **Facebook Pixel**, **Google Tag Manager** e **Google Analytics**. Os detalhes dessa configuração serão cobertos em documentação dedicada.

## Próximos passos

* Criar uma área
* Configurar horários e capacidade
* Experiências
* Política de cancelamento e no-show

# Áreas e Mesas

A subseção **Áreas e Mesas** centraliza toda a configuração dos espaços físicos do seu restaurante que aceitam reservas. Cada espaço é uma **Área** (Salão Principal, Terraço, Varanda) com seus próprios horários, capacidade, regras de cobrança e configurações avançadas.

Sem pelo menos uma Área ativa com horário configurado, o Link de Reservas não mostra opções aos clientes. Por isso essa é normalmente a primeira tela a configurar quando você começa a usar o módulo.

## O que você pode fazer

* Criar uma área — cadastrar um novo espaço físico (Salão Principal, Terraço, Varanda).
* Configurar horários e capacidade — definir quando a Área aceita reservas, com quantas pessoas e com cobrança ou não.
* Gerenciar uma área existente — navegar pela página de detalhes da Área, editar informações, ativar/inativar, excluir.
* Configurações Avançadas de Reserva — definir as 6 regras globais do módulo (dias de antecedência, confirmação automática, atualização automática de status, etc.).

## Onde acessar

No menu lateral, clique em **Reservas** → **Áreas e Mesas**.

Na tela principal você encontra:

* **Link de Reservas** no topo (URL pública única do restaurante). Detalhes em Link de Reservas.
* Botão **Configurações Avançadas** para abrir o painel com as 6 regras globais.
* Lista de Áreas existentes, cada uma com nome, status, descrição e mini-visualização semanal.
* Botão **+ Criar área de mesa** no canto superior direito.

## Por onde começar

Se você está configurando o módulo Reservas pela primeira vez, siga esta ordem:

1. Crie uma Área (ao menos uma).
2. Configure os horários e capacidade da Área — pelo menos um horário por dia da semana em que o restaurante atende.
3. Ajuste as Configurações Avançadas conforme suas regras de negócio (confirmação automática, dias de antecedência, etc.).
4. Compartilhe o seu Link de Reservas com clientes.

## Conceitos importantes

* **Capacidade compartilhada:** opção que define como a capacidade total de um horário se distribui entre os slots. Tem efeito grande no que o cliente vê — entenda em Configurar horários e capacidade.
* **Tipo de Lotação:** pelo número de pessoas (recomendado) ou pelo número de lugares (exige mapa de mesas). Definido na criação da Área.
* **Status Ativo/Inativo da Área:** Inativa não aparece no Link de Reservas, mas a equipe ainda pode criar reservas manualmente nela.

## Próximos passos

* Operar reservas pela Visão Geral — depois que as Áreas e horários estão prontos.
* Notificações automáticas para o cliente — configure lembretes por Área.
* Políticas e pagamentos — para Experiências pagas e cobrança em horários.

# Configurações Avançadas de Reserva

As **Configurações Avançadas de Reserva** são as 6 regras globais que valem para todas as reservas do estabelecimento — quando o cliente pode reservar, se há aprovação manual ou automática, quando o cliente pode cancelar e se ele precisa informar um motivo. Elas afetam tanto o **Link de Reservas** quanto reservas criadas manualmente.

## Como abrir o painel

No menu lateral, clique em **Reservas** → **Áreas e Mesas**. No topo da tela, clique no botão **Configurações Avançadas**. O painel abre como um popup no centro da tela.

Os campos sempre aparecem juntos — não há condições para mostrar ou esconder nenhum deles.

## Os 6 campos

| Campo                                  | Tipo    | O que faz                                                                                                                                                                                                                                                                                      |
| -------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dias de antecedência**               | Número  | Máximo de dias no futuro que o cliente pode reservar. Ex: 30 significa que hoje o cliente consegue reservar até daqui a 30 dias.                                                                                                                                                               |
| **Horário limite para o mesmo dia**    | Horário | Depois desse horário, o cliente não consegue mais reservar para o próprio dia.                                                                                                                                                                                                                 |
| **Atualização automática de status**   | Toggle  | Decide o destino automático das reservas em **Confirmada** 1h após o início. Veja a explicação abaixo.                                                                                                                                                                                         |
| **Confirmação automática**             | Toggle  | Quando ligado, novas reservas gratuitas nascem em **Confirmada**. Quando desligado, nascem em **Pendente** e precisam de aprovação manual.                                                                                                                                                     |
| **Permitir cancelamento pelo cliente** | Toggle  | Liga ou desliga **ao mesmo tempo** a possibilidade de o cliente cancelar e reagendar pelo **Link de Gerenciamento da Reserva**. Funciona em conjunto com os toggles individuais em **Políticas** — o cliente só vê os botões quando este toggle e o correspondente de Políticas estão ligados. |
| **Exigir motivo da reserva**           | Toggle  | Quando ligado, o campo **Motivo** vira obrigatório na criação manual e no Link de Reservas.                                                                                                                                                                                                    |

Após ajustar os campos, clique em **Salvar**.

## Como a Atualização automática de status funciona

O toggle **Atualização automática de status** tem um comportamento não-óbvio: mesmo **desligado**, o sistema continua atualizando o status automaticamente — ele apenas muda **para qual destino**.

* Com o toggle **ligado**, uma reserva em **Confirmada** vira **Sentados** automaticamente 1h após o início (assume que o cliente apareceu).
* Com o toggle **desligado**, a mesma reserva vira **Não Compareceu** 1h após o início (assume no-show).

A transição automática 3h depois para **Concluída** (a partir de **Sentados**) acontece sempre, independente desse toggle.

> 💡 **Dica:** se a sua equipe **sempre** marca Sentados ou Não Compareceu manualmente assim que o cliente chega ou some, escolha o destino que represente o caso mais comum. Em restaurantes onde a maioria dos clientes aparece, ligar o toggle dá menos trabalho de correção depois.

## Sobre Confirmação automática e reservas pagas

**Confirmação automática** atua apenas em reservas gratuitas. **Reservas pagas** seguem regra própria: nascem sempre em **Aguardando Pagamento** e vão para **Confirmada** depois do pagamento confirmado pelo adquirente, independente desse toggle.

## Relacionado

* Ciclo de vida de uma reserva
* Configurar horários e capacidade
* Política de cancelamento e no-show
* Política de reagendamento

# Criar uma área

Uma **Área** é um espaço físico do seu restaurante que aceita reservas — pode ser o salão principal, um terraço, uma varanda ou um salão privativo. Criar uma área é o primeiro passo para começar a receber reservas naquele espaço. Depois de criar, você precisa configurar os horários disponíveis.

## Como acessar

No menu lateral, clique em **Reservas** → **Áreas e Mesas**. No canto superior direito da tela, clique em **+ Criar área de mesa**.

## Passos

1. Clique em **+ Criar área de mesa**.
2. Preencha os campos do formulário (descritos na seção abaixo).
3. Escolha o **Tipo de Lotação**.
4. Clique em **Finalizar**.

A nova área aparece na lista de áreas. Para que ela aceite reservas, configure horários — veja Configurar horários e capacidade.

## Campos do formulário

| Campo               | Obrigatório | Descrição                                                                                                                                                                                                                                                                |
| ------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Nome da Área**    | Sim         | Como a área será exibida (até 50 caracteres). Ex: "Salão Principal", "Terraço", "Varanda".                                                                                                                                                                               |
| **Imagens da área** | Não         | Fotos do ambiente que aparecem no Link de Reservas. JPG ou PNG, máx. 5 MB por imagem.                                                                                                                                                                                    |
| **Descrição**       | Sim         | Breve texto que aparece para o cliente no Link de Reservas (até 200 caracteres).                                                                                                                                                                                         |
| **Status**          | —           | **Ativo** por padrão. **Inativo** oculta a área do Link de Reservas, mas a equipe continua podendo registrar reservas manualmente nela — útil para espaços como salão de eventos, em que você não quer exposição pública mas ainda quer controlar reservas internamente. |
| **Tipo de Lotação** | Sim         | Define como a capacidade é calculada. Detalhes na próxima seção.                                                                                                                                                                                                         |

## Tipo de Lotação

Você escolhe entre duas modalidades de capacidade:

* **Lotação pelo número de pessoas** *(recomendado)*: a capacidade é definida pelo total de pessoas no espaço. Você não precisa montar um mapa de mesas. É a opção mais simples e cobre a maioria dos casos.
* **Lotação pelo número de lugares**: a capacidade é calculada por lugar, e você precisa montar um mapa de mesas. Nesse modo, o cliente vê o mapa no Link de Reservas e escolhe a mesa desejada.

> ℹ️ **Observação:** quando o **Tipo de Lotação** é **Lotação pelo número de lugares**, a página de detalhes da área ganha uma terceira aba **Mapa de Mesas** para configurar o layout. A documentação detalhada dessa modalidade será publicada em página separada.

## Próximos passos

* Configurar horários e capacidade
* Gerenciar uma área existente
* Configurações Avançadas de Reserva

# Gerenciar uma área existente

Cada **Área** criada tem uma página própria de detalhes onde você visualiza a disponibilidade semanal, configura horários, edita informações ou exclui a área inteira. Esta página explica a navegação geral; a configuração detalhada de horários e capacidade é coberta em página separada.

## Como acessar e o que tem na página

No menu lateral, clique em **Reservas** → **Áreas e Mesas**. Em seguida, clique no **nome da área** que você quer gerenciar.

Você cai na página de detalhes da área, com:

* **Trilha de navegação** no topo: **Áreas** / **\[Nome da Área]**.
* **Indicador de status** (bolinha verde para Ativa, vermelha para Inativa) ao lado do nome.
* **Ícones ✏️ Editar e 🗑️ Excluir** ao lado do nome.
* **Toggle Ativo/Inativo** no canto superior direito.
* **Duas abas:** **Semana** e **Horários**.

Quando o **Tipo de Lotação** é **Lotação pelo número de lugares**, uma terceira aba **Mapa de Mesas** aparece para configurar o layout (não coberta nesta página).

## Aba Semana — disponibilidade semanal

A aba **Semana** mostra o painel **Disponibilidade Semanal**, com um card para cada dia da semana (Domingo a Sábado). Cada card exibe:

* Status do dia (**Aberto** ou **Fechado**) para reservas.
* Os horários configurados (ex: "18:00 — 22:50").
* Botão **+ Adicionar** para incluir um horário novo no dia.

Esta aba é uma visualização rápida da semana. Para criar, editar ou apagar horários em detalhe, use a aba **Horários** — veja Configurar horários e capacidade.

## Editar informações da área

Clique no ícone **✏️** ao lado do nome da área. Você pode alterar:

* **Nome da Área**
* **Imagens da área**
* **Descrição**

Os campos seguem as mesmas regras de Criar uma área.

## Ativar, desativar ou excluir

**Ativar ou desativar** uma área usa o toggle **Ativo** no canto superior direito.

* **Ativa:** a área aparece no Link de Reservas e aceita reservas tanto manuais quanto pelo cliente.
* **Inativa:** a área não aparece no Link de Reservas. A equipe ainda pode criar reservas manualmente nela — útil para espaços como salão de eventos em que o cliente não deve ter acesso direto.

**Excluir** uma área usa o ícone **🗑️** ao lado do nome.

> ⚠️ **Atenção:** excluir uma área é uma ação permanente e **não exibe alerta de confirmação**. Reservas confirmadas naquela área **ficam órfãs** — elas continuam existindo na base, mas sem área associada. Antes de excluir, **cancele ou transfira** as reservas existentes.

> 💡 **Dica:** se você só quer parar de receber reservas temporariamente, **desative** em vez de excluir. Desativar preserva a área e o histórico para reativação futura.

## Próximos passos

* Configurar horários e capacidade
* Configurações Avançadas de Reserva
* Criar uma área

# Configurar horários e capacidade

Cada **Área** define **quando** aceita reservas e **com quanta gente** por meio de **horários** configurados dentro dela. Um horário pode rodar em um ou mais dias da semana, ter capacidade própria, cobrança própria e regras avançadas de antecedência e intervalo entre slots.

## Como acessar

No menu lateral, clique em **Reservas** → **Áreas e Mesas** → clique no **nome da área** → abra a aba **Horários**.

A aba mostra um seletor com os dias da semana (Dom até Sáb). Selecione um dia para ver os horários cadastrados nele. Cada horário aparece como um card com a faixa horária (ex: "18:00 — 22:50") e badges resumindo as configurações principais (ex: **Gratuito**, **1 - 30 pessoas**, **Escala 10min**).

Use o botão **+ Adicionar Horário** para criar um novo, ou os ícones **✏️** e **🗑️** no card para editar ou apagar um existente.

## Criar um horário

Clique em **+ Adicionar Horário**. O formulário tem 4 blocos.

### Dias da semana e horário

| Campo                   | Descrição                                                                                 |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| **Dias da semana**      | Marque um ou mais dias em que esse horário vale (ex: só fim de semana, ou toda a semana). |
| **Horários de Reserva** | Hora de início e hora de fim do período de funcionamento (ex: 18:00 às 22:30).            |

### Capacidade

| Campo                               | Descrição                                                                                                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Capacidade total**                | Número máximo de pessoas atendidas dentro deste horário. Veja a seção **Capacidade compartilhada** abaixo para entender como esse total é distribuído. |
| **Mínimo de pessoas**               | Menor número de pessoas aceito por reserva.                                                                                                            |
| **Máximo de pessoas**               | Maior número de pessoas aceito por reserva.                                                                                                            |
| **Capacidade por Tamanho do Grupo** | Opcional. Define vagas específicas por faixa de tamanho de grupo (ex: até 3 reservas de grupos de 6+ pessoas por slot).                                |

### Pagamento

Use o toggle **Habilitar cobrança** quando quiser cobrar antecipadamente pela reserva. Quando ligado, aparecem campos extras:

| Campo                | Descrição                                                                                |
| -------------------- | ---------------------------------------------------------------------------------------- |
| **Tipo de cobrança** | **Por pessoa** (cobra por cabeça) ou **Valor fixo** (cobra um valor único pela reserva). |
| **Valor**            | Valor em reais a ser cobrado.                                                            |

> ℹ️ **Observação:** para que a cobrança chegue à sua conta, é preciso ter o recebimento configurado. Veja Configurar recebimento de reservas pagas.

### Configurações Avançadas

| Campo                            | Descrição                                                                                                                             |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Tempo mínimo de antecedência** | Quantos minutos ou horas antes do horário a reserva ainda pode ser feita. Ex: 60 minutos impede reservas para os próximos 60 minutos. |
| **Intervalo de tempo (minutos)** | Espaçamento entre os slots disponíveis. Ex: 30 minutos cria slots 19:00, 19:30, 20:00, 20:30...                                       |
| **Capacidade compartilhada**     | Define como a **Capacidade total** é distribuída entre os slots. Veja a explicação abaixo.                                            |

Depois de preencher os 4 blocos, clique em **Salvar Horário**.

## Capacidade compartilhada

O toggle **Capacidade compartilhada** (marcado como **Recomendado** no produto) muda o significado da **Capacidade total** do horário. É o conceito mais importante de capacidade no Dionísio — vale a pena entender bem antes de configurar.

**Exemplo:** janela de 19:00 às 22:00, intervalo de 30 minutos, **Capacidade total** 30.

* **Com Capacidade compartilhada ligada** *(recomendado)*: as 30 pessoas se distribuem entre **todos os slots** somados. Se 20 pessoas reservaram às 19:00, sobram 10 para os outros slots (19:30, 20:00, 20:30, 21:00, 21:30, 22:00). O último slot disponível para o cliente é **22:00**.
* **Com Capacidade compartilhada desligada**: cada slot tem **sua própria capacidade total** de 30 pessoas. Os slots não se afetam: 30 às 19:00, mais 30 às 19:30, e assim por diante. O último slot disponível para o cliente é **21:30**.

Na prática, **Capacidade compartilhada** ligada é a forma mais natural de pensar capacidade ("posso atender 30 pessoas a noite inteira"). Desligada é útil quando os slots têm rotatividade real e cada um deve ser tratado como um turno independente.

## Editar ou apagar horários existentes

Os ícones **✏️** e **🗑️** em cada card de horário permitem editar ou remover. Editar abre o mesmo modal de criação, com os campos preenchidos.

> ⚠️ **Atenção:** quando você **remove** um horário (ou muda os horários de funcionamento) e há **reservas confirmadas** dentro do horário removido, as reservas **permanecem** agendadas — não são canceladas automaticamente. Porém, elas **não contam mais para o cálculo de capacidade**. Para evitar confusão, **cancele ou transfira** as reservas antes de mexer no horário, ou ajuste-as manualmente depois.

## Próximos passos

* Criar uma área
* Gerenciar uma área existente
* Configurar recebimento de reservas pagas
* Experiências

# Experiências

Use **Experiências** para reservas paralelas a um evento ou formato específico do seu restaurante — com data, horário, capacidade e cobrança configurados de forma independente das reservas padrão. Exemplos: jantar especial de Dia dos Namorados, Brunch Dominical fixo, noite temática, harmonização com vinhos.

Toda Experiência é **paga** — não existe Experiência gratuita. A Experiência tem capacidade **própria**, que **não soma** com a capacidade das reservas padrão do mesmo dia. Na prática, criar uma Experiência **aumenta a capacidade efetiva** do dia: 30 lugares de Reserva padrão + 20 lugares de Experiência = 50 atendimentos possíveis.

## Como acessar e filtrar

No menu lateral, clique em **Reservas** → **Experiências**.

Na tela principal, use as abas para filtrar:

* **Todas** — exibe Experiências ativas e inativas.
* **Temporárias** — apenas as de período específico.
* **Permanentes** — apenas as recorrentes.

Use a **barra de busca** e o botão **Filtros** para localizar rapidamente por nome, período ou status.

## Tipos: Temporária e Permanente

Toda Experiência é de um dos dois tipos:

* **Temporária:** ocorre em uma data ou período específico. Exemplo: "Jantar de Natal — 24/12". Após a data, encerra automaticamente.
* **Permanente:** ocorre de forma recorrente. Exemplo: "Brunch Dominical" ou "Happy Hour de Sexta". Permanece ativa indefinidamente.

## Criar uma Experiência

Clique em **+ Criar experiência**. O formulário tem 4 passos.

### Passo 1 — Informações Básicas

| Campo                    | Obrigatório | Descrição                                                                            |
| ------------------------ | ----------- | ------------------------------------------------------------------------------------ |
| **Título**               | Sim         | Nome da Experiência. Aparece para o cliente no Link de Reservas. Máx. 50 caracteres. |
| **Descrição**            | Não         | Breve texto sobre a Experiência. Máx. 200 caracteres.                                |
| **Regras e Informações** | Não         | Regras ou informações adicionais para o cliente. Máx. 500 caracteres.                |
| **Tipo**                 | Sim         | **Temporária** ou **Permanente**.                                                    |

### Passo 2 — Configurações

**Áreas de Mesa.** Selecione uma ou mais Áreas disponíveis para esta Experiência. Para cada Área, você define a capacidade específica da Experiência (independente da capacidade configurada nos horários da Área).

**Período (apenas para Temporária):**

| Campo                  | Obrigatório | Descrição                                            |
| ---------------------- | ----------- | ---------------------------------------------------- |
| **Data de Início**     | Sim         | Primeiro dia em que a Experiência estará disponível. |
| **Data de Término**    | Sim         | Último dia do período.                               |
| **Horário de Início**  | —           | Hora de início diária.                               |
| **Horário de Término** | —           | Hora de encerramento diária.                         |

> ⚠️ **Atenção:** o horário configurado é aplicado igualmente a todos os dias do período. Para horários diferentes por dia, crie Experiências separadas.

**Escala de Tempo (minutos)** *(obrigatório)*. Intervalo entre os slots disponíveis. Padrão: 30 minutos → 19:00, 19:30, 20:00...

**Tamanho da Reserva:**

| Campo                 | Descrição                        |
| --------------------- | -------------------------------- |
| **Mínimo de pessoas** | Menor número aceito por reserva. |
| **Máximo de pessoas** | Maior número aceito por reserva. |

**Janelas de Chegada e Permanência:**

| Campo                  | Descrição                                                      |
| ---------------------- | -------------------------------------------------------------- |
| **Chegada antecipada** | Quanto tempo antes do horário o cliente pode chegar.           |
| **Chegada tardia**     | Quanto tempo após o horário o cliente ainda pode ser recebido. |
| **Permanência máxima** | Tempo máximo de permanência após o término do slot.            |

### Passo 3 — Pagamento

O passo de pagamento é **obrigatório** — toda Experiência tem cobrança.

| Campo                     | Obrigatório | Descrição                                                                                                        |
| ------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------- |
| **Tipo de Pagamento**     | Sim         | **Por pessoa** (cobra por cabeça) ou **Valor fixo** (cobra um valor único pela reserva).                         |
| **Valor**                 | Sim         | Valor em R$ a ser cobrado.                                                                                       |
| **Pagamento como caução** | —           | Toggle. Quando ativo, o valor é **reembolsável se o cliente comparecer**. Funciona como garantia contra no-show. |
| **Regras de Pagamento**   | Não         | Condições informadas ao cliente. Máx. 300 caracteres.                                                            |

> ℹ️ **Observação:** para receber o valor das reservas pagas, é preciso ter o recebimento configurado.

### Passo 4 — Revisão

Confira o resumo completo da configuração. Você pode editar qualquer seção antes de finalizar. Clique em **Finalizar** para salvar.

## Como aparece para o cliente

No Link de Reservas, o cliente vê as Experiências ativas como **alternativa à Reserva padrão** na primeira tela ("Como você quer reservar?"). Cada Experiência mostra título, descrição, período e valor antes de o cliente confirmar.

> 💡 **Dica:** mantenha título e descrição claros e atrativos — é o que o cliente vê na hora de escolher entre uma Experiência e uma reserva comum.

## Próximos passos

* Datas Especiais
* Bloqueios
* Configurar recebimento de reservas pagas
* Ciclo de vida de uma reserva

# Datas Especiais

Use **Datas Especiais** para aplicar configurações de horário diferentes em dias específicos do ano — feriados, datas comemorativas ou qualquer dia em que o funcionamento do restaurante mude. Por exemplo: em um feriado nacional você reduz os horários disponíveis, ou em um dia de evento abre um salão normalmente fechado.

A Data Especial é uma **regra de exceção** — ela não cria reservas nem bloqueia o dia. Apenas **substitui a configuração de horário** da Reserva padrão daquele dia, sobrepondo a configuração semanal normal da Área. Experiências ativas no mesmo dia continuam intactas com suas próprias configurações.

> 💡 **Dica:** se você quer **impedir reservas** em um dia, use o módulo Bloqueios. Datas Especiais é para **alterar os horários disponíveis** mantendo o dia aberto.

## Como acessar

No menu lateral, clique em **Reservas** → **Datas Especiais**.

## Criar uma Data Especial

Clique em **+ Criar data especial**. O formulário tem 3 passos.

### Passo 1 — Informações Básicas

| Campo         | Obrigatório | Descrição                                                                                        |
| ------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| **Data**      | Sim         | O dia em que a configuração especial será aplicada.                                              |
| **Status**    | —           | **Ativa** ou **Inativa**. Apenas Datas Especiais ativas substituem a configuração normal.        |
| **Descrição** | Não         | Texto de identificação para sua referência interna. Ex: "Feriado Nacional". Máx. 200 caracteres. |

### Passo 2 — Configurações de Horário

Neste passo você define **quais configurações de horário** serão aplicadas nessa data.

O sistema exibe as configurações de horário já existentes nas suas Áreas. Selecione as que devem valer naquele dia.

Se nenhuma configuração adequada existir, clique em **+ Nova Configuração de Horário** para criar uma específica para essa data.

> 💡 **Dica:** se você quer que um feriado funcione com horário reduzido, crie previamente uma configuração de horário com esse horário em **Áreas e Mesas** e selecione-a aqui. Veja Configurar horários e capacidade.

### Passo 3 — Revisão

Confira os dados antes de salvar: a data, as Áreas afetadas e as configurações de horário selecionadas. Clique em **Finalizar** para salvar.

## Gerenciar Datas Especiais existentes

Na tela principal, cada Data Especial mostra: descrição, status (**Ativa** ou **Inativa**), data exata, número de configurações aplicadas e Áreas afetadas.

Use as abas **Todas**, **Ativas** e **Inativas** para filtrar a visualização.

Você pode **editar** uma Data Especial a qualquer momento (incluindo a data em si), **desativá-la** pelo status sem excluir, ou **excluí-la** quando não for mais necessária.

## Próximos passos

* Bloqueios
* Configurar horários e capacidade
* Experiências
* Ciclo de vida de uma reserva

# Bloqueios

Use **Bloqueios** para impedir que reservas sejam feitas em períodos específicos — seja um dia inteiro, uma faixa de horário ou um conjunto de dias. Bloqueios são úteis para férias, reformas, eventos privados ou qualquer situação em que o espaço não esteja disponível para reservas comuns.

## Como acessar

No menu lateral, clique em **Reservas** → **Bloqueios**.

## Bloqueio, Data Especial e Experiência: quando usar cada um

Os três conceitos parecem próximos, mas resolvem situações diferentes:

|                                  | Bloqueio                                            | Data Especial                                                                    | Experiência                                                |
| -------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **O que faz**                    | Impede novas reservas no período.                   | Substitui os horários disponíveis no dia.                                        | Oferece uma reserva paralela paga, com capacidade própria. |
| **Quando usar**                  | O espaço está indisponível.                         | O horário muda, mas o dia continua aberto.                                       | Você quer vender um evento ou formato especial.            |
| **Cancela reservas existentes?** | Não. Reservas já confirmadas no período permanecem. | Não. As reservas existentes mantêm a configuração da época em que foram criadas. | Não se aplica.                                             |

## Criar um Bloqueio

Clique em **+ Criar bloqueio**. O formulário tem 4 passos.

### Passo 1 — Informações Básicas

| Campo               | Obrigatório | Descrição                                                                               |
| ------------------- | ----------- | --------------------------------------------------------------------------------------- |
| **Título do Bloco** | Sim         | Nome para identificar o Bloqueio. Ex: "Evento Privado — Dezembro". Máx. 100 caracteres. |
| **Descrição**       | Não         | Informação adicional para referência interna. Máx. 200 caracteres.                      |
| **Status**          | —           | **Ativo** ou **Inativo**. Apenas Bloqueios ativos impedem reservas.                     |

### Passo 2 — Programação

Defina o período em que o Bloqueio estará ativo:

| Campo                    | Obrigatório                  | Descrição                                              |
| ------------------------ | ---------------------------- | ------------------------------------------------------ |
| **Data de Início**       | Sim                          | Primeiro dia do Bloqueio.                              |
| **Data de Término**      | Sim                          | Último dia do período.                                 |
| **Bloquear Dia Inteiro** | —                            | Quando ativado, o Bloqueio cobre 24 horas de cada dia. |
| **Horário de Início**    | Sim (se não for dia inteiro) | Hora de início do Bloqueio diário.                     |
| **Horário de Término**   | Sim (se não for dia inteiro) | Hora de encerramento do Bloqueio diário.               |

> 💡 **Dica:** para bloquear apenas o período noturno durante uma semana, defina as datas de início e término, desative **Bloquear Dia Inteiro** e configure o horário de, por exemplo, 18:00 às 23:59.

### Passo 3 — Áreas

Selecione quais Áreas serão afetadas pelo Bloqueio.

Você também pode ativar o **Bloqueio de Experiências** — quando habilitado, o Bloqueio impede também reservas de Experiências nas Áreas selecionadas. Sem este toggle, o Bloqueio impede apenas reservas padrão; Experiências continuam abertas no período.

### Passo 4 — Revisão

Confirme as informações antes de salvar: título, status, período, horário e Áreas afetadas. Clique em **Finalizar** para salvar.

## Gerenciar Bloqueios existentes

Cada Bloqueio na lista mostra título, status (**Ativo** ou **Inativo**), período de início e término e Áreas afetadas. Use os botões **Editar** e **Excluir** em cada item para fazer alterações ou remover.

> ⚠️ **Atenção:** criar um Bloqueio **não cancela automaticamente** as reservas que já existem para aquele período. Se necessário, cancele as reservas manualmente pela tela de **Visão Geral**.

## Próximos passos

* Datas Especiais
* Experiências
* Configurar horários e capacidade
* Ciclo de vida de uma reserva

# Calendário

O **Calendário** oferece uma visualização gráfica de todas as reservas do estabelecimento, organizada por data. É útil para ter uma visão rápida do volume de reservas, identificar dias cheios e exportar listas para a equipe de recepção.

## Como acessar

No menu lateral, clique em **Reservas** → **Calendário**.

## Modos de visualização

No topo da tela você alterna entre três modos:

* **Mês** — exibe o mês completo em grade. Cada dia mostra o total de reservas, adultos e crianças.
* **Semana** — exibe os 7 dias da semana atual em formato de linha do tempo.
* **Dia** — exibe as reservas de um dia específico com todos os detalhes.

Use as setas de navegação para avançar ou retroceder entre períodos, ou clique em **Voltar para hoje** para retornar à data atual.

### Lendo o modo Mês

Cada célula de dia no modo Mês mostra:

| Informação             | O que significa                                |
| ---------------------- | ---------------------------------------------- |
| Ícone de confirmação   | Há reservas confirmadas no dia.                |
| Quantidade de reservas | Total de reservas para a data.                 |
| Adultos                | Total de adultos.                              |
| Crianças               | Total de crianças (aparece somente se houver). |

Clique em um dia para ver as reservas daquele dia no modo Dia.

## Filtros

Clique em **Filtros** para refinar quais reservas aparecem no Calendário:

| Filtro                  | Descrição                                                                                                                                                                                                                                      |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status das reservas** | Filtra por status (**Pendente**, **Confirmada**, **Sentados**, **Concluída**, **Não Compareceu**, **Cancelada pelo Cliente**, **Cancelada pelo Restaurante**, **Aguardando Pagamento**, **Erro ao Processar Pagamento**, **Cartão Recusado**). |
| **Tamanho**             | Filtra pelo número de pessoas da reserva.                                                                                                                                                                                                      |
| **Área**                | Filtra por Área específica.                                                                                                                                                                                                                    |
| **Motivo**              | Filtra pelo motivo da reserva (ex: aniversário).                                                                                                                                                                                               |
| **Horário exato**       | Exibe reservas de um horário específico.                                                                                                                                                                                                       |
| **Antes de / Após**     | Exibe reservas antes ou depois de um determinado horário.                                                                                                                                                                                      |

Clique em **Limpar** para remover todos os filtros ativos.

## Exportar PDF e criar reservas

O botão **Exportar PDF** gera um arquivo com a lista de reservas conforme os filtros ativos no momento. Útil para imprimir a lista do dia para a equipe de recepção.

O botão **+ Nova Reserva** no topo do Calendário abre o mesmo formulário de criação manual disponível na Visão Geral. Veja Criar uma reserva manualmente para o passo a passo.

## Próximos passos

* Operar reservas pela Visão Geral
* Criar uma reserva manualmente
* Confirmar, sentar, cancelar e Não Compareceu
* Histórico de Reservas

# Notificações

**Notificações** são mensagens automáticas enviadas para os clientes via WhatsApp em momentos específicos da reserva — um lembrete dias antes, uma confirmação de chegada, um aviso de cancelamento. Cada Área do estabelecimento pode ter suas próprias configurações de notificação independentes.

> ⚠️ **Atenção:** as notificações são enviadas via WhatsApp. Para que funcionem, o número de WhatsApp do estabelecimento precisa estar conectado e ativo. Confira em **WhatsApp** → **Conectar WhatsApp**.

## Como acessar

No menu lateral, clique em **Reservas** → **Notificações**.

## Tipos de Notificação

Você pode configurar três tipos de notificação, e cada Área pode ter quantos quiser de cada tipo.

| Tipo                  | Quando é enviada                    | Exemplo de uso                                            |
| --------------------- | ----------------------------------- | --------------------------------------------------------- |
| **Recorrente**        | Um tempo definido antes da reserva. | "Lembre o cliente 3 dias antes do jantar."                |
| **Agendada**          | Em um horário fixo do dia.          | "Envie uma mensagem às 18h do dia da reserva."            |
| **Mudança de Status** | Quando o status da reserva muda.    | "Notifique quando a reserva for confirmada ou cancelada." |

> 💡 **Dica:** cada tipo cria uma configuração separada. Você pode ter, por exemplo, uma Recorrente (lembrete 3 dias antes) e uma de Mudança de Status (confirmação) para a mesma Área.

## Criar uma Notificação

Clique em **+ Nova Notificação**. O formulário tem 3 passos.

### Passo 1 — Tipo de Notificação

O sistema informa para qual Área você está configurando. Em seguida:

* Ative o toggle **Ativar notificações para esta área**.
* Selecione o tipo: **Recorrente**, **Agendada** ou **Mudança de Status**.

### Passo 2 — Configuração da Mensagem

Os campos variam conforme o tipo escolhido no Passo 1.

**Para Recorrente:**

| Campo           | Descrição                                                      |
| --------------- | -------------------------------------------------------------- |
| **Tempo antes** | Número de dias, horas ou minutos antes da reserva para enviar. |
| **Unidade**     | Dias, Horas ou Minutos.                                        |
| **Mensagem**    | Texto que será enviado ao cliente.                             |

**Para Agendada:** configure o horário fixo do dia em que a mensagem será enviada e o texto.

**Para Mudança de Status:** configure qual mudança dispara a mensagem (confirmação, cancelamento, etc.) e o texto correspondente.

**Variáveis disponíveis na mensagem:**

Use as tags abaixo para personalizar com os dados reais da reserva:

| Tag             | Substituída por             |
| --------------- | --------------------------- |
| `{nome}`        | Nome do cliente             |
| `{data}`        | Data da reserva             |
| `{hora}`        | Horário da reserva          |
| `{restaurante}` | Nome do seu estabelecimento |

**Exemplo:** *"Tudo certo, {nome}! Sua reserva em {restaurante} para o dia {data} às {hora} está confirmada. Aguardamos você!"*

### Passo 3 — Revisão

Confira o resumo: tipo de notificação, status, tempo de envio e o texto da mensagem. Clique em **Finalizar** para salvar.

## Gerenciar notificações existentes

Cada notificação na lista mostra o tipo (Recorrente, Agendada ou Mudança de Status), o status (**Ativa** ou **Inativa**), a Área a que pertence e o momento de envio.

As ações disponíveis em cada item são:

* **Editar** — alterar qualquer configuração.
* **Duplicar** — cria uma cópia (útil para criar variações rapidamente).
* **Excluir** — remove a notificação permanentemente.

## Notificações padrão e email ao operador

O Dionísio dispara automaticamente algumas mensagens **mesmo sem configuração visível** na tela de Notificações:

* **Notificações de Mudança de Status padrão** já existem no backend para os status **Pendente**, **Confirmada**, **Cancelada pelo Cliente** e **Cancelada pelo Restaurante** (as duas formas de Cancelada usam a mesma mensagem). Disparam mesmo sem nada configurado por você.
* **Email ao operador** é enviado automaticamente quando uma reserva é criada ou cancelada — útil para a equipe acompanhar movimentações sem precisar abrir o painel toda hora.

> ℹ️ **Observação sobre custo:** quando o WhatsApp está conectado pela API oficial da Meta, o restaurante paga diretamente à Meta pelas mensagens enviadas, com o cartão cadastrado lá. Quando está pela conexão extraoficial (WhatsApp Web), o envio é gratuito, mas com risco de banimento da conta. Se um template Meta falhar no envio, o Dionísio reenvia a mensagem automaticamente pelo número oficial dele próprio, usando o texto padrão da plataforma.

## Próximos passos

* Ciclo de vida de uma reserva
* Configurar horários e capacidade
* Confirmar, sentar, cancelar e Não Compareceu

# Histórico

O **Histórico** reúne todas as reservas que já saíram da operação ativa do salão — concluídas, canceladas, com no-show ou com problemas de pagamento. Diferente da Visão Geral (que mostra reservas futuras e pendentes), o Histórico é o registro permanente do que já aconteceu, útil para consultas, acompanhamento de clientes recorrentes, análise de volume e exportação para análise externa.

## Como acessar

No menu lateral, clique em **Reservas** → **Histórico**.

## Consultar reservas no Histórico

Use os recursos da tela em três etapas.

### Defina o período

Ao abrir o Histórico, defina o intervalo que você quer consultar usando os campos **Data Inicial** e **Data Final**. Para agilizar, use os atalhos rápidos:

| Atalho              | Período carregado    |
| ------------------- | -------------------- |
| **Última Semana**   | Os últimos 7 dias.   |
| **Último Mês**      | Os últimos 30 dias.  |
| **Últimos 3 Meses** | Os últimos 90 dias.  |
| **Último Ano**      | Os últimos 365 dias. |

### Use a busca e filtros

Use a **barra de busca** para localizar reservas por nome do cliente, e o botão **Filtros** para refinar por Área, tamanho do grupo, motivo e horário.

### Visualize os cartões

As reservas são exibidas no mesmo formato de cartão da Visão Geral, com: nome do cliente, data, horário, número de pessoas, Área e status.

Use o botão de alternância no topo para mudar entre a visualização em **grade** e em **lista**.

> 💡 **Dica:** se nenhuma reserva for encontrada no período selecionado, a tela exibe a mensagem: *"Nenhuma reserva no histórico."*

## Exportar para Excel

O Histórico tem um botão de **Exportar para Excel** que gera uma planilha com todas as reservas dentro do período e filtros ativos. A planilha contém 24 colunas:

| Coluna                    | Descrição                                                  |
| ------------------------- | ---------------------------------------------------------- |
| **ID**                    | Identificador único da reserva.                            |
| **Cliente**               | Nome do cliente.                                           |
| **Telefone**              | Telefone do cliente.                                       |
| **Email**                 | Email do cliente.                                          |
| **CPF**                   | CPF do cliente.                                            |
| **Data de Nascimento**    | Data de nascimento do cliente.                             |
| **Status**                | Status atual da reserva.                                   |
| **Data**                  | Data da reserva.                                           |
| **Hora Início**           | Hora de início da reserva.                                 |
| **Hora Fim**              | Hora de término da reserva.                                |
| **Área**                  | Área da reserva.                                           |
| **Mesa**                  | Mesa selecionada (quando o Tipo de Lotação é por lugares). |
| **Adultos**               | Quantidade de adultos.                                     |
| **Crianças**              | Quantidade de crianças.                                    |
| **Total Pessoas**         | Soma de adultos e crianças.                                |
| **Descrição**             | Observações da reserva.                                    |
| **Pagamento Obrigatório** | Se a reserva exigia pagamento (Sim/Não).                   |
| **Método de Pagamento**   | PIX ou cartão de crédito.                                  |
| **Valor**                 | Valor cobrado.                                             |
| **Pagamento Repassado**   | Se o valor já foi repassado para a conta cadastrada.       |
| **Criado em**             | Data e hora em que a reserva foi registrada.               |
| **Atualizado em**         | Data e hora da última alteração.                           |
| **Criado por IA**         | Se a reserva foi criada pela IA (Sim/Não).                 |
| **Motivo**                | Motivo informado pelo cliente.                             |

> 💡 **Dica:** use a exportação para auditar pagamentos, calcular taxa de no-show por período, identificar clientes recorrentes ou levar dados para o seu sistema contábil. Aplique filtros antes de exportar para reduzir o tamanho da planilha.

## Ações disponíveis no Histórico

Mesmo em reservas passadas, é possível realizar ações pelos botões do cartão:

* **Confirmar Reserva** (caso ainda esteja em status diferente de **Confirmada**).
* **Marcar como Sentados** — registra que o grupo chegou.
* **Cancelar Reserva** — envia para **Cancelada pelo Restaurante**.
* **Marcar como Não Compareceu** — registra o no-show.

As ações disponíveis variam conforme o status atual da reserva. Para detalhes de cada uma, veja Confirmar, sentar, cancelar e Não Compareceu.

## Próximos passos

* Operar reservas pela Visão Geral
* Confirmar, sentar, cancelar e Não Compareceu
* Calendário de Reservas
* Ciclo de vida de uma reserva

# Políticas e pagamentos

A subseção **Políticas e pagamentos** reúne as configurações financeiras do módulo Reservas — onde os pagamentos das reservas pagas são depositados, em que condições o cliente pode cancelar ou reagendar, quanto recebe de volta e quanto é cobrado em caso de no-show.

Essas configurações não ficam dentro do menu **Reservas** no menu lateral. Elas moram no painel de configurações do administrador, acessível pelo **ícone de engrenagem** no canto superior direito de qualquer tela — nas abas **Recebimentos** e **Políticas**.

## O que você pode fazer

* Configurar recebimento de reservas pagas — cadastrar Chave PIX e dados bancários para receber os depósitos das reservas pagas.
* Política de cancelamento e no-show — definir se o cliente pode cancelar, os níveis de reembolso por antecedência e a taxa cobrada em no-show.
* Política de reagendamento — definir se o cliente pode reagendar, com taxas por antecedência e limites de uso.

## Onde acessar

Clique no **ícone de engrenagem** no canto superior direito de qualquer tela. No painel que abre, alterne entre as abas:

* **Recebimentos** — Chave PIX e Dados Bancários.
* **Políticas** — Taxa por Não Comparecimento, Política de Cancelamento e Política de Reagendamento.

## Por onde começar

Se você vai cobrar antecipadamente por reservas (Experiências pagas ou horários com **Habilitar cobrança** ligado), siga esta ordem:

1. Configure o recebimento — sem isso, o repasse não acontece.
2. Defina a Política de cancelamento e no-show — para deixar claras as regras de devolução antes de receber a primeira reserva paga.
3. Configure a Política de reagendamento se quiser permitir que clientes mudem a data da reserva.

## Conceitos importantes

* **Reservas pagas:** nascem em **Aguardando Pagamento** e só viram **Confirmada** depois que o adquirente confirma o pagamento. Cobrança ativa em horários comuns ou em Experiências exige recebimento configurado.
* **Dois toggles para cancelamento:** existe um toggle "master" em **Áreas e Mesas** → **Configurações Avançadas** (que controla cancelamento e reagendamento ao mesmo tempo) e dois toggles individuais aqui em **Políticas**. Para o cliente conseguir cancelar ou reagendar, é preciso que **ambos** estejam ligados.

## Próximos passos

* Configurações Avançadas de Reserva
* Experiências
* Configurar horários e capacidade
* Ciclo de vida de uma reserva

# Configurar recebimento

Antes de cobrar antecipadamente em horários e Experiências, é preciso cadastrar **onde** a Dionísio deve depositar o valor das reservas pagas. A tela de **Recebimentos** centraliza essa configuração — uma Chave PIX e os Dados Bancários da conta que vai receber os repasses.

## Antes de começar

Você precisa ter em mãos:

* Uma **Chave PIX** ativa (CPF, CNPJ, email, telefone ou chave aleatória).
* Os **dados bancários** da conta que vai receber os depósitos (banco, tipo de conta e dados do titular).

A configuração só precisa ser feita uma vez por estabelecimento.

## Como acessar

Clique no **ícone de engrenagem** no canto superior direito de qualquer tela. No painel que abre, selecione a aba **Recebimentos**.

## Cadastrar a Chave PIX

No bloco **Chave PIX**, preencha:

| Campo                 | Descrição                                                      |
| --------------------- | -------------------------------------------------------------- |
| **Chave PIX**         | Sua chave PIX (CPF, CNPJ, email, telefone ou chave aleatória). |
| **Tipo de chave PIX** | Tipo da chave que você informou no campo acima.                |

Clique em **Preencher Automaticamente** para que o sistema busque os dados bancários vinculados à sua chave e preencha o bloco **Dados Bancários** sozinho — economiza tempo e reduz erro de digitação.

## Cadastrar os Dados Bancários

Os **Dados Bancários** definem a conta para onde os depósitos das reservas pagas são feitos. O bloco tem duas partes.

### Titular

| Campo                          | Descrição                                                          |
| ------------------------------ | ------------------------------------------------------------------ |
| **Nome do titular da conta**   | Nome completo de quem é dono da conta.                             |
| **Tipo**                       | **CPF** ou **CNPJ**, conforme o titular.                           |
| **CPF do titular** *(ou CNPJ)* | Documento do titular, no formato correspondente ao tipo escolhido. |

### Conta

| Campo                              | Descrição                                                     |
| ---------------------------------- | ------------------------------------------------------------- |
| **Banco**                          | Use a busca para selecionar pelo nome ou código do banco.     |
| **Código do banco**                | Preenchido automaticamente ao selecionar o banco.             |
| **Tipo de conta**                  | **Conta Corrente** ou **Conta Poupança**.                     |
| **Conta padrão para recebimentos** | Toggle. Marque para que esta conta seja a usada nos repasses. |

Depois de preencher tudo, clique em **Salvar** no rodapé do painel.

## O que acontece depois

Com a Chave PIX e os Dados Bancários cadastrados, a Dionísio começa a repassar para essa conta o valor das reservas pagas — Experiências e horários com **Habilitar cobrança** ligado. O fluxo de cada reserva paga é:

1. O cliente paga via PIX ou cartão pelo Link de Reservas.
2. O pagamento é processado pelo adquirente da Dionísio.
3. A reserva muda de **Aguardando Pagamento** para **Confirmada**.
4. O valor é repassado para a conta configurada aqui.

> ℹ️ **Observação:** o valor de cada repasse já vem com a taxa do adquirente descontada. Para detalhes sobre prazos e taxas de repasse, fale com o suporte da Dionísio.

## Próximos passos

* Configurar horários e capacidade
* Experiências
* Política de cancelamento e no-show
* Política de reagendamento

# Política de cancelamento e no-show

A tela de **Políticas** centraliza as regras financeiras que valem quando uma reserva paga é cancelada ou termina em no-show. Duas configurações vivem aqui: a **Taxa por Não Comparecimento** (porcentagem cobrada quando o cliente não aparece) e a **Política de Cancelamento** com níveis de reembolso por antecedência.

Esta página cobre essas duas; o **reagendamento** mora em Política de reagendamento, na mesma tela.

## Como acessar

Clique no **ícone de engrenagem** no canto superior direito de qualquer tela. No painel que abre, selecione a aba **Políticas**.

## Taxa por Não Comparecimento

A **Taxa por Não Comparecimento** define qual porcentagem do valor da reserva paga é cobrada do cliente quando ele é marcado como **Não Compareceu**.

| Campo                   | Descrição                                                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Taxa de no-show (%)** | Porcentagem do valor que será retida em caso de no-show. Ex: 100% retém o valor inteiro; 50% retém metade e devolve metade. |

A cobrança acontece **automaticamente** assim que o status muda para **Não Compareceu** — seja manualmente (pelo botão **Marcar como Não Compareceu**) ou automaticamente, 1h após o início da reserva, quando **Atualização automática de status** está desligado.

> ⚠️ **Atenção:** essa taxa só se aplica a reservas **pagas**. Em reservas gratuitas, marcar como Não Compareceu não gera cobrança — só registra o status.

## Política de Cancelamento

A **Política de Cancelamento** decide se o cliente pode cancelar uma reserva paga e quanto recebe de volta. Tem duas configurações.

### Permitir cancelamento de reservas

Use o toggle **Permitir cancelamento de reservas** para ligar ou desligar a opção de cancelamento pelo cliente.

* **Ligado:** o cliente vê o botão de cancelar no **Link de Gerenciamento da Reserva**.
* **Desligado:** o cliente não pode cancelar — só o restaurante.

> ℹ️ **Observação:** existe também o toggle **Permitir cancelamento pelo cliente** em **Áreas e Mesas** → **Configurações Avançadas** que controla **cancelamento e reagendamento ao mesmo tempo**. Para o cliente conseguir cancelar pelo Link de Gerenciamento, **ambos** os toggles (este e o de Configurações Avançadas) precisam estar ligados. Se qualquer um estiver desligado, o botão fica escondido.

> ℹ️ **Observação:** quando o restaurante cancela uma reserva paga, o reembolso também é processado conforme os Níveis de Reembolso configurados abaixo. A diferença está em **quem inicia** o cancelamento — cliente ou restaurante — e no status final registrado (**Cancelada pelo Cliente** vs **Cancelada pelo Restaurante**).

### Configurar Níveis de Reembolso

Os **Níveis de Reembolso** funcionam como uma tabela escalonada: cada linha define um **prazo mínimo de antecedência** e o **percentual de reembolso** que o cliente recebe se cancelar dentro desse prazo.

| Campo                    | Descrição                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------- |
| **Prazo mínimo (horas)** | Quantas horas antes do início da reserva o cancelamento precisa acontecer para entrar nesse nível. |
| **Reembolso (%)**        | Percentual do valor pago que será devolvido ao cliente.                                            |

Use **+ Adicionar nível** para criar quantos níveis você precisar (ex: 48h → 100%, 24h → 50%, 6h → 0%).

Quando o cliente cancela, o sistema aplica o nível que corresponde ao prazo restante até o início da reserva.

Depois de configurar tudo, clique em **Salvar políticas** no rodapé.

## Como o reembolso é processado

O reembolso da reserva paga é **automático**. Quando uma reserva é cancelada (pelo cliente ou pelo restaurante), o sistema:

1. Identifica o nível de reembolso aplicável conforme o prazo restante até o início da reserva.
2. Calcula o valor a devolver com base no **Reembolso (%)** do nível.
3. Processa o estorno automaticamente.

> 💡 **Dica:** combine bem a **Taxa por Não Comparecimento** com a **Política de Cancelamento**. Se o no-show retém 100% e o cancelamento próximo do horário também não devolve nada, o cliente fica sem alternativa civil para avisar que não vai — o que pode aumentar disputas. Manter um pequeno percentual de reembolso para cancelamentos de última hora costuma valer mais do que cobrar 100% e perder o cliente.

## Próximos passos

* Configurar recebimento de reservas pagas
* Política de reagendamento
* Configurações Avançadas de Reserva
* Confirmar, sentar, cancelar e Não Compareceu

# Política de reagendamento

A **Política de Reagendamento** define se o cliente pode mudar a data e o horário de uma reserva confirmada, com possíveis taxas e limites. Ela vive na mesma tela que a Política de cancelamento e no-show.

Reagendar é diferente de cancelar e criar outra: a reserva original **é editada** (mesmo ID, mesmo histórico), preservando a rastreabilidade.

## Como acessar

Clique no **ícone de engrenagem** no canto superior direito de qualquer tela. No painel que abre, selecione a aba **Políticas** e role até o bloco **Política de Reagendamento**.

## Permitir reagendamento de reservas

Use o toggle **Permitir reagendamento de reservas** para ligar ou desligar a opção de reagendamento pelo cliente.

* **Ligado:** o cliente vê o botão de reagendar no **Link de Gerenciamento da Reserva**.
* **Desligado:** o cliente não pode reagendar — só o restaurante consegue editar a reserva pelo painel.

> ℹ️ **Observação:** existe também o toggle **Permitir cancelamento pelo cliente** em **Áreas e Mesas** → **Configurações Avançadas** que controla **cancelamento e reagendamento ao mesmo tempo**. Para o cliente conseguir reagendar pelo Link de Gerenciamento, **ambos** os toggles (este e o de Configurações Avançadas) precisam estar ligados. Se qualquer um estiver desligado, o botão fica escondido.

## Taxas por antecedência

As **Taxas por Antecedência** funcionam como uma tabela escalonada — quanto mais perto do horário da reserva o cliente reagendar, maior a taxa cobrada.

| Campo                    | Descrição                                                                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Prazo mínimo (horas)** | Quantas horas antes do início da reserva o reagendamento precisa acontecer para entrar nesse nível.                                              |
| **Taxa (%)**             | Percentual do valor da reserva paga cobrado como taxa de reagendamento. Ex: 0% para reagendamento sem custo, 25% para cobrar um quarto do valor. |

Use **+ Adicionar taxa** para criar quantos níveis você precisar (ex: 48h → 0%, 24h → 25%, 6h → 50%).

> ℹ️ **Observação:** as taxas só se aplicam a reservas **pagas**. Reservas gratuitas podem ser reagendadas sem custo, sujeitas apenas aos limites configurados abaixo.

## Limites de reagendamento

Os **Limites de Reagendamento** impedem que o cliente reagende várias vezes a mesma reserva.

| Campo                        | Descrição                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| **Máximo de reagendamentos** | Quantas vezes a mesma reserva pode ser reagendada. Ex: 1 permite reagendar uma única vez. |
| **Janela (dias)**            | Tempo, em dias, durante o qual o limite de reagendamentos é contado.                      |

Depois de configurar tudo, clique em **Salvar políticas** no rodapé do painel.

> 💡 **Dica:** o reagendamento dá flexibilidade ao cliente sem você perder a reserva. Em muitos casos, uma taxa moderada de reagendamento é mais bem aceita do que negar o reembolso de uma reserva cancelada de última hora — e mantém o cliente na agenda.

## Próximos passos

* Política de cancelamento e no-show
* Configurações Avançadas de Reserva
* Configurar recebimento de reservas pagas
* Ciclo de vida de uma reserva
