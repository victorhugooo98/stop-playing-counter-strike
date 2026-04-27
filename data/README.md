# Datasets do dossiê

Conjuntos de dados estruturados que sustentam afirmações quantitativas no texto. Cada CSV é a fonte de verdade para os números citados nos pilares; se houver discrepância entre número no texto e CSV, **o CSV vence** (e o texto deve ser corrigido).

---

## Esquema dos arquivos

### `lawsuits.csv` — processos legais e ações regulatórias

| Coluna | Tipo | Significado |
|---|---|---|
| `date` | YYYY-MM-DD ou YYYY-MM | Data do evento ou da petição |
| `jurisdiction` | string | País/estado/órgão |
| `plaintiff` | string | Quem move a ação |
| `defendant` | string | Geralmente Valve Corporation |
| `allegation_type` | enum | match_fixing, illegal_gambling_facilitation, deceptive_endorsement, illegal_gambling_lootboxes, illegal_gambling_minors, illegal_gambling_promotion, illegal_gambling_minors_psychological_design |
| `status` | enum | active, settled, dismissed, decided, enforcement_active, allowed_to_proceed |
| `key_outcome` | string | Resumo de uma frase do desfecho ou pedido |
| `fonte_url` | URL | Fonte primária ou imprensa de referência |

### `revenue-timeline.csv` — receita e mercado

| Coluna | Tipo | Significado |
|---|---|---|
| `period` | YYYY[-MM][_YYYY-MM] ou "lifetime" / "ongoing" | Período do dado |
| `metric` | string | Nome da métrica (ver abaixo) |
| `value_usd` | número | Valor em USD (decimal para porcentagem) |
| `scope` | string | Descrição do que é medido |
| `fonte_url` | URL | Fonte |

**Métricas em uso**:
- `gambling_volume` — volume movimentado em sites de gambling de skins
- `annual_revenue_cs` / `annual_revenue_cs2_skin_sales` — receita anual estimada
- `monthly_revenue_cs2_cases` — receita mensal de cases
- `skin_market_total` — valor total do estoque de skins em circulação
- `steam_estimated_revenue` — receita total da plataforma Steam
- `total_cases_opened` / `total_cases_revenue_estimate` — agregados lifetime
- `monthly_botfarm_industry_estimate` — estimativa do mercado paralelo de bots
- `steam_marketplace_commission_pct` — comissão (decimal: 0.15 = 15%)
- `sticker_record_sale` — recorde de venda individual

### `botfarm-services.csv` — indústria de bots e contas

| Coluna | Tipo | Significado |
|---|---|---|
| `service_name` | string | Nome do serviço/site/projeto |
| `url` | URL | Endereço público |
| `type` | enum | commercial_saas, opensource_plugin, opensource_general, smurf_account_seller, smurf_and_prime_seller, prime_account_seller, marketplace_for_accounts, aggregate |
| `publicly_visible` | yes/no | Se opera às claras na web aberta |
| `prime_required` | yes/no/n/a/sells_prime | Se exige Prime, ou se vende Prime |
| `automation_level` | string | Nível de automação para bots |
| `monthly_estimate_usd` | número ou "unknown" | Estimativa mensal de receita |
| `fonte_url` | URL | Onde a info foi confirmada |

---

## Datasets gerados pela coleta (Pilar 4 — v2.0)

Estes ainda **não existem**. Serão criados na Fase 4 do roadmap.

### `seed-profiles.csv` — perfis-semente

Pontos de partida do BFS. Públicos, autorizados pelos donos.

| Coluna | Tipo |
|---|---|
| `steam_id_64` | int |
| `steam_id_hash` | sha256 prefixado (para uso publicado) |
| `vanity_url` | string ou null |
| `cs2_hours` | int |
| `account_age_days` | int |
| `prime_status` | bool |
| `inventory_public` | bool |
| `friends_public` | bool |
| `consent` | string ("self", "third_party_public") |

### `steam-profiles-raw.csv` — coleta bruta

Cada linha = perfil Steam encontrado pelo crawler BFS. Inclui só perfis públicos. Sem nome real, sem avatar, sem comentários.

### `steam-profiles-analysis.csv` — coleta processada

Variáveis derivadas: valor de inventário (USD), categoria de quartile, indicadores de Prime/Trust Factor proxy.

### `leetify-matches.csv` — partidas

Match-level data via API Leetify. Inclui adversários da partida (todos públicos por desenho da plataforma).

---

## Política de PII

- **SteamID 64 nunca é publicado em texto corrido**. CSVs públicos usam `steam_id_hash` (SHA-256 prefixado).
- **Nome de usuário, avatar, comentários, friends list não são publicados**.
- **Localização** é agregada para nível de país/região; nunca cidade.
- O script `scripts/ethics_check.py` audita CSVs antes de qualquer commit. Se encontrar PII, falha o commit.
- Coleta restrita a perfis com privacy=public via API. Nada de bypass.

---

## Como reproduzir

```bash
# 1. Setup
cd "Stop Playing Counter Strike"
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r scripts/requirements.txt

# 2. Configurar .env (NÃO committar)
cp .env.example .env
# Edite .env com sua STEAM_API_KEY

# 3. Coleta de perfis (BFS — usa Steam Web API)
python scripts/seed_friends_crawler.py --hops 2 --max-profiles 3000

# 4. Coleta de inventários (3 etapas, separadas para cachear pricing)
python scripts/fetch_inventories.py        # busca conteúdo de cada inventário
python scripts/price_market_items.py       # precifica skin única só uma vez
python scripts/aggregate_inventory.py      # produz inventory-values.csv

# 5. Coleta Leetify (API pública Swagger)
python scripts/leetify_fetch.py

# 6. Análise estatística
python scripts/analyze_correlation.py

# 7. Visualizações
python scripts/plot_results.py

# 8. Auditoria ética (antes de commit)
python scripts/ethics_check.py
```

Seed fixo (`numpy.random.seed(42)`) para reprodutibilidade.

### Notas de rate limit

- **Steam Web API**: limite de 100k req/dia com chave gratuita; nosso rate limiter usa 100/min conservador.
- **Steam Community inventory endpoint**: requer User-Agent realista; sem chave necessária.
- **Steam Marketplace `priceoverview`**: ~20 req/min sem auth — gargalo principal. Cache TTL de 7 dias.
- **Leetify API pública**: ~60 req/min observados, sem auth.

A separação fetch → price → aggregate existe para que o cache de preços (`cache/market_prices.json`) seja **agressivamente reutilizado** entre execuções e entre perfis. Uma skin que aparece em 50 inventários é precificada **uma única vez**.

---

## Quando atualizar

- **Novos processos legais** (NY AG decisão de mérito, novos AGs estaduais, ações na Europa) → atualizar `lawsuits.csv` imediatamente e refletir em `01-cassino/02-cronologia-legal.md`.
- **Releases trimestrais de receita** da Valve (que não publica oficialmente, mas vazamentos/análises de Steam Marketplace acontecem) → atualizar `revenue-timeline.csv`.
- **Novos serviços de bot farm** descobertos → adicionar em `botfarm-services.csv`.
