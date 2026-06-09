# Configuração de Entrega

**Configuração de Entrega** é onde você define todas as regras do canal próprio de pedidos do restaurante: o que cobra, quando aceita, em quais regiões entrega e como o cliente paga. Tirando o cardápio (que você configura em paralelo), é tudo o que precisa estar pronto antes de aceitar o primeiro pedido.

## Para quem é

* **Dono** e **Administrador** — configuram a tela no onboarding e revisam periodicamente. Acesso por padrão.
* **Membro** — só vê a tela se o Administrador tiver habilitado a permissão. Detalhes em Pessoas.

## O que você pode fazer

* Configuração Geral — valores, pagamentos, tipos de pedido, agendamento e tipo de cálculo da taxa de entrega.
* Horários de Entrega — dias e turnos em que o canal próprio aceita pedidos.
* Cobertura de Entrega — raio, área personalizada ou cobrança por bairro.

## Abas da tela

| Aba                      | O que define                                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Configuração Geral**   | Valor mínimo, **Valor para Frete Grátis**, formas de pagamento, tipos de pedido aceitos, agendamento e tipo de cálculo da taxa de entrega. |
| **Horários de Entrega**  | Dias da semana e turnos em que o Link Público aceita pedidos.                                                                              |
| **Cobertura de Entrega** | Regiões geográficas que você atende, com taxa por região.                                                                                  |
| **Motoristas**           | **Em desenvolvimento.** A aba existe na tela mas a operação ainda não está ativa.                                                          |

## Atenções para o setup inicial

Três pontos que mais geram confusão depois de ativar o módulo:

> ⚠️ **Atenção:** o **Valor para Frete Grátis** vem em **R$ 0,00** por padrão. Se você não alterar, **todos os pedidos saem sem cobrança da taxa de entrega**, porque qualquer valor é "acima de zero".

> ⚠️ **Atenção:** o **endereço da loja em** **Minha Loja** **precisa estar com latitude e longitude válidos** para a cobertura por raio funcionar. Sem isso, o mapa cai para coordenadas de São Paulo como fallback e sua cobertura fica centrada no lugar errado — sem mensagem de erro.

> ⚠️ **Atenção:** se você escolher **Tipo de Cálculo de Distância → Por Bairro** e não cadastrar bairros na Cobertura, o Link Público quebra para o cliente — ele tenta escolher o bairro mas não tem opções.

## Integrações e canais

* **Minha Loja** — endereço da loja é o centro do cálculo de cobertura.
* **Pedidos** — consome todas as regras: cobertura, taxa, horário, aceitar automaticamente, agendamento.
* **Cardápios** — itens ativos formam o catálogo do Link Público.
* **Configuração de IA** — a Assistente IA usa o tipo de cálculo, a antecedência mínima de agendamento e os horários automaticamente, sem configuração extra.
* **Integrações** — quando iFood Shipping ou Lalamove estão conectados, aparece o campo **Atraso para Chamar Entregador** na Configuração Geral.
* **Link Público de Pedidos** — lê todas essas regras em tempo real.

## Começando

No primeiro acesso, configure nesta ordem:

1. Configuração Geral — atenção especial ao **Valor para Frete Grátis**.
2. Horários de Entrega — defina os turnos em que aceita pedidos.
3. Cobertura de Entrega — desenhe raios ou áreas.

Salve cada aba antes de passar para a próxima. **Configuração Geral** e **Horários de Entrega** compartilham o mesmo botão **Salvar Configuração** — confirme antes de trocar de aba.

## Próximos passos

* Cadastrar Cardápios
* Configurar Endereço em Minha Loja
* Pedidos

# Configuração Geral

A aba **Configuração Geral** concentra os valores e as regras de comportamento do canal próprio de pedidos: quanto você cobra, o que aceita como pagamento, em quais condições aceita pedido e como calcula a taxa de entrega.

## Antes de começar

Você precisa de:

* Plano de Pedidos ativo.
* Endereço da loja preenchido em Minha Loja.

## Como acessar

No menu lateral, clique em **Configuração de Entrega** → aba **Configuração Geral**.

## Passos

1. Preencha os campos da seção **Configurações de Entrega** (descritos abaixo).
2. (Opcional) Ligue **Permitir Agendamento de Pedidos** e ajuste a antecedência.
3. Clique em **Salvar Configuração** no canto superior direito.

