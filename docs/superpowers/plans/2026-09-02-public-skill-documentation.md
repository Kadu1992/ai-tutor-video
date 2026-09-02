# Public Skill Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Documentar, governar e validar publicamente o AI Tutor como um projeto educacional evolutivo no GitHub.

**Architecture:** `README.md` explica propósito, arquitetura e uso. `CONTRIBUTING.md`, `CHANGELOG.md` e `VERSION` definem contribuição e releases sem alterar o contrato pedagógico. GitHub Actions executa os validadores existentes em múltiplos sistemas operacionais e cria releases somente para tags compatíveis.

**Tech Stack:** Markdown, GitHub Actions YAML, Python 3.11+ standard library, `unittest`, semantic versioning.

**Spec:** `docs/superpowers/specs/2026-08-29-ai-tutor-v2-design.md` e o pedido do usuário para README, contribuição, CI e releases.

## Global Constraints

- `SKILL.md` permanece o único entrypoint descobrível.
- `skill_root` é somente leitura; `study_root` é escolhido explicitamente.
- Python 3.11+ e biblioteca padrão continuam suficientes.
- Mídia gerada não é evidência de domínio.
- Upload externo exige consentimento específico.
- O workflow de release valida a tag contra `VERSION` antes de publicar.
- Nenhum token, credencial ou caminho pessoal entra no repositório.

### Task 1: Documentação pública

**Files:**
- Create: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `CHANGELOG.md`
- Create: `VERSION`

- [x] Explicar objetivo, origem, arquitetura, quick start, uso, limites e segurança.
- [x] Documentar fluxo de issue, branch, testes, revisão e melhoria contínua.
- [x] Definir SemVer, changelog e critérios para tags de release.

### Task 2: Automação de qualidade

**Files:**
- Create: `tests/__init__.py`
- Create: `.github/workflows/validate.yml`
- Create: `.github/workflows/release.yml`

- [x] Tornar a suíte executável pelo `unittest discover` padrão.
- [x] Configurar validação em Ubuntu, Windows e macOS com Python suportado.
- [x] Configurar validação de tags de release e criação de GitHub Release apenas após os testes.

### Task 3: Gate final e publicação

- [x] Executar testes completos, validadores e compilação.
- [x] Fazer auditoria de segredos/caminhos pessoais e revisar diff.
- [ ] Commitar e enviar para `origin/main`.
- [ ] Confirmar o commit e os workflows no GitHub.
