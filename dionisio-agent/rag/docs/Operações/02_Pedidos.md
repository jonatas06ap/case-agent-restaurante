# Pedidos

**Pedidos** é a tela onde você acompanha em tempo real os pedidos de delivery e retirada feitos diretamente para o seu restaurante, sem passar por marketplaces. É o canal próprio do Dionísio — alternativa às plataformas com taxa, com cardápio digital próprio e Assistente IA atendendo no WhatsApp.

Pedidos chegam por quatro caminhos:

* **Link Público de Pedidos** — cliente acessa a URL do restaurante e finaliza sozinho.
* **Assistente IA do WhatsApp** — a IA conversa sobre o cardápio (preços, descrições, fotos) e envia o Link Público para o cliente fechar o pedido.
* **iFood integrado** — pedidos do iFood aparecem na mesma tela, unificados com os pedidos próprios.
* **Criação manual** — a equipe lança um pedido pelo painel, útil para pedidos por telefone ou balcão.

## Para quem é

* **Dono** e **Administrador** — operam a tela no dia a dia e configuram o módulo. Acesso por padrão.
* **Membro** — só vê a aba **Pedidos** se o Administrador tiver habilitado a permissão. Detalhes em Pessoas.

## O que você pode fazer

* Acompanhar pedidos — avançar, recusar e cancelar pedidos pelo kanban.
* Painel de controle — som, impressora, pausar delivery e modo de visualização.
* Criar pedido manualmente — lançar pedidos por telefone ou balcão.
* Editar itens e cliente de um pedido — ajustar pedidos em andamento.
* Atribuir motorista — escolher entre motoristas internos, iFood ou Lalamove.
* Aceitar troca de endereço — quando o cliente pede para alterar a entrega.
* Histórico de Pedidos — consultar e exportar pedidos finalizados.

## Principais conceitos

* Status do pedido — lista completa dos status, automações e janelas de tempo.

## Abas da tela

A tela é dividida em quatro abas. Em cada aba aparece apenas o que está **ativo** naquele canal — pedidos finalizados vão para o Histórico.

| Aba               | O que mostra                                                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Delivery**      | Pedidos para entrega no endereço do cliente.                                                                                    |
| **Retirada**      | Pedidos para o cliente buscar no balcão.                                                                                        |
| **Mesa**          | Pedidos para consumo no salão. **Disponível em breve** — a aba existe na tela mas a operação ainda não está ativa.              |
| **Cancelamentos** | Pedidos cancelados, solicitações de cancelamento abertas e cancelamentos negados — centralizados independente de canal ou tipo. |

## Integrações e canais

* **Cardápios** — itens ativos formam o catálogo do pedido manual e do Link Público. Itens desativados não aparecem.
* **Configuração de Entrega** — define cobertura, taxa, horários de entrega, agendamento e a regra de aceitar pedidos automaticamente.
* **Clientes** — telefone do cliente é usado para notificação no WhatsApp. O histórico de pedidos aparece no perfil dele.
* **WhatsApp** — o cliente recebe uma mensagem automática a cada mudança de status (não é possível desligar).
* **Configuração de IA** — a Assistente IA lê o cardápio e a Configuração de Entrega automaticamente; você não precisa configurar nada extra para ela falar de Pedidos.
* **Cupons** — o cliente aplica o código no carrinho do Link Público.
* **Integrações** — iFood (pedidos centralizados na tela), Lalamove (motorista), Atena, SaiPos, EyePdv e Open Delivery (emissão automática no PDV).
* **Relatórios** — dados dos pedidos alimentam métricas de faturamento e volume.
* **Satisfação** — depois que um pedido é finalizado, o cliente recebe uma pesquisa após um período configurado. Detalhes em Satisfação.

## Começando

Se você acabou de contratar o módulo, siga nesta ordem:

1. Configure os campos gerais e os horários em Configuração de Entrega.
2. Cadastre o cardápio em Cardápios.
3. Configure a impressora em Minha Loja, se quiser impressão automática.
4. Comece a operar pela tela Acompanhar pedidos.

# Acompanhar pedidos

A tela **Pedidos** é o seu painel operacional do dia: cada pedido aparece como um card numa coluna do kanban, e você avança o pedido entre colunas até ele ser entregue. Esta página cobre o fluxo principal de operar o kanban.

## Antes de começar

Você precisa de:

* Plano de Pedidos ativo.
* Configuração de Entrega preenchida (geral e horários).
* Cardápio com pelo menos um item ativo em Cardápios.

## Como acessar

