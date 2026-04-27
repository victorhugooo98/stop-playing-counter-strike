# Bot Farms Industriais

## Os players visíveis do mercado

A indústria de bot farming em CS2 não é underground. Tem **websites públicos com SSL**, **chat ao vivo**, **planos de assinatura**, e **suporte técnico**. Os principais identificados em abril/2026 estão registrados em [`data/botfarm-services.csv`](../data/botfarm-services.csv).

### FarmLabs.dev

Domínio público em https://farmlabs.dev/. Apresenta-se como **"AI Powered CS2 Automation"**. Vende serviços B2B de farming com diferenciais como:

- Automação por IA (não scripts hard-coded)
- Painéis de monitoramento para o cliente
- Estatísticas de drops por conta
- Suporte 24/7

Não publica preços diretamente. Modelo é provavelmente cotação por escala (número de contas).

### XteamFarm.com

Domínio em https://xteamfarm.com/. Apresenta-se como **"CS2 Farming Bot Panel | CS2 Case Farming Automation | Prime Status Farming"**. Diferenciais:

- "Prime Status Farming" — sugere também automação para subir contas a Prime via XP
- "Bot panel" — interface centralizada para o operador

### CS2Interface (Citrinate, GitHub)

Plugin **open source** para **ArchiSteamFarm (ASF)** em https://github.com/Citrinate/CS2Interface. ASF é uma ferramenta legítima para farm de cards de troca Steam (não-CS2). O plugin **estende** ASF para incluir interações específicas de CS2, viabilizando automação de farming.

Repositório no GitHub Topics — leetify e CS2 trading: https://github.com/topics/leetify e https://github.com/redlfox/awesome-cs2-trading.

A **existência open source** desse plugin é uma evidência adicional do volume da indústria — há demanda suficiente para que desenvolvedores **mantenham e atualizem ferramentas** publicamente.

### ArchiSteamFarm (ASF) base

O ASF original em https://github.com/JustArchiNET/ArchiSteamFarm é uma ferramenta que **a Valve tolera oficialmente** para farm de cards de troca. Sua arquitetura é, no entanto, **a fundação** sobre a qual plugins de farming de CS2 são construídos. A Valve **não desativou** o ASF, e continua tolerando seu uso para cards.

Esse é um detalhe importante: a Valve **escolhe** o que tolerar. Cards de troca foram tolerados; cases farmadas em escala via plugins similares **também são**, na prática.

## Os números agregados `[DOCUMENTADO]`

A análise mais citada vem de fontes especializadas em skins/trading:

