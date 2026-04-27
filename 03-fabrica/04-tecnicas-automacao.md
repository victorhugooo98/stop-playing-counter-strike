# Técnicas de Automação

Este arquivo descreve as técnicas usadas por bot farms **com finalidade documental** — entender o sistema é necessário para diagnosticá-lo. **Não é manual**. Não fornecemos código pronto, configurações específicas ou guias de implementação. As referências apontam para discussões públicas e código já existente, que a Valve já tem acesso e poderia derrubar quando quiser.

---

## A pilha técnica padrão

### Camada 1 — Isolamento de instância

Para rodar **múltiplas cópias de CS2 simultaneamente** em um único PC, operadores usam:

- **Sandboxie / Sandboxie-Plus** — sandboxa processos Windows, permitindo múltiplas instâncias do Steam/CS2 isoladamente
- **VMware Workstation / VirtualBox** — máquinas virtuais completas, mais pesadas mas mais isoladas
- **Docker / containers** — possível mas raro porque CS2 exige driver gráfico

A escolha típica é **Sandboxie** porque:
- É leve (10-15 instâncias por PC mediano)
- Rápido de configurar
- Não exige licença Windows separada por instância
- A Valve **não detecta** Sandboxie no nível de processo de jogo

### Camada 2 — Multilogin Steam

Cada instância precisa de uma conta Steam diferente, então operadores usam:

- **Steam command-line login** com credenciais diferentes por sandbox
- **Steam Mobile Authenticator desabilitado** (ou contas sem 2FA)
- **Cookie/token caching** para auto-login após reboot

Isso quebra padrões "normais" de uso, mas a Valve **não bana** em massa por isso — provavelmente porque o ASF tradicional (legítimo para card farming) usa estratégias similares.

### Camada 3 — Automação dentro do jogo

Uma vez dentro do CS2, o bot precisa **gerar XP**. Os scripts mais comuns:

**Modo deathmatch privado**:
- Cria lobby com 10 bots (2 times de 5)
- Configura mapa pequeno (Aim Maps são populares)
- Inicia partida
- Bots correm em círculos atirando uns nos outros
- XP acumula até 5.000 → drop

**Modo casual com bots**:
- Cria lobby casual privado
- Configura bots oponentes
- Rounds curtos com objetivo simples (planta bomba ou tempo)

**Comportamento humanizado**:
- Movimento com **micro-perturbações** (não move em linha reta perfeita)
- Atirar com **delay aleatorizado** (não atira no frame exato em que vê inimigo)
- **Pause aleatório** entre rounds
- **Alternar mapas** ocasionalmente

Tudo isso é programado para **passar nos critérios de "comportamento atípico"** que a Valve poderia usar para detecção. Bots **bem feitos** parecem jogadores casuais ruins.

### Camada 4 — Coordenação de múltiplos bots

Para escalar de 10 para 1.000 contas, o operador precisa:

- **Painel central** que monitora status de cada bot
- **Detecção de erros** (jogo crashou? Steam deslogou? VAC banido?)
- **Restart automático**
- **Monitoramento de drops** (o XP foi atingido? Care Package abriu?)
- **Coleta automática** dos itens dropados → Marketplace ou trade-out

Esse software de coordenação é **a IP** dos provedores comerciais. FarmLabs e XteamFarm essencialmente vendem **isso** — não os bots em si (qualquer um pode rodar bots), mas o **painel de gestão** que torna 10.000 bots tratáveis como uma operação.

### Camada 5 — Liquidação dos drops

Drops semanais não são receita até serem vendidos. Operadores vendem em:

**Steam Marketplace** (US$ 0,50–1,50 por drop):
- Mais simples, mais fricção (15% comissão Valve, dinheiro fica no Wallet)
- Útil para **trocar por outras skins** que serão vendidas em mercado externo

**Mercados externos** (DMarket, Skinport, BitSkins, CS.MONEY):
- Comissões de 5-12%
- Cash out em PayPal, crypto
- Risco de chargeback (mitigado por trade hold)

**B2B em volume**:
- Provedores de farming vendem **toda a produção** semanalmente para um trader único
- Trader cobra desconto (10-20% abaixo do preço de mercado) em troca de volume garantido
- Trader vende em retail nos mercados externos

