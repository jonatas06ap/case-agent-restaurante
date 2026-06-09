# Filas

O módulo de **Fila de Espera** organiza os clientes que chegam ao restaurante sem reserva e precisam aguardar uma mesa. Cada fila tem seu próprio link público e QR Code para que o cliente entre pelo celular, dispara notificações automáticas no WhatsApp quando é chamado, e separa o atendimento prioritário em uma fila paralela à normal. Restaurantes com alto fluxo nos horários de pico ganham controle, reduzem aglomeração no balcão e mantêm o registro de cada grupo que passou pela espera.

## Para quem é

* **Recepcionista** — opera a fila no dia a dia: adiciona participantes, chama clientes, marca como sentado, reordena e remove.
* **Dono e gerente** — configuram as filas e as regras (tempo médio de espera, verificação de localização, tags, numeração automática de comanda) e compartilham o link público.

## Como acessar

No menu lateral esquerdo, clique em **Filas**. Você verá a tela de **Gerenciamento de Filas** com todas as filas cadastradas no restaurante.

## O que você pode fazer

* Criar uma fila
* Adicionar um participante à fila
* Chamar e acomodar um participante
* Reordenar, editar e transferir participantes
* Limpar e reativar a fila
* Configurar tags e numeração de comandas
* Compartilhar o link público e o QR Code

## Principais conceitos

* Atendimento prioritário — fila paralela à normal para gestantes e idosos, sem penalizar a posição de quem já estava aguardando.
* Notificações da fila no WhatsApp — mensagens automáticas enviadas ao cliente quando entra na fila e quando é chamado.

## Integrações e canais

* **Clientes** — cada participante adicionado vira um registro no módulo **Clientes**. Se o telefone já existir, o Dionísio vincula automaticamente ao cadastro existente e a passagem pela fila fica registrada no histórico do cliente.
* **WhatsApp** — as notificações de fila são enviadas pelo **número oficial da Dionísio** por padrão, ou pelo número próprio do restaurante quando configurado no módulo **WhatsApp**.
* **Horários** — os horários de funcionamento exibidos para o cliente no link público vêm direto do módulo **Horários**.
* **Minha Loja** — endereço, contato, idade mínima e formas de pagamento exibidos no link público são herdados de **Minha Loja**.

> ℹ️ **Observação:** o módulo **Fila de Espera** é independente do módulo **Reservas**. Não é possível transformar um participante da fila em uma reserva automaticamente, nem o contrário.

## Começando

Se você está configurando o módulo pela primeira vez, siga nesta ordem:

1. Criar uma fila — dê um nome, defina o tempo médio de espera e as regras de entrada remota.
2. Configurar tags e numeração de comandas — personalize os rótulos da equipe e deixe o Dionísio numerar as comandas automaticamente.
3. Compartilhar o link público e o QR Code — coloque o QR Code na entrada do restaurante e divulgue o link nas redes sociais.

# Criar uma fila

Uma fila agrupa os clientes que estão aguardando mesa no seu restaurante. Você pode manter uma única fila permanente, criar uma nova por turno ou por dia, ou ter várias ativas ao mesmo tempo — cada uma com seu link público, QR Code e mensagens automáticas.

## Como acessar

No menu lateral, clique em **Filas**. O botão **Nova Fila** fica no canto superior direito da tela.

## Criar uma fila

1. Clique em **Nova Fila**.
2. Preencha o campo **Nome da fila**.
3. Ajuste os demais campos conforme a tabela abaixo.
4. Deixe o **Status da Fila** como **Ativa** para que ela comece a receber clientes.
5. Clique em **Criar Fila**.

A fila aparece como um card na tela principal, já com **link público**, **QR Code** e o botão **Compartilhar via WhatsApp** prontos para uso.