No menu lateral, clique em **Pedidos**.

## Passos

1. Selecione a aba do tipo de pedido que quer ver: **Delivery**, **Retirada** ou **Cancelamentos**.
2. Localize o card do pedido — pode usar o campo de busca no topo (número, nome do cliente ou telefone).
3. Clique no card para abrir os detalhes ou use os botões **Avançar**, **Recusar** ou o menu de ações direto no card.
4. Para mover o pedido entre colunas, você também pode **arrastar o card** com o mouse.

O pedido sai da aba quando chega na coluna **Concluído** (ou **Cancelado**). Use o Histórico para consultar pedidos finalizados.

## Colunas do kanban

As colunas mudam conforme a aba e o modo de visualização. No modo expandido o kanban tem mais detalhe; no modo compacto algumas colunas são fundidas. Veja Painel de controle para alternar.

### Delivery — modo expandido

| Coluna                  | Quando o pedido está aqui                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Novo**                | Pedido recém-criado. Aguardando você confirmar (a menos que **Aceitar Pedidos Automaticamente** esteja ligado). |
| **Confirmado**          | Você aceitou. Dispara automaticamente a cotação de motorista em iFood e Lalamove, se ativos.                    |
| **Pronto para Entrega** | Cozinha terminou, aguardando o motorista pegar.                                                                 |
| **Saiu para Entrega**   | Motorista a caminho do cliente.                                                                                 |
| **Concluído**           | Pedido entregue e fechado.                                                                                      |

No modo compacto, **Pronto para Entrega** some — a coluna **Confirmado** abrange tudo até o motorista sair.

### Retirada — modo expandido

| Coluna                   | Quando o pedido está aqui                      |
| ------------------------ | ---------------------------------------------- |
| **Novo**                 | Pedido recém-criado.                           |
| **Confirmado**           | Você aceitou.                                  |
| **Pronto para Retirada** | Cozinha terminou, aguardando o cliente buscar. |
| **Concluído**            | Pedido retirado e fechado.                     |

No modo compacto, **Concluído** some — pedidos ficam em **Pronto para Retirada** até a regra de auto-conclusão de 24 horas atuar (ou você avançar manualmente pelo detalhe do pedido).

### Cancelamentos

| Coluna                          | Quando o pedido está aqui                               |
| ------------------------------- | ------------------------------------------------------- |
| **Solicitação de Cancelamento** | Cliente pediu para cancelar, aguardando você decidir.   |
| **Cancelado**                   | Pedido cancelado, por você ou pela regra de 10 minutos. |
| **Cancelamento Negado**         | Você recusou a solicitação de cancelamento do cliente.  |

## Ações no card

Cada card oferece estas ações principais:

| Ação                              | O que faz                                                                                                                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Avançar**                       | Move o pedido para o próximo status do fluxo da aba.                                                                                                 |
| **Recusar**                       | Cancela um pedido em **Novo**. Pede o motivo. Útil quando você não consegue atender.                                                                 |
| **Cancelar**                      | Cancela um pedido em qualquer status até **Saiu para Entrega**. Pede motivo. Dispara estorno automático em pagamentos pré-pagos.                     |
| **Voltar um passo**               | Move o pedido para o status anterior. Não disponível em **Novo**, **Concluído** ou **Cancelado**.                                                    |
| **Atribuir motorista**            | Abre o painel de motoristas. Detalhes em Atribuir motorista.                       |
| **Editar Cliente / Editar Itens** | Atualiza dados do pedido em andamento. Detalhes em Editar itens e cliente de um pedido. |
| **Imprimir**                      | Reimprime a comanda na impressora configurada.                                                                                                       |

## Dicas e observações

> ℹ️ **Observação:** pedidos em **Novo** que ficarem 10 minutos sem confirmação são cancelados automaticamente, com o motivo "Cancelada automaticamente após 10 minutos sem confirmação". Em pagamentos pré-pagos, o estorno é processado em seguida.

> ℹ️ **Observação:** pedidos em qualquer estado ativo (Confirmado, Pronto, Saiu para Entrega, Entregue) há mais de 24 horas são marcados como **Concluído** automaticamente, com a nota "Concluída automaticamente após 24 horas". Veja a lista completa em Status do pedido.

> 💡 **Dica:** o cliente recebe uma mensagem no WhatsApp a cada mudança de status, com link de acompanhamento do pedido nos status intermediários. Não há configuração para desligar essas mensagens.

