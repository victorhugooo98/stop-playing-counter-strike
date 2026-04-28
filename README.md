# Stop Playing Counter-Strike

> Dossiê investigativo sobre quatro práticas da Valve que alimentam um único modelo de negócio: **a economia de skins de Counter-Strike 2**.

---

## TL;DR

A Valve fatura **mais de US$ 1 bilhão por ano** com Counter-Strike 2. Esse dinheiro vem majoritariamente de uma engrenagem que combina:

1. **Um cassino disfarçado** de jogo (lootboxes/cases) — sob processo da Procuradoria-Geral de Nova York desde fevereiro/2026.
2. **Tolerância deliberada com cheaters e smurfs**, porque a frustração que eles causam vende mais skins.
3. **Um sistema de XP semanal** que terceiriza a fabricação de cases para uma indústria paralela de bot farms (estimada em **US$ 1M+/mês**), da qual a Valve embolsa 15% de comissão a cada venda.
4. **Hipótese de manipulação direta da performance do jogador** conforme seu gasto em skins. **Investigamos empiricamente** com 1.540 perfis Steam e **não encontramos suporte estatístico** — placebo + confundidores explicam os dados disponíveis. Ver [Pilar 4](04-manipulacao/06-resultados-analise.md).

Cada um desses quatro pilares é, isoladamente, problemático. Juntos, formam um **ciclo fechado** em que cada falha alimenta a próxima.

Este dossiê documenta o que é fato, o que é alegação em curso, e o que ainda é hipótese — e oferece uma metodologia para testar a quarta acusação com dados públicos.

---

## Índice

### [00. Introdução](00-introducao/)
- [Proposta e tese central](00-introducao/proposta.md)
- [Glossário de termos](00-introducao/glossario.md)

### [01. O Cassino](01-cassino/) — *o motor financeiro*
> Como lootboxes viraram um esquema de jogo que sobreviveu a investigações regulatórias em pelo menos 4 países.

- [Resumo](01-cassino/00-resumo.md)
- [Mecânica do cassino](01-cassino/01-mecanica-do-cassino.md)
- [Cronologia legal 2014–2026](01-cassino/02-cronologia-legal.md)
- [O caso CSGOLotto e a FTC](01-cassino/03-csgolotto-influencers.md)
- [Impacto sobre menores](01-cassino/04-impacto-em-menores.md)
- [A receita da casa](01-cassino/05-receita-da-casa.md)

### [02. Vista Grossa](02-vista-grossa/) — *cheaters e smurfs PvP*
> Como a Valve transformou banimento em produto recorrente, e por que o anti-cheat só funcionou de verdade em setembro de 2025.

- [Resumo](02-vista-grossa/00-resumo.md)
- [A história de fracassos do VAC](02-vista-grossa/01-historia-do-vac.md)
- [A economia do cheating](02-vista-grossa/02-economia-do-cheating.md)
- [Smurfs e o Prime de US$ 14,99](02-vista-grossa/03-smurfs-e-prime-pago.md)
- [O mercado de contas](02-vista-grossa/04-mercado-de-contas.md)
- [Ação tardia: por que só agora?](02-vista-grossa/05-acao-tardia.md)
- [Trust Factor saturado: o sistema que funciona inversamente](02-vista-grossa/06-trust-factor-saturado.md)

### [03. A Fábrica](03-fabrica/) — *XP, drops semanais e bot farms*
> O sistema de recompensa que terceiriza a produção de cases para uma indústria de bots — e por que a Valve não tem incentivo para parar isso.

- [Resumo](03-fabrica/00-resumo.md)
- [Mecânica dos drops semanais](03-fabrica/01-mecanica-dos-drops.md)
- [Por que isso incentiva multi-conta](03-fabrica/02-incentivo-multi-conta.md)
- [Bot farms industriais](03-fabrica/03-bot-farms-industriais.md)
- [Técnicas de automação](03-fabrica/04-tecnicas-automacao.md)
- [Impacto no mercado de skins](03-fabrica/05-impacto-no-mercado.md)
- [A ação seletiva da Valve](03-fabrica/06-acao-seletiva-da-valve.md)

### [04. A Manipulação](04-manipulacao/) — *hipótese sob investigação*
> A acusação mais grave e a menos documentada. Apresentamos a hipótese, os incentivos estruturais que a tornam plausível, o contra-argumento honesto, e uma metodologia pré-registrada para testá-la.

- [Resumo](04-manipulacao/00-resumo.md)
- [Hipótese formal](04-manipulacao/01-hipotese-formal.md)
- [Incentivos estruturais](04-manipulacao/02-incentivos-estruturais.md)
- [Relatos da comunidade](04-manipulacao/03-relatos-da-comunidade.md)
- [Placebo e viés de confirmação](04-manipulacao/04-placebo-e-vies.md)
- [Metodologia de coleta (pré-registro)](04-manipulacao/05-metodologia-coleta.md)
- [Resultados da análise](04-manipulacao/06-resultados-analise.md) *(v2.0)*

### [05. Conclusão](05-conclusao/)
- [Síntese: como os quatro pilares se conectam](05-conclusao/sintese.md)
- [Chamada à ação](05-conclusao/chamada-acao.md)

### Apêndices
- [Bibliografia consolidada](REFERENCIAS.md)
- [Dados estruturados](data/) — CSVs com processos, receita, indústria de bots
- [Scripts de coleta](scripts/) — código Python para reproduzir a análise do Pilar 4

---

## Como ler este dossiê

Toda afirmação factual está marcada com um destes três níveis:

| Marcador | Significado |
|---|---|
| `[DOCUMENTADO]` | Sustentado por fonte primária acessível (decisão judicial, paper acadêmico, comunicado oficial) |
| `[ALEGADO]` | Acusação em processo legal ativo, ainda não decidida em mérito |
| `[HIPÓTESE]` | Conjectura sob investigação neste dossiê, com método explícito para testar |

Se você encontrar uma afirmação sem marcador ou sem fonte vinculada, **isso é um defeito do dossiê** — abra uma issue ou nos avise.

---

## Status do projeto

- **v1.0** (publicado em 26/04/2026): Pilares 1–3 completos, Pilar 4 teórico + metodologia pré-registrada.
- **v2.0** (publicado em 27/04/2026): Pilar 4 com resultados da coleta de dados (1.540 perfis Steam, 33 com Leetify público).
  - **Achado**: H1 não confirmada. Placebo + confundidores explicam os dados disponíveis.
  - Limitação principal: análise direta de performance teve N=14 (abaixo do mínimo pré-registrado).
  - Ver [resultados completos](04-manipulacao/06-resultados-analise.md).

---

## Licença e ética

- Texto sob CC BY-SA 4.0 — copie, redistribua, traduza, com atribuição.
- Código (scripts/) sob MIT.
- A coleta de dados respeita exclusivamente perfis Steam públicos. Nenhum bypass de privacidade. Sem PII em datasets publicados.
