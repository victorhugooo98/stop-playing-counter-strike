# Metodologia de Coleta (Pré-Registro)

## Status

> **Documento pré-registrado em**: 26 de abril de 2026 (versão 1.0).
>
> **Mudanças após esta data** devem ser registradas em changelog ao fim do arquivo, com **justificativa pública**.

Este arquivo descreve **como** os dados serão coletados e analisados. Foi escrito **antes** de qualquer coleta, exatamente para evitar que escolhas de método sejam **moldadas pelos resultados** (p-hacking).

## Princípios

1. **Apenas dados públicos** acessíveis via API Steam pública ou Leetify pública. Sem bypass de privacidade. Sem login automation contra ToS.
2. **Sem PII em datasets publicados**. SteamID 64 → SHA-256 hash em qualquer publicação.
3. **Reprodutibilidade**: scripts versionados, seed fixo, dados versionados, ambiente Python com `requirements.txt`.
4. **Auditoria ética automatizada**: `scripts/ethics_check.py` valida CSVs antes de qualquer commit.
5. **Consentimento explícito** para perfis-semente: vhs (autor) autorizou; Pastor Cururu é incluído pelo canal estritamente público.

## Sementes do BFS

| Perfil | SteamID 64 | Tipo de consentimento |
|---|---|---|
| **vhs** (vanity: vhschmidt) | A resolver via API | Auto-autorizado pelo autor |
| **Pastor Cururu** | 76561198152598576 | Inclusão pelo canal público |

## População alvo

- Perfis Steam **públicos**
- Que **possuam CS2** (jogo ID 730)
- Com **atividade nos últimos 30 dias**
- Com **inventário público**
- Com **friends list pública** (para BFS continuar)
- Com **estatísticas Leetify acessíveis** (perfil indexado)

## Estratégia de amostragem (BFS de 2-3 hops)

```
Hop 0 (sementes):
  └── vhs (autor)
  └── Pastor Cururu

Hop 1 (amigos diretos):
  ├── 29 amigos de vhs
  └── 129 amigos de Pastor Cururu
  → ~150 perfis únicos (com overlap esperado)

Hop 2 (amigos-de-amigos):
  → estimativa: 1.000-3.000 perfis únicos

Hop 3 (se necessário para atingir N alvo):
  → estimativa: 5.000-10.000 perfis únicos
```

**Filtros** aplicados em cada hop:
- Pula perfis privados (sem tentar bypass)
- Pula perfis sem CS2 (730 ausente em owned games)
- Pula contas com <100 horas em CS2 (provavelmente irrelevantes para hipótese)
- Pula contas inativas há >30 dias

**Critério de parada**:
- Atinge N = 1.500 (alvo) → para
- Atinge N = 3.000 → para mesmo se há mais hops disponíveis
- Atinge limite de rate da API → pausa, retoma no dia seguinte

## Variáveis a coletar

### Por perfil Steam

| Variável | Endpoint Steam Web API | Notas |
|---|---|---|
| `steam_id_64` | implícito | Hash imediato → `steam_id_hash` (SHA-256) |
| `account_age_days` | `GetUserSummaries.timecreated` | Calculado |
| `cs2_hours_played` | `GetOwnedGames` (appid=730, include_played_free_games=1) | Em horas |
| `steam_level` | `GetSteamLevel` | Inteiro |
| `country` | `GetUserSummaries.loccountrycode` | ISO-2 |
| `prime_status` | inferível via badges + activity em CS2 | Boolean |
| `private_rank` | API privada (apenas via in-game stats) | A coletar via `GetUserStatsForGame` |
| `inventory_item_count` | `IEconItems_730/GetPlayerItems` | Total de itens CS2 |
| `inventory_value_usd` | calculado: para cada item, query `priceoverview` | Soma em USD |
| `friends_count` | `GetFriendList` (se public) | Para BFS continuar |

### Por perfil Leetify (se disponível)

| Variável | Endpoint Leetify | Notas |
|---|---|---|
| `premier_rating` | `/profile/{id}` | CS Rating atual |
| `kd_ratio_30d` | `/profile/{id}/stats?period=30d` | Recente |
| `adr_30d` | idem | Average Damage per Round |
| `headshot_pct_30d` | idem | % |
| `win_rate_30d` | idem | % |
| `clutch_win_rate` | `/profile/{id}/clutches` | Se aplicável |
| `accuracy_30d` | idem | % |
| `entry_kill_rate` | `/profile/{id}/entries` | Se aplicável |

## Cálculo de `inventory_value_usd`

Para cada item no inventário público:

1. Extrai `market_hash_name` da entrada
2. Consulta `https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={url-encoded}`
3. Parse `lowest_price` (USD)
4. Soma todos os items × quantidades

**Tratamento de outliers**:
- Items raros sem preço listado → assumir 0 (conservador) ou skip (anotar caso)
- Items "non-marketable" (souvenirs únicos) → valor estimado por raridade (anotado)

**Cache**: respostas de `priceoverview` cacheadas por 24h para reduzir chamadas a API.

## Rate limiting