> ⚠️ **Atenção:** se um pedido já foi repassado financeiramente (PIX em 1 dia, cartão em 30 dias), o botão **Cancelar** retorna erro — o dinheiro já foi transferido para a loja e o estorno só pode ser tratado fora do Dionísio.

## Próximos passos

* Painel de controle
* Criar pedido manualmente
* Atribuir motorista
* Status do pedido

# Painel de controle

A barra superior da tela **Pedidos** concentra os controles operacionais que você ajusta durante o serviço: som, impressora, modo de visualização e pausa de entrada. Esta página explica cada controle.

## Como acessar

No menu lateral, clique em **Pedidos**. A barra de controles fica no topo da tela, acima das abas.

## Controles disponíveis

| Controle                   | O que faz                                                                                                                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Expandida / Compacta**   | Alterna o kanban entre o modo expandido (mais colunas, cards grandes) e o compacto (menos colunas, cards reduzidos). O modo escolhido vale apenas para a sua sessão.                                   |
| **Atualizar**              | Força um recarregamento da lista de pedidos. Útil se você suspeitar que algo não atualizou em tempo real.                                                                                              |
| **Som Ligado / Desligado** | Liga ou desliga o alerta sonoro que toca quando um pedido novo chega. Recomendado **ligado** em horários de pico.                                                                                      |
| **Impressora**             | Atalho para a configuração da impressora em Minha Loja → Impressoras. Uma vez configurada, cada pedido novo imprime automaticamente. |
| **Pausar Delivery**        | Interrompe a entrada de **novos** pedidos de delivery e retirada pelo Link Público e pela Assistente IA. Detalhes na seção abaixo.                                                                     |
| **Atraso: X min**          | Aparece apenas se você tiver integração com iFood Shipping ou Lalamove ativa. Define minutos adicionais comunicados ao serviço de logística externa.                                                   |
| **Criar Pedido**           | Abre o painel de criação manual. Detalhes em Criar pedido manualmente.                                                              |
| **Histórico**              | Vai para o Histórico de Pedidos.                                                                                                              |
| **Buscar**                 | Campo de busca por número do pedido, nome do cliente ou telefone. Aplica em todas as abas.                                                                                                             |

## Pausar Delivery

Pausar Delivery interrompe a entrada de pedidos novos pelos canais próprios. É útil em momentos de sobrecarga da cozinha, queda de equipe ou imprevisto pontual.

Para pausar:

1. Clique em **Pausar Delivery**.
2. Defina o **horário de início** e o **horário de fim** da pausa.
3. Escreva o **motivo** que aparece para o cliente no Link Público.
4. Clique em **Confirmar**.

Enquanto a pausa estiver ativa:

* Novos pedidos de **delivery** e **retirada** são bloqueados no Link Público com a mensagem do motivo.
* A Assistente IA também para de oferecer o link de pedido.
* Pedidos **já no kanban** continuam normalmente — você termina o serviço sem perder nada.
* A integração com iFood **não** é afetada — pedidos do iFood continuam chegando se o iFood estiver aberto lá.

Para retomar antes do horário programado, clique em **Pausar Delivery** novamente e remova a pausa.

> ⚠️ **Atenção:** apesar do nome, **Pausar Delivery** pausa também a entrada de pedidos de **retirada**. Pedidos do iFood continuam chegando normalmente.

## Modo Expandida vs Compacta

As duas visualizações mostram os mesmos pedidos, mas em colunas e tamanhos diferentes:

* **Expandida** — mais colunas no kanban (incluindo **Pronto para Entrega** e **Pronto para Retirada**) e cards com todos os detalhes do pedido. Útil para acompanhamento detalhado em telas grandes.
* **Compacta** — colunas reduzidas e cards menores. Útil para celular ou quando o volume de pedidos é alto.

A escolha vale só para a sua sessão. Outros usuários da loja podem ter modos diferentes na mesma hora.

## Dicas e observações

> 💡 **Dica:** deixe a impressora configurada antes do horário de pico. Como não há retentativa automática se a impressora estiver offline, configure e teste com calma fora do serviço.

> ℹ️ **Observação:** o som de alerta toca apenas quando um pedido novo entra. Mudanças de status de pedidos já no kanban (avanços manuais ou automáticos) não tocam som.

## Próximos passos

* Acompanhar pedidos
* Criar pedido manualmente
* Configurar impressora

# Criar pedido manualmente

Crie um pedido pela equipe sempre que o cliente fizer o pedido por telefone, balcão, WhatsApp manual ou qualquer canal fora do Link Público. O pedido criado aparece no kanban da aba correspondente ao tipo escolhido.

