# Resultados da Análise

> **Status: v2.0 — análise completa publicada em 27 de abril de 2026.**
> Pré-registro em [01-hipotese-formal.md](01-hipotese-formal.md) e metodologia em [05-metodologia-coleta.md](05-metodologia-coleta.md). Este texto **não foi modificado** após a inspeção dos resultados, exceto para registrar honestamente o que encontramos.

---

## TL;DR

> **H1 não confirmada.** A hipótese de que valor de inventário se correlaciona com performance além do explicado por confundidores **não foi sustentada** pelos dados. A explicação parsimônica permanece: **placebo + viés de confirmação + confundidores reais (horas jogadas, idade da conta)**.
>
> A análise diretamente performance-vs-inventário ficou limitada a **N=14** por baixa cobertura do Leetify entre os perfis-amostra (apenas ~4,5% têm Leetify público). Esse N é insuficiente para detectar correlações modestas — então o resultado é **inconclusivo no flanco de performance** e **negativo no flanco de proxies Steam**. Reconhecemos a limitação.
>
> **Os Pilares 1, 2 e 3 do dossiê não dependem deste pilar.** A inação documentada da Valve sobre cassino, cheaters e bot farms continua sustentada por evidências documentais. O que mudamos hoje é apenas o status epistêmico do Pilar 4: de **hipótese aberta** para **hipótese sem suporte empírico observável** com a metodologia disponível.

---

## 1. Configuração da coleta

### Sementes verificadas

| Perfil | SteamID 64 | CS2 hours | Country | Friends | Visibility |
|---|---|---|---|---|---|
| **vhs** (vanity vhschmidt) | 76561198081147232 | 2.581 | BR | 29 | público |
| **Pastor Cururu** | 76561198152598576 | 7.792 | BR | 129 | público |

Consentimento: vhs autorizou expressamente. Pastor Cururu incluído pelo canal estritamente público (mesmo critério usado para os 1.538 outros perfis descobertos via BFS).

### Pipeline executado

```
1. seed_friends_crawler.py    → BFS hop-2: 1.540 perfis coletados
2. fetch_inventories.py       → 735 perfis com inventário queriado
3. price_market_items.py      → 550 skins precificadas (cobertura 11% das únicas)
4. aggregate_inventory.py     → 204 perfis com valor > $0
5. leetify_fetch.py           → 33 perfis com Leetify público (4,5%)
6. analyze_correlation.py     → análises A (Steam) e B (Leetify)
7. plot_results.py            → 6 gráficos
8. ethics_check.py            → audit OK
```

Reprodutibilidade: scripts em `scripts/`, dados em `data/`, gráficos em `assets/`. Comando: ver `data/README.md`.

---

## 2. Composição da amostra

### Tamanho final
- **N total descoberto pelo BFS**: 1.540 perfis Steam
- **N útil (público + CS2 owned)**: 735
- **N com inventário processado**: 735 (todos)
- **N com inventário público + valor estimado > $0**: **204**
- **N com perfil Leetify público**: 33
- **N com Leetify público + inventário > $0**: **14** (gargalo da análise B)

### Distribuição geográfica

| País | N | % |
|---|---|---|
| **BR** | 527 | 71,7% |
| (não-declarado) | 120 | 16,3% |
| US | 11 | 1,5% |
| FR, AR, CA | 5 cada | 2,0% |
| RU | 4 | 0,5% |
| Outros (IT, DE, JP, etc.) | <5 cada | ~8% |

**Implicação metodológica**: estudo regional, com forte viés brasileiro (sementes em Brusque/SC). Replicações fora do Brasil podem chegar a resultados diferentes — não há nada na metodologia que nos permita generalizar para outros países.

### Distribuição de horas jogadas (todos os 735 úteis)

```
median:  1.601 h
mean:    2.284 h
std:     2.447 h
min:         0 h
max:    20.231 h
```

A amostra é, em média, mais "engajada" que o jogador típico de CS2 — efeito de coletar via friend graph de jogadores ativos.

### VAC bans
- **46 VAC bans** distribuídos em **45 perfis** (6,1% da amostra útil)
- **24 game bans** adicionais

---

