# A Mecânica dos Drops Semanais

## Como o jogador comum vê o sistema

Você instala CS2, joga competitivo ou casual algumas vezes, sobe seu Profile Rank, e em algum ponto percebe que ganhou uma **Care Package** — uma caixa especial que aparece no fim de uma partida. Você abre, vê 4 opções (skins ou cases), escolhe 2. As 2 que sobraram desaparecem. Próxima semana, repete.

É um sistema simples, e para a maioria dos jogadores **funciona como retenção emocional**: "joguei, ganhei coisinha de graça, semana que vem ganho de novo".

Para quem opera bot farms, é uma **linha de produção**.

## Os requisitos exatos `[DOCUMENTADO]`

Para receber um drop semanal:

| Requisito | Detalhe |
|---|---|
| **Prime Status** | Obrigatório — **US$ 14,99** na Steam Store |
| **Private Rank ≥ 2** | Pequena fricção contra contas recém-criadas |
| **5.000 XP na semana** | Acumular jogando partidas competitive, deathmatch, casual ou outros modos |
| **Reset semanal** | Ciclo zera toda terça-feira (UTC); XP não acumula entre semanas |

Se 5.000 XP forem atingidos:

1. Aparece **Weekly Care Package** ao final da partida
2. Pacote contém **4 itens** revelados
3. Jogador escolhe **2** para guardar
4. Os outros 2 desaparecem (sem opção de troca)

Em semanas com **Weekly XP Bonus** (multiplicador 4x), o XP necessário é alcançado em **2-3 partidas competitive normais** — algo como 90 minutos de jogo, em prática.

Fontes oficiais e da comunidade:
- [Hellcase blog — CS2 Weekly Drop System Guide](https://hellcase.com/blog/guides/cs2-weekly-drop-system-guide/)
- [Tradeit.gg — CS2 Drop Pool in 2026](https://tradeit.gg/blog/cs2-drop-pool/)
- [Skinport blog — Complete Guide to Weekly Drops](https://skinport.com/blog/complete-guide-to-weekly-drops-in-counter-strike-2-cs2)
- [Bo3.gg — XP Overload](https://bo3.gg/articles/what-is-xp-overload-in-cs2)

## A composição do pool

O pool de itens em um Care Package muda ao longo do tempo. Tipicamente inclui:

- **Cases** (lootboxes regulares, valor médio US$ 0,50–2,50 cada no Marketplace)
- **Skins de tier baixo** (Mil-Spec ou Restricted, valor médio US$ 0,03–0,30)
- **Stickers e patches** (valor variável)
- Eventualmente itens promocionais ou sazonais

O **valor esperado** de um Care Package no Steam Marketplace, **por semana**, fica em torno de **US$ 0,50–1,50** após comissão de 15% da Valve.

## Por que isso é insignificante para um jogador comum

Para alguém com 1 conta:

- US$ 1/semana × 52 semanas = **US$ 52/ano**
- O jogador investiu US$ 14,99 em Prime — **payback** em ~15 semanas
- Após payback, "lucro" anual é em torno de US$ 35

Esses US$ 35 ficam **presos no Steam Wallet**, não saem da Steam. Para o jogador comum, é **café-money digital** — algo simbólico.

## Por que isso é uma fortuna em escala

Para um operador com **100 contas**:

- 100 × US$ 1/semana = **US$ 100/semana** = **US$ 5.200/ano**
- Custo inicial: 100 × US$ 14,99 = US$ 1.499 (Prime)
- Payback em ~15 semanas
- A partir daí: **lucro líquido**

Para uma operação com **1.000 contas**:

- 1.000 × US$ 1/semana = **US$ 1.000/semana** = **US$ 52.000/ano**
- Custo inicial: US$ 14.990 em Prime
- Custos de infraestrutura: PCs, eletricidade, software (cobertos em [04-tecnicas-automacao.md](04-tecnicas-automacao.md))

Para uma operação industrial com **10.000+ contas** (FarmLabs e XteamFarm sugerem operar nessa escala via clientes B2B):

- US$ 10.000+/semana
- US$ 500.000+/ano por operador
- E batem na **estimativa de US$ 600k/mês** mencionada por BitSkins para a maior operação individual

## A escala em comparação

A Valve, ao recolher comissão de 15% sobre as vendas dos drops farmados, faz parte da equação:

- 1 conta normal: US$ 1/semana, 15% = **US$ 0,15** para a Valve
- 1.000 contas farmadas: US$ 1.000/semana, 15% = **US$ 150/semana** para a Valve da operação inteira
- Indústria global ~ US$ 1M/mês: 15% = **US$ 150 mil/mês** para a Valve **só de comissão sobre Marketplace de drops**, antes de considerar venda em mercados secundários

E isso **antes** de contar:
- Os US$ 14,99 que cada bot farm paga em Prime por conta
- A receita indireta de aceleração da economia (preços de cases caem, mas mais cases circulam = mais comissão acumulada)

A Valve ganha duas vezes da mesma operação: **vende o ingresso (Prime)** e **cobra comissão na saída (Marketplace)**.

## XP Overload — o exploit que ganhou virou alvo da Valve

Em 2024, alguns criadores de conteúdo descobriram e divulgaram **XP overload bugs** — bugs em que partidas anômalas geravam XP em quantidade muito superior ao normal, permitindo atingir os 5.000 semanais em **uma única partida deathmatch privada**.

A reação da Valve foi reveladora:

- Trade ban de **1 ano** para criadores que **expuseram** o bug publicamente
- Inventário **não confiscado** (apenas trade desabilitado)
- Sem ação contra **operadores comerciais** que usavam o mesmo princípio em escala

Veja [06-acao-seletiva-da-valve.md](06-acao-seletiva-da-valve.md) para análise completa desse padrão.

## A mecânica anti-farm que a Valve **diz** ter

A Valve afirma que tem proteções contra farming:

- **Contas novas** têm restrições (não recebem drops imediatamente)
- **Movement detection** detecta padrões de bot
- **VAC** banha contas suspeitas em waves

Na prática:

- Restrições de conta nova são **superadas em ~1 semana** com Prime
- Movement detection é **trivialmente burlada** com scripts que adicionam ruído humano
- VAC raramente bana bots de farming — **o cheating não envolve hooks de memória**, então o VAC tradicional não tem o que detectar

A combinação significa: **a defesa anti-farm da Valve é, em prática, uma defesa simbólica**. Funciona contra farming individual amador, não contra operações comerciais.

---

## Fontes deste arquivo

- Hellcase blog: https://hellcase.com/blog/guides/cs2-weekly-drop-system-guide/
- Tradeit.gg: https://tradeit.gg/blog/cs2-drop-pool/
- Profilerr — Weekly Drops Chances: https://profilerr.net/weekly-cs2-drop-system-explained-rewards-you-can-get/
- Skinport: https://skinport.com/blog/complete-guide-to-weekly-drops-in-counter-strike-2-cs2
- Bo3.gg — XP Overload: https://bo3.gg/articles/what-is-xp-overload-in-cs2
- DMarket — CS2 Drop System Advanced Guide: https://dmarket.com/blog/cs2-drop-system/
- cs.money — Weekly Drops in CS2: https://cs.money/blog/cs-go-skins/everything-about-weekly-drops-in-counter-strike-2/
- Blog Cs2.ad — CS2 Drops Guide: https://blog.cs2.ad/cs2-drops/
- Steam Discussion — Cs2 farm weekly drop: https://steamcommunity.com/app/730/discussions/0/576014018531068586/