## Antes de começar

Você precisa de:

* Plano de Pedidos ativo.
* Cardápio com pelo menos um item ativo em Cardápios. Itens desativados não aparecem.

## Como acessar

No menu lateral, clique em **Pedidos** → **Criar Pedido** (botão no topo da tela).

## Passos

1. Clique em **Criar Pedido**.
2. No **lado esquerdo**, escolha os itens no cardápio (veja a seção abaixo).
3. No **lado direito**, defina o **Tipo do pedido**, o **Agendamento**, a **Observação** e o **Pagamento**.
4. (Opcional) Vincule o **Cliente** para que o pedido fique registrado no perfil dele.
5. Confira o **Total** e clique em **Pagar — R$ X,XX** para finalizar.

O pedido aparece imediatamente no kanban, na aba correspondente ao **Tipo** escolhido.

## O painel de criação

O painel é dividido em dois lados que você usa em paralelo: à esquerda você escolhe os itens, à direita você define os dados do pedido e finaliza.

### Lado esquerdo — Cardápio

| Elemento           | O que faz                                                                                                   |
| ------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Categorias**     | Lista as categorias do cardápio com a quantidade de itens disponíveis em cada. Clique para ver os produtos. |
| **Buscar produto** | Pesquisa direta por nome do item, sem precisar abrir a categoria.                                           |
| **Produto**        | Clique para abrir o painel de seleção, escolher complementos e definir a quantidade.                        |

Se a loja tiver mais de um cardápio publicado, alterne entre eles pelo seletor no topo do painel. Itens só aparecem se estiverem ativos no cardápio selecionado.

### Lado direito — Resumo do pedido

| Campo                    | Obrigatório   | Descrição                                                                                                                                                                                |
| ------------------------ | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pesquisar cliente**    | Não           | Vincula o pedido a um cliente existente. Sem vínculo, o pedido não fica no histórico do cliente.                                                                                         |
| **Tipo do pedido**       | Sim           | **Entrega**, **Retirada** ou **Local / Mesa**. Define em qual aba do kanban o pedido vai aparecer.                                                                                       |
| **Agendamento**          | Sim           | **Para agora** ou agendar para data e hora futura. Só pode agendar dentro do horário configurado em Horários de Entrega. |
| **Endereço**             | Só em Entrega | Endereço de entrega do cliente. Precisa estar dentro da área de cobertura configurada.                                                                                                   |
| **Observação do pedido** | Não           | Texto livre para instruções especiais (ex: "sem cebola", "pedido para o andar 5").                                                                                                       |
| **Carrinho**             | Sim           | Itens selecionados no lado esquerdo. Você pode ajustar quantidade ou remover aqui.                                                                                                       |
| **Adicionar pagamento**  | Sim           | Forma de pagamento — dinheiro, cartão, PIX, etc. Veja abaixo.                                                                                                                            |
| **Subtotal / Total**     | —             | Calculados automaticamente conforme o carrinho. O Total inclui a taxa de entrega quando aplicável.                                                                                       |
| **Pagar — R$ X,XX**      | —             | Finaliza e registra o pedido.                                                                                                                                                            |

### Formas de pagamento aceitas

A forma de pagamento define como o sistema trata o pedido depois de criado:

* **Dinheiro, cartão na entrega, PIX na entrega** — o pedido entra no kanban como pago **na entrega**. O motorista ou o atendente acerta com o cliente no momento da entrega ou retirada.
* **PIX online ou cartão online** — não disponível na criação manual. Esses pagamentos acontecem apenas quando o cliente fecha o pedido pelo Link Público.

## Dicas e observações

> 💡 **Dica:** vincule o cliente sempre que possível. Além de manter o histórico no perfil, o cliente passa a receber automaticamente as mensagens de status no WhatsApp.

> 💡 **Dica:** para pedidos repetidos, busque o cliente primeiro. O sistema preenche endereço e dados anteriores automaticamente.

> ⚠️ **Atenção:** ao escolher **Agendamento** para data futura, confira se o horário está dentro da janela de entrega. Pedidos agendados fora do horário não passam pelo Link Público, mas no manual a equipe pode acabar criando pedido para um horário que a loja não atende.

## Próximos passos

* Acompanhar pedidos
* Editar itens e cliente de um pedido
* Status do pedido

# Editar itens e cliente de um pedido

Edite um pedido em andamento quando o cliente pedir mais um item, corrigir uma observação ou trocar dados de contato. A edição funciona em qualquer status, mas o ajuste financeiro do que foi adicionado fica por conta da equipe acertar com o cliente fora do Dionísio.

