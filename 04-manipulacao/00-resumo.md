# Pilar 4 — Manipulação de Performance: Investigação Própria

## Aviso editorial

**Este pilar é diferente dos três anteriores**. Os pilares 1, 2 e 3 são `[DOCUMENTADO]` — apoiados em fontes primárias, processos legais ativos, papers acadêmicos. **Este pilar 4 é `[HIPÓTESE]`** — uma conjectura sob investigação que ainda **não tem evidência direta** apontando para a Valve.

Por que ele entra no dossiê mesmo sendo especulativo:

1. É a acusação **mais frequente** na comunidade — desconfiança difusa de que skins/inventário afetam matchmaking, hit registration, ou outros aspectos de performance.
2. Existem **incentivos estruturais documentados** (patentes na indústria, modelo financeiro da Valve) que tornam a hipótese **plausível**, mesmo sem prova.
3. Há **metodologia disponível** para testar quantitativamente com dados públicos. Se não testarmos, a especulação continua circulando sem ser refutada **nem** confirmada.
4. O dossiê seria **incompleto** se ignorasse a hipótese mais comentada — mesmo para concluir "**não encontramos evidência**".

A diferença é que aqui **vamos publicar o resultado da análise honestamente**, mesmo que ela refute a hipótese. Se a análise não achar nada, o Pilar 4 vai dizer "não há evidência estatística — placebo é a explicação mais econômica". Se achar correlação anômala não explicada por confundidores, vai dizer isso também — com cuidado, controlando expectativas.

## A hipótese, em linguagem clara

**A versão fraca**: o algoritmo de matchmaking da Valve (Trust Factor, Premier rating, hit registration server-side) tem **algum viés** que correlaciona positivamente com **investimento financeiro** do jogador (skins, inventário valorizado, Prime ativo).

**A versão forte**: a Valve **deliberadamente** ajusta parâmetros de gameplay (tickrate efetivo, hit reg, matchmaking) com base em quanto cada jogador gasta, para **incentivar gasto** entre os que ainda não gastam.

A versão fraca é estatisticamente testável com dados públicos.
A versão forte exigiria **vazamento interno** ou **whistleblower** — não há, e o Pilar 4 não vai inventar.

## Por que **alguém** acreditaria na versão forte

Existem patentes industriais explícitas que fazem **exatamente** isso em outras empresas. A mais famosa:

- **Patente Activision US20160005270A1** — *"System and method for driving microtransactions in multiplayer video games"*. Concedida. Descreve, em texto literal, parear jogadores que possuem itens com jogadores que não possuem, para **induzir compras**.

Não é da Valve. Mas estabelece que **a tecnologia existe e é industrial**. Quando a Activision **patenteia** algo assim, fica difícil descartar a possibilidade de que **outros** também usem versões análogas, mesmo sem patente.

E quando o **modelo de negócio** da Valve é **vender skins** (Pilar 1), e o **incentivo financeiro** da Valve é **maximizar gasto por usuário**, a hipótese se torna **plausível por inferência estrutural** — mesmo que não temos a prova direta.

## A estratégia desse pilar

```
01-hipotese-formal.md          → H0/H1 formais e escopo do estudo
02-incentivos-estruturais.md   → As patentes, EOMM, e a economia da Valve
03-relatos-da-comunidade.md    → Sistematização de relatos (com ressalvas)
04-placebo-e-vies.md           → CONTRA-ARGUMENTO HONESTO antes da análise
05-metodologia-coleta.md       → PRÉ-REGISTRO público de método
06-resultados-analise.md       → A ser preenchido após coleta (v2.0)
```

A ordem é deliberada: **antes** de mostrar dados, mostramos:

1. A **hipótese formal**
2. Os **incentivos** que a tornam plausível
3. Os **relatos** que motivam investigação
4. O **contra-argumento honesto** (placebo, viés)
5. A **metodologia** (pré-registrada)
6. **Apenas então** os resultados

Esse ordenamento é como ciência séria deveria operar. Pré-registro **previne p-hacking** (escolher análises que confirmem a hipótese após ver os dados). Se publicarmos resultados sem ter ancorado a metodologia previamente, perdemos credibilidade.

## A versão honesta da expectativa

Antes de coletar qualquer dado, qual é a expectativa?

- **Provável**: encontrar correlação positiva entre valor de inventário e métricas de performance — porque jogadores com mais horas tendem a ter **mais skins** *e* **mais habilidade**, ambos consequências de tempo investido. Isso seria **explicado por confundidores**.
- **Improvável mas possível**: encontrar correlação **residual** entre valor de inventário e performance **mesmo controlando** por horas, idade da conta, Trust Factor proxy, e outros confundidores. Isso seria **anomalia** que merece atenção.
- **Plausível**: encontrar **diferenças entre jogadores Prime e não-Prime** que não sejam explicadas por skill — porque Prime literalmente **muda o pool de matchmaking** (mistura com mais ou menos cheaters/smurfs). Isso seria **esperado, não anômalo**.

Vamos entrar com expectativa **calibrada** e sair com **publicação honesta** do que encontrarmos.

## Recursos disponibilizados pelo autor do projeto

O autor (Victor Hugo / vhs) **autorizou expressamente**:
- Uso de seu perfil Steam público como semente de coleta
- Acesso à sua conta Leetify para scraping de partidas e adversários
- Inclusão de seus dados na análise (anonimizados via hash)

Um amigo de longa data (Pastor Cururu) tem **perfil público acessível**; sua inclusão se dá apenas pelo **canal público da API Steam** e respeita os mesmos limites de privacidade.

## Como ler este pilar

| Arquivo | Conteúdo | Status |
|---|---|---|
| [01-hipotese-formal.md](01-hipotese-formal.md) | H0 e H1, escopo do estudo | ✅ |
| [02-incentivos-estruturais.md](02-incentivos-estruturais.md) | Patentes, EOMM, economia da Valve | ✅ |
| [03-relatos-da-comunidade.md](03-relatos-da-comunidade.md) | Síntese de queixas comuns na comunidade | ✅ |
| [04-placebo-e-vies.md](04-placebo-e-vies.md) | Contra-argumento honesto | ✅ |
| [05-metodologia-coleta.md](05-metodologia-coleta.md) | Pré-registro do método | ✅ (v1.0) |
| [06-resultados-analise.md](06-resultados-analise.md) | Resultados e discussão | ⏳ v2.0 |
| [fontes.md](fontes.md) | Bibliografia mínima | ✅ |