- Steam Web API: ~100k chamadas/dia com API key gratuita
- Steam Market priceoverview: ~20 requests/min sem chave; mais com User-Agent identificado
- Leetify pública: limites não-oficiais, observar 429s

**Backoff exponencial**: 1s, 2s, 4s, 8s... até 60s entre tentativas em caso de erro.

## Análise (executada após coleta)

Em ordem (todas pré-registradas em [01-hipotese-formal.md](01-hipotese-formal.md)):

1. **Análise descritiva** (distribuições, médias, std)
2. **Correlação Pearson e Spearman** simples
3. **Regressão linear múltipla** com confundidores
4. **Correlação parcial** após controle
5. **Comparação entre quartis de inventário** (teste t com Bonferroni)
6. **Análise de subgrupos** (Prime/não-Prime, alta/baixa hours)

**Critério de conclusão pré-definido**:
- ✅ H1 confirmada: ≥2 métricas com p<0.01 corrigido + effect size ≥0.05
- ⚠️ Sinal sugestivo: 1 métrica + consistência direcional
- ❌ H1 refutada: nenhuma significativa após controle, ou padrões mistos

## Ferramentas e ambiente

```python
# scripts/requirements.txt
python>=3.11
requests
pandas>=2.0
numpy
scipy
statsmodels
matplotlib
seaborn
selenium  # apenas se Leetify Swagger não tiver dado o que precisa
beautifulsoup4
python-dotenv
```

Seed fixo:
```python
import random; random.seed(42)
import numpy as np; np.random.seed(42)
```

## Estrutura de scripts

```
scripts/
├── seed_friends_crawler.py        # BFS pelas sementes
├── scrape_steam_profile.py        # Wrapper Steam Web API
├── compute_inventory_value.py     # Steam Market priceoverview
├── leetify_fetch.py               # API Leetify Swagger
├── leetify_scrape_matches.py      # Selenium fallback (com login do usuário)
├── analyze_correlation.py         # Estatística (scipy + statsmodels)
├── plot_results.py                # matplotlib + seaborn
├── ethics_check.py                # Audita PII e dados
└── requirements.txt
```

## Processo de execução

```bash
# 1. Setup
cd "Stop Playing Counter Strike"
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
pip install -r scripts/requirements.txt

# 2. Variáveis de ambiente
echo "STEAM_API_KEY=..." > .env  # https://steamcommunity.com/dev/apikey
echo "LEETIFY_USER=..." >> .env  # Se for usar fallback Selenium
echo "LEETIFY_PASS=..." >> .env

# 3. Coleta
python scripts/seed_friends_crawler.py \
  --seeds 76561198XXX,76561198152598576 \
  --hops 2 \
  --max-profiles 3000 \
  --output data/seed-profiles.csv

python scripts/scrape_steam_profile.py \
  --input data/seed-profiles.csv \
  --output data/steam-profiles-raw.csv

python scripts/compute_inventory_value.py \
  --input data/steam-profiles-raw.csv \
  --output data/steam-profiles-analysis.csv

python scripts/leetify_fetch.py \
  --input data/steam-profiles-analysis.csv \
  --output data/leetify-matches.csv

# 4. Análise
python scripts/analyze_correlation.py \
  --steam data/steam-profiles-analysis.csv \
  --leetify data/leetify-matches.csv \
  --output-dir assets/

# 5. Auditoria ética antes de commit
python scripts/ethics_check.py
```

## Política de commits e privacidade

- `data/seed-profiles.csv`, `data/steam-profiles-*.csv` e `data/leetify-matches.csv` **devem usar SteamID hash**, não SteamID 64
- Versão **com SteamID 64 pleno** fica em `.gitignore` (apenas local)
- `.env` no `.gitignore`
- `ethics_check.py` valida que nenhum CSV no commit tem coluna `steam_id_64`, `username`, `realname`, `avatar`

## Limitações reconhecidas

(repetidas de [01-hipotese-formal.md](01-hipotese-formal.md))

1. Sample geográfico viesado (BR/SC) → estudo regional, não global
2. Self-selection (perfis públicos diferem dos privados)
3. Métricas Leetify dependem de upload de demos
4. Manipulação não-observável diretamente — apenas inferida
5. Correlação não implica causalidade

## Pré-registro: o que **não** vamos fazer

- **Não** vamos buscar correlação até achar uma significativa entre 100 variáveis
- **Não** vamos mudar a definição de "significativo" depois de ver dados
- **Não** vamos descartar dados que "parecem outliers" sem critério pré-definido
- **Não** vamos publicar apenas resultados que confirmem expectativa

## Compromisso de publicação

**Em qualquer caso** (H1 confirmada, sinal sugestivo, ou H1 refutada), publicaremos:

- Os resultados completos em `06-resultados-analise.md`
- Os dados brutos (anonimizados) em `data/`
- Os scripts de análise em `scripts/`
- Os gráficos em `assets/`

Sem **gaveta**. Sem **ajuste posterior**. Sem **publicação seletiva**.

---

## Changelog

- **v1.0** (26/04/2026): Pré-registro inicial.
