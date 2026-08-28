---
name: flashcards
description: Use when creating, reviewing, or scheduling study flashcards, including the /flashcards command.
---

# Flashcards

Leia `references/contratos-de-estado.md` antes de criar ou alterar cards.

Você gerencia os flashcards do aluno para reforçar a retenção de longo prazo.

## Quando ativada

1. Leia o arquivo `flashcards.md` (se existir).
2. Identifique o contexto da sessão atual (o que acabou de ser estudado).
3. Decida se deve:
   - Criar novos flashcards
   - Fazer uma sessão de revisão
   - Ambos

## Regras para criação de flashcards

- Crie cards curtos e objetivos.
- Preferência por cards do tipo:
  - Conceito → Explicação simples
  - Problema → Solução / código
  - “Por que isso funciona?” → Explicação
- Em programação: priorize cards que envolvam código real ou decisões de design.
- Evite cards genéricos demais.
- Cada card deve ter:
  - Frente (pergunta)
  - Verso (resposta)
  - Nível de dificuldade (fácil / médio / difícil)
  - Data da última revisão
  - Próxima revisão recomendada
  - Degrau (1–6)
  - Tópico correspondente em `progress.json`

## Sessão de revisão

- Mostre um card por vez.
- Peça que o aluno responda **sem olhar a resposta**.
- Após a resposta, mostre o verso e peça autoavaliação (Acertei / Quase / Errei).
- Atualize a próxima data usando exclusivamente a escada **1 → 3 → 7 → 16 → 35 → 60 dias**: `Acertei` avança um degrau, `Quase` mantém e `Errei` volta ao degrau 1. Card novo começa no degrau 1.

## Formato do arquivo `flashcards.md`

```markdown
# Flashcards

## Card 1
**Frente:** ...
**Verso:** ...
**Dificuldade:** médio
**Última revisão:** YYYY-MM-DD
**Próxima revisão:** YYYY-MM-DD (data da revisão + intervalo do degrau)
**Status:** ativo
**Degrau:** 1
**Tópico:** ...
```

## Ao final

Atualize o `flashcards.md` e informe quantos cards novos foram criados ou revisados.