| Campo                                         | Obrigatório  | Descrição                                                                                                                               |
| --------------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Nome da fila**                              | Sim          | Nome exibido para a equipe e para o cliente no link público. Ex.: "Fila Jantar Sexta", "Fila Principal".                                |
| **Descrição**                                 | Não          | Texto curto visível para a equipe. Útil quando você mantém várias filas ativas.                                                         |
| **Tempo médio de espera (minutos)**           | Não          | Estimativa informada ao cliente. Valor padrão: `0`. Atualize manualmente conforme o movimento.                                          |
| **Tempo de tolerância (minutos)**             | Não          | Tempo adicional permitido antes de considerar o cliente atrasado. Campo **informativo** — o sistema não remove ninguém automaticamente. |
| **Máximo de pessoas por cliente (remoto)**    | Não          | Limite de acompanhantes quando o cliente entra pelo link público. Deixe vazio para sem limite.                                          |
| **Exigir verificação de localização**         | —            | Se ativado, o cliente precisa autorizar o GPS no navegador para entrar pelo link. Quem estiver fora do raio é bloqueado.                |
| **Raio permitido (metros)**                   | Se GPS ativo | Distância máxima do restaurante aceita para entrar na fila. Padrão: `100`. Faixa: `10` a `1000`.                                        |
| **Exibir tempo médio de espera aos clientes** | —            | Quando ativo, o cliente vê a estimativa configurada acima na página da fila.                                                            |
| **Ocultar campo de observações**              | —            | Quando ativo, remove o campo **Observações** do formulário do link público.                                                             |
| **Status da Fila**                            | Sim          | **Ativa** (padrão) recebe clientes. **Inativa** pausa novas entradas sem apagar a fila.                                                 |

## Editar ou excluir uma fila

Nos cards da tela principal, cada fila tem dois botões de gerenciamento:

* **Editar Fila** — abre o mesmo formulário acima com os valores atuais. Ajuste o que precisar e clique em **Salvar**. Alterações em raio de GPS, limites e visualizações passam a valer para os próximos participantes; quem já estava na fila não é afetado.
* **Excluir Fila** — remove a fila permanentemente, junto com todos os participantes ainda listados nela. Pede confirmação antes de executar.

Se você só quer pausar a fila temporariamente (ex.: entre almoço e jantar), edite e mude o **Status da Fila** para **Inativa**. Quando reabrir, volte para **Ativa**.

> ⚠️ **Atenção:** excluir uma fila é irreversível. Os clientes que estavam nela não aparecem mais na tela de filas, mas o histórico de atendimento continua no CRM de cada cliente.

## Dicas e observações

> 💡 **Dica:** use **Inativa** em vez de excluir quando quiser reaproveitar a mesma fila depois. O link público e o QR Code continuam válidos.

> ℹ️ **Observação:** o status **Ativa/Inativa** é sempre manual. O horário de funcionamento da loja não ativa nem desativa filas automaticamente — quem controla é você.

> ℹ️ **Observação:** não existe limite técnico para quantas filas podem ficar ativas ao mesmo tempo, mas o uso mais comum é uma única fila permanente ou uma por turno.

## Próximos passos

* Adicionar um participante
* Link público e QR Code
* Configurações avançadas

# Adicionar um participante

Adicionar um participante registra um cliente na fila de espera. Use esta tarefa quando alguém chega no restaurante sem reserva, liga para pedir para ser colocado na fila, ou quando a equipe precisa cadastrar manualmente alguém que está no balcão.

## Como acessar

No menu lateral, clique em **Filas**. No card da fila desejada, clique em **Adicionar**.

## Adicionar um participante

1. Clique em **Adicionar** no card da fila.
2. Preencha **Nome**, **WhatsApp** e **Quantidade de Pessoas** (obrigatórios).
3. Preencha os campos opcionais conforme a necessidade (mesa, comanda, prioritário, atenção, tags, observação).
4. Clique em **Adicionar**.

O cliente aparece imediatamente no card da fila com status **Aguardando**.

## Campos do formulário

| Campo                                            | Obrigatório | Descrição                                                                                                                                                                                                  |
| ------------------------------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nome**                                         | Sim         | Nome do cliente, exibido na fila e nas mensagens automáticas.                                                                                                                                              |
| **WhatsApp**                                     | Sim         | Telefone completo com DDD. O prefixo `+55` já vem preenchido para Brasil. Esse número é usado para enviar as notificações e para vincular o contato ao CRM.                                                |
| **Quantidade de Pessoas**                        | Sim         | Total de pessoas, incluindo o titular. Valor padrão: `1`.                                                                                                                                                  |
| **Número da Mesa**                               | Não         | Use se já souber onde o cliente vai sentar. Pode ser preenchido depois, no momento de acomodar.                                                                                                            |
| **Número da Comanda**                            | Não         | Número da comanda para quando o cliente se sentar. Também pode ser preenchido depois.                                                                                                                      |
| **Atendimento prioritário (gestantes e idosos)** | —           | Marca o cliente como prioritário. Ele passa a ocupar a primeira posição na fila paralela de prioridade. Veja Atendimento prioritário. |
| **Precisa de atenção (equipe)**                  | —           | Sinaliza visualmente o cliente no card (ex.: comemoração, VIP, alergias). Não altera a posição na fila.                                                                                                    |
| **Tags**                                         | Não         | Uma ou mais etiquetas. O campo só aparece se houver tags cadastradas em **Filas → Configurações avançadas**.                                                                                               |
| **Observação**                                   | Não         | Texto livre visível para a equipe. Útil para registrar preferências ou pedidos específicos.                                                                                                                |