## 3. Análise A: Steam-only proxies (N=204)

Variável independente: `inventory_log = log(USD inventário + 1)`.
Variáveis "dependentes" (na verdade proxies de engajamento): horas, level, badges, etc.
Confundidores controlados na regressão: `cs2_hours`, `account_age_years`, `steam_level`.

### A.1 Correlações simples (Pearson + Spearman)

| Variável | n | r (Pearson) | p | r (Spearman) | p |
|---|---|---|---|---|---|
| CS2 hours played | 204 | **+0,188** | 0,007 | +0,147 | 0,036 |
| Steam level | 204 | +0,007 | 0,923 | -0,063 | 0,367 |
| Player XP | 204 | +0,032 | 0,649 | -0,064 | 0,366 |
| Badges count | 204 | -0,005 | 0,945 | -0,114 | 0,105 |
| Friends count | 204 | +0,151 | 0,031 | +0,158 | 0,024 |
| **Account age (years)** | 204 | **+0,241** | **<0,001** | +0,168 | 0,016 |
| VAC bans count | 204 | +0,105 | 0,136 | +0,102 | 0,145 |

### A.2 Regressão múltipla (controlando confundidores)

Coeficiente de `inventory_log` quando regredido contra cada variável **controlando** horas + idade da conta + level (sem auto-controle):

| Variável | n | coef | p | p_FDR_BH | r²_adj |
|---|---|---|---|---|---|
| CS2 hours played | 204 | 241,5 | 0,014 | 0,049 | 0,046 |
| Steam level | 204 | -0,938 | 0,302 | 0,423 | 0,057 |
| Player XP | 204 | 451,4 | 0,140 | 0,245 | 0,800 |
| Badges count | 204 | -0,217 | 0,704 | 0,704 | 0,509 |
| Friends count | 204 | +3,49 | 0,444 | 0,518 | 0,122 |
| **Account age (years)** | 204 | **+0,584** | **<0,001** | **0,006** | 0,096 |
| VAC bans count | 204 | +0,023 | 0,067 | 0,157 | 0,035 |

**Após correção FDR (p<0,01)**:
- ✅ `account_age_years` sobrevive (p_fdr = 0,006)
- Nenhuma outra variável Steam-side é significativa

### A.3 Comparações de quartis (Q1 vs Q4 de inventário)

Cohen's d entre quartil-baixo e quartil-alto:

| Variável | Q1 mean | Q4 mean | Cohen's d | Interpretação |
|---|---|---|---|---|
| CS2 hours played | 1.816 h | 3.031 h | **0,57** | medium effect |
| Friends count | 120 | 165 | **0,44** | small-medium |
| Account age (years) | 9,9 | 12,5 | **0,64** | medium effect |
| Steam level | 21,6 | 21,6 | 0,00 | nenhum |
| Player XP | 5.181 | 5.624 | 0,04 | nenhum |
| Badges count | 18,1 | 17,4 | -0,03 | nenhum |
| VAC bans count | 0,06 | 0,10 | 0,15 | trivial |

### Interpretação da Análise A

A única variável que sobrevive a FDR é **idade da conta**. Mas isso é **exatamente o que esperaríamos como confundidor**:

> **Contas mais antigas acumulam mais itens ao longo do tempo**, sem necessidade de invocar manipulação algorítmica.

CS2 hours played e friends count têm correlação modesta com inventário — também esperado: **quem joga mais e tem mais amigos no Steam acumula mais skins**.

Nenhum desses achados constitui evidência de manipulação. São consistentes com o cenário **placebo + confundidores** descrito em [04-placebo-e-vies.md](04-placebo-e-vies.md).

---

## 4. Análise B: Leetify performance metrics (N=14)

Análise restrita aos 14 perfis com **Leetify público + inventário não-zero**.

### B.1 Correlações simples (sem controle)

