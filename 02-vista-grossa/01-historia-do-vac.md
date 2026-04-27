# A História do VAC

## Visão geral

O Valve Anti-Cheat (VAC) existe desde **2002**. Em mais de vinte anos, **três limitações arquiteturais** se mantiveram constantes:

1. **Não opera em kernel-level**. Roda em user-mode. Cheats que injetam em kernel-mode ou que leem memória externamente (DMA cards) ficam fora do alcance.
2. **Detecção principalmente baseada em assinaturas conhecidas** — busca por padrões de bytes em memória. Cheats novos ou ofuscados passam.
3. **Banimento em batches** — VAC roda análises e bane em ondas. Cheaters operam por dias ou semanas antes da onda.

Em 2017, a Valve introduziu **VACnet**, uma camada de machine learning analisando demos e reports. Isso foi uma melhoria, mas seguiu sendo:
- **Reativa** (precisa de demos com cheating já consumado)
- **Confiando em reports** (cheaters sutis raramente são reportados)
- **Sem visibilidade kernel** (DMA cards continuam invisíveis)

## A linha do tempo do desfuncionamento

### 2018-2022 — A era do "VAC vai banir eventualmente"

Cheaters operavam abertamente em high Premier (MM), com profissionais reclamando publicamente. Banimentos vinham em **ondas trimestrais**, atingindo principalmente cheats grátis ou de baixa qualidade. Cheats pagos premium operavam **sem consequência por meses**.

### 2023 — Lançamento de CS2 e expectativa

Quando CS2 lançou em 2023, parte da comunidade esperava reset do problema com nova engine (Source 2). Não veio. **Cheats migraram em semanas**, frequentemente com features mais robustas (Source 2 facilitou hooks de memória em alguns aspectos).

### 2024 — A onda de DMA cards

**DMA cards** (Direct Memory Access) viraram a solução dominante para cheaters sérios. Funcionam assim:

- O cheater tem **dois PCs**: o de jogo (PC-A) e o de cheating (PC-B)
- Uma placa DMA (custando US$ 200-500) é instalada no PC-A
- Ela lê a memória do PC-A diretamente, sem o sistema operacional saber
- Os dados vão para o PC-B, que processa (vê posições inimigas, projeta crosshair, etc.)
- O resultado é **mostrado em uma tela auxiliar** ou via **HID injetado** (mouse/teclado virtual) no PC-A
- VAC **não vê nada**, porque nenhum software de cheating roda no PC-A

DMA cards eram **invisíveis ao VAC por design**. O único contra-medida era **detecção de padrões anômalos no comportamento** (VACnet) — e cheaters cuidadosos calibravam o cheat para parecer humano.