Os mesmos campos aparecem quando você **edita** um participante já cadastrado.

## O que acontece ao adicionar

* O cliente aparece no card da fila com status **Aguardando**.
* O número de WhatsApp recebe automaticamente uma mensagem com um link para o cliente acompanhar a própria posição.
* O contato é registrado no módulo **Clientes** (CRM). Se o número já existia, o Dionísio faz merge com o histórico anterior em vez de criar um cadastro duplicado.
* Se o cliente entrou também pelo link público, os dados convergem para o mesmo contato.

> ℹ️ **Observação:** o mesmo número de WhatsApp pode estar presente mais de uma vez na fila (ou em filas diferentes) ao mesmo tempo. O sistema não bloqueia duplicatas — isso é intencional para permitir casos como grupos separados registrados pela mesma pessoa.

## Dicas e observações

> 💡 **Dica:** se o seu restaurante costuma trabalhar com o cliente se cadastrando pelo celular, deixe o link público ou QR Code visível na entrada. A recepção só precisa adicionar manualmente quem prefere não usar o próprio telefone.

> 💡 **Dica:** preencha o campo **Observação** com alergias, aniversariantes, preferência de mesa — essas informações ficam visíveis para toda a equipe no card da fila.

> ⚠️ **Atenção:** o WhatsApp é usado para chamar o cliente quando a mesa estiver pronta. Se o número estiver errado, o cliente não vai receber a convocação.

## Próximos passos

* Chamar e acomodar
* Gerenciar participantes
* Link público e QR Code

# Chamar e acomodar

Essa é a sequência principal de atendimento da fila: o recepcionista chama o cliente quando a mesa estiver pronta, confirma que ele chegou, acomoda e encerra o atendimento. O fluxo é linear, mas **cada transição de status é manual** — nada avança sozinho.

## Como acessar

No menu lateral, clique em **Filas** e localize o card da fila em que o cliente está.

## Chamar um cliente

Quando a mesa estiver pronta:

1. Encontre o cliente no card da fila (status **Aguardando**).
2. Clique em **Chamar**.

O status muda automaticamente para **Chamado** e o cliente recebe uma mensagem no WhatsApp avisando que é hora de ir para a mesa.

### Chamar novamente

Se o cliente demorar para responder, clique em **Chamar novamente** no card dele (disponível enquanto o status estiver **Chamado**). Isso reenvia a mensagem no WhatsApp sem alterar a posição do cliente nem o status.

## Acomodar o cliente

Quando o cliente chega na mesa:

1. Abra o dropdown de status no card (ao lado do status atual **Chamado**).
2. Selecione **Sentado**.

O card sai da listagem ativa e fica registrado no histórico como cliente acomodado. Esse passo é sempre manual — o status não muda sozinho mesmo depois de o cliente confirmar pelo WhatsApp.

## Cancelar um cliente

Se o cliente desistir, não responder à convocação ou não aparecer para sentar:

1. Abra o dropdown de status no card.
2. Selecione **Cancelado**.

**Cancelar é diferente de excluir.** O status **Cancelado** mantém o cliente no histórico com o motivo registrado — útil para acompanhar no CRM os clientes que deram no-show. Para remover o registro por completo (ex.: cadastro duplicado ou erro de digitação), use o ícone 🗑️. Veja Gerenciar participantes.

## Dicas e observações

> 💡 **Dica:** para registrar **Número da Mesa** e **Número da Comanda** do cliente acomodado, edite o participante (ícone ✏️) antes ou depois de mudar o status para **Sentado**. Esses campos são informativos e ficam no histórico do atendimento.

> ℹ️ **Observação:** o status **Cancelado** é diferente de **Excluir**. Cancelar registra a desistência no histórico; excluir remove o registro da fila sem deixar rastro na tela de filas.