## Como acessar

No menu lateral, clique em **Pedidos**. Localize o pedido no kanban, clique no card para abrir as ações e escolha **Editar Cliente** ou **Editar Itens**.

## Passos — Editar Cliente

1. Clique no card do pedido.
2. No menu de ações, clique em **Editar Cliente**.
3. Atualize os campos disponíveis (nome, telefone, e-mail, CPF, observações).
4. Clique em **Salvar**.

## Passos — Editar Itens

1. Clique no card do pedido.
2. No menu de ações, clique em **Editar Itens**.
3. No painel de edição:
   * **Adicionar item:** clique no produto no cardápio e configure complementos.
   * **Remover item:** clique no ícone de lixeira ao lado do item no carrinho.
   * **Ajustar quantidade:** use os controles de + e − ao lado do item.
4. Clique em **Salvar**.

O total do pedido é recalculado automaticamente para refletir as mudanças.

## Quando faz sentido editar

A edição existe principalmente para um cenário: **o cliente entrou em contato depois do pedido criado e quer mais alguma coisa**. Em vez de criar um pedido novo, você adiciona ao existente.

| Situação                                                 | Edita?                                                                                                                              |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Cliente pede um item extra logo depois de criar o pedido | Sim, **Editar Itens**                                                                                                               |
| Cliente errou o telefone ou nome no Link Público         | Sim, **Editar Cliente**                                                                                                             |
| Cliente quer trocar de delivery para retirada            | Não — cancele e crie um pedido novo                                                                                                 |
| Cliente quer trocar o endereço de entrega                | Não — use Aceitar troca de endereço, que tem fluxo próprio |
| Cozinha errou o item e quer substituir                   | Sim, **Editar Itens**                                                                                                               |

## Dicas e observações

> ⚠️ **Atenção:** a edição **não dispara notificação no WhatsApp para o cliente**. Se você adicionar itens, comunique o cliente por outro canal para evitar surpresa na entrega.

> ⚠️ **Atenção:** o sistema **não cobra automaticamente** o valor extra dos itens adicionados. O acerto financeiro do que foi acrescentado fica fora do Dionísio — combine direto com o cliente (PIX externo, cartão, dinheiro no momento da entrega).

> ℹ️ **Observação:** edição funciona em qualquer status, inclusive **Saiu para Entrega**, mas faz pouco sentido editar pedidos já em rota. Use com cuidado quando o pedido está prestes a ser entregue.

## Próximos passos

* Acompanhar pedidos
* Aceitar troca de endereço

# Atribuir motorista

Em pedidos de **delivery**, o motorista é quem efetivamente leva o pedido até o cliente. O Dionísio combina três opções: motoristas internos cadastrados pelo restaurante, **iFood Shipping** e **Lalamove**. Para a maioria dos pedidos, você não precisa fazer nada — o Dionísio decide sozinho. Esta página cobre o automático e como forçar um provedor específico.

## Como acessar

No menu lateral, clique em **Pedidos**. Localize o pedido de delivery no kanban e clique no card.

## Como o automático funciona

Quando um pedido de delivery entra em **Confirmado**:

1. O Dionísio cota a taxa de entrega em **iFood Shipping** e **Lalamove** em paralelo, considerando apenas os provedores que você ativou em Integrações.
2. Escolhe o provedor com a taxa **mais barata** entre as cotações que retornaram com sucesso.
3. Solicita o motorista automaticamente. Você não precisa clicar em nada.
4. O card passa a mostrar o status da entrega externa e um **link para acompanhar** no painel do provedor.

Se nenhum provedor externo estiver ativo, o pedido segue sem motorista automático e você atribui um motorista interno manualmente.

## Forçar um provedor específico

Quando você prefere usar **iFood Shipping** ou **Lalamove** em vez do automático — por exemplo, porque um provedor está com tempo de espera melhor no momento — abra o detalhe do pedido e use os botões dedicados:

1. Clique no card do pedido em **Confirmado**.
2. No painel de detalhes, clique em **Solicitar via iFood** ou **Solicitar via Lalamove**.
3. O Dionísio pede o motorista direto naquele provedor, ignorando a cotação automática.
4. O link de acompanhamento aparece no card.

Para cancelar uma solicitação externa em andamento, use o botão **Cancelar entrega** no mesmo painel.

## Motoristas internos

Se o restaurante tem entregadores próprios cadastrados em Configuração de Entrega → Motoristas, eles aparecem como opção paralela.

