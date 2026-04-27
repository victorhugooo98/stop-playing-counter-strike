# A Mecânica do Cassino

## Como funciona, passo a passo

### Passo 1 — A aposta (a key) `[DOCUMENTADO]`

O jogador clica em "Buy Key" no inventário. Cada chave custa **US$ 2,49 a US$ 2,99** dependendo do tipo de case. O pagamento vai direto para a Valve, sem intermediário.

**Detalhe importante**: a key não é vendável no Steam Marketplace desde 2022. A Valve removeu a possibilidade de revender chaves justamente para impedir que sites de gambling usassem keys como moeda. Mas isso só fechou um vetor — o gambling com skins continua, e as keys continuam sendo o ingresso primário.

### Passo 2 — A roleta (a abertura)

Ao abrir a case, o jogador vê uma animação de **slot machine**: uma fita rolando horizontalmente com prévias de skins, desacelerando até parar em uma. A petição da NY AG descreve essa animação literalmente: "an animated spinning wheel that eventually rests on a selected item" — a procuradora usa o vocabulário de cassino de propósito.

### Passo 3 — A distribuição de probabilidades `[DOCUMENTADO, mas oculto fora da China]`

Cada case tem 5 tiers de raridade:
- Mil-Spec (azul) — comum
- Restricted (roxo) — ~16%
- Classified (rosa) — ~3,2%
- Covert (vermelho) — ~0,64%
- Special / Knife (dourado/amarelo) — **0,26%** (1 em 385)

Esses números **só foram divulgados** porque a Perfect World, parceira da Valve na China, é obrigada por lei chinesa (desde 2017) a publicar odds. Em todo o resto do mundo, **a Valve não publica os números** — quem os conhece, conhece pelo vazamento chinês.

A skin de raridade especial pode valer dezenas, centenas ou milhares de dólares dependendo da skin específica e do float (estado de desgaste). O retorno esperado é, na média, **menor que o custo da chave** — como qualquer caça-níquel honesto.

### Passo 4 — A liquidez (Steam Market) `[DOCUMENTADO]`

Para transformar a skin em algo aproveitável, o jogador tem duas rotas:

**Rota A — Steam Marketplace (oficial)**:
- Vende a skin
- A Valve cobra **15% de comissão** sobre o preço da venda
- O dinheiro vai para o **Steam Wallet**, que **só pode ser gasto na Steam** (em jogos, DLCs, ou novas keys/skins)
- Não tem cash out direto

**Rota B — Mercados de terceiros (cinza/ilegal)**:
- Sites como Skinport, BitSkins, DMarket, CS.MONEY
- Comissões variando 5%–15%
- Cash out em PayPal, crypto, transferência bancária — para o **dinheiro real**
- A Valve não controla esses mercados, mas tampouco os impede de operar (a maioria depende da API pública Steam, que a Valve poderia restringir)

A Rota B é o que dá ao esquema características claras de jogo de azar: a possibilidade de **converter o ganho em dinheiro real** é o que diferencia um sorteio em jogo de uma aposta em cassino.

### Passo 5 — O loop

Resultados pequenos = "azar, mas continua tentando".
Resultados grandes = "consegui agora, vou tentar de novo".
Resultados zero = "tá na hora de mudar a sorte".

Esse é o **comportamento clássico de jogador de slot**. Os papers acadêmicos referenciados em [04-impacto-em-menores.md](04-impacto-em-menores.md) documentam que crianças e adolescentes desenvolvem esse padrão de comportamento mais rápido que adultos.

---

## Os elementos legais que tipificam jogo de azar

A teoria jurídica clássica de jogo de azar requer três elementos:

| Elemento | Em CS2? |
|---|---|
| **Consideration** (algo de valor é apostado) | ✅ A key custa dinheiro real |
| **Chance** (resultado aleatório) | ✅ A skin sai por sorteio com probabilidade ~0,26% para top tier |
| **Prize** (recompensa de valor) | ✅ Skins valem dinheiro real (Marketplace + mercados terceiros) |

A Valve historicamente argumenta que o terceiro elemento não é satisfeito porque "a recompensa só pode ser usada no Steam". A NY AG, em 2026, descarta esse argumento citando que:

> "Esses itens podem ser liquidados via Steam Community Market ou plataformas externas de troca por dinheiro real" — petição NY v. Valve, ¶36 (parafraseado, ver PDF para texto literal)

E que, mesmo a regra "fica preso no Steam Wallet", **não desqualifica** o esquema porque o jogador apostou dinheiro real e teve resultado de valor variável e quantificável.

---

## Comparação com cassinos físicos regulados

| Atributo | Cassino físico (Las Vegas) | CS2 cases |
|---|---|---|
| Idade mínima | 21 (verificação documental) | 13 (checkbox auto-declarado) |
| Probabilidades publicadas | Obrigatório por lei | Apenas na China |
| Limite de gasto / auto-exclusão | Programas obrigatórios | Inexistente |
| Auditoria de RNG | Por agência reguladora estadual | Auditoria interna não publicada |
| Imposto sobre ganhos | IRS form W-2G acima de US$ 1.200 | Zero |
| Suporte a jogador problemático | Linhas de ajuda obrigatórias | Inexistente in-game |
| Comissão da casa | Geralmente 1%-15% | 15% (Marketplace) |

Em todos os critérios em que um cassino regulado é mais protetivo, **CS2 cases é menos**. O argumento de "não é cassino" se sustenta cada vez menos com o passar dos anos.

---

## A inovação Trade-Up Contract (outubro/2025)

Em 23 de outubro de 2025, a Valve adicionou a possibilidade de criar **facas e luvas** via Trade-Up Contract: 5 skins Covert (~vermelho) podem ser combinadas para garantir uma faca/luva.

Por que isso importa para a tese do cassino?

- O preço médio de facas raras **caiu 20%–50% em um único dia** (Dataconomy, out/2025).
- Significa que a Valve **controla a oferta** do item mais cobiçado — exatamente como um cassino controla os payouts.
- Ao mesmo tempo em que dilui o valor de quem já abriu cases, **incentiva mais aberturas** porque agora há um caminho garantido para o item raro.

É a definição clássica de **manipulação de mercado por house operator**.

---

## Fontes deste arquivo

- Probabilidades chinesas: divulgadas em https://csgo.com.cn/ (oficial Perfect World)
- Petição NY v. Valve (2026): https://ag.ny.gov/sites/default/files/court-filings/new-york-v-valve-corporation-complaint-2026.pdf
- Trade-Up Contract update: https://dataconomy.com/2025/10/23/cs2-trade-update-upends-skin-market-with-new-knife-crafting/
- Drop rates compilados: https://casecalculator.app/drop-rates
- Análise jurídica acadêmica: https://entertainmentlawreview.lls.edu/slot-machines-in-disguise-regulating-video-game-loot-boxes-under-gambling-law/