> ℹ️ **Observação:** cada transição de status é manual — mesmo depois de clicar em **Chamar**, é preciso mudar o status para **Sentado** quando o cliente chegar.

## Próximos passos

* Gerenciar participantes
* Notificações no WhatsApp
* Atendimento prioritário

# Gerenciar participantes

Esse fluxo cobre as ações do dia a dia sobre quem já está na fila: conferir o perfil, editar dados, mudar a ordem, transferir para outra fila ou remover o registro. Tudo parte dos ícones no card do participante e do botão **Reordenar** no topo da fila.

## Como acessar

No menu lateral, clique em **Filas** e abra a fila com o participante que você quer gerenciar. Cada card traz quatro ícones: 👁️ **Ver perfil** (abre o cliente no módulo **Clientes**), ✏️ **Editar**, ↔️ **Transferir** e 🗑️ **Excluir**.

## Editar um participante

1. Clique no ícone ✏️ no card do cliente.
2. Ajuste qualquer campo — os mesmos do cadastro original.
3. Clique em **Salvar**.

Todos os campos do formulário de adição ficam disponíveis: **Nome**, **WhatsApp**, **Quantidade de Pessoas**, **Número da Mesa**, **Número da Comanda**, **Atendimento prioritário**, **Precisa de atenção (equipe)**, **Tags** e **Observação**. A descrição completa de cada campo está em Adicionar um participante.

> 💡 **Dica:** use a edição para registrar **Número da Mesa** e **Número da Comanda** no momento de acomodar o cliente. Esses campos são informativos e não acionam nenhum comportamento automático.

## Reordenar a fila

Por padrão, a ordem da fila acompanha a hora de entrada de cada cliente. Quando precisar mudar manualmente:

1. Clique em **Reordenar** no topo do card da fila.
2. Arraste os participantes para a nova posição.
3. Clique novamente em **Reordenar** (ou no botão de confirmação) para sair do modo de ordenação.

Enquanto o modo **Reordenar** estiver ativo, as demais ações do card ficam desabilitadas — ative somente quando for mexer na ordem.

> ⚠️ **Atenção:** reordenar não envia nenhuma mensagem aos clientes. Quem subiu na fila não é notificado automaticamente sobre a nova posição.

## Transferir para outra fila

Se o cliente entrou na fila errada ou se você abriu uma nova fila e quer mover participantes:

1. Clique no ícone ↔️ (setas) no card do cliente.
2. Selecione a fila de destino entre as filas ativas.
3. Confirme.

O participante é movido para a fila de destino mantendo o mesmo status atual. Histórico e cadastro no CRM são preservados.

> ℹ️ **Observação:** a transferência só aparece quando existem outras filas ativas. Se houver apenas uma fila, o ícone ↔️ não é exibido.

## Excluir um participante

Para remover alguém da fila por completo:

1. Clique no ícone 🗑️ no card do cliente.
2. Confirme a exclusão.

**Excluir é diferente de Cancelar.** Excluir apaga o registro da tela de filas — o cliente some da lista. O status **Cancelado**, por outro lado, mantém o cliente no histórico com o motivo da saída. Use exclusão apenas para cadastros duplicados, erros de digitação ou quando o cliente pediu para remover o contato. Para registrar um no-show, prefira **Cancelado** (veja Chamar e acomodar).

## Próximos passos

* Chamar e acomodar
* Limpar e reativar a fila
* Atendimento prioritário

# Limpar e reativar a fila

**Limpar fila** é uma forma rápida de resetar a fila entre turnos ou serviços sem apagar a fila em si. O botão **Reativar** desfaz essa limpeza e traz todos os participantes de volta — mesmo que a operação tenha acontecido em outro dia.

## Como acessar

No menu lateral, clique em **Filas** e abra a fila desejada. Os botões **Limpar fila** e **Reativar** ficam nas ações do topo do card da fila.

## Limpar a fila

Quando precisar zerar a fila (ex.: entre almoço e jantar, ao fim do expediente):

1. Clique em **Limpar fila**.
2. Confirme na janela de segurança.

Todos os participantes somem da tela — incluindo quem estava em **Aguardando**, **Chamado**, **Sentado** ou **Cancelado**. Eles não são apagados: ficam guardados em um estado de "limpos", fora da visualização ativa, até você usar **Reativar**.

> ⚠️ **Atenção:** limpar é diferente de excluir a fila. **Limpar fila** remove apenas os participantes — a fila continua ativa e pronta para receber novos clientes. **Excluir fila** (veja Criar uma fila) apaga a fila inteira, junto com os participantes.