Para atribuir um motorista interno:

1. Clique no card do pedido.
2. No menu de ações, clique em **Atribuir motorista**.
3. Escolha o motorista na lista.
4. Clique em **Confirmar**.

O motorista interno fica registrado no pedido e aparece no filtro **Entregador** do Histórico de Pedidos. Não há comunicação automática com ele pelo Dionísio — combine o despacho fora do sistema.

## Comportamento em caso de erro

| Cenário                                          | O que acontece                                                                                                                                                        |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nenhum motorista Lalamove aceitou em 60 segundos | O Dionísio aumenta a gorjeta proposta automaticamente para atrair motorista.                                                                                          |
| Lalamove retornou erro na solicitação            | O Dionísio tenta nova solicitação ao Lalamove uma vez. Se falhar de novo, o pedido segue sem motorista externo e você pode atribuir um interno ou tentar manualmente. |
| iFood Shipping não cotou                         | Lalamove vence a cotação por padrão; se também falhar, o pedido segue sem motorista externo.                                                                          |
| Você cancelou a entrega externa                  | O motorista externo é dispensado. Você pode reatribuir manualmente.                                                                                                   |

## Dicas e observações

> 💡 **Dica:** mantenha a integração de iFood Shipping e Lalamove ativas ao mesmo tempo. Como o Dionísio escolhe o mais barato, você nunca paga taxa a mais por ter os dois ligados.

> ℹ️ **Observação:** apenas pedidos do tipo **Delivery** disparam motorista. Pedidos de **Retirada** ficam aguardando o cliente buscar.

## Próximos passos

* Acompanhar pedidos
* Configuração de Entrega

# Aceitar troca de endereço

Quando o cliente percebe que digitou o endereço errado ou precisa receber em outro local, ele pode pedir a troca pelo link de acompanhamento do pedido. O sistema avisa você com um banner no card e dois botões — você decide se aceita.

## Como acessar

No menu lateral, clique em **Pedidos** → aba **Delivery**. Pedidos com solicitação de troca de endereço mostram um **banner laranja** no topo do card.

## Passos

1. Localize o pedido com o banner de troca de endereço.
2. Confira o **endereço proposto** exibido no banner (rua, número, bairro, cidade, referência).
3. Compare com o endereço original do pedido.
4. Clique em **Aceitar** ou **Recusar**.
5. Se recusar, escolha um **motivo** na lista.

Quando você **Aceita**, o endereço do pedido é atualizado para o novo endereço, e o motorista (se já saiu) recebe a alteração no provedor de entrega.

Quando você **Recusa**, o pedido segue para o endereço original e o cliente é notificado com o motivo.

## Quando aceitar e quando recusar

A decisão depende de quando o pedido está e da distância da troca:

| Situação                                                                      | Recomendação                                                   |
| ----------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Pedido ainda em **Novo** ou **Confirmado**, novo endereço dentro da cobertura | Aceite — sem prejuízo operacional.                             |
| Pedido em **Saiu para Entrega**, novo endereço perto do original              | Aceite e comunique o motorista direto.                         |
| Pedido em **Saiu para Entrega**, novo endereço longe do original              | Recuse e oriente o cliente a fazer um pedido novo.             |
| Novo endereço fora da área de cobertura configurada                           | Recuse com motivo correspondente.                              |
| Cliente fez vários pedidos seguidos de troca                                  | Atenção — pode ser tentativa de fraude. Confirme por telefone. |

## Dicas e observações

> ℹ️ **Observação:** o cliente inicia a troca pelo link de acompanhamento do pedido — você não precisa fazer nada para abrir o pedido para troca. Quando ele envia, o banner aparece automaticamente.

> ⚠️ **Atenção:** trocas aceitas após o pedido sair para entrega podem virar reentrega. Verifique distância e custo antes de aceitar.

> 💡 **Dica:** se o cliente entrar em contato pelo WhatsApp pedindo a troca em vez de usar o link, oriente-o a abrir o link de acompanhamento e pedir por lá — assim o pedido fica registrado no histórico e o motorista recebe a alteração automática.

## Próximos passos

* Acompanhar pedidos
* Atribuir motorista

# Histórico de Pedidos

O **Histórico de Pedidos** lista todos os pedidos finalizados ou cancelados do restaurante — tanto do canal próprio do Dionísio quanto do iFood integrado. É a tela que você consulta para conferir vendas, encontrar um pedido antigo, ver pedidos cancelados ou exportar dados para fechamento de caixa.

## Como acessar

