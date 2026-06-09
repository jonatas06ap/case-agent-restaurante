# Satisfação

O módulo de **Satisfação** cria e gerencia **Pesquisas de Satisfação** (NPS) — os formulários que seus clientes respondem para avaliar a experiência no restaurante. Você monta a pesquisa com as perguntas que quiser, divulga por link ou QR Code, deixa o Dionísio enviá-la sozinho pelo WhatsApp após cada visita e acompanha os resultados em um painel com o NPS Score e a divisão entre promotores, neutros e detratores. É o canal para transformar a opinião de quem já foi atendido em um indicador acompanhável ao longo do tempo.

## Para quem é

* **Dono e gerente** — criam e configuram as pesquisas, definem as perguntas, escolhem recompensas, configuram o envio automático e analisam os resultados.

## Como acessar

No menu lateral esquerdo, clique em **Satisfação**. Você verá a tela **Gerenciamento de Pesquisas NPS** com todas as pesquisas cadastradas no restaurante.

## O que você pode fazer

* Criar uma pesquisa de satisfação
* Gerenciar as perguntas da pesquisa
* Compartilhar a pesquisa por link e QR Code
* Enviar a pesquisa automaticamente pelo WhatsApp
* Acompanhar as respostas
* Analisar os resultados

## Principais conceitos

* O que é NPS — a régua de promotores, neutros e detratores, o cálculo do NPS Score e a diferença entre a nota geral de 1 a 10 e a pergunta de avaliação de 1 a 5.

## Integrações e canais

* **WhatsApp** — a pesquisa pode ser enviada automaticamente após reserva, pedido ou fila. As mensagens saem pelo número de WhatsApp conectado ao estabelecimento; sem conexão, a Dionísio envia pelo número oficial dela. Veja Enviar a pesquisa automaticamente pelo WhatsApp. Se as pesquisas não estão chegando, veja Pesquisas não estão sendo enviadas.
* **Cupons** — você pode vincular um cupom de recompensa à pesquisa, entregue ao cliente na tela de agradecimento. A lista de cupons disponíveis vem do módulo **Cupons** e traz apenas cupons de **código único e ativos** (cada respondente recebe um código individual). Crie o cupom em **Cupons** antes de selecioná-lo na pesquisa.
* **Clientes** — quando a resposta está vinculada a um cliente, ela aparece associada ao cadastro dele.

## Começando

Se você está configurando o módulo pela primeira vez, siga nesta ordem:

1. Criar uma pesquisa de satisfação — defina nome, slug e, se quiser, um cupom de recompensa e o link de avaliação no Google.
2. Gerenciar as perguntas da pesquisa — adicione as perguntas e deixe a pesquisa com o status **Ativo**.
3. Compartilhar a pesquisa ou configurar o envio automático pelo WhatsApp — leve a pesquisa até os clientes.
4. Analisar os resultados — acompanhe o NPS Score e a evolução da satisfação por período.

# O que é NPS

**NPS** (Net Promoter Score) é uma forma de medir a lealdade do cliente a partir de uma única pergunta de recomendação. No Dionísio, ele aparece na **Pesquisa de Satisfação**: o cliente dá uma nota e essa nota o classifica em uma de três faixas — **promotor**, **neutro** ou **detrator**. O painel da pesquisa (aba **Analytics**) consolida essas faixas em um número-resumo, o **NPS Score**. É um conceito que pede atenção porque o Dionísio usa **duas escalas diferentes** na mesma pesquisa: a nota geral de **1 a 10** e uma pergunta de avaliação de **1 a 5** — e só a primeira gera o NPS Score.

## Como funciona

### A nota geral (1 a 10)

Toda resposta da Pesquisa de Satisfação tem uma nota geral de recomendação, em uma escala de **1 a 10**. É a pergunta clássica de NPS ("o quanto você recomendaria"). O cliente responde tocando em um número de 1 a 10, com a legenda indo de **Nada provável** a **Extremamente provável**.

Cada nota cai em uma faixa:

| Faixa        | Notas  | Significado                              |
| ------------ | ------ | ---------------------------------------- |
| **Detrator** | 1 a 6  | Cliente insatisfeito; tende a falar mal. |
| **Neutro**   | 7 a 8  | Cliente satisfeito, mas não engajado.    |
| **Promotor** | 9 a 10 | Cliente leal; tende a recomendar.        |

Essas faixas estão fixadas no código do painel: detrator quando a nota é **menor ou igual a 6**, neutro entre **7 e 8**, promotor **9 ou 10**.

### O NPS Score (cálculo)

O **NPS Score** é o número-resumo que aparece no card **NPS Score (promotores − detratores)** da aba **Analytics**. Ele é calculado sobre as notas gerais (1 a 10) das respostas no período selecionado:

**NPS Score = % de promotores − % de detratores** (os neutros não somam nem subtraem), arredondado para o inteiro mais próximo.

O resultado vai de −100 (todos detratores) a +100 (todos promotores). Quando não há nenhuma nota geral no período, o card mostra **—**.

A aba **Analytics** ainda mostra, sobre essa mesma escala 1–10: **Promotores (9–10)**, **Neutros (7–8)**, **Detratores (1–6)** e **Média NPS geral (1–10)**.

### A pergunta de avaliação (1 a 5) — escala separada

