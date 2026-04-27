# Impacto no Mercado de Skins

## A canibalização do jogador comum

O drop semanal foi vendido pela Valve como uma **recompensa para o jogador**. Em parte é. Mas o **valor monetário** desse presente colapsou ao longo dos anos — e a causa principal é o **excesso de oferta** gerado por bot farms.

## Como funciona o efeito sobre preços

Considere uma case popular como **Prisma 2 Case**:

- Drop rate em uma Care Package típica: ~25% de aparecer no pool
- Probabilidade de jogador escolher: ~50% (entre 4 itens, escolhe 2)
- Resultado: se você joga e atinge XP, sai um Prisma 2 Case a cada **~8 semanas**

Para 1 jogador casual, isso é entretenimento. Para 1.000.000 de jogadores casuais + 100.000 contas em bot farms, **milhões de cases** são despejadas no Steam Marketplace **toda semana**.

A demanda (jogadores comprando keys e abrindo cases para tentar ganhar skins de tier alto) é **alta mas limitada**. A oferta (jogadores e bots vendendo cases que caíram) é **muito maior**. Resultado:

- Cases caem para **US$ 0,03–0,30** dependendo da popularidade
- O drop semanal vale ~US$ 0,50-1,50 em Marketplace **só porque Steam impõe um piso** (a Valve não vende abaixo de certo limite por conta de comissão fixa mínima)
- O **jogador comum recebe centavos por semana**, mesmo que a Valve venda Prime por US$ 14,99

## Os números brutos

A Insider Gaming compilou:

> **2,065 bilhões** de cases abertas na história combinada de CS:GO + CS2.

Mesmo com 25% de drop rate em Care Packages e ~1 milhão de drop ativos por semana, é provável que **uma parcela substancial** desses 2 bilhões venha **de drops semanais**, não de aberturas pagas.

Se considerarmos uma estimativa conservadora — **30% das cases já abertas vieram de drops semanais farmados** — isso significa **600 milhões de cases** entrando no mercado **sem que o farmer pagasse pela case**. Cada uma dessas case foi vendida no Marketplace, gerando **15% de comissão para a Valve**.

A 30 centavos médios por case × 600 milhões × 15% = **US$ 27 milhões** de receita pura de comissão **sobre cases farmadas**. E essa estimativa é **conservadora**.

## Quem perde com isso

### O jogador casual

Quando o drop semanal vale apenas centavos:
- O incentivo para jogar pelo drop diminui
- A "compensação" pelos US$ 14,99 do Prime fica menor
- A retenção depende mais do **jogo em si** e menos da economia paralela

A Valve calcula que **isso é tolerável** — porque o jogo em si é divertido o suficiente para reter a base. Mas é uma escolha consciente: **transferir valor do drop semanal para a indústria de farming**.

### O comprador de skins de tier alto

Quando cases são baratas, **mais gente abre cases**. Mais aberturas = mais skins de todos os tiers no mercado. Mais skins = preços de tier alto pressionados para baixo (em parte).

Esse efeito é **parcial** — skins raras (Covert, Knife) ainda mantêm preços altos pela escassez relativa. Mas skins **de tier intermediário** (Classified, Restricted) flutuam muito, e quem comprou em pico vê seu "investimento" desvalorizar.

### O ecossistema profissional

Cases farmadas em escala distorcem **dados de mercado** usados para análise/previsão. Sites como SteamAnalyst, CSMarketCap, Steam Inventory Helper usam dados públicos do Marketplace para gerar análises de preço. Quando 30%+ das transações são entre bots/farms (e não entre jogadores reais), os dados ficam **enviesados**.

Isso afeta:
- Traders profissionais que perdem em decisões mal-informadas
- Pesquisa acadêmica sobre o mercado de skins (como o paper de [Frontiers in AI 2025](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1702924/full) sobre algorithmic trading)
- Reguladores tentando entender o tamanho real do mercado

## Quem ganha

### Operadores de farms

Já discutido no [03-bot-farms-industriais.md](03-bot-farms-industriais.md). **US$ 1M+/mês** globalmente.

### A Valve

Como discutido em [02-incentivo-multi-conta.md](02-incentivo-multi-conta.md):
- Receita de Prime para cada conta nova
- Comissão de 15% em cada venda farmada
- **Liquidez do mercado mantida** por preços baixos de cases (mais aberturas → mais comissão sobre skins de tier alto que saem dessas aberturas)

### Compradores de cases pagas

Indiretamente: cases mais baratas → mais aberturas → maior chance de skins raras saírem para alguém. Mas isso é **migalha** comparado ao que o sistema costaria se **cases tivessem preço de mercado real**.

## A escolha estrutural

Em um mundo onde a Valve realmente combatesse bot farming:

- Drops semanais valeriam **US$ 5-10 em vez de US$ 0,50-1,50**
- O "presente" anual seria de **US$ 250-500** por conta
- **Prime pagaria por si mesmo** em poucas semanas
- Jogadores casuais **se sentiriam recompensados** de forma tangível

Mas isso significaria:

- **Menos receita de Prime** para Valve (não compensa pagar de novo)
- **Menos comissão** sobre vendas farmadas (volume colapsa)
- **Preços de cases sobem** → menos aberturas → menos comissão do cassino

A Valve **escolhe** o equilíbrio atual: **drops baratos + farming tolerado + cassino otimizado**. O jogador casual é a **engrenagem que mais perde** no arranjo, mas a sua perda é **invisível** (você não sente que estaria ganhando US$ 5/semana — só recebe os US$ 0,50 e segue jogando).

## O impacto comparativo: o que outros jogos fazem

Para contraste, alguns jogos competitivos lidam com farming/inflação de forma mais agressiva:

- **Path of Exile**: itens não vendáveis automaticamente são auto-descartados
- **WoW**: bots banidos em waves agressivas com comunicações públicas; itens farmados são removidos de circulação
- **Riot League/Valorant**: skins são **só ligadas à conta** (não tradeable) → impossível farming comercial
- **Roblox**: limites estritos de transferência, KYC para volumes grandes, captchas frequentes

A Valve **escolhe** o modelo mais permissivo. Isso é uma escolha de **design + receita**, não uma limitação técnica.

## Síntese do impacto

O Pilar 3 explica como a Valve **converte** o sistema de recompensa por jogar em **fluxo financeiro paralelo** para uma indústria que ela poderia derrubar quando quisesse. Os jogadores comuns recebem **centavos por semana**, enquanto a Valve embolsa **comissões agregadas em milhões**. A indústria de bots **subsidia** a economia inteira de skins, mantendo preços baixos que sustentam o **volume de aberturas pagas** que sustenta o **cassino do Pilar 1**.

Tudo está **conectado**. Tudo está **alinhado**. E nada disso é coincidência.

---

## Fontes

- Insider Gaming — Valve Made $1 Billion From CS Cases: https://insider-gaming.com/valve-cs-cases-earnings/
- BitSkins — CS2 Case Farming: https://bitskins.com/blog/cs2-case-farming-a-look-into-one-of-the-most-lucrative/
- Dust2.in — Case farms: https://www.dust2.in/news/48201/case-farms-the-dark-side-of-counter-strike
- Frontiers in AI — Algorithmic trading CS2 skin market: https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1702924/full
- Steamanalyst (dados de mercado): https://www.steamanalyst.com/tools/cs2-stats
- CSMarketCap: https://csmarketcap.com
