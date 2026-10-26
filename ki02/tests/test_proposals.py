import json
import tempfile
import unittest
from pathlib import Path
from ki02.proposals import intake, validate_manifest

MANIFEST = {
    "candidate_id": "architect-001",
    "author_type": "model_generated",
    "hypothesis": "Check negation context before accepting support claims.",
    "target": "ki02-evidence-classifier",
    "change_summary": "Add context-sensitive rules.",
    "risk": "May overfit template phrases.",
    "source_path": "candidate.py",
}

class ProposalIntakeTests(unittest.TestCase):
    def test_manifest_validation(self):
        validate_manifest(MANIFEST)

    def test_reject_missing_field(self):
        with self.assertRaises(ValueError):
            validate_manifest({k: v for k, v in MANIFEST.items() if k != "risk"})

    def test_reject_unknown_author(self):
        with self.assertRaises(ValueError):
            validate_manifest(dict(MANIFEST, author_type="autonomous_superintelligence"))

    def test_intake_does_not_execute_candidate(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "candidate.py").write_text("raise RuntimeError('must not run')\n", encoding="utf-8")
            path = root / "manifest.json"
            path.write_text(json.dumps(MANIFEST), encoding="utf-8")
            result = intake(path, root)
            self.assertFalse(result["execution_performed"])
            self.assertTrue(result["review_required"])
            self.assertEqual(len(result["candidate_sha256"]), 64)

    def test_reject_source_escape(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            path = root / "manifest.json"
            path.write_text(json.dumps(dict(MANIFEST, source_path="../outside.py")), encoding="utf-8")
            with self.assertRaises(ValueError):
                intake(path, root)

if __name__ == "__main__":
    unittest.main()