Além da nota geral, uma pesquisa pode ter perguntas do tipo **NPS Score** com escala de **1 a 5**. Não confunda com o NPS Score do parágrafo anterior: aqui é um *tipo de pergunta* de avaliação de serviço (por exemplo, "como foi o atendimento?"). O cliente responde tocando em um número de 1 a 5, cada um com um emoji, e a legenda vai de **Muito ruim** a **Excelente**.

Essa escala 1–5 **não entra no cálculo do NPS Score** e **não** tem faixas de promotor/neutro/detrator. O painel apenas calcula a **média** dessas respostas, exibida no card **Média avaliação (1–5)** e na análise por pergunta como **Média (escala 1-5)**.

> ⚠️ **Atenção:** as duas escalas convivem na mesma pesquisa. A **nota geral 1–10** é a que vira NPS Score e faixas (promotor/neutro/detrator). A **pergunta de avaliação 1–5** só gera uma média. Quem analisa os resultados precisa olhar o card certo para não interpretar uma pela outra.

## Quando usar

* **Medir lealdade do cliente** após a visita, com um indicador único e comparável ao longo do tempo (o NPS Score).
* **Acompanhar a evolução** da satisfação por período, usando o filtro de datas da aba **Analytics**.
* **Detalhar a experiência** com perguntas de avaliação 1–5 (atendimento, comida, ambiente) quando você quer notas por aspecto, e não só a recomendação geral.

## Limitações

* **Duas escalas que não se misturam.** A nota geral é 1–10 e gera o NPS Score; a pergunta de avaliação é 1–5 e gera só média. Uma não converte na outra.
* **As faixas são fixas.** Detrator (1–6), Neutro (7–8) e Promotor (9–10) não são configuráveis no painel — seguem o padrão do código.
* **Sem respostas, sem número.** O NPS Score e as médias mostram **—** quando não há respostas com nota no período selecionado.
* **A pergunta 1–5 fica de fora do NPS Score.** Mesmo notas baixas de avaliação não puxam o NPS Score para baixo; só as notas gerais 1–10 contam.

## Relacionado

* Pesquisa de Satisfação
* Analisar resultados
* Criar pesquisa

# Criar uma pesquisa de satisfação

Use esta página para criar uma **Pesquisa de Satisfação** (NPS) — o formulário que seus clientes respondem para avaliar a experiência. Você define o nome, o endereço do link (slug), o status inicial e, se quiser, um cupom de recompensa e um link de avaliação no Google. Ao final, a pesquisa fica disponível na lista de pesquisas para você compartilhar.

> ℹ️ **Observação:** o diálogo de criação **não** define as perguntas da pesquisa nem uma mensagem de agradecimento. Aqui você cria a "casca" da pesquisa (identificação, status e recompensa); as perguntas são tratadas à parte — veja Gerenciar perguntas da pesquisa.

## Como acessar

No menu lateral, clique em **Satisfação**. Você cai na tela **Gerenciamento de Pesquisas NPS**.

## Passos

1. Na tela de **Satisfação**, clique em **Criar nova pesquisa** (no canto superior direito; no celular, use o botão **Nova Pesquisa** na barra inferior).
2. No diálogo **Criar Nova Pesquisa NPS**, preencha o **Nome da Pesquisa**.
3. Confira o **Slug** — ele é preenchido automaticamente a partir do nome, mas você pode editar.
4. Opcionalmente, preencha **Descrição**, ajuste o **Status da Pesquisa**, selecione um **Cupom de Recompensa (Opcional)** e informe o **Link do Google Review (Opcional)**.
5. Clique em **Criar Pesquisa**.

Ao salvar, aparece a mensagem **Pesquisa criada com sucesso!** e a nova pesquisa entra na lista.

> ℹ️ **Observação:** se a loja ainda não tem nenhuma pesquisa, o diálogo de criação abre sozinho ao entrar na tela de **Satisfação**.

## Configurações

Campos do diálogo **Criar Nova Pesquisa NPS**:

| Campo                                | Obrigatório | Descrição                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nome da Pesquisa**                 | Sim         | Nome interno da pesquisa, usado para identificá-la na lista. Não pode ficar vazio.                                                                                                                                                                                                                                                                                                                |
| **Slug**                             | Sim         | Trecho que compõe a URL da pesquisa. Aceita **apenas letras minúsculas, números e hífens** (`^[a-z0-9-]+$`). É gerado automaticamente a partir do nome; ao editá-lo, o preenchimento automático para.                                                                                                                                                                                             |
| **Descrição**                        | Não         | Texto livre (área de múltiplas linhas) para descrever a pesquisa. Uso interno.                                                                                                                                                                                                                                                                                                                    |
| **Status da Pesquisa**               | Não         | Define se a pesquisa está **Rascunho**, **Ativo**, **Pausado** ou **Encerrado**. Vem como **Rascunho** por padrão. **Só pesquisas em Ativo recebem respostas** — nas demais, o cliente que abre o link vê "Pesquisa indisponível".                                                                                                                                                                |
| **Cupom de Recompensa (Opcional)**   | Não         | Cupom entregue ao cliente que responde a pesquisa. A lista puxa os cupons do módulo Cupons e mostra **apenas cupons de código único e ativos** — porque cada respondente recebe um código individual; a primeira opção é **Nenhum cupom**. Se o cupom que você quer não aparece, crie-o antes em **Cupons** como cupom de código único. |
| **Link do Google Review (Opcional)** | Não         | URL da página de avaliação no Google. O botão **Avalie-nos no Google** aparece ao cliente na tela de agradecimento quando ele dá **nota geral 9 ou 10**. (O aviso do campo diz "nota 4 ou 5": isso vale para a régua antiga, quando a pesquisa usa a pergunta de avaliação de 1 a 5.)                                                                                                             |