> ℹ️ **Observação:** o botão **Salvar Configuração** persiste tanto a aba **Configuração Geral** quanto a aba **Horários de Entrega**. Se você editar nas duas, salve uma vez ao final — não há salvamento separado por aba.

## Configurações de Entrega

| Campo                                | Padrão     | Descrição                                                                                                                                                             |
| ------------------------------------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Valor Mínimo do Pedido**           | R$ 0,00    | Pedidos abaixo desse valor não são aceitos pelo Link Público.                                                                                                         |
| **Valor para Frete Grátis**          | R$ 0,00    | Pedidos acima desse valor saem sem cobrança de taxa de entrega. **Atenção: em R$ 0,00, todos os pedidos saem sem cobrança.**                                          |
| **Tipo de Cálculo de Distância**     | Linha Reta | Como a taxa de entrega é calculada. Três opções, detalhadas abaixo.                                                                                                   |
| **Aceitar Pagamentos na Entrega**    | Ligado     | Cliente paga ao receber: dinheiro, cartão ou PIX no momento da entrega.                                                                                               |
| **Aceitar Cartão de Crédito Online** | Ligado     | Habilita pagamento online por cartão no momento do pedido.                                                                                                            |
| **Aceitar PIX Online**               | Ligado     | Habilita pagamento online por PIX no momento do pedido.                                                                                                               |
| **Permitir Entrega**                 | Ligado     | Liga ou desliga o canal de delivery. Se desligar, o Link Público não oferece entrega.                                                                                 |
| **Permitir Retirada no Local**       | Ligado     | Liga ou desliga retirada no balcão no Link Público.                                                                                                                   |
| **Aceitar Pedidos Automaticamente**  | Desligado  | Quando ligado, pedidos novos viram **Confirmado** sem aprovação manual. Recomendado para operações com alto volume.                                                   |
| **Atraso para Chamar Entregador**    | —          | **Só aparece com iFood Shipping ou Lalamove conectado.** Minutos que o sistema espera depois do pedido virar Confirmado antes de pedir motorista. Máximo 120 minutos. |

### Tipo de Cálculo de Distância

A escolha do modo afeta como a taxa de entrega é calculada e como o cliente preenche o endereço no Link Público:

* **Linha Reta** *(recomendado)* — calcula a distância em linha reta entre o endereço do restaurante e o endereço do cliente. Funciona com cobertura por raio. É a opção mais simples e cobre a maioria dos casos.
* **Distância por Rota** — calcula a distância real pelas ruas, via Google Maps. Mais preciso em cidades onde a distância em linha reta não reflete bem o trajeto real (rios, vias bloqueadas).
* **Por Bairro** — ignora distância e cobra uma taxa fixa por bairro. O cliente escolhe o bairro no Link Público e o sistema aplica a taxa. **Use apenas se o Google Maps não funcionar bem na sua região** — em outros casos, Linha Reta é mais confiável.

> ℹ️ **Observação:** no modo **Por Bairro**, o sistema **não valida** se o endereço digitado pelo cliente realmente corresponde ao bairro escolhido. A taxa é aplicada com base no que o cliente seleciona.

## Agendamento de Pedidos

Habilita o cliente a fechar um pedido para uma data e hora futuras (por exemplo, almoço de domingo no sábado à noite).

| Campo                               | Padrão    | Descrição                                                          |
| ----------------------------------- | --------- | ------------------------------------------------------------------ |
| **Permitir Agendamento de Pedidos** | Desligado | Liga o agendamento no Link Público.                                |
| **Antecedência Mínima (minutos)**   | 30        | Tempo mínimo entre o momento do agendamento e o horário escolhido. |
| **Antecedência Máxima (dias)**      | 7         | Janela máxima para agendar adiante.                                |

> ⚠️ **Atenção:** se a antecedência mínima for maior que a máxima, o sistema bloqueia o salvamento com mensagem de erro.

## Dicas e observações

> 💡 **Dica:** depois de salvar, faça um pedido teste pelo Link Público para conferir como a taxa de entrega está sendo calculada. Pequenos erros (**Valor para Frete Grátis** em R$ 0,00 ou raios mal configurados) só aparecem na simulação.

> ℹ️ **Observação:** mudanças nesta aba valem **imediatamente para novos pedidos**. Pedidos já no kanban não são afetados — se você desligar PIX Online agora, pedidos que já estavam no fluxo do PIX seguem normalmente.

