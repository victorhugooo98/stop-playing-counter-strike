# Placebo e Viés de Confirmação

## A regra do dossiê

Antes de qualquer análise empírica, este arquivo apresenta **a explicação alternativa mais econômica** para os relatos de manipulação. É a posição **cética e charitativa** com a Valve. **Se a análise não conseguir refutar esta posição, ela vence** — porque é a hipótese mais simples.

Esse exercício existe **antes** dos resultados para evitar que, se a análise não confirmar H1, o dossiê pareça estar **se desculpando** por ter levantado a hipótese. Se levantamos a hipótese e ela não se confirma, **a posição cética estava certa o tempo todo**, e o dossiê reconhece isso transparentemente.

## A explicação cética em uma frase

> Skins não afetam gameplay no nível de código. **Todos os efeitos percebidos** são produto de placebo, viés de confirmação, regressão à média e confundidores legítimos (Trust Factor, smurfs no pool, idade da conta). A "manipulação" é projeção psicológica em sistema opaco.

Esta posição é **defensável** com argumentos sólidos:

## Argumento 1 — Skins não tocam o código de gameplay

Toda análise técnica disponível confirma:

- Skins são **modelos visuais aplicados sobre armas** após o cálculo de gameplay
- O dano, recoil, accuracy e hit reg são **calculados pelo servidor** sem referência ao skin equipado
- Análises de demos (que mostram o estado do servidor, não o cliente) confirmam que **skin não aparece** nas variáveis de gameplay