## Reativar a fila

Quando precisar recuperar participantes de uma limpeza:

1. Clique em **Reativar** no topo do card da fila.
2. Confirme.

Todos os clientes que estavam guardados na última limpeza voltam para a tela. Não há limite de tempo — você pode reativar no mesmo turno, horas depois, ou no dia seguinte.

> 💡 **Dica:** pense em **Reativar** como um atalho de correção para quando alguém clicou em **Limpar fila** por engano. Para o dia a dia, prefira não limpar enquanto ainda houver clientes em atendimento.

## Dicas e observações

> ℹ️ **Observação:** o histórico dos clientes no módulo **Clientes** (CRM) não é afetado por limpar ou reativar. Cada interação na fila continua registrada no perfil do cliente, independente da operação.

> ℹ️ **Observação:** limpar a fila não desativa a fila e não apaga as configurações. Para pausar novas entradas sem perder o estado atual, mude o **Status da Fila** para **Inativa** em Criar uma fila.

## Próximos passos

* Gerenciar participantes
* Criar uma fila

# Configurações avançadas

A tela de **Configurações avançadas** reúne ajustes que valem para todas as filas da loja: criação de **tags** de participantes e a **geração automática do número da comanda**. Os dois blocos ficam em um único modal.

## Como acessar

No menu lateral, clique em **Filas**. No canto superior direito da tela, clique em **Configurações avançadas**.

Ao terminar os ajustes, clique em **Salvar** no rodapé do modal. **Cancelar** descarta as alterações.

## Gerenciar tags

Tags são rótulos que a equipe atribui aos participantes para organizar e identificar clientes nas filas (ex.: "VIP", "Aniversariante", "Alergia"). Elas aparecem no formulário do participante (campo **Tags**) e ficam visíveis no card da fila.

Para criar uma tag:

1. No campo **Nova tag**, digite o nome.
2. Pressione **Enter** ou clique no botão **+**.

A tag aparece abaixo como um chip. Para **excluir**, clique no **×** ao lado do nome. As tags podem ser editadas ou excluídas a qualquer momento nesta mesma tela.

Não há limite de quantas tags você pode cadastrar, e um mesmo participante pode receber mais de uma tag.

> 💡 **Dica:** use nomes curtos e operacionais — eles ganham destaque no card da fila quando são fáceis de ler em um olhar. Prefira "Aniv." a "Aniversariante do dia".

## Numeração automática de comanda

Quando ativada, essa opção faz o Dionísio atribuir automaticamente um **Número da Comanda** a cada novo participante adicionado à fila, incrementando em +1 a cada cadastro. A ideia é eliminar o trabalho manual de digitar o número do PDV para cada cliente — a numeração segue a mesma faixa de comandas que o restaurante já usa no PDV.

Para configurar:

1. Ative o toggle **Gerar número da comanda automaticamente**.
2. Preencha o **Número inicial** (padrão: `1`).
3. Preencha o **Número final** (padrão: `999`).
4. Clique em **Salvar**.

Quando a contagem atingir o **Número final**, ela reinicia automaticamente a partir do **Número inicial** na próxima adição.

| Campo                                       | Obrigatório | Descrição                                                                                                                                                                |
| ------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Gerar número da comanda automaticamente** | —           | Liga ou desliga o preenchimento automático. Quando desligado, o campo **Número da Comanda** do participante fica em branco por padrão e pode ser preenchido manualmente. |
| **Número inicial**                          | Sim         | Primeiro número da faixa. Deve ser menor que o **Número final**.                                                                                                         |
| **Número final**                            | Sim         | Último número da faixa. Ao atingir esse valor, a contagem volta ao inicial na próxima adição.                                                                            |

> ℹ️ **Observação:** o intervalo precisa coincidir com a faixa de comandas usada pelo PDV do restaurante. Cada PDV costuma ter sua própria faixa — ajuste aqui conforme a realidade da casa.

## Reiniciar contagem

Se precisar voltar a contagem ao início manualmente (ex.: entre turnos, após fechar o caixa ou ao trocar de PDV):

1. Abra **Configurações avançadas**.
2. Clique em **Reiniciar contagem**.

A próxima adição à fila volta a usar o **Número inicial** configurado.

> ⚠️ **Atenção:** reiniciar não afeta participantes que já foram adicionados — muda apenas o ponto de partida para os próximos cadastros.