> ⚠️ **Atenção:** ao salvar, o sistema exige **pelo menos uma das opções ativas** entre **Permitir Entrega** e **Permitir Retirada no Local**. Se desligar as duas, aparece um banner de erro e o salvamento é bloqueado.

## Próximos passos

* Horários de Entrega
* Cobertura de Entrega
* Pedidos

# Horários de Entrega

A aba **Horários de Entrega** define em quais dias da semana e quais turnos o canal próprio aceita pedidos. É independente dos horários gerais da loja: você pode ter o salão aberto sem aceitar delivery, ou vice-versa.

## Antes de começar

Você precisa de:

* Plano de Pedidos ativo.

## Como acessar

No menu lateral, clique em **Configuração de Entrega** → aba **Horários de Entrega**.

## Passos

1. Para cada **dia da semana**, ative ou desative com o **toggle**.
2. No dia ativado, defina o **Horário de Abertura** e o **Horário de Fechamento** do turno.
3. (Opcional) Clique em **+ Adicionar horário** para criar um segundo turno no mesmo dia.
4. Clique em **Salvar Configuração** no canto superior direito.

> ℹ️ **Observação:** o botão **Salvar Configuração** persiste tanto a aba **Horários de Entrega** quanto a aba **Configuração Geral**. Se editou nas duas, salve uma vez ao final.

## Casos comuns

### Dia com dois turnos (almoço e jantar)

Restaurantes que operam em duas janelas separadas — fecham à tarde e reabrem à noite — configuram dois turnos no mesmo dia:

1. Defina o primeiro turno (ex: 11:30 às 14:30).
2. Clique em **+ Adicionar horário**.
3. Defina o segundo turno (ex: 18:00 às 23:00).
4. Salve.

Entre os turnos, o Link Público fica fechado.

### Turno que atravessa a meia-noite

Restaurantes noturnos costumam aceitar pedidos passando da meia-noite — por exemplo, 22:00 até 02:00 do dia seguinte. Configure como um único turno e o sistema **divide automaticamente** entre os dois dias da semana:

1. No dia que começa o turno (ex: sábado), defina 22:00 às 02:00.
2. O sistema entende que 00:00 às 02:00 vale para o dia seguinte (domingo).

Você não precisa criar dois turnos manualmente para isso.

### Dia inteiro fechado

Para um dia em que o restaurante não aceita pedidos pelo canal próprio (mesmo que o salão esteja aberto), **desligue o toggle do dia**. O Link Público mostra "fechado" naquele dia.

## Diferença para os Horários da Loja

A aba **Horários de Entrega** é independente da configuração de Horários, onde você define os horários gerais do estabelecimento. Os dois servem a propósitos diferentes:

| Tela                        | Para que serve                                                           |
| --------------------------- | ------------------------------------------------------------------------ |
| **Horários** (módulo geral) | Horário do salão, recepção, exibido no Google Meu Negócio e em vitrines. |
| **Horários de Entrega**     | Quando o Link Público e a Assistente IA aceitam pedidos.                 |

Você pode ter o salão aberto das 18:00 às 00:00 e o delivery aceitando até 22:00, por exemplo.

## Dicas e observações

> 💡 **Dica:** ajuste o horário de fechamento do delivery para fechar antes do salão. Assim, a cozinha tem folga para terminar os últimos pedidos sem virar a noite.

> ℹ️ **Observação:** mudanças nos horários valem imediatamente para novos acessos ao Link Público. Pedidos já criados não são afetados — quem agendou para um horário que você desativou depois continua válido.

> ⚠️ **Atenção:** se o cliente tentar agendar um pedido para um horário fora dessa janela (e o agendamento estiver habilitado em Configuração Geral), o Link Público bloqueia a escolha.

## Próximos passos

* Configuração Geral
* Cobertura de Entrega
* Horários (módulo geral)

# Cobertura de Entrega

A aba **Cobertura de Entrega** é onde você desenha no mapa as regiões que o restaurante atende e qual taxa de entrega cobra em cada uma. Combina três modos: **Por Raio** (área circular), **Por Área Personalizada** (polígono livre) e **Por Bairro** (lista de bairros).

## Antes de começar

Você precisa de:

* Plano de Pedidos ativo.
* **Endereço completo da loja em** **Minha Loja****, com latitude e longitude válidos.** Sem coordenadas válidas, o mapa cai para São Paulo como fallback e sua cobertura fica centrada no lugar errado.