| Variável | n | r (Pearson) | p |
|---|---|---|---|
| Premier rating | 11 | +0,403 | 0,219 |
| Leetify rating | 14 | -0,170 | 0,561 |
| Faceit level | 9 | (insuf.) | - |
| Win rate | 14 | -0,342 | 0,231 |
| Aim rating (Leetify) | 14 | -0,123 | 0,675 |
| Positioning rating | 14 | +0,026 | 0,930 |
| Utility rating | 14 | -0,186 | 0,524 |
| Headshot % | 14 | -0,066 | 0,822 |
| Preaim (lower=better) | 14 | -0,124 | 0,672 |
| Reaction time ms | 14 | -0,370 | 0,193 |
| Spray accuracy | 14 | -0,446 | 0,110 |
| Counter-strafing | 14 | -0,377 | 0,184 |

### B.2 Regressão múltipla

**N=14 é abaixo do mínimo (n≥30) que estabelecemos para regressão múltipla**. Pré-registramos esse limite em [01-hipotese-formal.md](01-hipotese-formal.md). Logo, **nenhum coeficiente é reportado** — seria estatisticamente irresponsável.

### Interpretação da Análise B

**A análise é inconclusiva por insuficiência de poder estatístico.** Para detectar correlação |r|=0,30 com α=0,01 e poder 0,80, precisaríamos N≈80. Temos N=14.

Ainda assim, vale notar que **as tendências numéricas no flanco Leetify são predominantemente negativas**:

- Win rate: r = -0,34 (jogadores com mais inventário **ganham menos** — mas não-significativo)
- Spray accuracy: r = -0,45 (precisão pior)
- Reaction time: r = -0,37 (mais rápida em ms — direção counterintuitiva, sem significância)
- Counter-strafing: r = -0,38 (pior)

Se essas tendências sobrevivessem em amostra maior, seriam o **oposto** da hipótese de manipulação positiva via skins. Mas **não há base estatística** para afirmar isso com N=14.

A leitura honesta: **a análise B não diz nada conclusivo**. Replicação com sample maior é a única forma de avançar.

---

## 5. Decisão pré-registrada (de [01-hipotese-formal.md](01-hipotese-formal.md))

| Critério | Resultado | Conclusão |
|---|---|---|
| ≥2 métricas com p_FDR<0,01 + effect size ≥0,05 | **NÃO** | H1 não confirmada |
| 1 métrica significativa | account_age (mas é confundidor, não performance) | n/a |
| Nenhuma após correção | mais próximo deste cenário | **placebo+confundidores suficientes** |

**Decisão**: ❌ **H1 NÃO CONFIRMADA**.

A explicação **mais parsimônica** continua sendo:

1. **Placebo** — jogadores com skin favorita focam mais e jogam melhor por motivos psicológicos (ver [04-placebo-e-vies.md](04-placebo-e-vies.md)).
2. **Viés de confirmação** — relatos comunitários filtrados pela memória.
3. **Confundidores legítimos** — quem joga mais (tempo) também tem mais skins **e** mais habilidade. Quem tem conta antiga acumula mais.

---

## 5.A Validação dos confundidores (atualização v2.1)

Antes de aceitar a decisão "H1 não confirmada" como robusta, precisamos verificar se as variáveis usadas como confundidores na regressão múltipla são realmente **independentes**. Se forem altamente colineares, o coeficiente de `inventory_log` na regressão pode estar mal estimado.

Script: [`scripts/validate_proxies.py`](../scripts/validate_proxies.py).

### Variance Inflation Factor (VIF)

| Variável | VIF |
|---|---|
| cs2_hours | 1,11 |
| account_age_years | 1,13 |
| **steam_level** | **14,88 ⚠️** |
| player_xp | 8,82 |
| badges_count | 3,55 |
| friends_count | 1,22 |

**Achado**: `steam_level` e `player_xp` são **altamente colineares** (correlação Pearson 0,89). Isso é esperado por design — Steam level é literalmente derivado de Player XP.

### Correção via PCA

Re-rodamos a Análise A controlando por **componentes principais (PC1+PC2)** em vez de variáveis individuais — eliminando o problema de multicolinearidade.

5 componentes são necessários para explicar ≥95% da variância dos confundidores (logo, há 5 dimensões reais), mas PC1 (42%) e PC2 (22%) capturam 64% da variância — suficiente para regressão limpa.

**Resultado da Análise A re-rodada com controles PCA**:
- 0 métricas significativas após FDR (mesmo padrão da análise original)
- A decisão **"H1 não confirmada"** se mantém
- A multicolinearidade entre `steam_level` e `player_xp` **não estava escondendo** efeito da variável independente

