# A Ação Seletiva da Valve

## O smoking gun do Pilar 3

A Valve **agiu** contra exploits de XP. Mas agiu **errado**:

- **Baniu creators que expuseram bugs publicamente** (trade ban de 1 ano)
- **Não baniu operações comerciais** que lucram com mecânicas similares (FarmLabs, XteamFarm continuam ativos)

Esse padrão revela a lógica real: **falar publicamente** sobre o problema é punido; **lucrar comercialmente** com ele é tolerado.

## O caso do XP overload

Em 2024, alguns criadores de conteúdo descobriram bugs específicos no sistema de XP que permitiam **acumular XP em quantidades anormalmente altas** em partidas privadas. Algumas técnicas envolviam:

- Configurações específicas de lobby que faziam o jogo recompensar XP mais do que o normal
- Modos de jogo com bots IA que geravam XP por kills sem limite efetivo
- Combinações de configuração que multiplicavam o ganho

Vários creators **publicaram vídeos no YouTube** mostrando como atingir os 5.000 XP necessários **em uma única partida** ou em 10-15 minutos de farming privado.

A reação da Valve, segundo cobertura de [Skin.land — How to Farm XP in CS:GO/CS2](https://skin.land/blog/csgo-and-cs2-xp-farming/) e discussões em [Steam Community](https://steamcommunity.com/app/730/discussions/0/603022666611306643/):

> *"Many CS2 creators who exploited bugged deathmatch XP lobbies received one-year trading bans, restricting their trading capabilities but not affecting their skin inventory."*

Detalhes importantes:

1. **Trade ban de 1 ano** — não banimento de jogo, não confisco de itens
2. **Atingiu creators conhecidos** que postaram vídeos
3. Aparentemente **não atingiu operações comerciais** que usavam o mesmo bug em larga escala

## O que isso comunica

A mensagem implícita é cristalina:

**Se você tem 1 milhão de seguidores no YouTube e mostra um bug → punição imediata visível**

**Se você tem 1.000 contas em sandboxes lucrando US$ 50.000/ano com o mesmo bug → você opera anos sem consequências**

A interpretação **caridosa**: a Valve usou os creators como **exemplo público** ("não façam isso") para desincentivar. Os bots, por serem invisíveis, são tratados separadamente.

A interpretação **honesta**: punir creators é **PR positivo gratuito** (vídeos chamando atenção do bug = ameaça à percepção do sistema). Punir bots é **receita negativa** (eliminar 100k contas = perder US$ 1,5M+ em Prime + comissão recorrente).

A história anterior do dossiê — particularmente o Pilar 2 e a virada de setembro/2025 — apoia a interpretação honesta. **A Valve age quando incentivos financeiros se alinham com a ação**. Punir creators alinhava-se. Punir bot farms não.

## A inconsistência da política

A política oficial da Valve sobre farming/multi-account, em qualquer leitura honesta do Steam Subscriber Agreement:

- **Multi-account farming viola TOS** ✅
- **Automação que "contorna mecânicas pretendidas"** viola TOS ✅
- **Venda de itens digitais via marketplace para fins comerciais não-pretendidos** existe em zona cinzenta ⚠️
- **Bots em deathmatch privado** — TOS não tem proibição direta, mas **viola o espírito** do sistema de drops ⚠️

Quem rodar bot farm em escala comercial está **violando TOS**. Mas a Valve **não enforce** essa regra. Não há histórico documentado de operação comercial de bot farming sendo desligada por iniciativa da Valve.

Comparação: **uma única conta** que tenta usar bots simples para farming sem cuidado **às vezes** é banida. A operação **com escala e sofisticação** **não é** — provavelmente porque:

1. Ela **paga mais Prime** (mais incentivo a manter)
2. Ela **gera mais comissão** (mais receita perdida ao banir)
3. Ela **distorce menos PR** (não há jogador real reclamando do bot)

A política de enforcement da Valve, na prática, é: **pune amadores baratos; tolera profissionais lucrativos**.

## A defesa do "API tolerada"

Há um argumento da Valve, em conversas privadas com a comunidade trade, de que **certos farming tools** são tolerados porque servem propósitos legítimos (ASF original, por exemplo, foi desenhado para card farming legítimo).

O problema com esse argumento:

- **O propósito** (cards) é só legítimo porque a Valve **chamou de legítimo**
- **A mesma arquitetura técnica** estende para CS2 cases via plugins (CS2Interface)
- A Valve **não desativa** a API que viabiliza tudo isso
- Resultado: a Valve criou **infraestrutura tolerada** que **se converte** em ferramenta de farming agressivo

A escolha de **manter** essa infraestrutura é decisão consciente. A Valve **podia** restringir API Steam para excluir uso programático de CS2 — não restringe.

## A ação preventiva que **falta**

Para um ator que realmente quisesse acabar com bot farming, há ações **óbvias** e **públicas**:

1. **Comunicado oficial** dizendo "vamos tomar ação" → atinge percepção sem custo direto
2. **Banimento de FarmLabs/XteamFarm** especificamente (com publicidade) → desincentiva clientes
3. **Limite hard de Prime por hardware/IP/método de pagamento** → fricção operacional
4. **Captcha periódico** em jogo → fricção comportamental
5. **Comunicado privado** a operadores comerciais (cease & desist) → economicamente eficaz, baixo PR risk

Nenhuma dessas ações foi tomada publicamente. A inação **é a política**.

## A pergunta para o leitor

Por que uma empresa que **detectou e desativou DMA cards** em uma noite (set/2025) **não consegue desativar** painéis de bot farming que **operam em domínios .com com SEO**?

A resposta honesta: porque **ela não quer**. E a razão de não querer é que esses painéis **são lucrativos** para ela, mesmo que ilegítimos.

Esse é o argumento central do Pilar 3, condensado: **a Valve não tem interesse financeiro em desligar a fábrica que ela mesma fingirá não ver**.

---

## Fontes

- Skin.land — How to Farm XP (citação do trade ban de 1 ano): https://skin.land/blog/csgo-and-cs2-xp-farming/
- Bo3.gg — XP Overload: https://bo3.gg/articles/what-is-xp-overload-in-cs2
- Steam Discussion — Item and XP Farmbot Problem: https://steamcommunity.com/app/730/discussions/0/603022666611306643/
- Steam Discussion — CS2 Bot Farming Out of Hand: https://steamcommunity.com/app/730/discussions/0/506199789077039666/
- BitSkins — CS2 Case Farming: https://bitskins.com/blog/cs2-case-farming-a-look-into-one-of-the-most-lucrative/
- Dust2.in — Case farms: https://www.dust2.in/news/48201/case-farms-the-dark-side-of-counter-strike
- FarmLabs (operação visível): https://farmlabs.dev/
- XteamFarm (operação visível): https://xteamfarm.com/
- Steam Subscriber Agreement: https://store.steampowered.com/subscriber_agreement/
