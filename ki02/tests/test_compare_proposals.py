import unittest
from ki02.compare_proposals import compare, load_proposal_001
from ki02.benchmark import load_cases

class ProposalComparisonTests(unittest.TestCase):
    def test_three_implementations_same_cases(self):
        report = compare(load_cases("dev"))
        self.assertEqual(report["count"], 6)
        self.assertEqual(set(report["scores"]), {"baseline", "candidate_v0", "architect_001"})
        self.assertEqual(len(report["per_case"]), 6)

    def test_reviewed_proposal_returns_valid_label(self):
        predictor = load_proposal_001()
        for case in load_cases("dev"):
            self.assertIn(predictor(case), {"accept", "reject", "abstain"})

if __name__ == "__main__":
    unittest.main()
