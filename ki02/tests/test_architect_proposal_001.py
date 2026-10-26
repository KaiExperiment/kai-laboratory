"""Transparent engineering smoke checks for proposal 001 (not a blind test)."""
import importlib.util
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "proposals" / "architect-001" / "candidate_001.py"
spec = importlib.util.spec_from_file_location("architect_proposal_001", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
candidate = module.candidate

class ArchitectProposal001Tests(unittest.TestCase):
    def test_positive_measurement(self):
        self.assertEqual(candidate({"evidence": "An independent measurement supports the claim."}), "accept")

    def test_direct_contradiction(self):
        self.assertEqual(candidate({"evidence": "A replication contradicts the claim."}), "reject")

    def test_irrelevant_contradiction(self):
        self.assertEqual(candidate({"evidence": "A report contradicts a different claim; there are no results for this one."}), "abstain")

    def test_marketing_is_not_evidence(self):
        self.assertEqual(candidate({"evidence": "A vendor supports this claim but supplies no independently checkable evidence."}), "abstain")

    def test_unknown(self):
        self.assertEqual(candidate({"evidence": "No measurements were recorded."}), "abstain")

if __name__ == "__main__":
    unittest.main()
