import json
import tempfile
import unittest
from pathlib import Path

from scripts.create_learning_pack import create_learning_pack
from scripts.init_study import atomic_write, initialize_study
from scripts.validate_study import validate_study


ROOT = Path(__file__).resolve().parents[1]
CONFIG = {
    "topic": "Distributed systems",
    "goal": "Explain and apply consistency models",
    "deadline": None,
    "weekly_hours": 5,
    "preferred_times": ["evening"],
    "initial_level": "beginner",
    "language": "pt-BR",
    "accessibility": ["alt_text"],
    "source_policy": {"prefer_primary": True, "prefer_pt_br": True},
}
SOURCES = [{
    "source_id": "source_a",
    "title": "Consistency reference",
    "url": "https://example.edu/reference",
    "content": "A consistency model defines allowed observations.",
}]


class EndToEndTests(unittest.TestCase):
    def test_initialize_resume_validate_and_create_multimodal_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp) / "learning program"
            initialize_study(ROOT, study, CONFIG)
            state_path = study / ".ai-tutor" / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["lessons"] = [{
                "lesson_id": "lesson_a",
                "status": "in_progress",
                "session_ids": ["session_a"],
            }]
            state["sessions"] = [{
                "session_id": "session_a",
                "status": "interrupted",
                "transitions": ["in_progress", "interrupted"],
                "lesson_ids": ["lesson_a"],
                "started_at": "2026-08-29T12:00:00Z",
                "ended_at": "2026-08-29T12:30:00Z",
                "checkpoint": "compare models",
                "resumable": True,
            }]
            atomic_write(state_path, json.dumps(state, indent=2) + "\n")
            self.assertEqual([], validate_study(study))
            pack = create_learning_pack(
                study,
                "lesson_a",
                SOURCES,
                ["cards", "image", "chart", "audio"],
                objective="Compare models",
            )
            self.assertTrue((pack / "manifest.json").is_file())
            self.assertTrue((pack / "local" / "image-brief.md").is_file())
            self.assertTrue((pack / "local" / "chart-data.csv").is_file())

    def test_validate_study_rejects_mismatched_study_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp) / "study"
            initialize_study(ROOT, study, CONFIG)
            media_path = study / ".ai-tutor" / "media-index.json"
            media = json.loads(media_path.read_text(encoding="utf-8"))
            media["study_id"] = "study_other"
            atomic_write(media_path, json.dumps(media, indent=2) + "\n")
            self.assertTrue(any("study_id mismatch" in error for error in validate_study(study)))

    def test_validate_study_rejects_evidence_eligible_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp) / "study"
            initialize_study(ROOT, study, CONFIG)
            media_path = study / ".ai-tutor" / "media-index.json"
            media = json.loads(media_path.read_text(encoding="utf-8"))
            media["artifacts"] = [{
                "artifact_id": "media_a",
                "type": "cards",
                "evidence_eligible": True,
            }]
            atomic_write(media_path, json.dumps(media, indent=2) + "\n")
            self.assertTrue(any("evidence_eligible" in error for error in validate_study(study)))


if __name__ == "__main__":
    unittest.main()
