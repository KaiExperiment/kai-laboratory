import unittest
from ki02.benchmark import baseline, load_cases, score
from ki02.candidate_v0 import candidate

class CandidateDevelopmentTests(unittest.TestCase):
    def test_dev_candidate_outperforms_naive_baseline(self):
        cases = load_cases("dev")
        base = score(cases, baseline)
        improved = score(cases, candidate)
        self.assertGreater(improved["correct"], base["correct"])
        self.assertEqual(improved["count"], base["count"])

    def test_candidate_never_returns_invalid_decision(self):
        for case in load_cases("dev"):
            self.assertIn(candidate(case), ("accept", "reject", "abstain"))

if __name__ == "__main__":
    unittest.main()
