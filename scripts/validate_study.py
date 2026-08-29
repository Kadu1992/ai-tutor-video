#!/usr/bin/env python3
"""Validate AI Tutor v2 study state and cross-file invariants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.create_learning_pack import validate_media_item


MASTERY_LEVELS = {0, 20, 40, 60, 80, 100}
RETENTION_LEVELS = {"unknown", "low", "medium", "high"}
STATUS_BY_MASTERY = {
    0: "not_started",
    20: "in_progress",
    40: "in_progress",
    60: "in_progress",
    80: "mastered",
    100: "mastered",
}
SESSION_TRANSITIONS = {
    "in_progress": {"completed", "interrupted"},
    "interrupted": {"resumed"},
    "resumed": {"completed", "interrupted"},
    "completed": set(),
}
ID_FIELDS = {
    "topics": "topic_id",
    "evidences": "evidence_id",
    "sessions": "session_id",
    "lessons": "lesson_id",
    "weak_points": "weak_point_id",
    "projects": "project_id",
}


def _unique_ids(state: dict) -> tuple[dict[str, set[str]], list[str]]:
    indexes: dict[str, set[str]] = {}
    errors: list[str] = []
    globally_seen: set[str] = set()
    for collection, field in ID_FIELDS.items():
        values: set[str] = set()
        for position, item in enumerate(state.get(collection, [])):
            value = item.get(field)
            if not isinstance(value, str) or not value:
                errors.append(f"{collection}[{position}]: missing {field}")
                continue
            if value in values or value in globally_seen:
                errors.append(f"duplicate id: {value}")
            values.add(value)
            globally_seen.add(value)
        indexes[collection] = values
    return indexes, errors


def _validate_sessions(state: dict, indexes: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for session in state.get("sessions", []):
        transitions = session.get("transitions", [])
        for before, after in zip(transitions, transitions[1:]):
            if after not in SESSION_TRANSITIONS.get(before, set()):
                errors.append(
                    f"invalid session transition {before} -> {after} in {session.get('session_id')}"
                )
        if transitions and session.get("status") != transitions[-1]:
            errors.append(f"session status does not match transitions: {session.get('session_id')}")
        if session.get("status") == "completed" and not session.get("ended_at"):
            errors.append(f"completed session missing ended_at: {session.get('session_id')}")
        for lesson_id in session.get("lesson_ids", []):
            if lesson_id not in indexes["lessons"]:
                errors.append(f"session references unknown lesson: {lesson_id}")
    return errors


def _valid_evidences(topic: dict, evidence_by_id: dict[str, dict]) -> list[dict]:
    return [
        evidence_by_id[evidence_id]
        for evidence_id in topic.get("evidence_ids", [])
        if evidence_id in evidence_by_id
        and evidence_by_id[evidence_id].get("autonomous") is True
        and evidence_by_id[evidence_id].get("result") == "correct"
    ]


def _validate_mastery(state: dict, indexes: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    evidence_by_id = {
        item["evidence_id"]: item
        for item in state.get("evidences", [])
        if item.get("evidence_id")
    }
    for evidence in evidence_by_id.values():
        if evidence.get("reference", {}).get("type") == "media":
            errors.append(f"media cannot be evidence: {evidence['evidence_id']}")
        if evidence.get("topic_id") not in indexes["topics"]:
            errors.append(f"evidence references unknown topic: {evidence.get('topic_id')}")

    for topic in state.get("topics", []):
        mastery = topic.get("mastery")
        if mastery not in MASTERY_LEVELS:
            errors.append(f"invalid mastery for {topic.get('topic_id')}: {mastery}")
            continue
        if topic.get("status") != STATUS_BY_MASTERY[mastery]:
            errors.append(f"status does not match mastery for {topic.get('topic_id')}")
        if topic.get("retention") not in RETENTION_LEVELS:
            errors.append(f"invalid retention for {topic.get('topic_id')}")
        unknown = [value for value in topic.get("evidence_ids", []) if value not in evidence_by_id]
        for evidence_id in unknown:
            errors.append(f"topic references unknown evidence: {evidence_id}")

        valid = _valid_evidences(topic, evidence_by_id)
        kinds = {item.get("kind") for item in valid}
        if mastery >= 60 and not {"feynman", "application"}.issubset(kinds):
            errors.append(f"mastery 60 requires autonomous Feynman and application: {topic.get('topic_id')}")
        if mastery >= 80 and not any(
            item.get("kind") == "application" and item.get("transfer") is True
            for item in valid
        ):
            errors.append(f"mastery 80 requires transfer application: {topic.get('topic_id')}")
        if mastery >= 100:
            sessions = {item.get("session_id") for item in valid if item.get("session_id")}
            contexts = {item.get("context") for item in valid if item.get("context")}
            advanced = any(item.get("limit_or_self_correction") is True for item in valid)
            if len(sessions) < 2 or len(contexts) < 2 or not advanced:
                errors.append(
                    f"mastery 100 requires two sessions, two contexts, and limit/self-correction: {topic.get('topic_id')}"
                )
    return errors


def _validate_cross_references(state: dict, indexes: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for lesson in state.get("lessons", []):
        for session_id in lesson.get("session_ids", []):
            if session_id not in indexes["sessions"]:
                errors.append(f"lesson references unknown session: {session_id}")
    return errors


def validate_state(state: dict) -> list[str]:
    """Return deterministic errors for a state payload."""

    errors: list[str] = []
    if state.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    if not isinstance(state.get("study_id"), str) or not state.get("study_id"):
        errors.append("study_id is required")
    indexes, id_errors = _unique_ids(state)
    errors.extend(id_errors)
    errors.extend(_validate_sessions(state, indexes))
    errors.extend(_validate_mastery(state, indexes))
    errors.extend(_validate_cross_references(state, indexes))
    return sorted(set(errors))


def validate_study(study_root: Path) -> list[str]:
    metadata = study_root.resolve() / ".ai-tutor"
    errors: list[str] = []
    for name in ("study-config.json", "state.json", "media-index.json"):
        if not (metadata / name).is_file():
            errors.append(f"missing study file: .ai-tutor/{name}")
    if errors:
        return errors
    payloads: dict[str, dict] = {}
    for name in ("study-config.json", "state.json", "media-index.json"):
        try:
            payloads[name] = json.loads((metadata / name).read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid {name}: {exc}")
    if errors:
        return errors

    state = payloads["state.json"]
    errors.extend(validate_state(state))
    expected_study_id = state.get("study_id")
    for name, payload in payloads.items():
        if payload.get("schema_version") != 2:
            errors.append(f"{name}: schema_version must be 2")
        if payload.get("study_id") != expected_study_id:
            errors.append(f"study_id mismatch: {name}")

    seen_artifacts: set[str] = set()
    for item in payloads["media-index.json"].get("artifacts", []):
        artifact_id = item.get("artifact_id")
        if artifact_id in seen_artifacts:
            errors.append(f"duplicate media artifact id: {artifact_id}")
        if artifact_id:
            seen_artifacts.add(artifact_id)
        errors.extend(validate_media_item(item))
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("study_root", type=Path)
    args = parser.parse_args()
    errors = validate_study(args.study_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("STUDY VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