A liquidação é **o gargalo** da operação — Steam Marketplace tem **rate limits** em listagens por hora, e mercados externos exigem trading com humanos via Steam (também com rate limit).

---

## Mecanismos de detecção que a Valve **não** está usando agressivamente

Há várias técnicas que **anti-bot moderno** poderia aplicar. Reconhecemos cada uma porque a Valve as **conhece** e **escolhe** não usar:

### 1. Análise de grafo de pagamento

1.000 contas comprando Prime em sequência, com cartões emitidos na mesma rede, em IPs do mesmo /24 → **assinatura óbvia** de operação coordenada.

A Valve poderia bloquear ou flag esses fluxos de pagamento. **Não bloqueia**.

### 2. Análise de comportamento estatístico

10 bots em uma lobby cujos movimentos têm correlação maior que entre 10 humanos em outra lobby → **assinatura ML detectável**.

A Valve **provavelmente coleta** essa telemetria. **Não age sobre ela** sistematicamente.

### 3. Captcha periódico

Inserir captchas leves (puzzles de 5 segundos) periodicamente em jogo → **trivial** para humano, **proibitivo** para bot em escala. Outros jogos usam (Roblox, MMOs). CS2 não usa.

### 4. Verificação de hardware

Coletar **fingerprint de hardware** (CPU ID, MAC, drivers instalados, etc.) e bloquear quando o **mesmo fingerprint** aparece em múltiplas contas Prime.

A Valve **coleta** algumas dessas informações. **Não as usa** consistentemente para anti-farm.

### 5. Análise de pico temporal

Se 1.000 contas todas atingem 5.000 XP em **janelas idênticas** todas as semanas, é estatisticamente impossível serem humanos diferentes coordenando independentemente. **Detecção trivial**.

### 6. Limite de contas Prime por método de pagamento

Limitar a **N contas Prime** que podem ser pagas com o **mesmo cartão de crédito** ou Steam Wallet. Outros serviços online fazem isso.

A Valve **não impõe limite**.

---

## A pergunta retórica

Cada uma dessas técnicas é **trivial** em comparação ao update de VAC Live de setembro/2025 (que detecta DMA cards via análise estatística). Se a Valve **pode** detectar DMA cards comerciais (US$ 200-500 de hardware com obfuscação de input), ela **certamente pode** detectar bot farms (1.000 contas com padrões de movimento idênticos rodando em sandboxes).

A Valve **não detecta** porque **não quer detectar**. E a explicação consistente — apoiada pelo dossiê inteiro — é que **o farming subsidia o cassino**. Se a Valve realmente quisesse acabar com o farming, **acabaria em semanas**, como acabou com cheats em setembro de 2025. Não acaba.

Esse é o resumo do pilar: **a inação é eloquente**.

---

## Aviso ético

Este documento é **descrição de sistema existente**, não **tutorial de operação**. Bot farming **viola** o Steam Subscriber Agreement e o CS2 Code of Conduct. Operadores podem ter contas banidas (mesmo que raramente), inventários travados, e em algumas jurisdições enfrentam exposição civil ou criminal por **fraude** ou **descumprimento de contrato**.

Recomendação a leitores: **não opere bot farms**. O dano à comunidade é real (degrada matchmaking de drops, desvaloriza o jogo dos jogadores casuais), mesmo que a Valve seja cumplice estrutural.

---

## Fontes

- BitSkins — CS2 Case Farming: https://bitskins.com/blog/cs2-case-farming-a-look-into-one-of-the-most-lucrative/
- Skin.land — How to Farm XP in CS:GO/CS2: https://skin.land/blog/csgo-and-cs2-xp-farming/
- Bo3.gg — XP Overload: https://bo3.gg/articles/what-is-xp-overload-in-cs2
- FarmLabs: https://farmlabs.dev/
- XteamFarm: https://xteamfarm.com/
- ArchiSteamFarm: https://github.com/JustArchiNET/ArchiSteamFarm
- Citrinate/CS2Interface: https://github.com/Citrinate/CS2Interface
- redlfox/awesome-cs2-trading (curadoria): https://github.com/redlfox/awesome-cs2-trading
- Sandboxie-Plus (ferramenta legítima): https://github.com/sandboxie-plus/Sandboxie
