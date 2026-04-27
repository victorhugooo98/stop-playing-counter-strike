# Como subir o repositório para o GitHub (privado)

O repositório git local já está pronto com 5 commits cronológicos. Faltam apenas dois passos manuais (autenticação interativa).

## Estado atual do repositório local

```
fa97a76 docs: v2.0+v2.1 - empirical results, plots, network analysis, VIF/PCA validation
ea7a34c data: collected datasets (anonymized SteamID hash)
9a78b71 feat(scripts): pipeline of 11 Python scripts + reference datasets
c040c16 docs: dossier v1.0 - text of pillars 1-4 and conclusion
02dc012 chore: initial scaffolding (gitignore, env example, README)
```

- **91 arquivos rastreados**
- ✅ `.env` e `data/friends-edges.csv` (com SteamID 64 plain) **não** estão no git (.gitignore)
- ✅ `data/friends-edges-hashed.csv` (hashada) está no git
- ✅ `cache/` e `.venv/` ignorados

## Passos para fazer o push

### Passo 1 — Autenticar no GitHub CLI

Abra um PowerShell ou Git Bash:

```bash
"/c/Program Files/GitHub CLI/gh.exe" auth login
```

Selecione:
1. **GitHub.com**
2. **HTTPS** (mais simples) ou **SSH** (se você já tem chave configurada)
3. **Login with a web browser**
4. Cole o código no navegador → autorize

### Passo 2 — Criar repositório privado e fazer push

```bash
cd "E:/Documents/Projetos/Stop Playing Counter Strike"
"/c/Program Files/GitHub CLI/gh.exe" repo create stop-playing-counter-strike --private --source=. --remote=origin --push
```

Isso cria o repositório `victorhugooo98/stop-playing-counter-strike` (privado) e faz push de todos os commits.

### Passo 3 — Verificar privacidade

```bash
"/c/Program Files/GitHub CLI/gh.exe" repo view stop-playing-counter-strike --json visibility
```

Deve retornar `{"visibility":"PRIVATE"}`.

## Alternativa manual (se preferir não usar gh)

1. Crie repositório vazio `stop-playing-counter-strike` em https://github.com/new (marque **Private**)
2. Não inicialize com README/license/gitignore (já temos)
3. No terminal local:

```bash
cd "E:/Documents/Projetos/Stop Playing Counter Strike"
git remote add origin https://github.com/victorhugooo98/stop-playing-counter-strike.git
git push -u origin main
```

## Para tornar público depois

```bash
"/c/Program Files/GitHub CLI/gh.exe" repo edit stop-playing-counter-strike --visibility public
```

Mas **antes** rode auditoria de privacidade final:

```bash
.venv/Scripts/python.exe scripts/ethics_check.py
```

E inspecione `git ls-files` para garantir que nada sensível foi rastreado.

## O que não está no repo (e por quê)

| Arquivo | Motivo |
|---|---|
| `.env` | Contém STEAM_API_KEY e credenciais Leetify |
| `data/friends-edges.csv` | SteamID 64 plain de amigos da rede; versão hashada está no repo |
| `cache/` | Regenerável (cache de Steam Web API + Steam Market) |
| `.venv/` | Ambiente virtual Python; reproduz com `pip install -r scripts/requirements.txt` |
| `.claude/` | Configuração local do Claude Code |
