# AI Tutor v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar o AI Tutor em uma skill portátil com estado v2 validável, workflows consistentes e integração híbrida NotebookLM/Gemini para materiais multimodais.

**Architecture:** Um único `SKILL.md` roteia intenções para referências internas. Scripts Python sem dependências externas inicializam, validam e migram ambientes de estudo; JSON versionado é canônico e Markdown é a superfície humana.

**Tech Stack:** Markdown, YAML, JSON, Python 3.11+ standard library, `unittest`, wrapper PowerShell compatível.

**Spec:** `docs/superpowers/specs/2026-08-29-ai-tutor-v2-design.md`

## Global Constraints

- Um único entrypoint descobrível: `SKILL.md`.
- Python 3.11+ e somente biblioteca padrão.
- `skill_root` é somente leitura; `study_root` é explícito.
- Todo JSON produtivo usa `schema_version: 2`.
- Domínio 60 exige Feynman + aplicação; 80 exige transferência; 100 exige repetição em duas sessões e contextos.
- Upload externo requer consentimento específico; credenciais nunca são manipuladas.
- Mídia gerada nunca é evidência de domínio.
- Assets produtivos não contêm exemplos ou placeholders que possam virar estado real.

---

### Task 1: Validador semântico da skill e estrutura v2

**Files:**
- Create: `scripts/validate_skill.py`
- Create: `tests/test_validate_skill.py`
- Modify: `tests/validate-skill.ps1`

**Interfaces:**
- Produces: `validate_skill(root: Path) -> list[str]`; CLI retorna 0 sem erros e 1 com erros.
- Produces: wrapper PowerShell que delega ao validador Python.

- [ ] **Step 1: Write the failing tests**

```python
class ValidateSkillTests(unittest.TestCase):
    def test_current_package_fails_until_v2_layout_exists(self):
        self.assertEqual([], validate_skill(ROOT))

    def test_rejects_nested_discoverable_skills(self):
        with copied_package() as root:
            (root / "skills" / "nested" / "SKILL.md").parent.mkdir(parents=True)
            (root / "skills" / "nested" / "SKILL.md").write_text("---\nname: nested\ndescription: Use when x\n---")
            self.assertIn("nested SKILL.md", "\n".join(validate_skill(root)))
```

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_validate_skill -v`

Expected: FAIL porque `scripts.validate_skill` ou o layout v2 ainda não existe.

- [ ] **Step 3: Implement the validator**

```python
REQUIRED = [
    "SKILL.md", "agents/openai.yaml", "references/architecture.md",
    "references/learning-contract.md", "references/state-contract.md",
    "references/output-contract.md", "references/media-providers.md",
    "assets/templates/study-config.json", "assets/templates/state.json",
    "assets/templates/media-index.json",
]

def validate_skill(root: Path) -> list[str]:
    errors = [f"missing: {p}" for p in REQUIRED if not (root / p).is_file()]
    nested = [p for p in root.rglob("SKILL.md") if p != root / "SKILL.md"]
    if nested:
        errors.append("nested SKILL.md: " + ", ".join(str(p.relative_to(root)) for p in nested))
    return errors
