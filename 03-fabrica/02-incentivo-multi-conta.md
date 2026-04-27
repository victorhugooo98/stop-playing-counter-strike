# Por que o Sistema Incentiva Multi-Conta

## O cálculo que torna multi-conta inevitável

A regra da Valve é: **1 conta Steam = 1 drop semanal**, qualquer que seja o tempo jogado além dos 5.000 XP/semana.

Isso significa que, do ponto de vista da otimização, **cada hora extra jogada em uma conta única** rende **zero drops adicionais**. Mas **cada conta nova** rende **1 drop a mais por semana**, sem teto coletivo.

Esse é o **convite estrutural à multi-conta**:

| Estratégia | Drops/semana | Custo |
|---|---|---|
| 1 conta jogada 40h/semana | 1 | US$ 14,99 (Prime) |
| 10 contas jogadas 4h/semana cada | 10 | US$ 149,90 (Prime × 10) |
| 100 contas com bots jogando 90 min/semana cada | 100 | US$ 1.499 (Prime × 100) + infra |

A escala é **linear no número de contas, não nas horas humanas**. E, crucialmente, **bots reduzem o custo marginal de cada conta a centavos**.

## As três escolhas de design que viabilizam isso

### Escolha 1 — Drop por conta, não por hora

Se a Valve usasse "1 drop por X horas humanas", o sistema seria muito mais difícil de farmar (bots teriam que fingir 40h/semana cada, o que aumenta detecção). Ao usar "1 drop por conta com 5.000 XP", a Valve **otimiza para o farmer**.

### Escolha 2 — XP atinge-se em ~90 minutos

Com Weekly XP Bonus ativo (multiplicador 4x), a meta semanal cai a 2-3 partidas competitive (~90 minutos). Para um humano, é razoável; para um bot, é trivial. Se a meta fosse 50.000 XP/semana ou exigisse modos não-automatizáveis, seria proibitivo para bots.

### Escolha 3 — Modo deathmatch privado é farmavel

CS2 permite criar lobbies **privados** com bots. Em deathmatch, jogadores acumulam XP por dano causado e por kills. Esses lobbies **não rendem partidas competitive públicas**, mas **rendem XP** — exatamente o que o farming precisa.

A Valve poderia:
- Restringir XP em lobbies privados sem outros humanos
- Exigir modos públicos para XP semanal
- Usar detecção de comportamento (movement patterns idênticos = todos os 10 bots seguem o mesmo path)

Não faz nada disso eficazmente.

## A operação típica de um farm individual

Um operador semi-amador (alguém com conhecimento técnico mas escala pequena) opera mais ou menos assim:

1. **Cria 10-50 contas Steam** (gratuitas — só email)
2. **Compra Prime em cada uma** (custo: US$ 150-750)
3. **Roda 10 instâncias de CS2 em paralelo** via Sandboxie/Sandboxie-Plus
4. **Usa script** que:
   - Cria lobby privado deathmatch
   - Move o personagem em padrões pré-programados
   - Atira em direção a oponentes (outros bots na mesma lobby)
5. Após 5.000 XP por conta, **abre Care Package** automaticamente
6. **Vende drops** no Steam Marketplace

Custo:
- Prime: ~US$ 750 inicial (50 contas)
- Eletricidade: ~US$ 30/mês (10 instâncias rodando 24h)
- Software: gratuito (ASF + plugins) ou US$ 0-50/mês para serviços comerciais
- Computador: 1 PC mediano-bom roda 10-15 instâncias razoavelmente

Receita:
- 50 contas × US$ 1/semana = US$ 50/semana
- US$ 200/mês de receita bruta
- Após 15-20 semanas, opera no lucro

Não é riqueza, mas é uma **renda passiva** mais alta que muitos hobbies.

## A operação industrial

Operadores comerciais como **FarmLabs.dev** e **XteamFarm.com** fazem isso em escala B2B:

- **Cliente** (geralmente outro operador, ou um trader de skins) contrata o serviço
- Provedor mantém **dezenas a milhares de contas** rodando
- Provedor **vende** drops (em volume) ou **opera** as contas em nome do cliente
- Provedor cobra **mensalidade** ou **% dos drops gerados**

O modelo é o mesmo de **mineração de criptomoedas em pool**: capital intensivo, escala industrial, retornos consistentes mas modestos por unidade.

A diferença é que **mineração é (geralmente) legal**. Bot farming em CS2 viola Steam ToS — mas a violação não é punida.

## A Valve **lucra duas vezes** com cada conta farmada

Esta é a parte mais importante para o argumento do dossiê:

**Lucro 1 — Prime Status**

Cada conta farmada paga **US$ 14,99** em Prime. Isso vai **direto** para a Valve. Em uma operação de 1.000 contas, **US$ 14.990** já foram pagos à Valve antes de qualquer drop.

**Lucro 2 — Comissão Marketplace**

Quando a operação vende as cases farmadas no Steam Marketplace, **15%** do preço de venda vai para a Valve. Em escala:

- 1.000 contas × US$ 1/semana × 15% = US$ 150/semana **para a Valve, dessa única operação**
- Em 1 ano: **US$ 7.800** de comissão sobre essa operação

E a Valve recebe **independentemente** de o farming ser legal ou não. A comissão é sobre cada venda de skin, sem distinção da origem.

## O conflito de interesse formal

Se a Valve **derrubasse** todas as bot farms amanhã:

- Perderia **dezenas de milhões em Prime** já vendidos para essas contas (não-reembolsáveis, mas perde-se receita futura de venda)
- Perderia a **comissão recorrente** sobre vendas de drops farmados
- O **mercado de cases ficaria mais escasso** → preços subiriam → menos jogadores casuais comprariam → receita do cassino diminuiria

Em outras palavras: bot farms **subsidiam o ecossistema de skins**. Sem elas, o cassino do Pilar 1 funcionaria pior. E a Valve sabe disso.

A inação não é descuido. É **alinhamento estrutural**.

## A reação institucional honesta seria

Se a Valve quisesse **realmente** matar bot farming, teria várias opções:

1. **Drop por hora humana, não por conta** — como em alguns MMOs (e.g., Path of Exile).
2. **Detecção de comportamento** com classificadores ML treinados em padrões de bot.
3. **Verificação de identidade** ligada a Prime — KYC equivalente.
4. **Bloqueio de Sandboxie e similares** com checks de processo.
5. **Drops apenas em partidas públicas com 10 humanos verificados**.

Nenhuma dessas medidas está em curso publicamente. A Valve **escolhe** não fazer cada uma delas. E a explicação consistente — apoiada pelos outros pilares — é que **a Valve lucra com a inação**.

---

## Fontes

- Hellcase — Weekly Drop System Guide: https://hellcase.com/blog/guides/cs2-weekly-drop-system-guide/
- Tradeit.gg — CS2 Drop Pool: https://tradeit.gg/blog/cs2-drop-pool/
- BitSkins — CS2 Case Farming: https://bitskins.com/blog/cs2-case-farming-a-look-into-one-of-the-most-lucrative/
- Dust2.in — Case farms: The dark side of Counter-Strike: https://www.dust2.in/news/48201/case-farms-the-dark-side-of-counter-strike
- Skin.land — How to Farm XP: https://skin.land/blog/csgo-and-cs2-xp-farming/
- Steam Discussion — The Item and XP Farmbot Problem of CS2: https://steamcommunity.com/app/730/discussions/0/603022666611306643/
