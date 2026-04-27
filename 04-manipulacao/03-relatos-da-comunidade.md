# Relatos da Comunidade

## Aviso

**Relato não é evidência**. Esta seção sistematiza o que jogadores **dizem** experimentar — não para validar como verdade, mas para mapear **o quê** a investigação empírica precisará explicar (sob a hipótese de manipulação) ou refutar (sob a hipótese de placebo).

Quando milhares de jogadores reportam experiências similares, **uma de três coisas** está acontecendo:

1. **Há um padrão real** detectável estatisticamente (caso H1)
2. **Há viés cognitivo compartilhado** (placebo coletivo, confirmação de viés, treinamento social)
3. **Há um confundidor não-óbvio** que parece ser "manipulação" mas é outra coisa

O Pilar 4 trata as três possibilidades a sério.

## Os relatos mais frequentes

Sintetizados de fóruns Steam, threads Reddit (r/GlobalOffensive, r/cs2, r/csgomarketforum), Discord servers, e cobertura de imprensa especializada.

### Relato A — "Hit reg fica pior depois de uma boa sequência"

**Padrão alegado**: jogador joga bem por 3-5 partidas seguidas (rating subindo, K/D alto). Em seguida, sente **hit reg degradar** — tiros aparentemente certeiros não registram.

**Interpretação dos jogadores**: a Valve "está tentando me forçar a perder" para "manter rating estável" ou para "induzir frustração que vende skins".

**Explicações alternativas**:
- **Regressão à média**: depois de série incomum boa, partidas seguintes voltam ao normal — percebido como "pior"
- **Adversários melhores**: ganhar muito sobe rating, e adversários ficam mais difíceis
- **Cansaço cognitivo**: jogar muitas partidas reduz performance
- **Placebo invertido**: expectativa negativa cria experiência negativa

### Relato B — "Adversário com inventário caro acerta tudo"

**Padrão alegado**: jogadores notam que oponentes com **skins caras** parecem ter **performance acima da média** — incluindo headshots impossíveis, hit reg perfeito, comportamento que parece "favorecido".

**Interpretação**: a Valve dá vantagem oculta a quem investiu mais.

**Explicações alternativas**:
- **Confirmação seletiva**: jogador nota oponentes ricos quando perdem para eles, esquece quando ganham
- **Skill correlacionada com gasto**: jogadores que gastam mais tendem a jogar mais (pelo investimento) → mais habilidade
- **Smurfing**: jogadores fortes em contas secundárias com inventário mantido alto

### Relato C — "Hit reg melhora depois de comprar Prime"

**Padrão alegado**: jogadores que migram de free-to-play para Prime relatam **partidas melhores** após a compra — não apenas matchmaking diferente, mas **performance própria** parecendo melhor.

**Interpretação**: a Valve "premia" novos compradores com matches mais favoráveis.

**Explicações alternativas**:
- **Trust Factor melhora** com Prime → match com jogadores melhores comportados
- **Pool de adversários muda**: Prime = sem free-to-play smurfs farmadores
- **Placebo de compra**: ato de pagar gera expectativa positiva
- **Controle por idade da conta**: contas Prime tendem a ser jogadas mais sério

### Relato D — "Open de skins parece dar mais loot quando recém comprou Prime"

**Padrão alegado**: jogadores reportam abrir cases logo após compra de Prime e receber skins **acima da média esperada**, levando a abertura compulsiva — que reverte à média ou pior depois.

**Interpretação**: "primeira impressão" manipulada para induzir gasto continuado.

**Explicações alternativas**:
- **Memória seletiva**: lembramos das vezes em que "deu certo logo no início"
- **Aleatoriedade não tem memória**: cada caixa é independente; sequências boas e ruins existem por chance
- **Pequena amostra**: 5 cases não é suficiente para ver convergência ao valor esperado

### Relato E — "Matches ficam mais difíceis quando se está perto de upgrade de rank"

**Padrão alegado**: ao chegar perto de mudança de rating significativa (e.g., 25.000 Premier), partidas ficam **subitamente mais difíceis** — adversários melhores, teammates piores, "roubo" de matches.

**Interpretação**: a Valve "controla" o tempo de progressão.

