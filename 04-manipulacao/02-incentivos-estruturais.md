# Incentivos Estruturais

## O argumento

O Pilar 4 não tem prova direta. Mas tem **incentivos estruturais** documentados que tornam a hipótese **plausível por inferência**. Este arquivo apresenta esses incentivos com fontes — para que o leitor possa avaliar **por si mesmo** se eles são suficientes para justificar investigação empírica (que faremos em [05-metodologia-coleta.md](05-metodologia-coleta.md) e [06-resultados-analise.md](06-resultados-analise.md)).

## Incentivo 1 — A receita da Valve depende do Pilar 1

Resumido em [01-cassino/05-receita-da-casa.md](../01-cassino/05-receita-da-casa.md):

- US$ 1B+/ano em CS2 cases
- US$ 4,3B mercado total de skins
- 15% de comissão sobre cada venda

Para uma empresa nessa estrutura financeira, **toda decisão de design** que aumente o **gasto médio por jogador** é incentivada. Se manipulação de matchmaking pudesse — sutilmente, dentro do plausível — induzir mais aberturas de cases, **a Valve teria incentivo financeiro** para fazê-lo.

Isso não prova que faz. Estabelece que **se fizesse, seria racional** dentro do modelo econômico da empresa.

## Incentivo 2 — A indústria já desenvolveu a tecnologia

A patente **Activision US20160005270A1** — concedida — descreve, em texto literal:

> *"O matchmaking system pode identificar marquee players que usam itens que se quer promover, e parear esses marquee players com outros jogadores que **não** usam esses itens, para influenciar decisões de compra."*

E ainda:

> *"O matchmaking pode promover **resultados específicos** que demonstrem o valor de itens promocionais."*

