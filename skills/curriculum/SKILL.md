---
name: curriculum
description: Use when creating or updating a progressive study roadmap, its mastery checklists, or the /curriculum command.
---

# Curriculum

Você é responsável por criar e manter o currículo de estudos do aluno.

## Quando ativada

1. Leia `references/contratos-de-estado.md` e os arquivos de estado existentes (`curriculum.md`, `progress.json`, `session-log.md`).
2. Se ainda não existir currículo, crie um do zero com base nas informações do setup.
3. Se já existir, atualize-o de acordo com o progresso real do aluno.

## Regras de criação do currículo

- Organize o conteúdo em **fases progressivas**.
- Cada fase deve ter:
  - Objetivo claro
  - Lista de conceitos essenciais
  - Checklist de domínio (o que o aluno precisa conseguir fazer)
  - Projeto prático associado (obrigatório quando o tema for Programação)
- Cada item do checklist deve ser observável e só pode ser marcado `[x]` conforme a seção 5 do contrato: domínio ≥ 80, duas evidências independentes, registro no log e commit do aluno quando envolver código.
- Nunca coloque conceitos avançados antes dos fundamentais.
- Sempre conecte a teoria a uma aplicação concreta.

## Quando o tema for Programação

- Estruture o currículo em torno de **projetos reais e progressivos**.
- Cada projeto deve ter potencial de se tornar uma ferramenta útil ou parte de um negócio.
- Exemplo de progressão:
  1. Projeto simples (ex: CLI ou script)
  2. API básica
  3. API + Banco de Dados
  4. API + autenticação + deploy
  5. Integração com LLM / Agentes
  6. Solução completa para cliente

## Formato do `curriculum.md`

Use esta estrutura:

```markdown
# Currículo: [Tema]

## Objetivo Final
...

## Fase 1 – [Nome]
**Objetivo:** ...
**Conceitos:** ...
**Checklist de domínio:**
- [ ] ...
**Projeto:** ...

## Fase 2 – [Nome]
...
```

## Após criar ou atualizar

Mostre o currículo de forma clara e pergunte se o aluno quer ajustar alguma fase ou prioridade. Não marque um item como concluído apenas por leitura, explicação do tutor ou checklist verbal.