## Próximos passos

* Adicionar um participante
* Criar uma fila
* Gerenciar participantes

# Link público e QR Code

Cada fila do Dionísio tem um **link público** e um **QR Code** próprios, que permitem ao cliente entrar na fila pelo celular sem depender da recepção. Os dois apontam para a mesma página, hospedada em `q.odionisio.com`.

Não existe link mestre ou intermediário — cada fila gera o seu. Se você tem duas filas ativas, são dois links diferentes.

## Como acessar

No menu lateral, clique em **Filas**. No card da fila desejada, você encontra três ações de compartilhamento: **Copiar Link**, **Compartilhar via WhatsApp** e **Baixar QR Code**.

## Copiar, compartilhar e baixar o QR Code

* **Copiar Link** — copia a URL da fila. Cole em redes sociais, no site, no Google Meu Negócio ou em qualquer canal digital.
* **Compartilhar via WhatsApp** — abre o WhatsApp Web ou o app com uma mensagem pronta contendo o link. Útil para enviar para grupos ou clientes específicos.
* **Baixar QR Code** — salva um arquivo de imagem do QR Code. Imprima e coloque na entrada, no cardápio ou nas mesas. Ao escanear, o cliente é levado direto para a página da fila.

> 💡 **Dica:** o QR Code é a forma mais prática de oferecer o autoatendimento na entrada. A recepção só precisa orientar clientes que preferirem não usar o celular — esses você cadastra manualmente em Adicionar um participante.

## Como o cliente entra na fila

Ao abrir o link ou escanear o QR Code:

1. O cliente preenche **Nome**, **WhatsApp** e **Quantidade de Pessoas**.
2. Preenche **Observação** (se o campo estiver visível).
3. Confirma a entrada.

O cliente aparece imediatamente no painel do recepcionista e recebe no WhatsApp a mensagem automática com o link para acompanhar a posição. O cadastro é vinculado ao CRM pelo número do WhatsApp — com merge automático se o contato já existir.

O campo **Quantidade de Pessoas** respeita o limite definido em **Máximo de pessoas por cliente (remoto)** da fila (veja Criar uma fila).

> ℹ️ **Observação:** o cliente **não escolhe** entrar como atendimento prioritário. Somente a recepção pode marcar essa opção no participante (veja Atendimento prioritário).

## Verificação de GPS

Se a fila tiver **Exigir verificação de localização** ativada:

1. O navegador do cliente pede permissão de localização.
2. O sistema compara a posição com o **Raio permitido (metros)** configurado.
3. Se estiver dentro do raio, a entrada segue normalmente. Se estiver fora, o cliente é bloqueado.

A verificação usa apenas o navegador — não exige baixar app. Se o cliente negar a permissão, a entrada não se completa.

## Saída da fila pelo cliente

O cliente pode desistir da espera direto pelo próprio link:

1. Acessa o link da fila (pelo WhatsApp ou pelo QR Code).
2. Clica no botão para sair da fila.

O status do participante muda para **Cancelado** no painel do recepcionista. O registro permanece no histórico com o motivo da saída — igual ao cancelamento feito pela equipe (veja Chamar e acomodar).

> ⚠️ **Atenção:** a página do cliente **não atualiza em tempo real**. Se a posição mudar ou se o cliente for chamado, é necessário **atualizar a página** para ver o novo estado. A convocação para a mesa chega sempre pelo WhatsApp — é lá que o cliente deve ficar atento.

## Próximos passos

* Adicionar um participante
* Criar uma fila
* Notificações no WhatsApp

# Atendimento prioritário

O **atendimento prioritário** é uma fila paralela à fila normal, destinada a clientes com direito de preferência (gestantes, idosos, pessoas com deficiência e outros grupos previstos em lei ou por política da casa). No Dionísio, ele funciona como uma segunda fila dentro da mesma fila principal — cada uma com sua própria ordem e seu próprio "primeiro lugar".

## Como funciona

Quando um participante é marcado com **Atendimento prioritário (gestantes e idosos)** pela recepção (veja Adicionar um participante), ele entra em uma lista paralela exclusiva dos prioritários. A fila normal continua funcionando sem alteração — nenhum cliente "comum" perde posição.

Na prática, a tela mostra **duas posições 1**:

* O **primeiro da fila normal** — o mais antigo entre os não-prioritários.
* O **primeiro da fila prioritária** — o mais antigo entre os marcados como prioritário.