Cobertura: [community.skin.club](https://community.skin.club/en/news/cs2-anti-cheat-problems-external-cheat-dev), [key-drop.com](https://key-drop.com/blog/cs2-cheat-developer-exposes-vac-valve-anti-cheat-problems/).

### Final de 2024 / início de 2025 — o ápice da impunidade

**Cheat developers anônimos**, em entrevistas a Skin.Club Community e Key-Drop:

> *"VACnet está desatualizado e ineficaz. É mais fácil bypassar agora do que era em CS:GO."*

Pro players da cena profissional:

- **ropz** (FaZe): Premier "infested with cheaters" em alto nível
- Outras vozes pro: descreveram Premier como **inutilizável** acima de certo rating
- A imprensa (Dexerto, Richard Lewis Substack) cobriu repetidamente

A Valve responde com **batches periódicos de banimentos** — geralmente de **5.000-30.000 contas por wave**. Mas a impressão geral era que **a cada banido, dois entravam**.

### Julho/2025 — VACnet 3.0 offline

Em **julho de 2025**, a comunidade percebe via thread de Steam Discussion (596027788789443789) que o VACnet 3.0 está **offline**. Aparentemente uma atualização da Valve quebrou o sistema, e ele ficou desligado por **semanas**.

Durante esse período, cheaters operavam virtualmente sem detecção comportamental. Apenas detecção por assinatura permanecia, que cheats sofisticados já contornavam.

Isso é importante: **não foi apenas inação**. Foi **regressão funcional não comunicada à base de jogadores**.

### 12-13 de setembro de 2025 — A virada `[DOCUMENTADO]`

Sem aviso público, a Valve deploy uma atualização do **VAC Live** que faz coisas que ela jurava não conseguir fazer:

- **Detecta DMA cards** via análise de padrões anômalos de input (mouse movements impossivelmente perfeitos, latência inconsistente entre input e output)
- **Detecta "closet cheaters"** (cheats sutis usados por bons jogadores para parecer um pouco melhor) que escapavam há anos
- **Bane em tempo real**, não em wave — o cheater vê seu próprio banimento durante a partida

Cobertura:
- [Strafe](https://www.strafe.com/news/read/vac-live-update-devastates-cs2-cheating-community/)
- [Bo3.gg — Eliminates Nearly All Cheats](https://bo3.gg/news/valve-has-eliminated-nearly-all-cheats-in-cs2-vac-live-even-blocks-dma-cards)
- [Skin.Club Community — VAC Update Triggers CS2 Cheat Panic](https://community.skin.club/en/news/valve-vac-update-cs2-cheaters-panic-2025)

Em fóruns de cheat e canais Telegram, **vendedores em pânico**: refunds em massa, sites tirados do ar, cheats premium descontinuados. Pela primeira vez em anos, era **mais difícil estar trapaceando** que jogando limpo.

---

## A pergunta que organiza o pilar

> **Por que esperaram?**

Quando um sistema é mantido em ineficácia por mais de uma década e então corrigido em uma atualização sem aviso, há três explicações possíveis:

### Hipótese A — Limite técnico real, finalmente quebrado

Defensável até 2024. **Cada vez menos defensável** depois disso. DMA cards são tecnologia conhecida desde os anos 2000. Anti-cheats kernel-level (Vanguard da Riot, Easy Anti-Cheat da Epic) detectam DMA há anos. A Valve **escolheu** não ir kernel.

### Hipótese B — Recursos de engenharia limitados

Valve tem **<400 funcionários** segundo estimativas. Mas tem **US$ 16B/ano de receita estimada**. Contratar mais 50 engenheiros de segurança não é o gargalo. **A escolha foi de prioridade**, não de recursos.

### Hipótese C — Conflito de interesse

A explicação que se encaixa melhor com o resto do dossiê: enquanto o problema de cheaters era visto como **gerador de tilt → gerador de receita**, a Valve não tinha pressa. Quando o problema começou a ser visto como **risco existencial** (NY AG processando, pressão sobre lootboxes, possíveis acordos com Major organizers exigindo certificação anti-cheat), a Valve teve incentivo para resolver. E resolveu — em semanas.

A hipótese C **não pode ser provada** sem documento interno. Mas a hipótese A não explica os 10 anos de lentidão, e a hipótese B não explica como funcionários da Valve entregaram em semanas o que diziam ser impossível.

---

## O que isso significa para o futuro

**Bom**: o update de set/2025 melhorou drasticamente a integridade do jogo. Banimentos continuam saindo em volume. Pro players reportam menos suspeitas.

**Ruim**: a Valve mostrou que **pode fazer o trabalho quando quer**. Isso significa que toda inércia anterior **foi escolha**. E também significa que, se as pressões diminuírem, **a inércia pode voltar**.

**Pendente**: cheaters sempre se adaptam. A próxima onda já está em desenvolvimento (DMA cards mais discretos, simulação de input via firmware modificado, AI-powered humanizer). A pergunta é se a Valve vai responder em **dias** ou em **anos** dessa vez. A história anterior diz: depende de quanto está em jogo.

---

## Fontes deste arquivo

- Skin.Club — Anti-Cheat Problems Explained by External Cheat Dev: https://community.skin.club/en/news/cs2-anti-cheat-problems-external-cheat-dev
- Skin.Club — VAC Update Triggers CS2 Cheat Panic: https://community.skin.club/en/news/valve-vac-update-cs2-cheaters-panic-2025
- Strafe — VAC Live Update Devastates CS2 Cheating Community: https://www.strafe.com/news/read/vac-live-update-devastates-cs2-cheating-community/
- Bo3.gg — Eliminates Nearly All Cheats: https://bo3.gg/news/valve-has-eliminated-nearly-all-cheats-in-cs2-vac-live-even-blocks-dma-cards
- Key-Drop — CS2 Cheat Developer Exposes VAC: https://key-drop.com/blog/cs2-cheat-developer-exposes-vac-valve-anti-cheat-problems/
- Dexerto — Valve needs to address CS2's cheating problem: https://www.dexerto.com/counter-strike-2/valve-needs-to-address-cs2s-cheating-problem-before-it-ruins-hype-from-the-major-2624656/
- Richard Lewis: https://richardlewis.substack.com/p/talking-about-cheaters-in-cs2-has
- Steam Discussion — VacNet 3.0 offline: https://steamcommunity.com/app/730/discussions/0/594027788789443789/
- Steam Support oficial — VAC: https://help.steampowered.com/en/faqs/view/571A-97DA-70E9-FF74