> *"Segundo dados de um dos maiores desenvolvedores de bot farms, todos os case farmers do mundo fazem aproximadamente **US$ 600.000 por mês** através de um único programa, com a indústria inteira estimada em mais de **US$ 1.000.000 por mês**."*
>
> — [BitSkins blog: CS2 Case Farming](https://bitskins.com/blog/cs2-case-farming-a-look-into-one-of-the-most-lucrative/)

A Dust2.in (cobertura especializada em CS) corrobora:

> *"Por adicionar centenas de milhares de cases ao supply mensal, esses farmers destroem o ratio supply/demand, derrubando preços de cases e tornando os drops semanais quase sem valor."*
>
> — [Dust2.in: Case farms — The dark side of Counter-Strike](https://www.dust2.in/news/48201/case-farms-the-dark-side-of-counter-strike)

## Como uma operação grande funciona, do ponto de vista logístico

Vamos imaginar uma operação de **1.000 contas** (FarmLabs e XteamFarm operam provavelmente nessa ordem ou maior em pico):

### Hardware
- **20 PCs medianos-bons**, cada um rodando **50 instâncias** de CS2 em sandboxes
- Custo: ~US$ 30.000 em hardware
- Espaço: um cômodo médio com ventilação adequada
- Eletricidade: ~US$ 800-1.500/mês (dependente da região)

### Infraestrutura de rede
- Conexão fibra simétrica
- VPN/proxies para distribuir IPs (evitar fingerprint compartilhado)
- Custo: ~US$ 500/mês

### Software
- **Sandboxie-Plus** ou **VMware** para isolamento
- **CS2Interface** (gratuito, open source)
- **ArchiSteamFarm** (gratuito)
- Scripts customizados para coordenação dos 1.000 bots
- Investimento de tempo: alta, mas não recorrente

### Contas
- **1.000 contas Steam** com Prime
- Custo: 1.000 × US$ 14,99 = **US$ 14.990 inicial**
- Captcha-solving services para criação em massa: ~US$ 500
- Email/SMS verification: ~US$ 200

### Receita
- 1.000 × US$ 1/semana = **US$ 1.000/semana**
- 1.000 × US$ 4-5/mês = **US$ 4.000-5.000/mês**
- Anualizando: **US$ 50.000-65.000/ano** de receita bruta

### Margem
- Custos recorrentes: ~US$ 1.500/mês = US$ 18.000/ano
- Margem: ~US$ 32.000-47.000/ano por essa escala
- Payback do investimento inicial em ~12 meses

Para operações maiores (10.000+ contas), os números **escalam linearmente** — e os custos fixos são distribuídos em mais unidades. **A operação de US$ 600k/mês** mencionada por BitSkins corresponde provavelmente a algo na ordem de **150.000 contas**, possivelmente operadas via vários servidores/datacenters.

## A invisibilidade técnica explicada

Como uma operação de 150.000 contas funciona sem ser detectada?

1. **Tráfego distribuído**: cada bot opera em horário distribuído, não simultaneamente
2. **IPs rotativos**: VPN/residential proxies fazem com que cada bot pareça vir de um lugar diferente
3. **Hardware fingerprinting**: cada sandbox tem MAC, GPU ID, etc. simulados
4. **Padrões de movimento humanizados**: ML treinada em demos reais ensina bots a imitar humanos
5. **Compras pequenas**: cada conta compra Prime de cartão diferente (frequentemente cartões pré-pagos comprados em massa)

A Valve **poderia** detectar isso com:
- Análise de grafo (10.000 contas comprando Prime do mesmo IP/método de pagamento)
- Análise de comportamento agregado (todos os 10 bots em uma lobby seguem padrão de movimento estatisticamente correlacionado)
- Análise temporal (todas as 1.000 contas atingem 5.000 XP em janelas estatisticamente improváveis)

A engenharia para fazer isso **não é trivial**, mas é **exatamente o tipo** de problema que ML moderno resolve — e a Valve já demonstrou em setembro/2025 que pode aplicar ML a problemas mais difíceis (cheats sutis humanos).

## Por que a Valve **não** ataca a indústria

Vamos enumerar honestamente:

**Razão 1 — Receita direta de Prime**: cada conta farmada **paga US$ 14,99**. Em escala mundial, é **dezenas a centenas de milhões em Prime** vendido para bots.

**Razão 2 — Comissão Marketplace**: 15% sobre todas as vendas dos drops farmados. Provavelmente **US$ 100k-200k por mês** só dessa categoria.

**Razão 3 — Liquidez do mercado**: bot farms **inundam** o mercado com cases, mantendo preços acessíveis a jogadores casuais. Sem isso, cases ficariam mais caras → menos abertura → menos comissão **do cassino primário**.

**Razão 4 — Risco PR baixo**: bot farms são "abstratas" — não há jogador real frustrado por bot. Comparar a cheaters/smurfs, que **frustram pessoas reais publicamente**.

A combinação dessas quatro razões explica por que a Valve **não age** de forma consistente. **Tudo o que faz** (banimentos esporádicos, restrições de conta nova) é **simbólico** o suficiente para defender publicamente, mas **não eficaz** o suficiente para acabar com a indústria.

---

## Fontes deste arquivo

- BitSkins — CS2 Case Farming: https://bitskins.com/blog/cs2-case-farming-a-look-into-one-of-the-most-lucrative/
- Dust2.in — Case farms: The dark side of Counter-Strike: https://www.dust2.in/news/48201/case-farms-the-dark-side-of-counter-strike
- FarmLabs: https://farmlabs.dev/
- XteamFarm: https://xteamfarm.com/
- Citrinate/CS2Interface (GitHub): https://github.com/Citrinate/CS2Interface
- ArchiSteamFarm: https://github.com/JustArchiNET/ArchiSteamFarm
- redlfox/awesome-cs2-trading: https://github.com/redlfox/awesome-cs2-trading
- YouTube — YOUR CASE FARM. HOW TO CREATE A FARM IN CS2: https://www.youtube.com/watch?v=SpXm8wbZqu4
- Steam Discussion — CS2 Bot Farming Is Getting Out of Hand: https://steamcommunity.com/app/730/discussions/0/506199789077039666/
