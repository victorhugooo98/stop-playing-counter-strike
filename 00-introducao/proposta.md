# Proposta e Tese Central

## O que este dossiê é

Uma investigação jornalística com pretensão acadêmica sobre quatro práticas da Valve Corporation envolvendo Counter-Strike 2. O objetivo não é "expor a Valve" no sentido sensacionalista — é **organizar evidências dispersas em um modelo causal coerente**, distinguindo o que está documentado do que ainda é especulação, e oferecendo uma metodologia para testar a parte especulativa.

## O que este dossiê **não** é

- **Não é um manifesto anti-Valve genérico.** Counter-Strike 2 é um jogo competente em muitos aspectos. As críticas aqui são específicas e ancoradas.
- **Não é uma denúncia anônima.** Toda afirmação tem fonte. Quando não tiver, é porque está marcada como `[HIPÓTESE]`.
- **Não é uma tese de doutorado.** A linguagem é jornalística. O rigor é maior do que jornalismo de portal, menor do que peer review.

---

## Tese central — "O Cassino que Fabrica Suas Próprias Fichas"

A Valve construiu, em torno de Counter-Strike, um modelo de negócio em que **a economia de skins virou o produto principal**, e o jogo virou infraestrutura para sustentar essa economia.

Esse modelo tem quatro engrenagens interligadas:

```
                    ┌──────────────────────────────┐
                    │  PILAR 1 — O CASSINO         │
                    │  Lootboxes → Marketplace     │
                    │  US$ 1B+/ano em receita      │
                    └──────────────┬───────────────┘
                                   │
              ┌────────────────────┼─────────────────────┐
              ▼                    ▼                     ▼
   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
   │ PILAR 2          │  │ PILAR 3          │  │ PILAR 4 (?)      │
   │ Vista grossa     │  │ A Fábrica        │  │ Manipulação de   │
   │ Cheaters/smurfs  │  │ XP + bot farms   │  │ performance via  │
   │ aumentam tilt    │  │ alimentam supply │  │ skins            │
   └──────────┬───────┘  └────────┬─────────┘  └────────┬─────────┘
              │                    │                     │
              └────────────────────┼─────────────────────┘
                                   │
                                   ▼
                          Frustração + chasing
                          → Mais aberturas de cases
                          → Mais comissão para Valve
                          → Loop fechado
```

**A tese é**: cada um dos quatro "crimes" deixa de parecer aleatório quando lido como **proteção da receita do Pilar 1**. Atacar cheaters reduz tilt → reduz chasing → reduz receita. Derrubar bot farms reduz oferta de cases → reduz comissão → reduz receita. A inação não é incompetência; é alinhamento.

---

## Por que esta moldura é melhor que tratar os quatro pilares separadamente

A imprensa especializada já cobriu cada um deles em isolado. Existem reportagens excelentes sobre lootboxes (PC Gamer), sobre VAC (Richard Lewis), sobre bot farms (BitSkins blog), sobre matchmaking suspeito (Dexerto). Mas **ninguém juntou os pontos**.

Quando se junta, três coisas mudam:

1. **A explicação fica mais simples.** Em vez de quatro problemas independentes, há uma causa raiz.
2. **O comportamento da Valve fica previsível.** Se a tese estiver certa, a Valve vai mexer com mais energia em coisas que ameaçam o cassino e arrastar os pés em coisas que o sustentam. Isso é testável historicamente — e a história confirma (set/2025: VAC só foi atualizado de verdade após pressão internacional crescente sobre lootboxes; bot farms continuam intocadas).
3. **As recomendações ficam coerentes.** Não adianta pedir "mais bans de cheater". Tem que pedir reforma do modelo de receita.

---

## Princípios editoriais

### 1. Três níveis de afirmação, sempre marcados

| Tag | Critério |
|---|---|
| `[DOCUMENTADO]` | Há fonte primária acessível: decisão judicial, paper revisado por pares, comunicado oficial da Valve, FTC, gambling commission. |
| `[ALEGADO]` | Acusação formal em processo legal ativo (ex.: petição da NY AG contra Valve, fevereiro/2026). Não é fato confirmado, mas tem peso institucional. |
| `[HIPÓTESE]` | Conjectura nossa, sob investigação. Sempre acompanhada de método para testar. |

Se uma afirmação não tiver tag, é um **bug do dossiê**.

### 2. Fonte primária sempre que possível

Imprensa secundária é aceitável quando a fonte primária não é acessível em português ou quando já compilou múltiplas fontes. Mas o link primário (PDF da petição, decisão da corte, paper do PMC) é preferível.

### 3. Reconhecer contra-argumentos

O Pilar 4 é o mais frágil. Ele começa com um capítulo dedicado **a derrubar a própria hipótese** (placebo, viés de confirmação) antes de apresentar a investigação. Se a análise estatística não achar nada, o dossiê **publica isso** e não tenta esconder.

### 4. Linguagem firme, não sensacionalista

"Valve opera um cassino disfarçado" — sustentado por petição da NY AG e ações regulatórias internacionais. ✅
"Valve odeia seus jogadores e quer destruir vidas" — não. ❌

A credibilidade é a moeda. Cada parágrafo retórico em excesso queima um pouco dela.

---

## Escopo (e o que está fora)

### Dentro do escopo
- Counter-Strike: Global Offensive (2012–2023) e Counter-Strike 2 (2023–presente)
- Lootboxes, drops semanais, Steam Marketplace, Trust Factor, VAC/VACnet, Premier mode
- Conduta documentada da Valve quanto a cheaters, smurfs, bot farms
- Patentes de matchmaking de Activision/EA como evidência **da existência** da tecnologia (não da sua aplicação pela Valve)

### Fora do escopo
- Outras franquias Valve (Dota 2, Team Fortress 2 entram só como comparativo legal — porque a NY AG inclui as três no processo)
- Sites de gambling de terceiros em detalhe (CSGORoll, CSGOEmpire, Stake) — citados mas não auditados
- Esports profissional como tópico isolado (entra em caso histórico — iBUYPOWER 2014)
- Análise técnica de cheats individuais ou DMA cards a nível de hardware

---

## Recursos disponíveis para a investigação

- **Pesquisa documental**: petições judiciais públicas, decisões regulatórias, papers acadêmicos, imprensa especializada.
- **Coleta de dados** (Pilar 4):
  - Steam Web API pública (perfis, inventários, amigos)
  - Steam Market `priceoverview` para valor de skins
  - Leetify Swagger pública para estatísticas de match
  - Perfis-semente fornecidos pelo autor do projeto: vhs (`/id/vhschmidt/`) e Pastor Cururu (`/profiles/76561198152598576/`)
- **Análise**: Python + scipy/statsmodels/pandas. Scripts versionados, dados versionados, seed fixo.

---

## Como contribuir

Este dossiê é colaborativo. Se você:

- Encontrar afirmação sem tag ou sem fonte → reporte.
- Souber de processo legal não listado → adicione a `data/lawsuits.csv`.
- Quiser replicar a análise do Pilar 4 → siga `04-manipulacao/05-metodologia-coleta.md`.
- Tiver dados de inventário/match para contribuir voluntariamente → ver instruções em `data/README.md`.

A proposta é tornar este o dossiê de referência em português sobre o assunto. A Valve mantém um ecossistema bilionário falando em código. Este texto fala devolta.
