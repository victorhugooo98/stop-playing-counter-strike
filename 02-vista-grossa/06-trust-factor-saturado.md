# Trust Factor Saturado: O Sistema que Funciona Inversamente

## A tese

> **O Trust Factor, sob a combinação de (a) opacidade total, (b) dependência em reports saturados de frustração e (c) ausência de canal de apelação, deixa de proteger o jogador honesto e passa a puni-lo. Cheaters e smurfs, por sua vez, mantêm Trust Factor "fresco" via contas novas — ferramenta que viraram mercadoria visível em sites como WaytoSmurf e PlayerAuctions.**

A acusação é forte. Mas não é nova: pro players e a comunidade técnica articulam essa hipótese há anos em fóruns, threads de Reddit e cobertura de imprensa especializada. Este capítulo organiza a evidência, formaliza o mecanismo, e oferece dados próprios que são **consistentes** com a tese (sem prová-la em sentido causal).

Status epistêmico (ver [proposta](../00-introducao/proposta.md)): a estrutura do sistema é `[DOCUMENTADO]`; o ciclo descendente é `[ALEGADO]` por relatos consistentes; a inversão da função é `[HIPÓTESE]` apoiada em camadas documentadas.

---

## Como o Trust Factor funciona — versão oficial `[DOCUMENTADO]`

A documentação oficial da Valve no Steam Support afirma:

> *"O Trust Factor leva em conta uma combinação de fatores incluindo o comportamento do usuário em outros jogos Steam, a frequência de reports de outros jogadores, o tempo gasto jogando CS2 e outros jogos Steam, e mais. Para evitar manipulação, **a fórmula exata não é divulgada**."*
>
> — [Steam Support oficial](https://help.steampowered.com/en/faqs/view/00EF-D679-C76A-C185)

Três pilares declarados:
1. **Comportamento em outros jogos Steam** (sinal multi-aplicação)
2. **Reports recebidos de outros jogadores** (sinal social, ruidoso)
3. **Tempo de jogo** (proxy de engajamento)

Ao jogador, o Steam só expõe **um bit informativo**: o "matchmaking quality" (verde/amarelo/vermelho). Não há:
- Valor numérico do Trust Factor
- Histórico de mudanças
- Lista de eventos que afetaram o score
- Canal de apelação para reports infundados
- Instruções de como recuperar

A defesa oficial é "evitar manipulação". A consequência prática é **opacidade absoluta**.

---

## Os três problemas estruturais

### Problema 1 — Saturação por reports falsos `[ALEGADO]`

Counter-Strike é um jogo cuja **frustração é parte do produto**. Jogador frustrado por uma sequência ruim:

- **Reporta o oponente** que o matou (mesmo sem evidência de cheat)
- **Reporta o teammate** que errou em momento crítico
- **Reporta por raiva** sem critério honesto

A frustração é amplificada pelos pilares 1, 2 e 3 deste dossiê:
- Cassino ([Pilar 1](../01-cassino/00-resumo.md)) → tilt monetiza skins, mas também produz ruído de report
- Cheaters tolerados ([Pilar 2 — VAC](01-historia-do-vac.md)) → "este me matou — deve ser cheater" vira automatismo
- Smurfs impunes ([Pilar 2 — Smurfs](03-smurfs-e-prime-pago.md)) → "este é bom demais para o rank — deve ser cheater"

Quando o **report é o mesmo botão para "cheater real" e "ele é melhor que eu hoje"**, o sinal **satura**. Em estatística, isso se chama **baixa razão sinal-ruído**: o algoritmo recebe os mesmos clicks por motivos completamente diferentes.

Não temos como medir diretamente a taxa de reports falsos (Valve não publica). Mas o argumento estrutural é forte: **se o produto produz frustração e a frustração produz reports, reports não podem ser limpos**.

### Problema 2 — Opacidade total `[DOCUMENTADO]`

A defesa "evitar manipulação" tem um custo:

| Custo | Consequência |
|---|---|
| Auditoria externa impossível | Acadêmicos, jornalistas, reguladores não podem verificar |
| Sem canal de apelação | Reports falsos acumulam sem contestação |
| Sem feedback ao jogador | Não é possível corrigir comportamento que está sendo punido |
| Sem benchmarking | Comunidade não pode comparar perfis e identificar padrões |

A Valve **podia** divulgar a lista de variáveis (sem pesos) — como faz Riot com Vanguard, ou como fazem jogos com Trust System mais sofisticados. **Escolhe** não fazer.

A consequência mais grave é a próxima.

### Problema 3 — Recuperação não-roteirizável `[ALEGADO]`

Se o Trust Factor caiu, o jogador não sabe:
- **Quanto** caiu
- **Por que** caiu
- **O que fazer** para subir

Os conselhos comunitários (como aparecem em [cs.money/blog](https://cs.money/blog/games/how-do-i-raise-my-trust-factor-in-csgo/), [tradeit.gg](https://tradeit.gg/blog/checking-your-trust-factor-in-cs2/), [Skin.Club Community](https://community.skin.club/en/articles/cs2-trust-factor)) são todos **especulação coletiva**:

- "Jogue outros jogos Steam" (sinal indireto)
- "Não use VPN" (penaliza VPN involuntariamente)
- "Não tenha account-sharing" (penaliza família)
- "Abra cases" (?)
- "Tenha um inventário maior" (?)

Note que **vários conselhos populares envolvem gastar dinheiro com a Valve**. Não há prova de que funcionem — mas tampouco há prova de que **não** funcionem. A opacidade é fértil para essa especulação.

E **o tempo de "sentença" não é declarado**. Jogadores reportam ficar com Trust Factor baixo por **meses** após eventos que não conseguem identificar.

---

## O ciclo descendente

Junte os três problemas. O resultado é um circuito fechado para o jogador honesto skilled:

```
1. Jogador joga bem (boa K/D, alto win rate)
       ↓
2. Adversários frustrados reportam por "suspeita de cheat"
       ↓
3. Reports somam sem contestação (sinal saturado, sem apelação)
       ↓
4. Trust Factor cai (silencioso, opaco)
       ↓
5. Próximo matchmaking: pool com TF mais baixo
       ↓ (estatisticamente: mais smurfs com contas novas, mais cheaters não-detectados,
          mais comportamento tóxico)
6. Jogador frustrado, joga pior, recebe MAIS reports (toxicidade defensiva)
       ↓
7. [retorna ao passo 3]
```

O jogador honesto entra no ciclo **por excesso de skill** — mecanismo que deveria ser premiado vira gatilho de degradação. Cheaters e smurfs **não entram nesse ciclo** porque mantêm contas novas em rotação:

- VAC ban? Comprar Prime US$ 14,99, conta nova com Trust Factor neutro
- Reports começando a acumular? Vender a conta em [csgosmurfnation, WaytoSmurf, etc.](04-mercado-de-contas.md), comprar outra
- O **mercado de contas Prime** é uma forma comercial de **terceirizar o Trust Factor**

A inversão é completa: **o sistema que deveria proteger o jogador honesto está estruturado para uma indústria que protege o oposto.**

---

## A análise empírica colateral

Não podemos medir Trust Factor diretamente — Valve não expõe. Mas podemos fazer uma pergunta adjacente: **os preditores públicos (que jogador honesto pode ver e controlar) predizem quem foi banido?**

Se o sinal coletivo (reports + VAC) fosse **claro**, esperaríamos preditores fortes: cheaters teriam padrões distintos (muitas horas, contas novas com inventário caro, etc.). Se o sinal for **saturado/ruidoso**, preditores públicos seriam **fracos**.

### Amostra
- **735 perfis** (público + CS2 owned) coletados via BFS
- **45 VAC banidos** (6,1%)
- **24 game banidos** (3,3%)
- **68 com algum ban** (9,3%)

### Achado 1 — Banidos jogam MENOS, não MAIS

| Métrica | Banidos (mean) | Limpos (mean) | Cohen's d | p |
|---|---|---|---|---|
| **CS2 hours played** | menor | maior | **-0,61** | <0,0001 |
| Friends count | menor | maior | -0,27 | 0,014 |
| Badges count | menor | maior | -0,16 | 0,008 |
| Steam level | menor | maior | -0,18 | 0,063 |
| Account age (years) | menor | maior | -0,18 | 0,121 |
| Inventory log | maior | menor | +0,29 | 0,038 |

Counterintuitivo. A intuição popular é "cheater = vicia". Os dados dizem que **banidos têm metade das horas dos limpos**. Provável explicação: **conta queimada antes de acumular horas** — exatamente o ciclo de smurfs/cheaters comerciais descrito em [04-mercado-de-contas.md](04-mercado-de-contas.md).

### Achado 2 — Modelos preditivos são fracos

Regressão logística com 8 preditores públicos rendeu **McFadden pseudo-R² = 0,12**. Para referência:
- < 0,10: poder preditivo muito fraco
- 0,10–0,20: fraco a moderado
- > 0,20: moderado a forte

Apenas `cs2_hours` (p=0,003) e `inventory_log` (p=0,048) sobreviveram com significância. Os outros confundidores típicos (account age, steam level, badges, friends, games owned, total_usd) **não predizem ban**.

Visualização: ver [`assets/trust_factor_vac_distribution.png`](../assets/trust_factor_vac_distribution.png).

### Interpretação cuidadosa

Esses dados **são consistentes com** a tese, mas **não a provam**:

- ✅ Consistente: se preditores públicos não conseguem capturar o sinal de "quem cheater", reports comunitários (que dependem desses mesmos sinais) também devem ser ruidosos.
- ⚠️ Caveat: VAC bans são apenas os **caught**. Trust Factor opera num espaço maior, parcialmente invisível.
- ⚠️ Caveat: pode haver preditores fortes que **não coletamos** (Trust Factor não-publicado, número de reports recebidos, demos analisadas por VACnet).

A análise não é uma prova. É **circumstancial corroborativa**. O argumento principal continua sendo o **estrutural**: opacidade + reports saturados + sem apelação = sistema que favorece o ruim.

---

## Por que isto é "vista grossa", não falha técnica

A Valve **escolhe** este modelo. Algumas alternativas viáveis:

| Mudança | Custo | Benefício |
|---|---|---|
| Divulgar variáveis do Trust Factor (sem pesos) | Zero | Auditoria externa, contestação informada |
| Canal de apelação para reports falsos | Pequeno (suporte) | Sinal mais limpo, jogador não fica preso |
| Histórico visível de eventos do TF | Zero | Jogador entende o que está acontecendo |
| Penalizar reports infundados (após análise) | Pequeno | Reduz frustração-driven false positives |
| Roteiro público de recuperação | Zero | Evita especulação que recomenda gastar |
| Usar machine learning kernel-level (como Vanguard) | Médio | Detectar cheaters reais antes do report |
| Limitar criação de Prime por hardware/IP | Pequeno | Quebra o mercado de contas |

Nenhuma dessas mudanças é tecnicamente difícil para a Valve. Cinco delas têm **custo zero**. Seguem não implementadas há anos.

A explicação consistente com o resto do dossiê: **a opacidade serve ao modelo de negócio**:

- Banimentos vendem mais Prime (Pilar 2)
- Frustração vende mais cases (Pilar 1)
- Mercado de contas alimenta volume de Marketplace (Pilar 3)
- Auditoria externa expõe o que custa caro reverter

A inação é **alinhamento financeiro**, não falha técnica.

---

## Conexão com o ciclo do dossiê

Trust Factor saturado é o **mecanismo invisível** que faz o ciclo dos quatro pilares se autosustentar:

```
Cassino (1) gera tilt
    ↓
Tilt gera reports falsos
    ↓
Trust Factor satura (este capítulo)
    ↓
Honesto vai para pool degradado
    ↓
Encontra mais smurfs/cheaters (Pilares 2, 3)
    ↓
Frustração aumenta → mais cases (Pilar 1)
    ↓
[loop fecha]
```

O Pilar 4 ([Manipulação](../04-manipulacao/00-resumo.md)) testou empiricamente **uma hipótese específica** (skin → performance) e não encontrou suporte. A hipótese deste capítulo (Trust Factor saturado) é **menos forte epistemicamente** do que aquela — não foi testada em um pré-registro com critério explícito de falseamento — mas é **mais forte estruturalmente**: cada peça do mecanismo é defensável isoladamente, e a Valve teria resolvido qualquer uma se quisesse.

---

## O que a comunidade pode fazer

Se você é um jogador afetado pelo ciclo descendente (ou crê estar):

1. **Não agrave**: não responda a tilt com reports infundados. Você está alimentando o sistema que está te punindo.
2. **Diversifique**: jogar outros jogos Steam é o único conselho oficial vagamente sustentado.
3. **Documente**: se mantiver registro do seu Trust Factor (verde/amarelo/vermelho) ao longo do tempo, contribui para análise comunitária futura.
4. **Pressione por transparência**: cada thread/post pedindo divulgação das variáveis do TF é input político.

E se você é pesquisador: o experimento ideal seria coletar Trust Factor (via "matchmaking quality" exibido in-game) ao longo do tempo para um painel de jogadores e correlacionar com eventos de jogo. Esse painel longitudinal **não existe** publicamente até abril/2026.

---

## Fontes deste arquivo

### Fontes documentais

- Steam Support oficial — Trust Factor Matchmaking: https://help.steampowered.com/en/faqs/view/00EF-D679-C76A-C185
- cs.money — How to raise Trust Factor in CS2: https://cs.money/blog/games/how-do-i-raise-my-trust-factor-in-csgo/
- TradeIt.gg — CS2 Trust Factor Check (2026): https://tradeit.gg/blog/checking-your-trust-factor-in-cs2/
- Skin.Club Community — Trust Factor in CS2: https://community.skin.club/en/articles/cs2-trust-factor
- DMarket — Trust Factor in CS2: https://dmarket.com/blog/trust-factor-in-cs2/
- Hellcase — Tips to skyrocket Trust Factor: https://hellcase.com/blog/guides/tips-to-skyrocket-your-cs2-trust-factor/

### Comunidade / discussões

- Steam Discussion — Skill Based Matchmaking please god please: https://steamcommunity.com/app/730/discussions/0/4637112519824058784/
- Steam Discussion — All the issues with CS2 (megathread): https://steamcommunity.com/app/730/discussions/0/3821921664847998844/

### Análise empírica (este dossiê)

- [`scripts/analyze_trust_factor.py`](../scripts/analyze_trust_factor.py) — script reproduzível
- [`assets/trust_factor_vac_predictors.csv`](../assets/trust_factor_vac_predictors.csv) — t-tests por preditor
- [`assets/trust_factor_summary.txt`](../assets/trust_factor_summary.txt) — sumário textual
- [`assets/trust_factor_vac_distribution.png`](../assets/trust_factor_vac_distribution.png) — boxplot