Fonte: [sellyourskins.com — Do Skins Affect Gameplay?](https://sellyourskins.com/blog/do-skins-affect-gameplay/) e múltiplas análises técnicas comunitárias.

> *"CS2 mantém skins puramente cosméticas, com armas causando o mesmo dano, seguindo os mesmos padrões de recoil, e funcionando da mesma forma seja com um skin simples ou um item colecionável de US$ 100.000."*

Para que H1 seja verdade, a Valve precisaria estar manipulando **algo além do skin** — algum parâmetro de matchmaking, hit reg, ou Trust Factor — **com base no inventário**, não no skin equipado. Isso é tecnicamente possível, mas é uma **manipulação indireta** que precisaria de evidência separada.

## Argumento 2 — O efeito placebo é robusto e bem documentado

Em psicologia esportiva e cognitiva:

- **Atletas com equipamento favorito** performam mensuravelmente melhor que com equipamento neutro, mesmo quando o equipamento é **idêntico em performance objetiva**
- O efeito é **maior** em tarefas que exigem **foco e confiança**
- Em jogos competitivos, isso se traduz em melhor **decisão sob pressão**, melhor **mecânica fina**, e melhor **leitura do jogo**

Aplicado a CS2: jogador com skin cara que ele gosta:

- **Confiante** ao começar a partida
- **Mais focado** nos primeiros rounds críticos
- **Menos defensivo** (toma duels que jogador menos confiante evitaria)
- **Aceita mais risco controlado** — o que melhora performance em partidas mais ofensivas

Resultado: o **placebo positivo** das skins **realmente** melhora performance de quem as tem. Mas a melhoria vem **do efeito psicológico do jogador**, não de uma vantagem mecânica do sistema.

## Argumento 3 — Viés de confirmação é estatisticamente devastador

A psicologia cognitiva documenta que humanos:

- **Lembram** de eventos consistentes com sua hipótese
- **Esquecem** de eventos inconsistentes
- **Reinterpretam** eventos ambíguos como confirmação
- **Buscam ativamente** evidência que confirme expectativa

Aplicado a relatos de "manipulação":

- Jogador suspeita que matchmaking é injusto após perda
- **Lembra das partidas frustrantes** com oponentes com skin caro
- **Esquece** das partidas em que ganhou contra eles ou contra oponentes pobres em skin
- **Reinterpreta** rounds ambíguos (dano não-letal, hit reg duvidoso) como evidência

Em uma comunidade onde **a hipótese de manipulação é discutida abertamente**, novos jogadores **chegam pré-disposto** a interpretar suas experiências através dessa lente. É um efeito **autorreforçador**.

## Argumento 4 — Regressão à média explica "boa sorte segue má sorte"

Quase todos os relatos de "padrões anômalos" envolvem **sequências**:

- "5 partidas boas, depois 5 ruins"
- "Comprei Prime, próximas 10 partidas foram ótimas, depois caiu"
- "Atingi 25k rating, daí começou a cair"

Em qualquer série temporal com aleatoriedade:

- **Sequências extremas** (boas ou ruins) **regridem à média** com o tempo
- A média **não é constante** — é a **performance esperada do jogador** dado seu skill atual
- **Performance excepcionalmente acima da média** é, por definição, **temporária**

Quando jogador tem 10 partidas boas, ele está **provavelmente** acima da sua média esperada. As próximas 10 partidas, em média, vão ser **piores que as 10 anteriores** — não porque a Valve está sabotando, mas porque **a aleatoriedade é assim**.

Esse efeito é amplificado por:

- **Cansaço** após 10 partidas
- **Adversários ficaram mais difíceis** porque rating subiu
- **Confiança cresceu** → tomadas de risco mal-calibradas

Tudo isso explica **sem precisar de manipulação**.

## Argumento 5 — Confundidores explicam relatos coletivos

Vimos no Pilar 2 que **smurfs e cheaters** são problema documentado. Vimos no Pilar 3 que **bot farms** distorcem o pool. Esses são **confundidores reais** que fazem o matchmaking parecer "injusto" sem que a Valve precise estar manipulando especificamente.

Quando jogador atribui sua frustração a "manipulação por skins", pode estar **culpando o mecanismo errado**. A frustração é real. Mas a causa pode ser **smurfs no time adversário** ou **partida com bot farm em deathmatch**, não **conspiração de matchmaking**.

A análise empírica deveria conseguir **distinguir** entre essas explicações: se o efeito desaparece quando controlamos por Trust Factor proxy, **provavelmente é confundidor**. Se persiste, **algo mais está em jogo**.

## A consequência metodológica

Se entrarmos na análise **sem reconhecer** essa posição cética, corremos risco de:

- **Confirmar** H1 com correlação fraca (p-hacking)
- **Tratar placebo** como se fosse manipulação
- **Sensacionalizar** achado modesto

Pré-registramos os critérios em [01-hipotese-formal.md](01-hipotese-formal.md) justamente para evitar esses riscos. O critério de **p < 0.01 corrigido + effect size ≥ 0.05** existe para que **placebo não dispare H1**.

## A consequência editorial

Se a análise refutar H1, o dossiê **reconhece o cenário cético como vencedor** — mas isso **não invalida** os Pilares 1, 2, 3. Os outros pilares **não dependem** da hipótese de manipulação. A frustração documentada pode ser **suficientemente explicada** por:

- **Pilar 1**: tilt induzido por aberturas de cases
- **Pilar 2**: cheaters tolerados + smurfs impunes
- **Pilar 3**: bot farms distorcendo pool

Esses três pilares **isoladamente** explicam grande parte da experiência ruim em CS2. O Pilar 4, mesmo refutado, terá **valor metodológico** ao ter testado a hipótese mais forte e **dispensado** ela formalmente — em vez de a deixar como conjuntura permanente.

## A possibilidade que **não** podemos descartar

Mesmo a posição cética **não pode descartar** completamente que algum **pequeno efeito** exista, abaixo do limiar detectável estatisticamente. Manipulações sutis em sistemas opacos são, por definição, **difíceis de detectar com métodos observacionais**.

A honesta conclusão será sempre: "**dentro do que podemos testar, com a amostra disponível, com os métodos aplicáveis**". Manipulação **fora desse escopo** continua possível mas indemonstrável.

## A pergunta para o leitor

Antes de ver os resultados (em [06-resultados-analise.md](06-resultados-analise.md), preenchidos em v2.0), considere:

> Se a análise refutar H1, **isso muda** sua opinião sobre se a Valve manipula performance via skins?

Se sua resposta é "sim", você está sendo **bayesiano** corretamente — atualizando crença com evidência.

Se sua resposta é "não, eu sei que manipulam mesmo assim", você está em uma posição **não-falsificável** — e o dossiê não pode te alcançar a partir daí. Vale refletir.

---

## Fontes

- sellyourskins.com — Do Skins Affect Gameplay?: https://sellyourskins.com/blog/do-skins-affect-gameplay/
- Eloking — Do Skins Help in CS2?: https://eloking.com/blog/do-skins-help-in-csgo
- aboutchromebooks.com — Do Counter Strike Skins Make You Better Player?: https://www.aboutchromebooks.com/do-counter-strike-skins-actually-make-you-a-better-player/
- Wikipedia — Confirmation bias: https://en.wikipedia.org/wiki/Confirmation_bias
- Wikipedia — Regression toward the mean: https://en.wikipedia.org/wiki/Regression_toward_the_mean
- Wikipedia — Placebo effect: https://en.wikipedia.org/wiki/Placebo
- Princípios de pré-registro contra p-hacking: https://www.cos.io/initiatives/prereg