**Explicações alternativas**:
- **Compressão estatística**: rating mais alto significa **menos jogadores** acima → matchmaking força contra cada vez mais fortes
- **Performance regredindo à média** após sequência boa que **levou** ao rating
- **Atenção elevada**: jogador perto de marco lembra mais das partidas decisivas

## O que esses relatos têm em comum

Estruturalmente:

- **Foram reportados por anos** em múltiplas plataformas
- **São consistentes entre regiões** (Brasil, EUA, Europa, Ásia reportam similar)
- **Geram debate acalorado** entre crentes e céticos
- **A Valve nunca respondeu publicamente** com explicação técnica detalhada

A consistência transregional pode indicar:

(a) Padrão real
(b) Viés cognitivo humano universal
(c) Cultura de jogo de CS específica que reforça esses padrões mentais

A análise empírica do [06-resultados-analise.md](06-resultados-analise.md) será capaz de discriminar entre alguns desses relatos:

- Relato A (hit reg após boa sequência): testável com **dados de hit reg vs rating change**
- Relato B (oponentes com skins caras): testável com **performance dos adversários por inventário**
- Relato C (Prime mudou tudo): testável com **before/after Prime upgrade** se houvesse painel longitudinal
- Relato D (open recém-Prime): **não testável** com dados públicos (probabilidade individual de cada lootbox não é exposta)
- Relato E (ratings altos = matches difíceis): **parcialmente testável** com curva de win rate por rating

## A diferença entre "explicado" e "rejeitado"

**Importante**: se a análise refutar a hipótese de manipulação direta, isso não significa que **os relatos sejam falsos**. Significa apenas que a **explicação manipulacionista** não é necessária.

Os relatos podem ser **acuradamente capturados** por uma combinação de:

- Trust Factor variável (Pilar 2)
- Smurfs misturados (Pilar 2)
- Bot farms vs humanos no pool (Pilar 3)
- Variação natural de skill própria
- Vieses cognitivos bem documentados
- Cansaço, hora do dia, fatores físicos

Tudo isso pode **somar** para criar uma sensação coletiva de "algo está manipulado" sem que **nada explicitamente** esteja sendo manipulado.

O dossiê reconhece isso. **A não-confirmação de H1 não é vergonhosa** — é um achado relevante. E mesmo na não-confirmação, os Pilares 1, 2 e 3 explicam **boa parte** da experiência ruim que os jogadores reportam.

## A lição metodológica

Quando uma comunidade grande reporta consistentemente uma sensação de injustiça em um sistema **fechado, opaco e desenhado para gastos**, há **três possibilidades**:

1. A sensação é **real** e o sistema é **manipulado** → H1 do dossiê
2. A sensação é **vieses cognitivos** + sistema **opaco** que não permite verificar → placebo + falta de transparência
3. A sensação é **real** mas o **mecanismo é diferente** do imaginado (e.g., bot farms distorcem mais que skins) → confundidor inesperado

O dossiê leva os 3 a sério. O **resultado da análise** vai informar qual é a melhor explicação para os dados disponíveis.

---

## Fontes

- Steam Community — Hit Registration discussions: https://steamcommunity.com/app/730/discussions/0/583876375391257995/
- Reddit r/GlobalOffensive (referências gerais — não citamos posts individuais para preservar usuários)
- Steam Discussion — Skill Based Matchmaking: https://steamcommunity.com/app/730/discussions/0/4637112519824058784/
- Steam Discussion — All the issues with CS2 (megathread): https://steamcommunity.com/app/730/discussions/0/3821921664847998844/
- Steam Discussion — EOMM em CS2: https://steamcommunity.com/app/730/discussions/0/4339861173663968580/
- Blog Clash.gg — CS2 Hit Reg: My Experience: https://blog.clash.gg/cs2-hit-reg
- xplay.gg — CS2 Lag, Packet Loss & Hit-Reg Practical Fixes: https://xplay.gg/blog/cs2-lag-packet-loss-hit-reg-practical-fixes/
- Skin.Club — Matchmaking Algorithm: How Fair Is It?: https://steamcommunity.com/sharedfiles/filedetails/?id=3463801366
