#!/usr/bin/env python3
"""Initialize a portable AI Tutor study directory."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import uuid
from copy import deepcopy
from pathlib import Path


JSON_ASSETS = ("study-config.json", "state.json", "media-index.json")
MARKDOWN_ASSETS = ("curriculum.md", "session-log.md", "flashcards.md")
REQUIRED_CONFIG = (
    "topic",
    "goal",
    "deadline",
    "weekly_hours",
    "preferred_times",
    "initial_level",
    "language",
    "accessibility",
    "source_policy",
)


def atomic_write(path: Path, content: str) -> None:
    """Replace a text file atomically on the same volume."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_config(config: dict) -> None:
    missing = [key for key in REQUIRED_CONFIG if key not in config]
    if missing:
        raise ValueError("missing setup fields: " + ", ".join(missing))
    if not config["topic"].strip() or not config["goal"].strip():
        raise ValueError("topic and goal must not be empty")
    if not isinstance(config["weekly_hours"], (int, float)) or config["weekly_hours"] <= 0:
        raise ValueError("weekly_hours must be positive")


def initialize_study(
    skill_root: Path,
    study_root: Path,
    config: dict,
    *,
    force: bool = False,
) -> list[Path]:
    """Create a v2 study from packaged assets and return created files."""

    skill_root = skill_root.resolve()
    study_root = study_root.resolve()
    _validate_config(config)
    metadata_root = study_root / ".ai-tutor"
    if metadata_root.exists() and not force:
        raise FileExistsError(f"study already exists: {study_root}")

    assets = skill_root / "assets" / "templates"
    study_id = f"study_{uuid.uuid4()}"
    created: list[Path] = []

    for directory in (metadata_root, study_root / "lessons", study_root / "media", study_root / "projects"):
        directory.mkdir(parents=True, exist_ok=True)

    payloads: dict[str, dict] = {}
    for name in JSON_ASSETS:
        payload = _load_json(assets / name)
        payload["study_id"] = study_id
        payloads[name] = payload

    study_config = payloads["study-config.json"]
    for key in REQUIRED_CONFIG:
        study_config[key] = deepcopy(config[key])
    study_config["external_consents"] = deepcopy(config.get("external_consents", {}))

    for name, payload in payloads.items():
        destination = metadata_root / name
        atomic_write(destination, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        created.append(destination)

    for name in MARKDOWN_ASSETS:
        destination = study_root / name
        atomic_write(destination, (assets / name).read_text(encoding="utf-8"))
        created.append(destination)

    return created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-root", required=True, type=Path)
    parser.add_argument("--config-json", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    initialize_study(
        Path(__file__).resolve().parents[1],
        args.study_root,
        json.loads(args.config_json),
        force=args.force,
    )
    print(f"Initialized AI Tutor study at {args.study_root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
