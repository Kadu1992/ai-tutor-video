#!/usr/bin/env python3
"""Validate the AI Tutor package without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/architecture.md",
    "references/learning-contract.md",
    "references/state-contract.md",
    "references/output-contract.md",
    "references/media-providers.md",
    "references/programming.md",
    "assets/templates/study-config.json",
    "assets/templates/state.json",
    "assets/templates/media-index.json",
    "assets/templates/curriculum.md",
    "assets/templates/session-log.md",
    "assets/templates/flashcards.md",
)

WORKFLOWS = (
    "setup",
    "session",
    "curriculum",
    "lesson",
    "review",
    "feynman",
    "flashcards",
    "progress",
    "sources",
    "media",
)

LOCAL_REFERENCE = re.compile(
    r"`((?:references|assets|scripts)/[^`]+\.(?:md|json|py))`"
)
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
DOMAIN_60_TRANSFER = re.compile(
    r"(?:dom[ií]nio|domain)\s*(?:>=?|≥)?\s*60[^\n]{0,100}transfer",
    re.IGNORECASE,
)
PLACEHOLDER = re.compile(
    r"(?:\bTBD\b|\bTODO\b|YYYY-MM-DD|exemplo_topico|## Card [12]\b|^\s*\.\.\.\s*$)",
    re.MULTILINE,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _validate_frontmatter(root: Path, errors: list[str]) -> None:
    entrypoint = root / "SKILL.md"
    if not entrypoint.is_file():
        return
    text = _read(entrypoint)
    match = FRONTMATTER.search(text)
    if not match:
        errors.append("SKILL.md: invalid or missing YAML frontmatter")
        return
    header = match.group(1)
    name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", header)
    description = re.search(r"(?m)^description:\s*(.+?)\s*$", header)
    if not name:
        errors.append("SKILL.md: name must use lowercase letters, digits, and hyphens")
    if not description or not description.group(1).startswith("Use when"):
        errors.append("SKILL.md: description must start with 'Use when'")


def _validate_references(root: Path, errors: list[str]) -> None:
    markdown_files = [root / "SKILL.md"]
    references = root / "references"
    if references.is_dir():
        markdown_files.extend(references.rglob("*.md"))
    for markdown in markdown_files:
        if not markdown.is_file():
            continue
        for relative in LOCAL_REFERENCE.findall(_read(markdown)):
            if not (root / relative).is_file():
                errors.append(
                    f"{markdown.relative_to(root)}: missing local reference: {relative}"
                )


def _validate_assets(root: Path, errors: list[str]) -> None:
    templates = root / "assets" / "templates"
    if not templates.is_dir():
        return
    for path in templates.rglob("*"):
        if not path.is_file():
            continue
        text = _read(path)
        if PLACEHOLDER.search(text):
            errors.append(f"production placeholder: {path.relative_to(root)}")
        if path.suffix == ".json":
            try:
                payload = json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON {path.relative_to(root)}: {exc}")
                continue
            if payload.get("schema_version") != 2:
                errors.append(f"{path.relative_to(root)}: schema_version must be 2")


def validate_skill(root: Path) -> list[str]:
    """Return semantic package errors. An empty list means valid."""

    root = root.resolve()
    errors = [f"missing: {relative}" for relative in REQUIRED_FILES if not (root / relative).is_file()]

    nested = [
        path.relative_to(root)
        for path in root.rglob("SKILL.md")
        if path.resolve() != (root / "SKILL.md").resolve()
        and ".worktrees" not in path.parts
    ]
    if nested:
        errors.append("nested SKILL.md: " + ", ".join(map(str, nested)))

    for workflow in WORKFLOWS:
        path = root / "references" / "workflows" / f"{workflow}.md"
        if not path.is_file():
            errors.append(f"missing workflow: {path.relative_to(root)}")

    _validate_frontmatter(root, errors)
    _validate_references(root, errors)
    _validate_assets(root, errors)

    workflow_root = root / "references" / "workflows"
    if workflow_root.is_dir():
        for path in workflow_root.glob("*.md"):
            if DOMAIN_60_TRANSFER.search(_read(path)):
                errors.append(f"domain 60 transfer contradiction: {path.relative_to(root)}")

    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0]) if args else Path(__file__).resolve().parents[1]
    errors = validate_skill(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"VALIDATION: FAIL ({len(errors)} errors)")
        return 1
    print("VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
