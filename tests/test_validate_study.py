import copy
import unittest

from scripts.validate_study import validate_state


def evidence(evidence_id, kind, *, session_id="session_a", transfer=False, autonomous=True, reference_type="lesson"):
    return {
        "evidence_id": evidence_id,
        "topic_id": "topic_a",
        "session_id": session_id,
        "kind": kind,
        "autonomous": autonomous,
        "transfer": transfer,
        "context": f"context-{evidence_id}",
        "recorded_at": "2026-08-29",
        "reference": {"type": reference_type, "id": "lesson_a"},
        "result": "correct",
        "error": None,
    }


def base_state():
    return {
        "schema_version": 2,
        "study_id": "study_a",
        "revision": 1,
        "updated_at": "2026-08-29T12:00:00Z",
        "topics": [{
            "topic_id": "topic_a",
            "name": "Consistency",
            "mastery": 0,
            "retention": "unknown",
            "status": "not_started",
            "last_practice": None,
            "evidence_ids": [],
        }],
        "evidences": [],
        "sessions": [],
        "lessons": [{"lesson_id": "lesson_a", "status": "planned", "session_ids": []}],
        "weak_points": [],
        "projects": [],
        "next_focus": None,
    }


class ValidateStudyTests(unittest.TestCase):
    def test_domain_60_needs_feynman_and_application(self):
        state = base_state()
        item = evidence("evidence_f", "feynman")
        state["evidences"] = [item]
        state["topics"][0].update(mastery=60, status="in_progress", evidence_ids=[item["evidence_id"]])
        self.assertTrue(any("mastery 60" in error for error in validate_state(state)))

    def test_domain_60_does_not_need_transfer(self):
        state = base_state()
        items = [evidence("evidence_f", "feynman"), evidence("evidence_a", "application")]
        state["evidences"] = items
        state["topics"][0].update(mastery=60, status="in_progress", evidence_ids=[item["evidence_id"] for item in items])
        self.assertEqual([], validate_state(state))

    def test_domain_80_needs_transfer(self):
        state = base_state()
        items = [evidence("evidence_f", "feynman"), evidence("evidence_a", "application")]
        state["evidences"] = items
        state["topics"][0].update(mastery=80, status="mastered", evidence_ids=[item["evidence_id"] for item in items])
        self.assertTrue(any("mastery 80" in error and "transfer" in error for error in validate_state(state)))

    def test_domain_100_needs_two_sessions_and_contexts(self):
        state = base_state()
        items = [
            evidence("evidence_f", "feynman", session_id="session_a"),
            evidence("evidence_a", "application", session_id="session_a", transfer=True),
        ]
        state["evidences"] = items
        state["topics"][0].update(mastery=100, status="mastered", evidence_ids=[item["evidence_id"] for item in items])
        errors = validate_state(state)
        self.assertTrue(any("mastery 100" in error for error in errors), errors)

    def test_interrupted_session_can_transition_to_resumed(self):
        state = base_state()
        state["sessions"] = [{
            "session_id": "session_a",
            "status": "resumed",
            "transitions": ["in_progress", "interrupted", "resumed"],
            "lesson_ids": ["lesson_a"],
            "started_at": "2026-08-29T12:00:00Z",
            "ended_at": None,
            "checkpoint": "exercise-2",
            "resumable": True,
        }]
        state["lessons"][0]["session_ids"] = ["session_a"]
        self.assertEqual([], validate_state(state))

    def test_rejects_invalid_session_transition(self):
        state = base_state()
        state["sessions"] = [{
            "session_id": "session_a",
            "status": "completed",
            "transitions": ["in_progress", "completed", "resumed"],
            "lesson_ids": [],
            "started_at": "2026-08-29T12:00:00Z",
            "ended_at": "2026-08-29T13:00:00Z",
            "checkpoint": None,
            "resumable": False,
        }]
        self.assertTrue(any("invalid session transition" in error for error in validate_state(state)))

    def test_media_cannot_be_evidence(self):
        state = base_state()
        item = evidence("evidence_m", "application", reference_type="media")
        state["evidences"] = [item]
        state["topics"][0]["evidence_ids"] = [item["evidence_id"]]
        self.assertTrue(any("media cannot be evidence" in error for error in validate_state(state)))

    def test_rejects_duplicate_ids_and_dangling_references(self):
        state = base_state()
        duplicate = copy.deepcopy(state["topics"][0])
        state["topics"].append(duplicate)
        state["topics"][0]["evidence_ids"] = ["evidence_missing"]
        errors = validate_state(state)
        self.assertTrue(any("duplicate id" in error for error in errors), errors)
        self.assertTrue(any("unknown evidence" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