```

O validador também verificará frontmatter, links locais, JSON v2, placeholders produtivos, contradição 60/80 e campos obrigatórios de acessibilidade.

- [ ] **Step 4: Run GREEN after Task 4 supplies the complete layout**

Run: `python -m unittest tests.test_validate_skill -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_skill.py tests/test_validate_skill.py tests/validate-skill.ps1
git commit -m "test: add semantic skill validator"
```

---

### Task 2: Inicialização portátil e assets v2

**Files:**
- Create: `scripts/init_study.py`
- Create: `tests/test_init_study.py`
- Create: `assets/templates/study-config.json`
- Create: `assets/templates/state.json`
- Create: `assets/templates/media-index.json`
- Move/Rewrite: `templates/*.md` → `assets/templates/*.md`

**Interfaces:**
- Produces: `initialize_study(skill_root: Path, study_root: Path, config: dict) -> list[Path]`.
- CLI: `python scripts/init_study.py --study-root PATH --config-json JSON [--force]`.

- [ ] **Step 1: Write failing initialization tests**

```python
def test_initializes_path_with_spaces(self):
    study = Path(self.temp.name) / "meu estudo"
    created = initialize_study(ROOT, study, VALID_CONFIG)
    self.assertTrue((study / ".ai-tutor/state.json").is_file())
    self.assertEqual(2, json.loads((study / ".ai-tutor/state.json").read_text())["schema_version"])
    self.assertNotIn("exemplo_topico", (study / ".ai-tutor/state.json").read_text())

def test_refuses_existing_study(self):
    initialize_study(ROOT, study, VALID_CONFIG)
    with self.assertRaises(FileExistsError):
        initialize_study(ROOT, study, VALID_CONFIG)
```

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_init_study -v`

Expected: FAIL por módulo ausente.

- [ ] **Step 3: Create empty, production-safe assets**

```json
{
  "schema_version": 2,
  "study_id": "",
  "topic": "",
  "goal": "",
  "preferences": {},
  "external_consents": {}
}
```

Os assets Markdown terão apenas cabeçalhos e instruções HTML não interpretáveis como estado.

- [ ] **Step 4: Implement atomic initialization**

```python
def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
```

- [ ] **Step 5: Run GREEN**

Run: `python -m unittest tests.test_init_study -v`

Expected: PASS para caminho com espaços, assets vazios e recusa de sobrescrita.

- [ ] **Step 6: Commit**

```bash
git add scripts/init_study.py tests/test_init_study.py assets/templates
git commit -m "feat: add portable study initializer"
```

---

### Task 3: Validação de estado, domínio e máquinas de estado

**Files:**
- Create: `scripts/validate_study.py`
- Create: `tests/test_validate_study.py`
- Create: `references/state-contract.md`
- Create: `references/learning-contract.md`

**Interfaces:**
- Produces: `validate_state(state: dict) -> list[str]`.
- Produces: `validate_study(study_root: Path) -> list[str]`.

- [ ] **Step 1: Write failing invariant tests**

```python
def test_domain_60_needs_feynman_and_application(self):
    state = valid_state(topic(domain=60, evidence=[feynman()]))
    self.assertIn("domain 60", "\n".join(validate_state(state)))

def test_domain_80_needs_transfer(self):
    state = valid_state(topic(domain=80, evidence=[feynman(), application()]))
    self.assertIn("transfer", "\n".join(validate_state(state)))

def test_interrupted_session_can_transition_to_resumed(self):
    state = valid_state(session(status="interrompida", transitions=["em_andamento", "interrompida", "retomada"]))
    self.assertEqual([], validate_state(state))

def test_media_cannot_be_evidence(self):
    state = valid_state(evidence(reference_type="media"))
    self.assertIn("media cannot be evidence", "\n".join(validate_state(state)))
```

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_validate_study -v`

Expected: FAIL por módulo ausente.

- [ ] **Step 3: Implement structural and semantic validation**

```python
SESSION_TRANSITIONS = {
    "em_andamento": {"concluida", "interrompida"},
    "interrompida": {"retomada"},
    "retomada": {"concluida", "interrompida"},
}

def validate_state(state: dict) -> list[str]:
    errors = []
    if state.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    errors.extend(validate_unique_ids(state))
    errors.extend(validate_references(state))
    errors.extend(validate_sessions(state))
    errors.extend(validate_mastery(state))
    return errors
```

- [ ] **Step 4: Run GREEN**

Run: `python -m unittest tests.test_validate_study -v`

Expected: PASS para schemas, referências, transições e matriz de domínio.

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_study.py tests/test_validate_study.py references/state-contract.md references/learning-contract.md
git commit -m "feat: validate tutor state invariants"
```

---

### Task 4: Entry point único e workflows consolidados

**Files:**
- Rewrite: `SKILL.md`
- Create: `agents/openai.yaml`
- Create: `references/architecture.md`
- Create: `references/programming.md`
- Create: `references/workflows/{setup,session,curriculum,lesson,review,feynman,flashcards,progress,sources,media}.md`
- Remove after transfer: `skills/*/SKILL.md`, `references/contratos-de-estado.md`, `references/projetos-e-codigo.md`, `references/programming-paths.md`

**Interfaces:**
- Produces: one discoverable skill `ai-tutor`.
- Consumes: normative contracts from Tasks 2–3.

- [ ] **Step 1: Extend validator tests for routing and contradictions**

```python
def test_all_routes_are_reachable_from_entrypoint(self):
    self.assertEqual([], validate_skill(ROOT))

