# Glossário

Termos que aparecem repetidamente no dossiê. Para o leitor que conhece CS2 isso é redundante; para quem chegou pelo ângulo legal/regulatório, é a chave de leitura.

---

## Termos da economia de skins

**Skin** — Cosmético aplicado a uma arma em CS2. Não altera mecânica de jogo. Pode valer de centavos a mais de US$ 1 milhão (caso documentado pela petição da NY AG, 2026). Trocável e vendável no Steam Marketplace.

**Case** (caixa, lootbox) — Recipiente virtual contendo um conjunto pré-definido de skins. Aberto consome uma **chave** (key) paga (US$ 2,49–2,99). O conteúdo é aleatório, com probabilidades divulgadas apenas na China desde 2017 (forçadas pela Perfect World, parceira local).

**Key** (chave) — Item pago necessário para abrir uma case. Vendido pela Valve. **A key é a aposta.** Não é reembolsável e não pode ser revendida no Marketplace (medida da Valve para impedir uso de keys como moeda em sites de gambling).

**Drop semanal / Care Package** — Recompensa gratuita por jogar. Requer Prime + Private Rank 2 + 5.000 XP semanais. O jogador escolhe 2 de 4 itens oferecidos. Pode ser case, skin de baixo tier ou stickers.

**Trade-Up Contract** — Mecânica que permite trocar 10 skins de uma raridade pela tentativa de uma skin de raridade superior. Em outubro/2025, expandida para incluir facas (5 Covert → 1 faca/luva).

**Steam Marketplace / Steam Community Market** — Mercado oficial onde jogadores compram e vendem skins entre si. **A Valve cobra 15% de comissão sobre cada transação.** O dinheiro fica preso no Steam Wallet (não pode ser sacado).

**Inventário** — Conjunto de skins que um jogador possui. Pode ser público, privado ou apenas-amigos. Inventários públicos são raspáveis sem autenticação.

---

## Termos de jogabilidade e matchmaking

**Premier mode** — Modo competitivo principal de CS2 desde 2023. Sistema de rating numérico (CS Rating) substitui os antigos ranks com nomes (Silver, Gold, Global Elite).

**CS Rating / Rating Premier** — Pontuação numérica de 0 a 30.000+ que define o matchmaking em Premier. Reflete habilidade individual segundo algoritmo da Valve (não totalmente divulgado).

**MM / Competitive (legacy)** — Modo competitivo clássico com ranks nomeados e mapas individuais. Coexiste com Premier, com matchmaking separado.

**Trust Factor** — Algoritmo opaco da Valve que classifica "confiabilidade" do jogador para parear com outros similares. Considera comportamento dentro e fora de CS2 (reports recebidos, tempo em outros jogos Steam, idade da conta). Valve **não divulga a fórmula**.

**Smurf** — Jogador habilidoso usando uma conta secundária com rating baixo para enfrentar adversários mais fracos. Viola o Code of Conduct do Steam, mas a Valve não pune em CS2.

**Bot farm** — Operação industrial que mantém dezenas ou centenas de contas Steam em modo automatizado para acumular drops semanais e revendê-los. Estimada em US$ 1M+/mês como indústria global.

**Hit registration / Hit reg** — Detecção de tiros acertados pelo servidor. Falhas de hit reg são uma das queixas mais frequentes em CS2 e alimentam a desconfiança que o Pilar 4 investiga.

---

## Termos de anti-cheat

**VAC (Valve Anti-Cheat)** — Sistema de detecção de cheats da Valve, ativo desde 2002. **Não opera em kernel-level**, o que limita o que consegue detectar.

**VACnet** — Camada de machine learning sobre o VAC, treinada em demos e reports. Detecta padrões anômalos de comportamento. Versão 3.0 ficou offline em julho/2025 (Steam Discussion 594027788789443789).

**VAC Live** — Detecção em tempo real durante a partida (anuncia a saída do cheater no meio do jogo). Atualização stealth em **12–13 de setembro de 2025** disrompeu drasticamente o ecossistema de cheats.

