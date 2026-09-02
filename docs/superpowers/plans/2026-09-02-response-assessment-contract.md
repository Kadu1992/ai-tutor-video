# Response Assessment Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tornar a avaliação das respostas do AI Tutor literal, contextual e não-perfeccionista sem alterar os critérios de domínio.

**Architecture:** A regra normativa vive em `references/learning-contract.md`, que já é a autoridade única para evidência e domínio. Cenários comportamentais registram os riscos de regressão; a instalação global recebe somente os arquivos validados da fonte canônica.

**Tech Stack:** Markdown, JSON, Python 3.11+ standard library, `unittest`, validadores existentes da skill.

**Spec:** `docs/superpowers/specs/2026-08-29-ai-tutor-v2-design.md` e o pedido do usuário para avaliar respostas por ideia central, contexto, justificativa, limites, feedback e leitura literal.

## Global Constraints

- A matriz de domínio 60/80/100 permanece inalterada.
- Tutor-provided content and generated media remain non-evidence.
- Não inferir autorização, acesso irrestrito ou outras afirmações ausentes no texto.
- Omissões opcionais não rebaixam uma resposta sem requisito explícito.
- A fonte canônica deve passar pelos testes e validadores antes da instalação global.
- Não fazer commit, merge, push ou publicação externa sem pedido separado.

### Task 1: Registrar cenários de regressão

**Files:**
- Modify: `tests/scenarios/behavioral.json`
- Modify: `tests/test_validate_skill.py`

- [x] Adicionar cenários de leitura literal, omissão opcional e autocorreção.
- [x] Criar teste RED que exige as cláusulas normativas no contrato.
- [x] Executar o teste e confirmar falha por cláusula ausente.

### Task 2: Atualizar o contrato normativo

**Files:**
- Modify: `references/learning-contract.md`

- [x] Definir os seis pontos de avaliação.
- [x] Definir as classificações correta, parcial e incorreta.
- [x] Preservar a matriz de domínio e os limites da escada de ajuda.

### Task 3: Validar a fonte canônica

- [x] Executar a suíte `unittest` completa.
- [x] Executar `scripts/validate_skill.py` e `quick_validate.py`.
- [x] Revisar o diff e confirmar ausência de arquivos temporários.

### Task 4: Propagar a versão validada

**Files:**
- Update: `<global-skill-root>/references/learning-contract.md`

- [x] Copiar somente o componente normativo permitido para a instalação global.
- [x] Comparar hashes fonte/instalação.
- [x] Fazer smoke check lendo o contrato instalado.
