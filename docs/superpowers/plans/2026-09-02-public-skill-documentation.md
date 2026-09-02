# Public Skill Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Documentar e validar publicamente o AI Tutor como um projeto educacional evolutivo no GitHub.

**Architecture:** `README.md` explica propósito, arquitetura, uso, limites e segurança. GitHub Actions executa os validadores existentes em múltiplos sistemas operacionais sem alterar o contrato pedagógico.

**Tech Stack:** Markdown, GitHub Actions YAML, Python 3.11+ standard library e `unittest`.

**Spec:** `docs/superpowers/specs/2026-08-29-ai-tutor-v2-design.md` e o pedido do usuário para documentação pública e validação contínua.

## Global Constraints

- `SKILL.md` permanece o único entrypoint descobrível.
- `skill_root` é somente leitura; `study_root` é escolhido explicitamente.
- Python 3.11+ e biblioteca padrão continuam suficientes.
- Mídia gerada não é evidência de domínio.
- Upload externo exige consentimento específico.
- Nenhum token, credencial ou caminho pessoal entra no repositório.

### Task 1: Documentação pública

**Files:**
- Create: `README.md`

- [x] Explicar objetivo, origem, arquitetura, quick start, uso, limites e segurança.
- [x] Explicar a separação entre a instalação da skill e os diretórios de estudo.

### Task 2: Automação de qualidade

**Files:**
- Create: `tests/__init__.py`
- Create: `.github/workflows/validate.yml`

- [x] Tornar a suíte executável pelo `unittest discover` padrão.
- [x] Configurar validação em Ubuntu, Windows e macOS com Python suportado.
- [x] Corrigir a expectativa do teste para comparar caminhos canônicos em Windows e macOS.

### Task 3: Gate final e publicação

- [x] Executar testes completos, validadores e compilação.
- [x] Fazer auditoria de segredos/caminhos pessoais e revisar diff.
- [x] Commitar e enviar para `origin/main`.
- [x] Confirmar o commit e o workflow de validação no GitHub.
