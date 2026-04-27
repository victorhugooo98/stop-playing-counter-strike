# Hipótese Formal

## A pergunta de pesquisa

> Existe correlação **estatisticamente significativa e persistente após controle de confundidores** entre o **valor estimado do inventário Steam** de um jogador de CS2 e suas **métricas de performance**?

## H0 e H1

### Hipótese nula (H0)

> O valor estimado do inventário Steam de um jogador **não tem correlação** com métricas de performance além do que pode ser explicado por:
> 1. Tempo total jogado em CS2
> 2. Idade da conta Steam
> 3. Trust Factor proxy (medido via badges, level Steam, reports recebidos)
> 4. Status Prime
> 5. Region do jogador

### Hipótese alternativa (H1)

> Existe correlação **estatisticamente significativa** entre o valor de inventário e ao menos uma métrica de performance, **persistente após controle pelos confundidores acima**, com effect size não-trivial.

### O que conta como "significativa"

- p-valor < **0.01** (não 0.05 — usamos limite mais estrito por ser estudo exploratório com múltiplos testes)
- Correção para múltiplos testes via **Bonferroni** ou **Benjamini-Hochberg FDR**
- **Effect size** (R² parcial ou Cohen's d) interpretável: pelo menos 0.05 (modesto)

Correlações pequenas com p baixo em N grande **não** contam. Queremos **sinal real**, não artefato de amostragem grande.

## Variáveis

### Variável independente principal

**`inventory_value_usd`** — Valor total estimado do inventário CS2 do jogador, em USD.

Cálculo:
1. Coletar lista de itens públicos via Steam Web API
2. Para cada item, consultar **Steam Market `priceoverview`** (preço médio recente)
3. Somar preços × quantidades

Tratamento:
- Outliers extremos (top 1%) cortados ou tratados separadamente
- Possível transformação log (inventários têm distribuição muito assimétrica)

### Variáveis dependentes (métricas de performance)

| Variável | Fonte | Descrição |
|---|---|---|
| `premier_rating` | Steam profile / Leetify | Rating CS2 Premier atual |
| `kd_ratio` | Leetify | Kill/Death ratio em ranked últimos 30 dias |
| `adr` | Leetify | Average Damage per Round |
| `headshot_pct` | Leetify | Headshot percentage |
| `win_rate_30d` | Leetify | Win rate últimos 30 dias |
| `clutch_win_rate` | Leetify | Clutch win rate (1vN) |
| `accuracy` | Leetify | Tiros acertados / disparados |
| `entry_kill_rate` | Leetify | Entry kills / entry attempts |

### Variáveis de controle (confundidores)

| Variável | Fonte | Por que controlar |
|---|---|---|
| `cs2_hours_played` | Steam Web API | Skill é fortemente correlacionada com horas |
| `account_age_days` | Steam Web API | Contas antigas tendem a ter mais skins **e** mais skill |
| `steam_level` | Steam Web API | Proxy de engajamento geral com a plataforma |
| `prime_status` | Steam Web API / inferido | Muda pool de matchmaking |
| `private_rank` | Steam Web API | Indica progresso em CS2 |
| `country` | Steam profile (público) | Region matchmaking afeta dificuldade média |

### Não-coletados intencionalmente

| Variável | Motivo |
|---|---|
| Nome real / username | PII — sem necessidade analítica |
| Avatar / fotos | Idem |
| Friends list expandida | Privacidade respeitada, mesmo sendo pública |
| Comentários de perfil | PII potencial |

## Análises planejadas (pré-registradas)

Em ordem de execução:

### 1. Análise descritiva
- Distribuições, médias, medianas, std
- Histograms de cada variável
- Detecção de outliers
- Visualização da amostra (mapa de calor de correlações)

### 2. Correlação de Pearson e Spearman
- Para cada par (inventory_value, performance_metric)
- Spearman para robustez a outliers
- **Sem ainda controlar confundidores**

### 3. Regressão linear múltipla
- Modelo: `performance ~ inventory_value + horas + idade_conta + steam_level + prime + private_rank + country`
- Coeficientes, p-valores, R²
- **Coeficiente de inventory_value isolado** é o foco

### 4. Correlação parcial
- Correlação entre `inventory_value` e cada métrica de performance, **controlando** todos os outros confundidores
- Compara com correlação simples para ver "o quanto sobra após controle"

### 5. Comparação entre quartis de inventário
- Q1 (inventário baixo) vs Q4 (inventário alto)
- Teste t com Bonferroni para múltiplas métricas
- Effect size (Cohen's d)

### 6. Análise de subgrupos
- Apenas Prime
- Apenas não-Prime
- Apenas conta com >1.000 horas
- Identificar se o efeito (se houver) é homogêneo ou se aparece só em algum subgrupo

## Critérios pré-definidos para conclusão

Para evitar **p-hacking**, o que conta como "achado" foi definido **antes** de ver os dados:

- ✅ **H1 confirmada**: pelo menos 2 das 8 métricas mostram correlação parcial significativa (p < 0.01 corrigido) com effect size ≥ 0.05
- ⚠️ **Sinal sugestivo**: 1 métrica significativa **e** consistência direcional nas outras (todas no mesmo sentido)
- ❌ **H1 refutada**: nenhuma correlação significativa após controle, ou correlações mistas sem padrão claro

Em qualquer dos três casos, **publicamos**. A diferença é só na **conclusão** e na **comunicação**.

## Tamanho de amostra alvo

- **Mínimo**: 500 perfis públicos com todas as variáveis disponíveis
- **Alvo**: 1.500-3.000 perfis
- **Stretch**: 5.000+ se factível dentro de rate limits

Com N = 1.500, podemos detectar correlações de magnitude **r = 0.07** com poder estatístico 0.80 e α = 0.01 (calculado via análise de poder, ferramenta G*Power).

## Limitações reconhecidas previamente

1. **Sample geográfico viesado**: BFS de seeds brasileiros do sul (vhs e Pastor Cururu, Brusque/SC) tende a coletar uma amostra **enriquecida em jogadores brasileiros**. Isto **não** invalida o estudo — mas obriga a **rotular como estudo regional**, não global. Análises secundárias podem expandir hops para diversificar.

2. **Self-selection**: jogadores com perfis públicos podem ser **diferentes** dos privados (mais engajados, mais sociais). Isto pode enviesar a amostra.

3. **Métricas Leetify dependem de demos**: jogadores que **não** sobem demos para Leetify estão **fora** da amostra. Pode enviesar para jogadores mais engajados/sérios.

4. **Variável "manipulação"** é construto não-observável: a hipótese real (Valve manipula matchmaking) **não pode ser confirmada** com correlação observacional. Apenas **inferida** com cautela. Mesmo H1 confirmada deixaria espaço para explicações alternativas (p.ex., jogadores com inventário grande têm Trust Factor maior por outras razões).

5. **Causalidade**: correlação **não** implica causalidade. Mesmo sinal forte exigiria estudo experimental (com manipulação de inventário) para conclusão causal — o que **não fazemos**.

## Decisão de pré-registro

Este arquivo (`01-hipotese-formal.md`) e o `05-metodologia-coleta.md` serão **versionados antes** de a análise final ser executada. Após a coleta de dados começar, **não modificamos** método nem hipóteses sem **registrar a mudança publicamente** com justificativa.

Esse compromisso é o que diferencia investigação séria de **achismo legitimado por estatística após o fato**.

---

## Fontes

- Diretrizes de pré-registro: https://www.cos.io/initiatives/prereg
- G*Power para análise de poder: https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower
- Bonferroni e FDR (revisão): https://en.wikipedia.org/wiki/Multiple_comparisons_problem