No menu lateral, clique em **Pedidos** → **Histórico** (botão no topo da tela).

## Passos

1. Aplique os filtros que precisar (data, fonte, tipo, status, busca).
2. Escolha o modo de visualização: **Grade**, **Lista** ou **Calendário**.
3. (Opcional) Clique em **Exportar** para baixar os pedidos exibidos.
4. Clique em qualquer pedido para abrir os detalhes.

## Modos de visualização

| Modo           | Quando usar                                                                                                                                                                                                     |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Grade**      | Exibe pedidos como cards. Cada card mostra cliente, total, status, forma de pagamento e canal. Bom para consulta visual rápida.                                                                                 |
| **Lista**      | Exibe em formato de tabela densa. Mais linhas visíveis por vez. Bom para varrer muitos pedidos.                                                                                                                 |
| **Calendário** | Visão mensal. Cada dia mostra o **total em R$** e o **número de pedidos**. Dias sem pedidos ficam em branco. Use as setas para navegar entre meses. Clique em um dia para abrir a lista de pedidos daquele dia. |

## Filtros

| Filtro             | Opções                                                                                                  | O que faz                                                                                                            |
| ------------------ | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Buscar pedidos** | Texto livre                                                                                             | Busca por número do pedido, nome do cliente ou telefone.                                                             |
| **Fonte**          | Todos, Dionísio, iFood                                                                                  | Filtra pelo canal de origem.                                                                                         |
| **Tipo**           | Todos, Delivery, Retirada, Mesa                                                                         | Filtra pelo tipo de atendimento.                                                                                     |
| **Status**         | Criado, Confirmado, Em Preparo, Pronto para Retirada, Saiu para Entrega, Entregue, Concluído, Cancelado | Filtra pelo status do pedido. Veja Status do pedido. |
| **Período**        | Data início e fim                                                                                       | Restringe ao intervalo. Por padrão mostra o mês atual.                                                               |
| **Limpar Filtros** | —                                                                                                       | Remove todos os filtros aplicados.                                                                                   |

## Exportar

Clique em **Exportar** para baixar um arquivo com os pedidos atualmente exibidos. Os filtros valem para a exportação — restrinja o período ou os tipos antes de exportar para evitar arquivos grandes demais.

## Dicas e observações

> 💡 **Dica:** use o modo **Calendário** no fim do mês para encontrar o dia de maior faturamento e o de menor — facilita planejamento de equipe e estoque.

> ℹ️ **Observação:** pedidos cancelados pela regra de 10 minutos aparecem com status **Cancelado** e o motivo "Cancelada automaticamente após 10 minutos sem confirmação" no detalhe.

> ℹ️ **Observação:** pedidos do **iFood** aparecem aqui com **Fonte = iFood**. Para análise separada por canal, use o filtro **Fonte**.

> ⚠️ **Atenção:** pedidos com pagamento online não confirmado (PIX não pago, cartão recusado) **não aparecem no kanban operacional**, mas podem aparecer no histórico dependendo do que aconteceu depois. Eles não contam como faturamento.

## Próximos passos

* Acompanhar pedidos
* Status do pedido
* Relatórios

# Status do pedido

Esta página lista todos os status de um pedido no Dionísio, como cada um é atingido e quais automações movem pedidos entre estados sem ação humana. Consulte ao operar o kanban, filtrar o histórico ou diagnosticar por que um pedido sumiu de uma aba.

## Onde aparece

Esses status aparecem no kanban da tela Pedidos, no filtro **Status** do Histórico de Pedidos, nas mensagens automáticas que o cliente recebe no WhatsApp e nos dados exportados.

## Status visíveis ao operador

| Status oficial              | O que significa                                                                                                                                                    |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Novo**                    | Pedido recém-criado aguardando confirmação. Se **Aceitar Pedidos Automaticamente** estiver ligado, o pedido pula esse status.                                      |
| **Confirmado**              | Pedido aceito. Em delivery, dispara a cotação automática de motorista.                           |
| **Em Preparo**              | Pedido entrou na cozinha. Aparece como sub-estado de **Confirmado** no kanban; é exibido separadamente apenas quando integrações externas reportam essa transição. |
| **Pronto para Entrega**     | Delivery pronto, aguardando o motorista pegar. Visível só no modo expandido da aba Delivery.                                                                       |
| **Saiu para Entrega**       | Motorista a caminho do cliente.                                                                                                                                    |
| **Pronto para Retirada**    | Retirada pronta, aguardando o cliente.                                                                                                                             |
| **Entregue**                | Cliente recebeu o pedido (delivery) ou retirou (retirada).                                                                                                         |
| **Concluído**               | Pedido finalizado e fechado. Sai do kanban operacional.                                                                                                            |
| **Cancelado**               | Pedido cancelado por ação manual ou pela regra de 10 minutos.                                                                                                      |
| **Cancelamento Solicitado** | Cliente pediu para cancelar pelo link de acompanhamento. Aguardando decisão do restaurante.                                                                        |
| **Cancelamento Negado**     | Restaurante recusou a solicitação de cancelamento do cliente.                                                                                                      |

