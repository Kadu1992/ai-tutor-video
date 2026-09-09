import json
import tempfile
import unittest
from pathlib import Path

from scripts.init_study import initialize_study


ROOT = Path(__file__).resolve().parents[1]
VALID_CONFIG = {
    "topic": "Sistemas distribuídos",
    "goal": "Projetar serviços resilientes",
    "deadline": None,
    "weekly_hours": 6,
    "preferred_times": ["noite"],
    "initial_level": "iniciante",
    "language": "pt-BR",
    "accessibility": [],
    "source_policy": {"prefer_primary": True, "prefer_pt_br": True},
}


class InitializeStudyTests(unittest.TestCase):
    def test_initializes_path_with_spaces_without_fake_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp) / "meu estudo"
            created = initialize_study(ROOT, study, VALID_CONFIG)
            self.assertIn((study / ".ai-tutor" / "state.json").resolve(), created)
            state = json.loads((study / ".ai-tutor" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(2, state["schema_version"])
            self.assertEqual([], state["topics"])
            self.assertEqual([], state["sessions"])
            self.assertNotIn("exemplo_topico", json.dumps(state))

    def test_persists_every_setup_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp) / "study"
            initialize_study(ROOT, study, VALID_CONFIG)
            config = json.loads((study / ".ai-tutor" / "study-config.json").read_text(encoding="utf-8"))
            for key, value in VALID_CONFIG.items():
                self.assertEqual(value, config[key])

    def test_refuses_to_overwrite_existing_study(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp) / "study"
            initialize_study(ROOT, study, VALID_CONFIG)
            with self.assertRaises(FileExistsError):
                initialize_study(ROOT, study, VALID_CONFIG)

    def test_creates_transcripts_directory_and_persists_video_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = Path(tmp) / "study_video"
            video_config = dict(VALID_CONFIG)
            video_config.update({
                "course_id": "curso-em-video",
                "playlist_url": "https://www.youtube.com/playlist?list=PLHz_AreHm4dn",
                "platform_api_url": "http://localhost:8000",
            })
            initialize_study(ROOT, study, video_config)
            self.assertTrue((study / "transcripts").is_dir())
            config = json.loads((study / ".ai-tutor" / "study-config.json").read_text(encoding="utf-8"))
            self.assertEqual("curso-em-video", config.get("course_id"))
            self.assertEqual("http://localhost:8000", config.get("platform_api_url"))


if __name__ == "__main__":
    unittest.main()