> ℹ️ **Observação:** ao validar o **Slug**, se ele tiver caracteres fora do permitido, o Dionísio mostra **"O slug deve conter apenas letras minúsculas, números e hífens"** e não salva.

## O que o cliente vê com cupom e Google Review

Quando o cliente termina de responder, ele chega à tela de agradecimento da pesquisa:

* Se você preencheu o **Link do Google Review** e o cliente deu **nota geral 9 ou 10**, aparece o botão **Avalie-nos no Google**.
* Se você selecionou um **Cupom de Recompensa**, aparece a seção **Recompensa** com o cupom ganho (benefício, código para copiar e, quando aplicável, QR Code).

## Dicas e observações

> 💡 **Dica:** deixe a pesquisa em **Rascunho** enquanto a configura. Mude para **Ativo** quando ela estiver pronta para receber respostas.

> ⚠️ **Atenção:** não existe ação de **Duplicar** pesquisa. Para reaproveitar uma configuração, crie uma nova pesquisa do zero.

> ℹ️ **Observação:** depois de criada, a pesquisa pode ser editada (**Editar pesquisa**), ter o link copiado (**Copiar link**), o QR Code baixado (**Baixar QR Code**) ou ser excluída (**Excluir pesquisa**) pela lista de pesquisas.

## Próximos passos

* Gerenciar perguntas da pesquisa
* Compartilhar a pesquisa
* O que é NPS
* Visão geral de Satisfação

# Gerenciar perguntas da pesquisa

Uma Pesquisa de Satisfação no Dionísio é composta por **várias perguntas** — não por uma nota única. Nesta página você adiciona, edita, reordena e exclui as perguntas de uma pesquisa, escolhendo entre cinco tipos diferentes. É na aba **Perguntas** da pesquisa que tudo isso acontece.

> ℹ️ **A nota geral de NPS é automática e obrigatória.** Toda pesquisa já inclui, de forma fixa, a pergunta de recomendação **"De 1 a 10, o quanto você recomendaria esta experiência a um amigo ou familiar?"**. Você **não** cria essa pergunta nesta aba e não pode removê-la, e o cliente **precisa respondê-la** para enviar a pesquisa. As perguntas que você adiciona aqui são **complementares** a essa nota geral — é dela que sai o NPS Score (veja O que é NPS).

## Antes de começar

Você precisa de:

* Uma Pesquisa de Satisfação já criada. Se ainda não tem, veja Criar uma pesquisa de satisfação.

## Como acessar

No menu lateral, abra a lista de pesquisas e clique na pesquisa que quer editar. Na tela de detalhes, selecione a aba **Perguntas**.

Se a pesquisa ainda não tem nenhuma pergunta, a aba mostra **Nenhuma pergunta cadastrada** com o botão **Criar Pergunta**.

## Passos

### Adicionar uma pergunta