def test_no_workflow_requires_transfer_for_domain_60(self):
    text = "\n".join(p.read_text() for p in (ROOT / "references/workflows").glob("*.md"))
    self.assertNotRegex(text, r"60[^\n]{0,80}transfer")
```

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_validate_skill -v`

Expected: FAIL por subskills aninhadas, rotas ausentes e layout antigo.

- [ ] **Step 3: Rewrite the router and workflows**

```markdown
## Roteamento

| Intenção observável | Ler |
| --- | --- |
| iniciar programa persistente | `references/workflows/setup.md` |
| continuar ou retomar estudo | `references/workflows/session.md` |
| produzir material multimodal | `references/workflows/media.md` |

Uma explicação pontual não cria arquivos de estado. Antes de alterar estado,
leia `references/state-contract.md` e `references/learning-contract.md`.
```

- [ ] **Step 4: Run GREEN**

Run: `python -m unittest tests.test_validate_skill -v`

Expected: PASS com entrypoint único e todas as referências alcançáveis.

- [ ] **Step 5: Commit**

```bash
git add SKILL.md agents references skills
git commit -m "refactor: consolidate ai tutor workflows"
```

---

### Task 5: Migração v1 → v2 recuperável e idempotente

**Files:**
- Create: `scripts/migrate_state.py`
- Create: `tests/test_migrate_state.py`
- Create: `tests/fixtures/v1-study/`

**Interfaces:**
- Produces: `migrate(study_root: Path, dry_run: bool = False) -> MigrationReport`.
- CLI: `python scripts/migrate_state.py --study-root PATH [--dry-run]`.

- [ ] **Step 1: Write failing migration tests**

```python
def test_dry_run_does_not_write(self):
    before = snapshot(study)
    report = migrate(study, dry_run=True)
    self.assertEqual(before, snapshot(study))
    self.assertTrue(report.valid)

def test_migration_is_idempotent(self):
    migrate(study)
    once = snapshot(study)
    migrate(study)
    self.assertEqual(once, snapshot(study))

def test_does_not_invent_evidence_from_observations(self):
    migrate(study)
    state = load_state(study)
    self.assertEqual([], state["evidences"])
```

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_migrate_state -v`

Expected: FAIL por migrador ausente.

- [ ] **Step 3: Implement migration with backup and report**

```python
def migrate(study_root: Path, dry_run: bool = False) -> MigrationReport:
    if is_v2(study_root):
        return MigrationReport(changed=False, valid=True, warnings=[])
    converted = convert_v1(read_v1(study_root))
    errors = validate_state(converted.state)
    if errors:
        return MigrationReport(changed=False, valid=False, warnings=errors)
    if not dry_run:
        backup_v1(study_root)
        write_v2(study_root, converted)
    return converted.report
```

- [ ] **Step 4: Run GREEN**

Run: `python -m unittest tests.test_migrate_state -v`

Expected: PASS para dry-run, backup, preservação e idempotência.

- [ ] **Step 5: Commit**

```bash
git add scripts/migrate_state.py tests/test_migrate_state.py tests/fixtures
git commit -m "feat: migrate ai tutor state to v2"
```

---

### Task 6: Contratos multimodais e integração NotebookLM/Gemini

**Files:**
- Create: `references/output-contract.md`
- Create: `references/media-providers.md`
- Create: `assets/templates/notebooklm-manifest.json`
- Create: `assets/templates/cards.json`
- Create: `assets/templates/quiz.json`
- Create: `scripts/create_learning_pack.py`
- Create: `tests/test_learning_pack.py`

**Interfaces:**
- Produces: `create_learning_pack(study_root, lesson_id, sources, formats) -> Path`.
- Produces: pacote `media/<lesson-id>/notebooklm/{source-pack.md,prompts.md,manifest.json,exports/}`.

- [ ] **Step 1: Write failing media contract tests**

```python
def test_pack_contains_grounded_prompts_and_consent_gate(self):
    pack = create_learning_pack(study, "lesson_1", SOURCES, ["cards", "mind_map", "audio"])
    manifest = json.loads((pack / "manifest.json").read_text())
    self.assertFalse(manifest["external_upload"]["consented"])
    self.assertEqual(["cards", "mind_map", "audio"], manifest["requested_formats"])

