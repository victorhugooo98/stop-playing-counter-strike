# A Economia do Cheating

## Cheating como mercado, não como acidente

Quem trapaceia em CS2 raramente está escrevendo seu próprio cheat. Existe um **mercado profissional** de cheats com:

- **Vendedores** com domínios públicos, painéis de admin, suporte ao cliente
- **Distribuidores afiliados** (revendedores)
- **Testers** (cheats premium oferecem demos)
- **Atualizações regulares** sincronizadas com patches da Valve
- **Garantias de não-detecção** com refund em caso de banimento

É uma **indústria de software** funcionando como qualquer SaaS — só que ilegal.

## Faixas de preço (pré-set/2025)

| Tier | Preço/mês | O que oferece |
|---|---|---|
| **Grátis / freeware** | US$ 0 | Cheats antigos, alta taxa de banimento, "experimente por sua conta" |
| **Entry-level pago** | US$ 5-20 | Aimbot básico, ESP/wallhack, atualizações esporádicas |
| **Premium "rage"** | US$ 30-80 | Cheats agressivos, com humanizadores básicos, suporte |
| **Premium "legit"** | US$ 80-200+ | Cheats sutis, ML-tuned para parecer humano, anti-screenshot |
| **DMA setup** | US$ 200-500 hardware + US$ 50-150/mês software | Indetectável a VAC tradicional |

A faixa premium-legit é a mais perigosa porque **não chama atenção** — cheaters nesse tier parecem apenas "boas". Foram exatamente esses os mais atingidos pelo update de set/2025.

## A logística do cheat-as-a-service

Sites típicos pré-2025 (alguns ainda ativos, outros derrubados pelo update de setembro):

- Domínios genéricos com palavras-chave de gaming + segurança
- Pagamento em **PayPal, crypto, gift cards Steam**
- Loja com licenças mensais ou semestrais
- Discord/Telegram com canal de status e suporte
- "Status pages" com indicador verde "VAC undetected" (frequentemente desatualizadas após o update)

A própria existência desses domínios e canais é evidência. A Valve **sabe que existem** — eles aparecem em qualquer busca. A escolha era priorizar **quais derrubar** e **quando**.

## O ecossistema DMA — visão técnica

**Hardware**:
- Placas DMA típicas: **PCILeech-compatible** (FPGAs como Squirrel, ScreamerM2)
- Custo: US$ 200-500 nas placas básicas, até US$ 1.500 em setups avançados

**Software**:
- Bibliotecas como **MemProcFS**, **PCILeech** (open source) servem de base
- Cheats DMA são camadas comerciais sobre essas bibliotecas
- Dois PCs em rede local: um joga, outro processa

**Detecção (pré set/2025)**: virtualmente impossível para anti-cheat user-mode. **Pós set/2025**: VAC Live aparentemente detecta via análise estatística de input (mouse movements impossíveis para humano, padrões de visão impossíveis para campo de visão real do jogador).

## Tamanho do mercado

Estimativas (não-oficiais, agregadas de imprensa especializada):

- **Compradores ativos**: dezenas a centenas de milhares globalmente
- **Receita anual da indústria de cheats** (apenas CS-relacionados): centenas de milhões USD
- **Operações maiores individualmente**: receitas mensais de **6-7 dígitos**

Compare com a indústria de bot farms (Pilar 3): também US$ 1M+/mês individualmente para os maiores. **Ambas existem porque o ecossistema permite**, e ambas são lucrativas. A diferença é que a Valve **lucra diretamente** com bot farms (via comissão de 15%) e **não lucra diretamente** com cheats — mas lucra **indiretamente** via tilt → mais cases.

## A dinâmica de tilt → cases

A psicologia é o conector entre cheaters e o cassino:

1. Jogador perde rounds para cheater suspeito
2. Frustração/raiva ativa o sistema dopaminérgico (não positivamente — em "alerta de perda")
3. Ao final da partida, há tendência a:
   - **Continuar jogando** ("uma boa pra compensar")
   - **Buscar reforço fácil** (uma case com chance de skin valiosa)
   - **Comprar Prime de novo** se foi banido injustamente ou trocou de conta
4. Todos os três comportamentos **monetizam para a Valve**.

Esse loop é estudado em literatura de game design predatório. Não estamos inventando o mecanismo — estamos apontando que **a Valve** se beneficia dele e, **portanto, tem incentivo para mantê-lo ativo**.

A Valve poderia, em teoria, ter feito o update de setembro/2025 em **2018**. Não fez. Os cheaters geraram, ao longo desses 7+ anos, **bilhões de dólares de tilt-driven case openings** — não diretamente quantificáveis, mas inegavelmente substanciais.

---

## O que muda pós setembro/2025

**Se o update se mantiver eficaz**:
- Cheating cai significativamente
- Tilt diminui (em parte)
- Receita de cases pode cair na margem
- Mas a credibilidade do jogo aumenta → retenção de jogadores → receita de longo prazo aumenta

**Se cheaters se adaptarem**:
- O jogo do gato e rato continua
- A Valve **agora tem precedente** de poder consertar quando quer
- Próximo ciclo de tolerância vai ser **mais difícil de defender publicamente**

A janela de credibilidade vai depender de **quão rápido** a Valve responde a próximas levas. O dossiê deve ser atualizado periodicamente para refletir.

---

## Fontes

- Skin.Club — Anti-Cheat Problems: https://community.skin.club/en/news/cs2-anti-cheat-problems-external-cheat-dev
- Key-Drop — Cheat Developer Exposes VAC: https://key-drop.com/blog/cs2-cheat-developer-exposes-vac-valve-anti-cheat-problems/
- Bo3.gg — VAC Live blocks DMA: https://bo3.gg/news/valve-has-eliminated-nearly-all-cheats-in-cs2-vac-live-even-blocks-dma-cards
- Strafe — VAC Live Update: https://www.strafe.com/news/read/vac-live-update-devastates-cs2-cheating-community/
- ExitLag — CS2 Cheats: Complete Breakdown: https://www.exitlag.com/blog/cs2-cheats/
- Tradeit.gg — CS2's Anti-Cheat System: https://tradeit.gg/blog/cs2s-anti-cheat-system-how-valve-tackles-cheating-in-counter-strike-2/
- Blog Cs2.ad — CS2 Cheating Problem: An Expert's Guide: https://blog.cs2.ad/cs2-cheating-problem/
- Blix.gg — CS2 Cheating 2025: https://blix.gg/blog/news/cs-2/cs2-cheating-problem-an-in-depth-look/