1. Na aba **Perguntas**, clique em **Nova Pergunta** (ou **Criar Pergunta**, quando a pesquisa ainda está vazia).
2. Em **Tipo de Pergunta**, escolha um dos cinco tipos (veja a tabela em [Tipos de pergunta](#tipos-de-pergunta)).
3. Preencha o **Título da Pergunta**.
4. Opcionalmente, preencha a **Descrição (opcional)** e ative **Pergunta Obrigatória**.
5. Para os tipos **Seleção Única**, **Múltipla Escolha** e **Ranking**, preencha as **Opções de Resposta** (clique em **Adicionar Opção** para cada uma; são necessárias pelo menos 2).
6. Clique em **Criar Pergunta**.

Ao salvar, o Dionísio mostra **Pergunta criada com sucesso!** e a pergunta aparece na lista.

### Editar uma pergunta

1. No card da pergunta, abra a edição. O diálogo abre com o título **Editar Pergunta** e os campos preenchidos.
2. Altere o que precisar e clique em **Atualizar Pergunta**.

Ao salvar, o Dionísio mostra **Pergunta atualizada com sucesso!**.

### Reordenar perguntas

O botão **Reordenar** só aparece quando a pesquisa tem **2 ou mais perguntas**.

1. Clique em **Reordenar**. Abre o diálogo **Reordenar Perguntas**.
2. Use as setas **para cima** e **para baixo** ao lado de cada pergunta para mudar a ordem.
3. Clique em **Atualizar Ordem**.

Ao salvar, o Dionísio mostra **Ordem das perguntas atualizada com sucesso**. Essa ordem é exatamente a sequência em que as perguntas aparecem para o cliente que responde a pesquisa.

### Excluir uma pergunta

1. No card da pergunta, escolha excluir.
2. O Dionísio pede confirmação: **"Tem certeza que deseja excluir a pergunta ...? Esta ação não pode ser desfeita."** Clique em **Excluir**.

Ao confirmar, o Dionísio mostra **Pergunta excluída com sucesso!**.

## Campos da pergunta

Estes são os campos do diálogo de criar/editar pergunta.

| Campo                    | Obrigatório                                        | Descrição                                                                                                                                  |
| ------------------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Tipo de Pergunta**     | Sim                                                | Define como o cliente responde. Cinco opções (veja [Tipos de pergunta](#tipos-de-pergunta)).                                               |
| **Título da Pergunta**   | Sim                                                | O texto da pergunta que o cliente lê. Salvar sem preencher mostra **"O título da pergunta é obrigatório"**.                                |
| **Descrição (opcional)** | Não                                                | Texto auxiliar abaixo da pergunta.                                                                                                         |
| **Pergunta Obrigatória** | Não                                                | Quando ativado, o cliente precisa responder esta pergunta para concluir. Desativado por padrão.                                            |
| **Opções de Resposta**   | Sim (só Seleção Única, Múltipla Escolha e Ranking) | Lista de opções que o cliente vê. Use **Adicionar Opção** para incluir cada uma. São necessárias **pelo menos 2** opções, todas com texto. |

> ℹ️ **Observação:** ao adicionar opções, salvar com menos de 2 mostra **"Perguntas de seleção precisam de pelo menos 2 opções"**; deixar uma opção em branco mostra **"Todas as opções precisam ter um texto"**.

## Tipos de pergunta

São cinco tipos. Cada um muda como o cliente responde na tela da pesquisa.

| Tipo                 | O que é                                                                 | Como o cliente responde                                                     |
| -------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **NPS Score (1-5)**  | Nota de 1 a 5.                                                          | Escolhe uma nota de 1 a 5 (com carinhas de "Muito ruim" a "Excelente").     |
| **Seleção Única**    | Pergunta de uma escolha entre as opções. Precisa de opções.             | Marca **uma** opção (botão de rádio).                                       |
| **Múltipla Escolha** | Pergunta em que o cliente pode marcar várias opções. Precisa de opções. | Marca **uma ou mais** opções (caixas de seleção).                           |
| **Texto Aberto**     | Resposta livre, sem opções.                                             | Digita um texto, com limite de **5.000 caracteres** e contador na tela.     |
| **Ranking**          | O cliente ordena as opções por importância. Precisa de opções.          | Reordena as opções com setas, "da mais importante para a menos importante". |

## Dicas e observações

> ⚠️ **Atenção:** excluir uma pergunta é definitivo — o Dionísio avisa que **a ação não pode ser desfeita**.

> 💡 **Dica:** a ordem das perguntas é a sequência em que o cliente as vê. Use **Reordenar** para colocar primeiro o que mais importa.

## Próximos passos

* Criar uma pesquisa de satisfação
* Acompanhar as respostas
* O que é NPS

# Compartilhar a pesquisa

Depois de criar uma Pesquisa de Satisfação, você precisa levá-la até os clientes. O Dionísio gera um **link público** para cada pesquisa e permite baixar o **QR Code** correspondente — útil para colocar na mesa, na conta ou em qualquer material impresso. Esta página cobre o compartilhamento **manual**; para disparar a pesquisa automaticamente por WhatsApp, veja Enviar pesquisa automaticamente pelo WhatsApp.

## Antes de começar

Você precisa de:

* Uma Pesquisa de Satisfação já criada (veja Criar uma pesquisa de satisfação).

## Como acessar

No menu lateral, clique em **Satisfação**. A tela **Gerenciamento de Pesquisas NPS** lista todas as suas pesquisas.

Cada pesquisa aparece como um cartão (ou linha, na visualização em tabela) com as ações de compartilhamento. Você também encontra as mesmas opções ao abrir os detalhes de uma pesquisa.

## Passos

### Copiar o link público

1. Na lista de pesquisas, localize a pesquisa que quer divulgar.
2. Clique em **Copiar link** (ícone de cópia). A ação está disponível tanto no menu de opções (**⋮**) quanto nos botões de ação do cartão.
3. O link é copiado para a área de transferência e aparece a mensagem **Link copiado com sucesso!**. Cole o link onde quiser (WhatsApp, e-mail, redes sociais, bio).

Você também pode copiar o link de dentro da pesquisa: ao abrir os detalhes, o banner **Link da Pesquisa NPS** mostra a URL com o texto "Compartilhe este link para que os clientes respondam à pesquisa" e um botão **Copiar link**.

### Baixar o QR Code

1. Na lista de pesquisas, localize a pesquisa.
2. Clique em **Baixar QR Code** (ícone de QR Code), no menu de opções (**⋮**) ou nos botões de ação.
3. O arquivo **PNG** é baixado automaticamente e aparece a mensagem **QR Code baixado com sucesso!**. Imprima-o ou inclua em materiais de mesa, balcão ou na conta.

## Configurações

| Item               | Descrição                                                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Copiar link**    | Copia para a área de transferência a URL pública da pesquisa, no formato `https://n.odionisio.com/{slug-da-loja}/survey/{slug-da-pesquisa}`.                 |
| **Baixar QR Code** | Gera e baixa um QR Code da mesma URL, em arquivo **PNG de 512×512 pixels**, nomeado `qrcode-nps-{nome}-{slug}.png`. O QR Code é gerado no próprio navegador. |

O link e o QR Code apontam para a página pública de resposta, que abre no app de pesquisas para o cliente final.

## Dicas e observações

> 💡 **Dica:** o QR Code funciona bem impresso em cardápios, comandas, totens ou no comprovante de pagamento — o cliente aponta a câmera e cai direto na pesquisa.

> ⚠️ **Atenção:** o link usa o **slug da loja** e o **slug da pesquisa**. Se você alterar o slug de uma pesquisa já divulgada, **os links e QR Codes antigos param de funcionar** — eles apontam para o slug anterior, que deixa de existir. Gere e divulgue um novo link/QR Code após a alteração.

## Próximos passos

* Enviar pesquisa automaticamente pelo WhatsApp
* Criar uma pesquisa de satisfação
* Visão geral do módulo Satisfação

# Enviar a pesquisa pelo WhatsApp

Você pode fazer o Dionísio enviar sua **Pesquisa de Satisfação** sozinho, pelo WhatsApp, depois que o cliente faz uma reserva, um pedido ou entra na fila. Cada um dos três gatilhos — Reservas, Pedidos e Fila — é configurado de forma independente.

> ℹ️ **Você não começa do zero.** Quando o NPS é ativado na sua loja, o Dionísio já monta uma **configuração padrão automática**: cria três pesquisas (**Pesquisa de Reserva**, **Pesquisa de Pedido** e **Pesquisa de Fila**, já **Ativas** e com perguntas prontas) e deixa as três seções de envio **ligadas**, cada uma com a sua pesquisa selecionada e um tempo padrão. Esta página é, na prática, sobre **revisar e ajustar** esse padrão.

## Antes de começar

* Um número de WhatsApp conectado para que as pesquisas sejam enviadas. Sem conexão, a Dionísio envia pelo número oficial dela.
* Normalmente já há pesquisas disponíveis (as padrão acima). Se a loja não tiver nenhuma pesquisa interna **Ativa** nem a integração **Falae** conectada, a tela mostra o aviso **Nenhuma pesquisa disponível**, com atalhos para **Criar Survey** ou **Configurar Falae**.

## Como acessar

Na tela de **Pesquisas NPS** do módulo **Satisfação**, clique no botão **Configurar WhatsApp**.

Você chega à tela **NPS - Net Promoter Score**, com o subtítulo "Configure as pesquisas de satisfação dos clientes".

## Passos

A tela tem três seções, uma para cada gatilho de envio: **Reservas**, **Pedidos** e **Fila** — todas já vêm **ligadas** com a configuração padrão. As três funcionam de forma independente.

Para cada seção, revise ou ajuste:

1. Confirme se o botão da seção (**Reservas**, **Pedidos** ou **Fila**) está **ligado**. Para desligar um gatilho, desligue o botão da seção.
2. No campo **Pesquisa NPS**, confira ou troque a pesquisa que será enviada. As opções aparecem marcadas com **(Interno)** para os surveys criados no Dionísio e **(Falae)** para as pesquisas da integração Falae.
3. No campo **Tempo Mínimo (minutos)**, ajuste quantos minutos o Dionísio deve esperar após o evento antes de enviar a pesquisa.
4. Se quiser, escreva um texto no campo **Mensagem Personalizada (opcional)**, que vai junto com o link da pesquisa.
5. Clique em **Salvar Configurações**.

Ao salvar, aparece a mensagem **Configuração NPS salva com sucesso**.

## Configurações

Os campos abaixo se repetem, iguais, em cada uma das três seções (**Reservas**, **Pedidos** e **Fila**).

| Campo                                 | Obrigatório | Descrição                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pesquisa NPS**                      | Não         | Qual pesquisa será enviada. Opções: surveys internos **Ativos** (marcados **(Interno)**) e, se a integração Falae estiver conectada, as pesquisas dela (marcadas **(Falae)**). Você pode enviar só a mensagem personalizada sem escolher pesquisa.                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Tempo Mínimo (minutos)**            | Sim         | Quantos minutos esperar **após o evento da seção** para enviar a pesquisa. O evento é: **Reservas** — a reserva ser concluída; **Pedidos** — o pedido entrar em Concluído; **Fila** — o cliente ser sentado (em atendimento). Já vem preenchido com o tempo padrão da seção (ver a dica abaixo). Com **0**, a pesquisa sai imediatamente, sem espera. Precisa ser maior ou igual a 0 — valor negativo bloqueia o salvamento com o aviso "Deve ser maior ou igual a 0". \<!-- prod: dionisio-crm/functions/src/pubsub/onReservationConcludedNps/index.ts:132; onOrderUpdateNPS/index.ts:48 (status -> CONCLUDED); firestore/onQueueClientsWrite/index.ts:233 (cliente sentado/IN\_SERVICE); delay = minAfter |
| **Mensagem Personalizada (opcional)** | Não         | Texto que acompanha o link da pesquisa no WhatsApp. Em branco por padrão.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

## Dicas e observações

> ℹ️ **Observação:** as pesquisas são enviadas pelo número de WhatsApp conectado ao seu estabelecimento. Se não houver conexão, a Dionísio envia pelo número oficial dela.

> 💡 **Dica — quanto tempo usar:** o **Tempo Mínimo** começa a contar a partir do evento da seção (reserva concluída, pedido concluído ou cliente sentado) e serve para dar ao cliente o tempo de viver a experiência antes de ser perguntado sobre ela. O Dionísio já vem com tempos padrão: **5 minutos** para Reservas e Pedidos e **120 minutos (2 horas)** para Fila. Use-os como ponto de partida e ajuste ao seu ritmo: para **delivery**, alguns minutos após a entrega costumam bastar; para uma **reserva** ou **fila** (cliente ainda na mesa), deixe um intervalo maior — em torno de 1 a 2 horas — para que ele já tenha vivido a refeição. Com **0**, a pesquisa sai assim que o evento acontece.

> ⚠️ **Atenção:** cada seção só dispara enquanto o botão dela estiver ligado. Desligar uma seção interrompe os novos envios daquele gatilho.

> ❓ **As pesquisas não estão chegando?** Veja Minhas pesquisas de satisfação não estão sendo enviadas — cobre seção desligada, pesquisa inativa, tempo de envio e a entrega no WhatsApp (janela de 24 horas e template).

## Próximos passos

* Criar uma pesquisa de satisfação
* Compartilhar uma pesquisa de satisfação
* Pesquisas não estão sendo enviadas
* Visão geral de Satisfação

# Acompanhar respostas

A aba **Respostas** de uma Pesquisa de Satisfação reúne tudo o que os clientes responderam: quem respondeu, a nota geral, o status de conclusão e as respostas pergunta a pergunta. Use esta tela para acompanhar o feedback que chega e, quando precisar, registrar manualmente uma resposta que o cliente deu por outro canal.

## Antes de começar

Você precisa de:

* Uma Pesquisa de Satisfação já criada (veja Criar uma pesquisa).
* Pelo menos uma pergunta cadastrada na pesquisa, caso vá adicionar uma resposta manual — o botão **Salvar Resposta** fica desabilitado quando a pesquisa não tem perguntas.

## Como acessar

No menu lateral, abra a lista de pesquisas e clique na pesquisa desejada para abrir os detalhes. Na tela de detalhes, selecione a aba **Respostas**.

## O que a lista mostra

Cada resposta aparece como um card. Os dados de cada card vêm direto da resposta do cliente:

| Informação              | Descrição                                                                                                                                                      |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nome do cliente**     | Nome do cliente vinculado à resposta. Quando não há cliente associado, aparece **Cliente Anônimo**.                                                            |
| **Telefone**            | Telefone do cliente, exibido abaixo do nome quando disponível.                                                                                                 |
| **NPS** (geral)         | Nota geral de recomendação de **1 a 10**, exibida com cor: verde para 9–10, amarelo para 7–8 e vermelho para 1–6. Só aparece quando a resposta tem nota geral. |
| Nota da pergunta (`/5`) | Primeira nota de pergunta do tipo avaliação, na escala de **1 a 5**, exibida como `X/5` com cor: verde para 4–5, amarelo para 3 e vermelho para 1–2.           |
| Status                  | **Completa** (verde) quando o cliente concluiu a resposta; **Em andamento** (amarelo) enquanto ela não foi finalizada.                                         |
| Quantidade de respostas | Número de perguntas respondidas (ex: "3 respostas").                                                                                                           |
| Iniciado em             | Data e hora em que a resposta começou.                                                                                                                         |
| Concluído em            | Data e hora da conclusão; só aparece em respostas **Completa**.                                                                                                |

> ℹ️ **Observação:** o card de uma resposta **Completa** mostra "Concluído em" com a data e hora; o de uma resposta **Em andamento** não tem essa linha.

### Buscar uma resposta

Use o campo de busca no topo da aba para filtrar por **nome ou telefone do cliente**. A lista filtra conforme você digita.

Quando ainda não há nenhuma resposta, a aba mostra **Nenhuma resposta recebida** e um botão **Criar Resposta Manualmente**.

## Ver os detalhes de uma resposta

Clique em um card para abrir o diálogo **Detalhes da Resposta**. Ele mostra:

* **Informações do Cliente** — nome (ou **Cliente Anônimo**), telefone e e-mail, quando houver.
* **Status da Resposta** — **Resposta Completa** ou **Em Andamento**, com "Iniciado em", "Concluído em" (se concluída), o total de respostas (ex: "3 de 5") e o **NPS geral (1–10)**.
* **Respostas** — cada pergunta com o que o cliente respondeu, exibido conforme o tipo da pergunta: nota na escala 1 a 5, opção escolhida, opções marcadas, texto livre ou ranking ordenado.

## Adicionar uma resposta manualmente

Use a resposta manual para registrar um feedback que o cliente deu fora da pesquisa online.

> ⚠️ **Atenção:** o campo de cliente da resposta manual é o **ID do Cliente (opcional)**, identificador interno do cliente, não o nome. Deixe em branco se você não tiver esse ID — a resposta fica registrada sem cliente vinculado.

1. Na aba **Respostas**, clique em **Nova Resposta** (ou em **Criar Resposta Manualmente**, quando ainda não há respostas).
2. (Opcional) Preencha o **ID do Cliente (opcional)** para vincular a resposta a um cliente.
3. Escolha o **NPS geral (1–10)** clicando em um número de 1 a 10. Esse campo é obrigatório.
4. Responda às perguntas da pesquisa. Perguntas marcadas como **Obrigatória** precisam de resposta.
5. Clique em **Salvar Resposta**.

Ao salvar, a resposta é criada já como **Completa** e aparece na lista.

### Campos da resposta manual

| Campo                        | Obrigatório | Descrição                                                                                                                                                             |
| ---------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ID do Cliente (opcional)** | Não         | Identificador interno do cliente. Se informado, a resposta é vinculada a esse cliente; em branco, fica como resposta sem cliente.                                     |
| **NPS geral (1–10)**         | Sim         | Nota geral de recomendação, de 1 a 10. É a recomendação geral, independente das perguntas.                                                                            |
| Respostas às perguntas       | Depende     | Cada pergunta marcada como **Obrigatória** precisa ser respondida; as demais são opcionais. O tipo de campo (nota, seleção, texto, ranking) segue o tipo da pergunta. |

## Dicas e observações

> ⚠️ **Atenção:** se você tentar salvar sem escolher o **NPS geral (1–10)**, aparece a mensagem **"Informe o NPS geral (1 a 10)"**. Se faltar responder uma pergunta obrigatória, aparece **"A pergunta '...' é obrigatória"** com o título da pergunta.

> ℹ️ **Observação:** ao buscar com um termo que não casa com nenhuma resposta, a lista mostra **Nenhuma resposta encontrada**; limpe a busca para ver todas de novo.

> ⚠️ **Atenção:** uma resposta **não pode ser editada nem excluída** depois de criada — não há ação de editar ou apagar no card nem na tela de detalhes.

> ℹ️ **Observação:** a resposta manual conta nas métricas da aba **Analytics** igual a uma resposta enviada pelo cliente — entra no total, nas faixas e no NPS Score do período. Veja Analisar os resultados.

## Próximos passos

* Gerenciar perguntas da pesquisa
* Analisar os resultados da pesquisa

# Analisar resultados

A aba **Analytics** de uma Pesquisa de Satisfação reúne os indicadores de NPS e os gráficos das respostas recebidas. Use esta tela para acompanhar a satisfação dos clientes ao longo do tempo e ver o desempenho de cada pergunta. Se você ainda não sabe o que é NPS ou como o score é calculado, comece por O que é NPS.

## Antes de começar

Você precisa de:

* Uma Pesquisa de Satisfação criada e com **respostas** recebidas. Sem respostas no período selecionado, os indicadores aparecem zerados ou como `—`.

## Como acessar

1. No menu lateral, abra **Satisfação**.
2. Clique na pesquisa que você quer analisar para abrir a tela de detalhes.
3. Clique na aba **Analytics**.

> ℹ️ **Observação:** a mesma tela tem as abas **Perguntas**, **Respostas** e **Analytics**. Esta página cobre apenas a aba **Analytics**.

## Filtrar por período

Todos os indicadores e gráficos da aba refletem as respostas recebidas dentro do período selecionado no campo **Selecione o período**.

* **Padrão:** ao abrir, o filtro mostra os **últimos 7 dias**.
* **Formato das datas:** DD/MM/AAAA.
* **Atalhos:** ao abrir o seletor, há atalhos prontos (**Hoje**, **Ontem**, **Últimos 7 dias**, **Últimos 30 dias**, **Semana passada**, **Essa semana**, **Mês passado**, **Esse mês**, **Últimos 3 meses**, **Último ano**) ao lado do calendário. Escolha as datas no calendário e clique em **Aplicar**.
* **Limite:** o período não pode exceder **365 dias**. Se você selecionar um intervalo maior, aparece o aviso *"O período selecionado não pode exceder 365 dias"*.

## Ler os indicadores

A aba mostra um conjunto de cartões com os números do período. A tabela abaixo descreve o que cada um representa.

| Indicador                               | O que mostra                                                                                                                        |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Total de Respostas**                  | Quantidade de respostas recebidas no período (completas ou não).                                                                    |
| **Respostas Completas**                 | Quantidade de respostas que o cliente finalizou.                                                                                    |
| **NPS Score (promotores − detratores)** | O score de NPS do período, calculado a partir da nota geral. Exibe `—` quando não há nota geral no período.                         |
| **Promotores (9–10)**                   | Quantidade de clientes que deram nota geral 9 ou 10, com o percentual entre parênteses (ex: `12 (60.0%)`). Exibe `—` sem respostas. |
| **Neutros (7–8)**                       | Quantidade de clientes que deram nota geral 7 ou 8. Exibe `—` sem respostas.                                                        |
| **Detratores (1–6)**                    | Quantidade de clientes que deram nota geral de 1 a 6. Exibe `—` sem respostas.                                                      |
| **Média NPS geral (1–10)**              | Média das notas gerais (escala de 1 a 10). Exibe `—` sem respostas.                                                                 |
| **Média avaliação (1–5)**               | Média das respostas às perguntas de nota da pesquisa.                                                                               |
| **Total de Perguntas**                  | Quantidade de perguntas cadastradas na pesquisa.                                                                                    |

> ℹ️ **Observação:** as faixas de promotor (9–10), neutro (7–8) e detrator (1–6) seguem a régua do NPS. A teoria está em O que é NPS.

## Ler os gráficos

Abaixo dos cartões, dois blocos de gráficos detalham as respostas do período.

### Distribuição NPS geral (1–10)

Gráfico de barras com a quantidade de respostas para cada nota geral, de 1 a 10. As barras são coloridas pela faixa: vermelho para **Detratores (1–6)**, amarelo para **Neutros (7–8)** e verde para **Promotores (9–10)**; uma legenda abaixo do gráfico repete essas faixas. Ao passar o cursor sobre uma barra, aparece a quantidade de respostas e o percentual daquela nota.

### Analytics por Pergunta

Um cartão por pergunta da pesquisa, na ordem em que aparecem, mostrando o total de respostas e um detalhamento conforme o tipo de pergunta:

* **Perguntas de nota:** a média das notas em destaque.
* **Perguntas de seleção** (única ou múltipla): um gráfico de rosca com a distribuição das opções escolhidas.
* **Perguntas de texto livre:** apenas a contagem de respostas em texto (o conteúdo é lido na aba **Respostas**).
* **Perguntas de ranking:** apenas a contagem de respostas de ranking.

## Dicas e observações

> ℹ️ **Observação:** quando a pesquisa ainda não tem nenhuma resposta, os cartões aparecem zerados (ou `—`) e, no lugar dos gráficos, a tela mostra a mensagem *"Nenhum dado disponível"*.

> 💡 **Dica:** para ler uma resposta individual (quem respondeu, o que escreveu no texto livre), use a aba **Respostas**. Veja Acompanhar respostas.

## Próximos passos

* O que é NPS
* Acompanhar respostas
* Visão geral de Satisfação

# Pesquisas não estão sendo enviadas

Use esta página quando você configurou o envio automático da **Pesquisa de Satisfação** pelo WhatsApp, mas os clientes não estão recebendo a mensagem após a reserva, o pedido ou a fila. As causas vão da configuração da própria pesquisa (mais comum) até a entrega no WhatsApp.

## Sintomas

* O cliente **não recebe** nenhuma mensagem de pesquisa no WhatsApp depois de ser atendido.
* A aba **Respostas** da pesquisa continua vazia mesmo com clientes atendidos no período.
* O cliente recebeu uma **mensagem de texto** pedindo a opinião, mas **sem o link** da pesquisa.

## Causas comuns

Verifique nesta ordem, da mais frequente para a menos. As três primeiras são de configuração da Satisfação (você resolve sozinho); a última é na entrega do WhatsApp.

### 1. A seção do gatilho está desligada

Cada gatilho — **Reservas**, **Pedidos** e **Fila** — é independente e só dispara enquanto o botão da seção estiver ligado. Se a seção do canal em questão estiver desligada, nenhuma pesquisa sai por ali.

**Como verificar:** na tela de **Satisfação**, clique em **Configurar WhatsApp** e veja se o botão da seção correspondente (Reservas, Pedidos ou Fila) está **ligado**.

**Solução:** ligue a seção, confira os campos e clique em **Salvar Configurações**. Veja Enviar pesquisa automaticamente pelo WhatsApp.

### 2. A pesquisa selecionada não está Ativo (ou nenhuma foi selecionada)

O envio só leva o **link da pesquisa** quando a seção aponta para uma pesquisa com status **Ativo**. Se a pesquisa escolhida está em **Rascunho**, **Pausado** ou **Encerrado** — ou se nenhuma pesquisa foi selecionada na seção — o Dionísio envia apenas uma **mensagem de texto** pedindo a opinião, sem o link, e nenhuma resposta é registrada.

**Como verificar:** em **Satisfação**, confirme que a pesquisa usada na seção existe e está com o status **Ativo** na lista de pesquisas. Em **Configurar WhatsApp**, confira o campo **Pesquisa NPS** da seção.

**Solução:** deixe a pesquisa em **Ativo** (veja Criar uma pesquisa de satisfação) e selecione-a no campo **Pesquisa NPS** da seção.

### 3. O evento ainda não aconteceu ou o Tempo Mínimo não passou

A pesquisa só é disparada **após o evento da seção**, com o atraso do **Tempo Mínimo**: **Reservas** — a reserva ser concluída; **Pedidos** — o pedido entrar em **Concluído**; **Fila** — o cliente ser sentado. Enquanto o evento não acontece, ou enquanto o tempo configurado não passa, a pesquisa não sai.

**Como verificar:** confirme que o atendimento chegou ao estado que dispara o envio (reserva concluída, pedido em Concluído, cliente sentado) e veja o **Tempo Mínimo** da seção — a pesquisa só sai depois desse intervalo a partir do evento.

**Solução:** aguarde o tempo configurado após o evento. Se você precisa de um envio mais rápido para testar, reduza o **Tempo Mínimo** da seção (ex.: `0` para envio imediato) em **Configurar WhatsApp**.

### 4. A mensagem não foi entregue pelo WhatsApp

Se a configuração acima está correta mas a mensagem ainda não chega, o problema está na **entrega pelo WhatsApp**, não na Satisfação. A pesquisa é enviada como uma mensagem do WhatsApp e, na conexão **Meta (Oficial)**, depende de um **template aprovado** e da **janela de 24 horas** — as mesmas regras de qualquer notificação.

**Como verificar:** confira a conexão do número em **WhatsApp** → **Conectar WhatsApp** e siga o diagnóstico de entrega.

**Solução:** veja Minha mensagem não foi enviada no WhatsApp — cobre número desconectado, texto fora da janela de 24 horas, template não aprovado/pausado, cartão na Meta e limites de envio.

## Se nada disso resolver

* As notificações de satisfação têm **fallback pelo número oficial da Dionísio**: mesmo sem o seu número conectado, a pesquisa pode sair pelo número oficial. Se nem assim chega, o problema provavelmente é o telefone do cliente (sem WhatsApp, inválido) ou a entrega — confira a página de mensagem não enviada.
* Reúna as informações: canal (reserva, pedido ou fila), telefone do cliente, horário do atendimento e qual pesquisa está configurada na seção.
* Abra um chamado pelo canal de suporte da Dionísio com esses dados.

## Relacionado

* Enviar pesquisa automaticamente pelo WhatsApp
* Minha mensagem não foi enviada no WhatsApp
* Criar uma pesquisa de satisfação