**DMA card** — *Direct Memory Access card*. Hardware externo que lê a memória do jogo e roteia informações para um segundo PC, **invisível ao VAC** porque o cheat não roda na máquina monitorada. Bypass dominante de 2023 a setembro/2025.

**Cheat externo / closet cheater** — Cheat sutil (aim assist leve, walls intermitentes) usado para parecer apenas "muito bom" em vez de obviamente trapaceando. Dominante no nível alto de Premier antes do update de set/2025.

---

## Termos legais e regulatórios

**Loot box / mystery box** — Termo técnico-regulatório para case. Em jurisdições como Bélgica e Holanda, classificado como **jogo de azar** desde 2018.

**WSGC (Washington State Gambling Commission)** — Comissão estadual que emitiu cease & desist contra a Valve em 2016 sobre skin gambling.

**FTC (Federal Trade Commission)** — Agência federal dos EUA. Em 2017 firmou acordo com TmarTn e Syndicate (CSGOLotto) — primeiro caso da história do FTC contra influenciadores.

**NY AG (New York Attorney General)** — Procuradoria-Geral de Nova York. Em 25 de fevereiro de 2026, Letitia James protocolou ação contra a Valve por jogo de azar ilegal em CS2, TF2 e Dota 2.

**Class action** — Ação coletiva. A Hagens Berman protocolou class action federal contra a Valve em **9 de março de 2026** sobre o mesmo tema das lootboxes.

**Cease & desist** — Ordem para cessar conduta sob pena de ação civil/criminal. WSGC enviou em 2016.

**Disgorgement** — Devolução de lucros obtidos ilegalmente. É um dos pedidos da NY AG na ação contra a Valve.

---

## Patentes e teoria de matchmaking

**EOMM (Engagement Optimized Matchmaking)** — *Framework* publicado em 2017 por pesquisadores da UCLA e EA. Otimiza matchmaking para maximizar engajamento (e não para igualdade de skill). Paper: web.cs.ucla.edu/~yzsun/papers/WWW17Chen_EOMM.pdf.

**Patente Activision US20160005270A1** — "System and method for driving microtransactions in multiplayer video games". Descreve explicitamente parear jogadores que possuem itens com jogadores que não possuem, para **induzir compras**. Concedida.

**Patente EA US20170259178A1** — "Multiplayer video game matchmaking optimization". Variante do EOMM aplicada a microtransações.

**Importante**: nenhuma dessas patentes é da Valve. Elas estabelecem que **a tecnologia existe e é industrialmente aplicada** em jogos competidores. A questão do Pilar 4 é se a Valve usa algo análogo — e **não temos evidência direta disso**.

---

## Recursos e ferramentas

**Steam Web API** — Interface programática oficial da Valve. Endpoints relevantes: `GetPlayerSummaries`, `GetFriendList`, `GetOwnedGames`, `GetSteamLevel`, `GetUserStatsForGame`.

**Steam Market priceoverview** — Endpoint público que retorna o preço médio de uma skin no Marketplace. Usado para estimar valor de inventário.

**Leetify** — Plataforma terceira de estatísticas de CS2. Coleta demos e gera métricas de performance individual (ADR, K/D, headshot %, multikills, clutch rate). Tem **API Swagger pública** em `api-public-docs.cs-prod.leetify.com`.

**csstats.gg / Faceit Insights** — Outras plataformas de estatísticas, citadas como alternativa de validação.

**FarmLabs / XteamFarm** — Serviços comerciais de bot farming para CS2. Documentados no Pilar 3.

**ASF (ArchiSteamFarm)** — Aplicativo open-source de farming de cartões de troca Steam, com plugins comunitários (CS2Interface) que estendem para CS2.

---

## Convenções deste dossiê

- **Valores em USD** salvo indicação contrária. Conversão para BRL não é estável.
- **Datas no formato DD/MM/AAAA** ou "março/2025" para mês.
- **Termos em inglês** mantidos quando são nomes próprios (VAC, Premier, Trust Factor) ou jargão sem tradução estabelecida (case, skin, smurf).
- **`[DOCUMENTADO]`, `[ALEGADO]`, `[HIPÓTESE]`** — ver `proposta.md` para definição.