Essa patente **existe**. **Foi concedida** pelo USPTO. Está em domínio público. Você pode ler a íntegra em [Google Patents](https://patents.google.com/patent/US20160005270A1/en).

A patente pertence a uma **competidora direta da Valve**. Não há evidência pública de que a Valve **use** algo análogo. Mas o fato de que **a tecnologia foi desenvolvida e patenteada** demolira o argumento "isso é teoria conspiratória, ninguém faria isso".

A indústria de games **já admitiu**, via patente, que esse tipo de manipulação é **uma direção de produto**.

## Incentivo 3 — EOMM como framework acadêmico publicado

Em 2017, pesquisadores da **UCLA + EA** publicaram em WWW (uma das principais conferências de Web research) o paper:

**"EOMM: An Engagement Optimized Matchmaking Framework"**
[PDF aqui](https://web.cs.ucla.edu/~yzsun/papers/WWW17Chen_EOMM.pdf)

Resumo: o paper descreve um framework de matchmaking que **maximiza engagement** em vez de **igualdade de skill**. Considera variáveis como:

- **Skill** (rating tradicional)
- **Esportividade** (toxicidade)
- **Estilo de jogo** (defensivo, agressivo)
- **Tipo de ataque preferido**

E pode ser configurado para otimizar para:

- **Tempo de jogo** (manter jogador engajado)
- **Retenção** (reduzir churn)
- **Spending** (aumentar gasto)

A **palavra "spending" aparece literalmente** no paper como objective configurável.

Se EA + UCLA publicaram esse framework em 2017, **outras empresas o conhecem**. A Valve, com sua escala e seus engenheiros, **pode** estar usando algo análogo. Não há evidência pública de que use. Mas **a tecnologia está documentada como aplicável**.

## Incentivo 4 — Trust Factor é opaco por design

A Valve mantém o **Trust Factor** como sistema **deliberadamente não-transparente**. A documentação oficial:

> *"O Trust Factor leva em conta uma combinação de fatores incluindo o comportamento do usuário em outros jogos Steam, a frequência de reports de outros jogadores, o tempo gasto jogando CS2 e outros jogos Steam, e mais."*

E, crucialmente:

> *"Para evitar manipulação, **a fórmula exata não é divulgada**."*

Esse argumento ("não divulgar evita manipulação") é circular: também impede **auditoria externa**. Sistemas de matchmaking de outras empresas (Riot Vanguard, EA EOMM) também são opacos — mas não há motivo de princípio para que **opacidade seja a única resposta**. Trust Factor poderia ser opaco em parte e auditável em outra (p.ex., divulgar variáveis incluídas mas não pesos).

A escolha de manter **inteiramente opaco** torna **impossível** descartar — formalmente — que skins/inventário sejam variáveis. **Não confirma**. Mas a falta de transparência é **incentivo a desconfiar**.

## Incentivo 5 — Hit registration é controvertido sem ser explicado

Hit registration em CS2 **continuamente** gera reclamações na comunidade:

- "Mirei na cabeça e não acertou"
- "Player com mais ping pareceu acertar antes que eu visse"
- "Comportamento parece inconsistente entre matches"

A explicação técnica padrão é:

- CS2 usa **hit registration server-side**
- Latência variável afeta a **percepção** de hit reg
- Diferenças entre tickrate (CS2 usa subtick) confundem expectativas vindas de CS:GO

Tudo isso é razoável. Mas há também **discordância dentro da comunidade técnica** sobre como exatamente o hit reg funciona, e a Valve **não publica documentação técnica detalhada** equivalente, por exemplo, à que Quake/Doom developers publicaram historicamente.

A combinação de **comportamento percebido como inconsistente** + **falta de documentação técnica detalhada** + **modelo de negócio que beneficia de tilt** = **incentivo para desconfiar** que não há explicação inocente.

Isso não é evidência. É **suspeita razoável** — que merece investigação empírica.

## Incentivo 6 — A Valve não é monitorada externamente

Diferente de empresas listadas em bolsa (que precisam reportar a investidores e enfrentam SOX/auditoria) ou empresas de gambling regulado (que são auditadas por agências), a Valve **não tem auditoria externa** comparável.

- **Empresa privada**: não publica resultados financeiros
- **Não tem regulador específico**: lootboxes não são "gambling oficial" na maioria das jurisdições
- **Trust Factor opaco**: nem comunidade nem reguladores podem verificar
- **Algoritmos internos**: não auditáveis

Em sistemas onde **incentivos financeiros** se alinham com **comportamento adverso ao usuário** e **mecanismos de monitoramento** estão ausentes, **o senso comum institucional** sugere que **comportamento adverso vai existir** em algum grau. Não necessariamente extremo. Mas não-zero.

Esse é o argumento estrutural: **na ausência** de auditoria, **na presença** de incentivos, e **com tecnologia disponível**, é **estatisticamente improvável** que **nada** esteja acontecendo.

## A síntese

Os 6 incentivos juntos:

1. Receita da Valve **depende** de gasto em skins
2. Tecnologia para induzir gasto via matchmaking **existe e é patenteada**
3. EOMM é **documentado academicamente** com objective de spending
4. Trust Factor é **opaco por design**
5. Hit registration tem **inconsistências percebidas** sem explicação pública detalhada
6. Não há **auditoria externa** que possa verificar

Tudo isso é **circumstancial**. Nenhum item, isolado, prova manipulação. Mas a **acumulação** torna a hipótese **mais plausível** que a alternativa "nada existe e é tudo placebo".

A análise empírica do [06-resultados-analise.md](06-resultados-analise.md) tentará discriminar entre as duas. **Esperamos provavelmente** encontrar **placebo** como explicação suficiente. Se encontrarmos algo mais, com o cuidado metodológico devido, será uma contribuição.

---

## Fontes

- Patente Activision US20160005270A1: https://patents.google.com/patent/US20160005270A1/en
- Patente EA US20170259178A1 (matchmaking optimization): https://patents.google.com/patent/US20170259178A1/en
- EOMM paper (UCLA + EA): https://web.cs.ucla.edu/~yzsun/papers/WWW17Chen_EOMM.pdf
- PCGamesN — EA matchmaking patent: https://www.pcgamesn.com/ea-matchmaking-microtransactions-eomm-engagement-patent
- TechRaptor — EA Filed Patents: https://techraptor.net/gaming/news/ea-filed-patents-for-online-matchmaking-algorithms-focusing-on-player-engagement
- Steam Discussion sobre EOMM em CS2: https://steamcommunity.com/app/730/discussions/0/4339861173663968580/
- Steam Discussion sobre matchmaking patent (Call of Duty): https://steamcommunity.com/app/1938090/discussions/0/4361249916213003725/
- Steam Support — CS2 Trust Factor Matchmaking: https://help.steampowered.com/en/faqs/view/00EF-D679-C76A-C185
- Dot Esports — Call of Duty SBMM transparency: https://dotesports.com/call-of-duty/news/call-of-duty-players-are-begging-for-transparency-over-how-sbmm-works
- YouTube — EOMM Theory: https://www.youtube.com/watch?v=IDYWBeCGdgQ
- YouTube — EOMM Explained: https://www.youtube.com/watch?v=-bimIjrNzBc