def test_visual_artifacts_require_accessibility(self):
    errors = validate_media_item({"type": "image", "alt_text": ""})
    self.assertIn("alt_text", "\n".join(errors))

def test_media_is_never_evidence_eligible(self):
    manifest = build_manifest("lesson_1", SOURCES, ["cards"])
    self.assertFalse(manifest["evidence_eligible"])
```

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_learning_pack -v`

Expected: FAIL por módulo ausente.

- [ ] **Step 3: Implement local learning packs**

```python
SUPPORTED_FORMATS = {
    "cards", "quiz", "mind_map", "chart", "image", "infographic",
    "slides", "audio", "video", "study_guide",
}

def create_learning_pack(
    study_root: Path,
    lesson_id: str,
    sources: list[dict],
    formats: list[str],
) -> Path:
    requested = validate_formats(formats)
    manifest = {
        "schema_version": 2,
        "lesson_id": lesson_id,
        "requested_formats": requested,
        "external_upload": {"provider": "notebooklm", "consented": False},
        "evidence_eligible": False,
    }
    pack = study_root / "media" / lesson_id / "notebooklm"
    atomic_write(pack / "manifest.json", json.dumps(manifest, indent=2))
    atomic_write(pack / "source-pack.md", render_sources(sources))
    atomic_write(pack / "prompts.md", render_prompts(requested, sources))
    (pack / "exports").mkdir(parents=True, exist_ok=True)
    return pack
```

Prompts diferenciarão artefatos do NotebookLM Studio e conversa no Gemini. Automação por navegador será condicionada a ferramenta disponível, login existente e consentimento; o pacote manual sempre será produzido.

- [ ] **Step 4: Run GREEN**

Run: `python -m unittest tests.test_learning_pack -v`

Expected: PASS para todos os formatos, acessibilidade, grounding e consentimento.

- [ ] **Step 5: Commit**

```bash
git add references/output-contract.md references/media-providers.md assets/templates scripts/create_learning_pack.py tests/test_learning_pack.py
git commit -m "feat: add multimodal notebook learning packs"
```

---

### Task 7: Regressão completa e limpeza da v1

**Files:**
- Modify: `scripts/validate_skill.py`
- Modify: `tests/*.py`
- Remove: diretórios v1 já substituídos e templates antigos

**Interfaces:**
- Consumes: todos os componentes anteriores.
- Produces: pacote v2 sem caminhos mortos, placeholders ou divergências.

- [ ] **Step 1: Add end-to-end test**

```python
def test_initialize_validate_pack_and_resume(self):
    initialize_study(ROOT, study, VALID_CONFIG)
    state = load_state(study)
    state["sessions"].append(interrupted_session())
    save_state(study, state)
    self.assertEqual([], validate_study(study))
    pack = create_learning_pack(study, LESSON_ID, SOURCES, ["cards", "image", "chart"])
    self.assertTrue((pack / "manifest.json").is_file())
```

- [ ] **Step 2: Run the complete suite**

Run: `python -m unittest discover -s tests -p "test_*.py" -v`

Expected: todos os testes passam.

- [ ] **Step 3: Run package and diff checks**

```bash
python scripts/validate_skill.py .
python -m compileall -q scripts tests
git diff --check
git status --short
```

Expected: validação sem erros, compilação exit 0, diff limpo de whitespace e apenas mudanças intencionais.

- [ ] **Step 4: Verify removed routes and stale terminology**

Run: `rg -n "skills/|exemplo_topico|Card 1|60.*transfer|Gemini Notebook.*artefatos" SKILL.md references assets scripts tests`

Expected: nenhuma referência v1 indevida; ocorrências em testes negativos devem estar explicitamente marcadas.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: complete ai tutor v2 architecture"
```