### Conclusão da validação

A decisão original é **robusta** ao problema de multicolinearidade. Os confundidores reais são, em essência, **2 dimensões independentes**:
- **Engajamento Steam-amplo** (level + xp + badges) — captura "quanto tempo a pessoa investiu no ecossistema Steam"
- **Atividade CS2 + sociabilidade** (hours + friends + age) — captura "quanto a pessoa joga CS2 e quão socialmente conectada"

A hipótese de manipulação **não sobrevive** a nenhuma das duas formulações de controle (variáveis individuais OU componentes principais).

Outputs em `assets/`:
- `confounder_correlation_matrix.csv`
- `vif_table.csv`
- `pca_explained_variance.png`
- `pca_loadings.csv`
- `analysis_a_pca_controls.csv`
- `validate_proxies_summary.txt`

---

## 5.B Análise de rede social (atualização v2.1)

A coleta produziu também um **grafo de amizades** (735 nós, 818 arestas, 1 componente conexo, densidade 0,003). Isso permite perguntar: **"Jogadores com inventários grandes formam clusters? Têm centralidade maior?"**

Script: [`scripts/network_analysis.py`](../scripts/network_analysis.py).

### Métricas computadas

- **Degree** (número de amigos dentro do sample)
- **Betweenness centrality** (importância como ponte na rede)
- **Local clustering coefficient** (quão denso é o vizinho)

### Resultado: correlação `inventory_log` vs métricas de rede (n=204)

| Métrica de rede | Pearson r | Pearson p | Spearman r | Spearman p |
|---|---|---|---|---|
| Degree | **+0,334** | **<0,001** | +0,062 | 0,38 |
| Clustering | -0,074 | 0,30 | -0,035 | 0,62 |
| Betweenness | +0,256 | <0,001 | +0,170 | 0,015 |

### Interpretação

A discrepância entre Pearson (alto, significativo) e Spearman (baixo, não-significativo) sugere que a correlação Pearson é **dirigida por outliers** — possivelmente um único nó hub com inventário alto e muitos amigos no sample.

**Hipótese alternativa**: como uma das sementes (Pastor Cururu) tem 129 amigos e inventário alto, ele atua como **nó central** que enviesa Pearson, mas Spearman (baseado em ranking) é insensível a essa magnitude isolada.

**Conclusão**: a estrutura de rede **não fornece evidência convincente** de que jogadores com inventários grandes formam clusters distintos. O sinal "linear" dos hubs é explicado pela estrutura da nossa amostragem (BFS a partir de poucas sementes).

Outputs em `assets/`:
- `network-graph.png` — visualização do grafo (cor = inventário)
- `network-degree-vs-inventory.png`
- `network-clustering-distribution.png`
- `network-summary.txt`

Dataset:
- `data/network-metrics.csv` — métricas de rede por perfil (hash)

---

## 6. Visualizações geradas

Todas em `assets/`. Imagens individuais:

- `inventory_distribution.png` — distribuição linear + log do valor de inventário (cauda longa, mediana ≈ $7,75)
- `inventory_vs_premier.png` — scatter de inventory_log × Premier rating (n=11, sem padrão claro)
- `quartile_boxplots.png` — performance Leetify por quartil de inventário
- `correlation_heatmap.png` — heatmap completo de variáveis
- `country_breakdown.png` — composição da amostra por país (72% BR)
- `hours_vs_inventory.png` — confundidor principal (horas) vs inventário em escala log

A `correlation_heatmap.png` é especialmente reveladora: `inventory_log` se correlaciona modestamente com `cs2_hours`, `account_age` e `friends_count` — e quase nada com qualquer métrica de performance Leetify.

---

## 7. Crítica honesta do método

### O que correu bem
- Pipeline reproduzível (3 etapas separadas para fetch/price/aggregate)
- Cache de preços evitou trabalho redundante
- Anonimização (SHA-256) implementada desde o início
- Pré-registro respeitado: nada foi modificado após ver resultados

