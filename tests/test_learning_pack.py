import json
import tempfile
import unittest
from pathlib import Path

from scripts.create_learning_pack import (
    build_manifest,
    create_learning_pack,
    validate_media_item,
)
from scripts.init_study import initialize_study


SOURCES = [{
    "source_id": "source_a",
    "title": "Official consistency guide",
    "url": "https://example.edu/consistency",
    "content": "Consistency models describe visibility guarantees for operations.",
}]
CONFIG = {
    "topic": "Consistency",
    "goal": "Compare consistency models",
    "deadline": None,
    "weekly_hours": 4,
    "preferred_times": ["evening"],
    "initial_level": "beginner",
    "language": "pt-BR",
    "accessibility": ["alt_text"],
    "source_policy": {"prefer_primary": True, "prefer_pt_br": True},
}
ROOT = Path(__file__).resolve().parents[1]


class LearningPackTests(unittest.TestCase):
    def test_pack_contains_grounded_prompts_and_closed_consent_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp)
            pack = create_learning_pack(
                study,
                "lesson_a",
                SOURCES,
                ["cards", "mind_map", "audio"],
                objective="Compare consistency guarantees",
            )
            manifest = json.loads((pack / "manifest.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["external_upload"]["consented"])
            self.assertEqual(["cards", "mind_map", "audio"], manifest["requested_formats"])
            self.assertTrue((pack / "exports").is_dir())
            prompts = (pack / "prompts.md").read_text(encoding="utf-8")
            self.assertIn("source_a", prompts)
            self.assertIn("Compare consistency guarantees", prompts)

    def test_rejects_unknown_format_and_missing_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                create_learning_pack(Path(tmp), "lesson_a", SOURCES, ["hologram"], objective="Learn")
            with self.assertRaises(ValueError):
                create_learning_pack(Path(tmp), "lesson_a", [], ["cards"], objective="Learn")

    def test_visual_artifacts_require_accessibility(self):
        errors = validate_media_item({
            "artifact_id": "media_a",
            "type": "image",
            "alt_text": "",
            "evidence_eligible": False,
        })
        self.assertTrue(any("alt_text" in error for error in errors), errors)

    def test_audio_and_video_require_transcript(self):
        errors = validate_media_item({
            "artifact_id": "media_a",
            "type": "audio",
            "transcript": "",
            "evidence_eligible": False,
        })
        self.assertTrue(any("transcript" in error for error in errors), errors)

    def test_media_is_never_evidence_eligible(self):
        manifest = build_manifest(
            "lesson_a", SOURCES, ["cards"], "Retrieve definitions"
        )
        self.assertFalse(manifest["evidence_eligible"])
        errors = validate_media_item({
            "artifact_id": "media_a",
            "type": "cards",
            "evidence_eligible": True,
        })
        self.assertTrue(any("evidence_eligible" in error for error in errors), errors)

    def test_source_pack_preserves_citations(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = create_learning_pack(
                Path(tmp), "lesson_a", SOURCES, ["study_guide"], objective="Explain guarantees"
            )
            text = (pack / "source-pack.md").read_text(encoding="utf-8")
            self.assertIn("Official consistency guide", text)
            self.assertIn("https://example.edu/consistency", text)

    def test_updates_canonical_media_index_for_initialized_study(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp) / "study"
            initialize_study(ROOT, study, CONFIG)
            create_learning_pack(
                study, "lesson_a", SOURCES, ["cards"], objective="Retrieve concepts"
            )
            index = json.loads(
                (study / ".ai-tutor" / "media-index.json").read_text(encoding="utf-8")
            )
            self.assertEqual(1, len(index["artifacts"]))
            self.assertFalse(index["artifacts"][0]["evidence_eligible"])
            self.assertEqual("prepared", index["artifacts"][0]["status"])

    def test_every_format_has_a_local_fallback(self):
        expected = {
            "cards.json",
            "quiz.json",
            "concept-map.mmd",
            "chart-data.csv",
            "chart-spec.md",
            "image-brief.md",
            "infographic-brief.md",
            "slides-outline.md",
            "audio-script.md",
            "video-storyboard.md",
            "study-guide.md",
        }
        with tempfile.TemporaryDirectory() as tmp:
            pack = create_learning_pack(
                Path(tmp),
                "lesson_a",
                SOURCES,
                sorted({
                    "cards", "quiz", "mind_map", "chart", "image", "infographic",
                    "slides", "audio", "video", "study_guide",
                }),
                objective="Use every learning modality",
            )
            self.assertEqual(expected, {path.name for path in (pack / "local").iterdir()})


if __name__ == "__main__":
    unittest.main()
