# O Caso CSGOLotto e a FTC

## O que aconteceu, em uma linha

Em 2017, a Federal Trade Commission firmou acordo com **Trevor "TmarTn" Martin** e **Thomas "Syndicate" Cassell** por terem promovido seu próprio site de skin gambling no YouTube **sem informar que eram donos**. Foi o **primeiro caso da história do FTC contra influenciadores de mídia social**.

E é parte da história do cassino da Valve porque o site deles, **CSGOLotto.com**, operava inteiramente sobre a infraestrutura Steam — e movimentou volumes nada irrelevantes antes de ser exposto.

## A operação

A CSGOLotto, Inc. foi incorporada na Flórida em 2015. Operava como **site de cassino para skins de CS:GO**: jogadores depositavam skins (via API Steam), apostavam em jogos como coin flip e jackpot, e ganhavam ou perdiam para outros jogadores ou para a casa. A casa retinha uma fração das vitórias.

TmarTn e Syndicate produziam vídeos no YouTube com títulos do tipo:
- *"HOW TO WIN $13,000 IN 5 MINUTES (CS-GO Betting)"*
- *"$24,000 COIN FLIP (HUGE CSGO BETTING!)"*

Nesses vídeos, eles "ganhavam" no site sem revelar que **a casa era deles**. Outros influenciadores grandes foram pagos (em segredo) para promover o site também.

## A descoberta

**Junho/2016**: o YouTuber **HonortheCall** publicou registros de incorporação da Flórida provando que TmarTn e Syndicate eram os donos da CSGOLotto. Vídeo recebeu atenção limitada.

**Julho/2016**: o canal **H3H3 Productions** (mais de 1 milhão de inscritos na época) publicou um vídeo cobrindo o caso. **Aí o escândalo explodiu**: TmarTn fez vídeo de "desculpas" choroso, deletou conteúdo antigo, processou H3H3 (e perdeu), e a história dominou a imprensa de games por semanas.

## A ação do FTC

**Setembro/2017**: A FTC firma acordo com Martin, Cassell e CSGOLotto, Inc. Os termos:

1. **Sem multa imediata** — mas violações futuras de regras de endossamento custam **US$ 40.654 por infração**.
2. Obrigação permanente de divulgar **conexões materiais** com qualquer produto endossado.
3. Os dois ficam permanentemente proibidos de fazer endossamento enganoso de gambling.

**Ponto-chave**: a FTC **não** processou o esquema de gambling em si — só o engano publicitário. Esse limite é importante: a FTC entendeu que **proibir o gambling era trabalho de outra agência** (gambling commissions estaduais ou Department of Justice). E nenhuma delas atacou o problema de frente — até a NY AG em 2026.

Fontes:
- [FTC case page](https://www.ftc.gov/legal-library/browse/cases-proceedings/162-3184-csgolotto-trevor-martin-thomas-cassell-matter)
- [FTC press release oficial (2017)](https://www.ftc.gov/news-events/news/press-releases/2017/09/csgo-lotto-owners-settle-ftcs-first-ever-complaint-against-individual-social-media-influencers)
- [Petição (PDF)](https://www.ftc.gov/system/files/documents/cases/1623184_c-_csgolotto_complaint.pdf)
- [Cobertura ESPN](https://www.espn.com/gaming/story/_/id/20635149/federal-trade-commission-settles-owners-csgo-lotto)
- [Dot Esports](https://dotesports.com/counter-strike/news/csgolotto-scandal-ftc-settlement-order-17234)

---

## Por que isso importa para o caso da Valve

A defesa histórica da Valve nesse pilar é: "**não somos responsáveis por o que terceiros fazem com a API Steam**". Esse argumento aparece em sua resposta de 2016 à WSGC e ainda é a base da defesa em 2026.

O caso CSGOLotto **expõe a fragilidade dessa defesa** em três pontos:

### 1. A Valve não fechou a CSGOLotto antes de ser pressionada

CSGOLotto operou abertamente entre **2015 e 2016**. A Valve só agiu (cease & desist a 40+ sites de gambling, incluindo CSGOLotto) **depois** da pressão da WSGC em outubro/2016. Antes disso, a empresa **sabia que esses sites existiam** — eles dependiam tecnicamente da API Steam, e a Valve viu o tráfego — e não fez nada.

Isso tem duas implicações:

- **Ou a Valve aprovava implicitamente** o ecossistema (porque ele aumentava o valor de skins, e portanto o engagement no jogo).
- **Ou a Valve ignorava negligentemente** algo que sabia.

Em ambos os casos, a defesa "somos só plataforma neutra" fica mais frágil.

### 2. A operação tecnicamente dependia da Valve

Sites como a CSGOLotto **só funcionavam** porque:

- Tinham acesso à **API pública Steam** para receber skins via trade.
- Podiam abrir **bots Steam** para receber depósitos automaticamente.
- Confiavam no **trade hold** da Valve (que segura skins por dias) como infraestrutura anti-fraude.

Quando a Valve quis, em 2018, bloquear skin trading na Holanda e Bélgica, **ela conseguiu** — porque controla a infraestrutura. A escolha de não bloquear globalmente é uma decisão de negócio, não uma limitação técnica.

### 3. A própria Valve regularizou a relação com sites de gambling depois

Em 2019, a Valve atualizou seu **Steam API Terms of Use** para proibir explicitamente uso de bots para gambling. Mas a aplicação foi **reativa, não proativa**: sites são fechados quando reclamados ou quando quebram outras regras, raramente por iniciativa da Valve.

A indústria de gambling com skins **continua existindo em 2026**. Sites como CSGORoll, CSGOEmpire, Stake (com seção de CS) operam abertamente. Alguns são vagamente mais cuidadosos com KYC; muitos não.

---

## O subtexto cultural

O caso CSGOLotto também explica por que a comunidade de CS tem uma desconfiança crônica:

- Jovens (TmarTn e Syndicate eram jovens, públicos jovens) se autoinfectaram em algo que a estrutura permitia.
- A Valve foi **tornada beneficiária passiva** do esquema por anos antes de qualquer regulação chegar.
- E quando a regulação chegou, foi pelo **engano publicitário** — não pelo gambling em si.

Para muitos jogadores, o caso ficou marcado como **"o sistema é manipulável, e quem manda vai sempre sair impune"**. Isso é importante para entender o tom de cinismo que o Pilar 4 (manipulação de performance) tem na comunidade — porque uma vez que se acredita que **o cassino tolera abuso**, a hipótese de que ele **opera abusos** se torna intuitivamente mais plausível.

---

## O que o caso ensina sobre o que esperar em 2026

A NY AG, ao contrário da FTC, **vai direto na Valve** e direto no gambling em si — não em endossamento.

Se o caso for adiante, há quatro cenários:

1. **Valve perde** → desativação global de cases, possivelmente oficialização de um sistema regulado de skins (improvável a curto prazo).
2. **Settlement grande** → multa nove dígitos + reformas pontuais, mas modelo segue (cenário mais provável).
3. **Valve ganha** → cassino segue como está, e o caso vira precedente de proteção (mas Hagens Berman continua, e outros AGs estaduais podem entrar).
4. **Caso se arrasta indefinidamente** → padrão histórico desde 2016. A Valve é boa em ganhar tempo.

O único cenário que muda o pilar de verdade é o **1**. Os outros três significam que o cassino sobreviveu mais um round, mais um pouco machucado, mas funcional.