### O que correu mal
- **Steam Marketplace rate-limit muito agressivo** (~4s por chamada após primeiras dezenas) — limitou pricing a 11% das skins únicas. Mitigação: cache acumulativo, mas insuficiente para uma rodada.
- **Leetify cobertura baixa entre amigos casuais** (4,5%) — esperávamos algo como 10–15%. Resultado: análise principal de performance ficou com N=14, abaixo do nosso pré-registrado mínimo de 30.
- **Sample geográfico viesado** — 72% BR, sem replicação fora do Brasil.

### O que faria diferente em uma v3.0
1. **Múltiplas seeds em diferentes países** — começar com 5–10 perfis públicos de regiões diferentes
2. **Foco em jogadores Faceit/ESEA** — onde Leetify cobertura é alta (>30% provavelmente)
3. **Pricing assíncrono com vários workers** — distribuir entre IPs ou usar API paga
4. **Amostra-alvo: N≥80 com Leetify público + inventário não-zero** — para poder detectar correlações modestas

### Variáveis que deveríamos ter coletado
- **Trust Factor proxy** mais sofisticado (taxa de reports recebidos vs envios)
- **Histórico de inventário** (snapshots ao longo do tempo) — só temos cross-section
- **Hits & misses por servidor/região** — mais granular

---

## 8. O que isto **não** prova

- **Não prova** que a Valve não manipula. Análise observacional não pode descartar manipulações sutis abaixo do limiar detectável.
- **Não prova** que skins são puramente cosméticas em algum sentido absoluto. Apenas que, neste sample, **inventário não correlaciona com performance** após confundidores.
- **Não prova** que outras regiões ou faixas de skill não exibam o efeito.

A ausência de evidência **não é evidência de ausência** — mas, na ausência de outro estudo similar, **a hipótese precisa de evidência positiva** que o presente estudo não trouxe.

---

## 9. O que isto sugere

- A hipótese popular **"a Valve regula matchmaking pelo inventário"**, na sua forma forte, **não tem suporte empírico observável** com os dados públicos disponíveis.
- A explicação parsimônica (placebo + confundidores) é **suficiente** para os dados que coletamos.
- Os Pilares 1, 2 e 3 explicam a frustração comunitária com CS2 sem precisar invocar manipulação algorítmica direta.
- Replicação com amostra maior fora do Brasil é o próximo passo lógico para qualquer pesquisador que queira avançar a investigação.

---

## 10. Reprodutibilidade

### Versão dos arquivos no momento da análise

```
data/steam-profiles-raw.csv          1.541 linhas (incl. header)
data/inventories.csv                 16.270 linhas (cada item = uma linha)
data/inventory-values.csv            735 perfis (204 com valor > $0)
data/leetify-profiles.csv            735 perfis (33 públicos)
data/market-prices.csv               550 skins precificadas
data/steam-profiles-analysis.csv     735 perfis (joined)
cache/market_prices.json             550 entradas
```

### Scripts (`scripts/`)

- `steam_api.py` — wrapper Steam Web API + community endpoints
- `seed_friends_crawler.py` — BFS
- `fetch_inventories.py` — coleta inventários
- `price_market_items.py` — pricing por skin única
- `aggregate_inventory.py` — soma por perfil
- `leetify_fetch.py` — perfis Leetify
- `analyze_correlation.py` — análises A e B
- `plot_results.py` — gráficos
- `ethics_check.py` — audit PII

### Para reproduzir

Ver [`data/README.md`](../data/README.md). Tempo total: ~5 horas (limitado pelo rate limit do Steam Marketplace).

---

## 11. Compromisso honrado

Este texto **não é** uma autodefesa de uma hipótese refutada. É a publicação **honesta** de um resultado que **não confirmou** a hipótese pré-registrada. Pré-registro é compromisso público, e este compromisso foi cumprido.

Se em algum momento for replicado um estudo análogo com amostra maior que **encontre** correlação não-explicada por confundidores, este dossiê será atualizado para refletir essa nova evidência. Mas **até lá**, a posição honesta é: **manipulação direta de performance via inventário não tem suporte observável**.

A força do dossiê inteiro continua nos Pilares 1, 2 e 3 — onde a evidência documental é abundante e não depende de inferência estatística.
