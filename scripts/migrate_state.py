#!/usr/bin/env python3
"""Migrate an AI Tutor v1 study to validated v2 state."""

from __future__ import annotations

import argparse
import json
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from scripts.init_study import atomic_write
from scripts.validate_study import validate_state


LEGACY_FILES = ("progress.json", "curriculum.md", "session-log.md", "flashcards.md")


@dataclass(frozen=True)
class MigrationReport:
    changed: bool
    valid: bool
    warnings: tuple[str, ...]


def _stable_id(prefix: str, study_key: str, entity_key: str) -> str:
    value = uuid.uuid5(uuid.NAMESPACE_URL, f"ai-tutor:{study_key}:{prefix}:{entity_key}")
    return f"{prefix}_{value}"


def _is_v2(study_root: Path) -> bool:
    state_path = study_root / ".ai-tutor" / "state.json"
    if not state_path.is_file():
        return False
    try:
        return json.loads(state_path.read_text(encoding="utf-8")).get("schema_version") == 2
    except json.JSONDecodeError:
        return False


def _convert(study_root: Path) -> tuple[dict, dict, dict, list[str]]:
    progress_path = study_root / "progress.json"
    if not progress_path.is_file():
        raise FileNotFoundError(f"legacy progress.json not found: {study_root}")
    legacy = json.loads(progress_path.read_text(encoding="utf-8-sig"))
    study_key = str(study_root.resolve())
    study_id = _stable_id("study", study_key, legacy.get("tema", "study"))
    topic_ids: dict[str, str] = {}
    topics = []
    for key, topic in legacy.get("topicos", {}).items():
        topic_id = _stable_id("topic", study_key, key)
        topic_ids[key] = topic_id
        mastery = topic.get("dominio", 0)
        status = "not_started" if mastery == 0 else "mastered" if mastery >= 80 else "in_progress"
        notes = topic.get("observacoes", "")
        topics.append({
            "topic_id": topic_id,
            "name": key.replace("_", " ").strip(),
            "mastery": mastery,
            "retention": "unknown",
            "status": status,
            "last_practice": topic.get("ultima_pratica"),
            "evidence_ids": [],
            "notes": notes,
        })

    weak_points = []
    warnings: list[str] = []
    for index, text in enumerate(legacy.get("pontos_fracos", [])):
        weak_points.append({
            "weak_point_id": _stable_id("weak", study_key, f"{index}:{text}"),
            "topic_id": None,
            "category": "unclassified",
            "cause": str(text),
            "supporting_evidence_ids": [],
            "entered_at": legacy.get("ultima_atualizacao"),
            "exit_condition": "classify and collect two autonomous correct evidences in different sessions",
            "status": "active",
        })
        warnings.append(f"weak point requires topic/category classification: {text}")

    state = {
        "schema_version": 2,
        "study_id": study_id,
        "revision": 0,
        "updated_at": legacy.get("ultima_atualizacao"),
        "topics": topics,
        "evidences": [],
        "sessions": [],
        "lessons": [],
        "weak_points": weak_points,
        "projects": [],
        "next_focus": legacy.get("proximo_foco") or None,
    }
    config = {
        "schema_version": 2,
        "study_id": study_id,
        "topic": legacy.get("tema", ""),
        "goal": legacy.get("objetivo_especifico", ""),
        "deadline": None,
        "weekly_hours": legacy.get("horas_semanal_disponivel", 0),
        "preferred_times": [],
        "initial_level": legacy.get("nivel_geral", ""),
        "language": "pt-BR",
        "accessibility": [],
        "source_policy": {"prefer_primary": True, "prefer_pt_br": True},
        "external_consents": {},
    }
    media = {"schema_version": 2, "study_id": study_id, "artifacts": []}
    return config, state, media, warnings


def _backup_legacy(study_root: Path) -> None:
    destination = study_root / ".ai-tutor" / "migrations" / "v1-backup"
    destination.mkdir(parents=True, exist_ok=True)
    for name in LEGACY_FILES:
        source = study_root / name
        if source.is_file():
            shutil.copy2(source, destination / name)


def migrate(study_root: Path, dry_run: bool = False) -> MigrationReport:
    study_root = study_root.resolve()
    if _is_v2(study_root):
        return MigrationReport(changed=False, valid=True, warnings=())

    config, state, media, warnings = _convert(study_root)
    errors = validate_state(state)
    if errors:
        return MigrationReport(changed=False, valid=False, warnings=tuple(errors + warnings))
    if dry_run:
        return MigrationReport(changed=True, valid=True, warnings=tuple(warnings))

    _backup_legacy(study_root)
    metadata = study_root / ".ai-tutor"
    for name, payload in (
        ("study-config.json", config),
        ("state.json", state),
        ("media-index.json", media),
    ):
        atomic_write(metadata / name, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return MigrationReport(changed=True, valid=True, warnings=tuple(warnings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = migrate(args.study_root, dry_run=args.dry_run)
    print(json.dumps({
        "changed": report.changed,
        "valid": report.valid,
        "warnings": list(report.warnings),
    }, ensure_ascii=False, indent=2))
    return 0 if report.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
