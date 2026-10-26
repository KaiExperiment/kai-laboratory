"""Proposal 002 transparent smoke tests: not independent validation."""
import importlib.util
import json
import unittest
from pathlib import Path
from ki02.benchmark import load_cases, score

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "proposals" / "architect-002" / "candidate_002.py"
spec = importlib.util.spec_from_file_location("architect_proposal_002", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ArchitectProposal002Tests(unittest.TestCase):
    def test_dev_regressions(self):
        cases = load_cases("dev")
        report = score(cases, module.candidate)
        self.assertEqual(report["count"], 6)
        self.assertEqual(report["correct"], 6)

    def test_diagnostic_cases_and_labels(self):
        cases = json.loads((ROOT / "diagnostics" / "adversarial-v1.json").read_text(encoding="utf-8"))
        report = score(cases, module.candidate)
        self.assertEqual(report["count"], 8)
        self.assertEqual(report["correct"], 8)

    def test_unseen_paraphrase_not_guaranteed(self):
        # This is a known limitation, not a success criterion.
        self.assertIn(module.candidate({"evidence": "The methodology was inconclusive."}),
                      {"accept", "reject", "abstain"})

if __name__ == "__main__":
    unittest.main()