## Automações

Três regras movem pedidos entre status sem ação humana. Conhecer essas regras evita estranheza quando um pedido "muda sozinho" no kanban.

| Regra                               | Quando dispara                                                                                                                                                 | O que faz                                                                                                                                            |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Aceitar Pedidos Automaticamente** | Toggle em Configuração de Entrega. Quando ligado, todo pedido novo entra direto em Confirmado. | **Novo → Confirmado** sem clique.                                                                                                                    |
| **Auto-cancelamento de 10 minutos** | Pedido em **Novo** há 10 minutos sem você clicar em **Avançar** ou **Recusar**.                                                                                | **Novo → Cancelado** automático, com nota "Cancelada automaticamente após 10 minutos sem confirmação". Dispara estorno se houver pagamento pré-pago. |
| **Auto-conclusão de 24 horas**      | Pedido em **Confirmado**, **Em Preparo**, **Pronto para Entrega**, **Saiu para Entrega**, **Pronto para Retirada** ou **Entregue** há mais de 24 horas.        | Vira **Concluído** automático, com nota "Concluída automaticamente após 24 horas".                                                                   |

> ℹ️ **Observação:** a regra de 24 horas roda de hora em hora. Um pedido que completa 24h pode levar até 1 hora para mudar de status — não é imediato.

## Notificações no WhatsApp por status

O cliente recebe uma mensagem automática a cada mudança de status, exceto em **Novo**. Os status intermediários enviam mensagem com link de acompanhamento; os finais enviam só texto.

| Status                      | Mensagem ao cliente                               |
| --------------------------- | ------------------------------------------------- |
| **Confirmado**              | "Pedido confirmado" — com link                    |
| **Em Preparo**              | "Pedido em preparo" — com link                    |
| **Pronto para Retirada**    | "Pedido pronto para retirada" — com link          |
| **Saiu para Entrega**       | "Pedido enviado" — com link                       |
| **Cancelamento Solicitado** | "Solicitação de cancelamento recebida" — com link |
| **Entregue**                | "Pedido entregue" — sem link                      |
| **Concluído**               | "Pedido concluído" — sem link                     |
| **Cancelado**               | "Pedido cancelado" — sem link                     |
| **Cancelamento Negado**     | "Cancelamento negado" — sem link                  |

Não há configuração para desligar essas notificações. Toda loja com conexão WhatsApp ativa envia.

## Estados internos de pagamento

Existem dois estados que aparecem só nas mensagens ao cliente e no banco de dados, **sem aparecer no kanban operacional**:

| Estado interno               | Significado                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------ |
| **Aguardando Pagamento PIX** | Cliente escolheu PIX online e o pagamento ainda não foi confirmado pelo banco. |
| **Pagamento Recusado**       | Cartão online recusado pelo adquirente.                                        |

Pedidos nesses estados são "limbo de pagamento" — não entram no kanban porque ainda não há pedido confirmado para a equipe operar. Se o pagamento confirma, o pedido entra como **Novo** (ou **Confirmado**, se o auto-aceitar estiver ligado).

## Repasse financeiro e cancelamento

Cada pedido tem um indicador interno de **repasse financeiro** — quando o valor foi transferido para o restaurante. Pedidos repassados não podem mais ser cancelados pelo Dionísio.

| Forma de pagamento       | Prazo para repasse                                                       |
| ------------------------ | ------------------------------------------------------------------------ |
| **PIX**                  | 1 dia após pagamento confirmado.                                         |
| **Cartão**               | 30 dias após pagamento confirmado.                                       |
| **Pagamento na entrega** | Não há repasse pela Dionísio — o dinheiro vai direto para o restaurante. |

> ⚠️ **Atenção:** se você tentar cancelar um pedido já repassado, o sistema retorna erro. O ajuste com o cliente nesse caso precisa ser feito fora do Dionísio.

## Relacionado

* Acompanhar pedidos
* Histórico de Pedidos
* Atribuir motorista
* Configuração de Entrega
