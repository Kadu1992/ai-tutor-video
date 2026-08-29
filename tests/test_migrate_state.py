import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.migrate_state import migrate


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "v1-study"


def snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.study = Path(self.temp.name) / "legacy study"
        shutil.copytree(FIXTURE, self.study)

    def tearDown(self):
        self.temp.cleanup()

    def test_dry_run_does_not_write(self):
        before = snapshot(self.study)
        report = migrate(self.study, dry_run=True)
        self.assertEqual(before, snapshot(self.study))
        self.assertTrue(report.valid)
        self.assertTrue(report.changed)

    def test_migration_is_idempotent(self):
        first = migrate(self.study)
        once = snapshot(self.study)
        second = migrate(self.study)
        self.assertEqual(once, snapshot(self.study))
        self.assertTrue(first.changed)
        self.assertFalse(second.changed)

    def test_preserves_observation_without_inventing_evidence(self):
        migrate(self.study)
        state = json.loads((self.study / ".ai-tutor" / "state.json").read_text(encoding="utf-8"))
        self.assertEqual([], state["evidences"])
        self.assertEqual(40, state["topics"][0]["mastery"])
        self.assertIn("Ainda confunde retorno", state["topics"][0]["notes"])

    def test_keeps_recoverable_backup(self):
        migrate(self.study)
        backup = self.study / ".ai-tutor" / "migrations" / "v1-backup"
        self.assertTrue((backup / "progress.json").is_file())
        self.assertEqual((FIXTURE / "progress.json").read_bytes(), (backup / "progress.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