## Como acessar

No menu lateral, clique em **Configuração de Entrega** → aba **Cobertura de Entrega**.

## Modos de cobertura

Você combina três modos no mesmo mapa. Use raio para a cobertura padrão, áreas personalizadas quando precisar de polígonos livres (e para criar exclusões) e bairros apenas quando o **Tipo de Cálculo de Distância** estiver em **Por Bairro**.

### Por Raio

Crie um ou mais raios circulares ao redor do endereço da loja, cada um com sua taxa.

1. Clique em **Adicionar Raio**.
2. Digite o **raio em quilômetros** (ex: 3 km).
3. Digite a **taxa de entrega** para esse raio (ex: R$ 5,00).
4. Clique em **Salvar**.

Repita para criar raios maiores com taxas progressivas — por exemplo: 3 km a R$ 5,00, 5 km a R$ 8,00, 7 km a R$ 12,00.

Quando o cliente está dentro de **mais de um raio** ao mesmo tempo, o sistema aplica a taxa do **raio mais próximo do centro da loja**. Por isso, raios menores cobrem regiões próximas e raios maiores capturam apenas o anel que sobra.

### Por Área Personalizada

Quando o raio circular não representa bem sua área de atendimento — por exemplo, sua rua principal é longa mas você não entrega para os lados —, desenhe um polígono diretamente no mapa.

1. Clique em **Adicionar Área Personalizada**.
2. Selecione o tipo: **Incluir** (a região passa a ser atendida) ou **Excluir** (a região vira um "buraco" dentro do raio).
3. Clique no mapa para marcar os pontos do polígono — cada clique adiciona um vértice.
4. Quando terminar de desenhar, clique em **Finalizar Desenho**.
5. Digite a **taxa de entrega** para essa área (apenas em áreas do tipo Incluir).
6. Clique em **Salvar**.

Use o tipo **Excluir** para tirar pedaços da cobertura existente: um rio que você não atravessa, um condomínio fechado que não atende, um bairro problemático no meio da sua área. A área excluída sobrepõe qualquer raio ou área de inclusão — clientes dentro de uma região excluída não conseguem pedir, mesmo que estejam dentro de um raio válido.

### Por Bairro

Use **apenas se** o **Tipo de Cálculo de Distância** estiver definido como **Por Bairro** em Configuração Geral. Nesse modo, o cliente escolhe o bairro no Link Público e o sistema aplica a taxa cadastrada.

1. Clique em **Adicionar Bairro**.
2. Digite o **nome do bairro**.
3. Digite a **taxa de entrega** para esse bairro.
4. Clique em **Salvar**.

Repita para cada bairro que você atende.

> ⚠️ **Atenção:** se você ativou **Tipo de Cálculo → Por Bairro** mas não cadastrou nenhum bairro aqui, **o Link Público quebra** — o cliente não tem opções para escolher e não consegue finalizar o pedido.

> ℹ️ **Observação:** no modo **Por Bairro**, o sistema não verifica se o endereço digitado pelo cliente realmente corresponde ao bairro escolhido. A taxa é aplicada com base na seleção dele.

## Dicas e observações

### Excluir uma região cadastrada

Para remover um raio, área personalizada ou bairro existente, clique na região na lista lateral ou no mapa, clique em **Excluir** ou no ícone de lixeira e confirme. Pedidos passados que usaram essa região continuam normalmente — a exclusão não afeta histórico, apenas remove a região para pedidos futuros.

> 💡 **Dica:** comece pelo raio mais simples (um círculo de 3 a 5 km com taxa única) e refine depois. Em vez de tentar configurar tudo de uma vez, faça pedidos teste pelo Link Público para identificar onde a cobertura falha.

> 💡 **Dica:** confira o endereço da loja em Minha Loja antes de desenhar raios. Se o ponto central do mapa estiver no Brasil mas longe da sua loja, é sinal de que a loja ainda não tem latitude e longitude válidos.

> ℹ️ **Observação:** mudanças na cobertura valem imediatamente para novos acessos ao Link Público. Cliente com o link aberto precisa recarregar a página para ver a atualização. Pedidos já no kanban não são afetados.

## Próximos passos

* Configuração Geral
* Horários de Entrega
* Configurar Endereço em Minha Loja
