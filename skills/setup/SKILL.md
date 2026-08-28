---
name: setup
description: Use when starting a new study topic, initializing the tutor state, or receiving the /setup command.
---

# Setup do Tutor AI

Quando esta skill for ativada, siga rigorosamente este fluxo:

## 1. Coleta de informações (faça uma pergunta por vez)

1. Qual é o tema principal que você quer aprender?
2. Qual é o seu objetivo específico com esse tema? (Ex: “conseguir criar APIs com FastAPI e conectar a um banco de dados”)
3. Qual é o seu nível atual nesse tema? (Iniciante total / Já sei o básico / Intermediário / Avançado)
4. Quantas horas por semana você consegue dedicar?
5. Prefere estudar em quais horários do dia?
6. Você quer que eu use fontes de universidades (MIT, Stanford, etc.) como base?
7. Tem algum prazo ou data limite?

## 2. Após coletar as respostas

- Crie a estrutura de pastas e arquivos:
  - `curriculum.md`
  - `progress.json`
  - `lessons/`
  - `flashcards.md`
  - `session-log.md`
  - `projects/` (especialmente importante se for programação)

- Se os arquivos ainda não existirem, copie os modelos, sem recriar o schema:

```powershell
New-Item -ItemType Directory -Force lessons, projects
if (!(Test-Path curriculum.md)) { Copy-Item templates/curriculum-template.md curriculum.md }
if (!(Test-Path progress.json)) { Copy-Item templates/progress-template.json progress.json }
if (!(Test-Path flashcards.md)) { Copy-Item templates/flashcards-template.md flashcards.md }
if (!(Test-Path session-log.md)) { Copy-Item templates/session-log-template.md session-log.md }
```

- Preencha o `curriculum.md` com um roadmap inicial baseado nas respostas e no contrato de estado.
- Se o tema for **Programação**, já estruture o currículo em torno de projetos reais e progressivos.
- Não sobrescreva estado existente sem registrar a migração; acrescente `evidencias[]` aos tópicos antigos quando necessário.

## 3. Confirmação final

Mostre um resumo claro do que foi configurado e pergunte:
“Está tudo certo? Posso começar a montar as primeiras lições?”

Só avance para a criação detalhada do currículo depois da confirmação do aluno.