Essa separação existe por um motivo de experiência do cliente: se os prioritários entrassem na mesma lista, cada novo prioritário empurraria os demais para trás e o cliente da fila normal veria sua posição "piorar" — gerando frustração. Com duas filas, o cliente comum só vê clientes comuns na frente.

O recepcionista atende conforme a política do restaurante (em geral, alternando entre as duas filas e dando preferência à prioritária quando houver mesa disponível). O chamamento pelo WhatsApp e a acomodação seguem o fluxo descrito em Chamar e acomodar.

## Quando usar

* **Gestantes, idosos e pessoas com deficiência** — para atender à legislação brasileira de preferência no atendimento.
* **Lactantes e pessoas com crianças de colo** — grupos frequentemente incluídos como cortesia pela casa.
* **Clientes VIP, convidados ou cortesias** — a critério do restaurante.

A decisão de marcar um cliente como prioritário é sempre da equipe de recepção. O cliente **não pode** se auto-classificar pelo link público da fila.

## Limitações

* A marcação acontece apenas no cadastro do participante (pela equipe). Não existe fluxo de solicitação pelo cliente.
* Não existe prioridade parcial ou escalonada — o participante é prioritário ou não; não há "meio-prioritário".
* As mensagens automáticas de WhatsApp enviadas pelo Dionísio são as mesmas para participantes normais e prioritários. Os templates não diferenciam os dois grupos.

## Relacionado

* Adicionar um participante
* Gerenciar participantes
* Chamar e acomodar
* Notificações no WhatsApp

# Notificações no WhatsApp

As **notificações no WhatsApp** são as mensagens automáticas que o Dionísio envia aos clientes da fila em momentos-chave do atendimento. Elas conectam o restaurante ao cliente sem exigir ação manual da recepção — e são a única forma pela qual o cliente é avisado que a mesa está pronta.

## Como funciona

O Dionísio dispara mensagens em dois eventos da fila:

* **Ao adicionar o cliente na fila** — o cliente recebe uma mensagem com o link da página pública da fila, para acompanhar a posição (veja Link público e QR Code). Isso vale tanto para o cadastro manual pela recepção quanto para o autocadastro pelo cliente.
* **Ao clicar em "Chamar" ou "Chamar novamente"** — o cliente recebe a convocação avisando que a mesa está pronta.

Todo o conteúdo vem de **templates fixos** aprovados pela Meta. O restaurante não edita o texto das mensagens.

### Por qual número sai o envio

A origem da mensagem depende da configuração de WhatsApp do restaurante:

* **Número oficial da Dionísio (padrão)** — sem configuração adicional. Todas as mensagens da fila saem de um número institucional da Dionísio. É a opção automática para quem não configurou um número próprio.
* **Número do próprio restaurante** — a casa cadastra um cartão de crédito diretamente na Meta e usa a WhatsApp Business API própria. As mensagens passam a sair do número oficial do restaurante. Nesse modelo, a Meta cobra por conversa. A configuração é feita no módulo de conexão do WhatsApp.

## Quando usar

As notificações acontecem automaticamente — você não liga ou desliga evento por evento. O que fica sob seu controle é:

* **Qual número envia** — aceitar o padrão da Dionísio ou configurar o próprio (recomendado para restaurantes que querem reforçar a identidade e já têm WhatsApp Business API).
* **Qualidade do cadastro** — como o WhatsApp é o único canal de convocação, o número precisa estar correto. Um número errado em Adicionar um participante significa que o cliente não vai receber a convocação.

## Limitações

* Os templates são **fixos**. O texto das mensagens de entrada e de convocação não é editável pelo restaurante, porque precisam de aprovação prévia da Meta.
* Não há integração com a **Assistente IA**. O módulo de Filas envia mensagens de forma independente e a IA não participa da conversa. Respostas que o cliente mandar no WhatsApp **não são processadas** pela IA do Dionísio.
* Se o cliente bloqueou o número do remetente (Dionísio ou restaurante), ele não recebe as notificações — e não existe aviso de falha no painel.
* Mensagens são disparadas apenas pelos eventos **Adicionar** e **Chamar/Chamar novamente**. Mudanças manuais de status (ex.: mover para **Sentado** ou **Cancelado**) **não enviam** nenhuma mensagem.

## Relacionado

* Adicionar um participante
* Chamar e acomodar
* Link público e QR Code
