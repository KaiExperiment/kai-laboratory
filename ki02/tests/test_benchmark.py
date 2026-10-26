import unittest
from ki02.benchmark import baseline, load_cases, score

class BenchmarkTests(unittest.TestCase):
    def test_splits_disjoint(self):
        dev, held = load_cases("dev"), load_cases("holdout")
        self.assertTrue(dev and held)
        self.assertFalse({x["id"] for x in dev} & {x["id"] for x in held})

    def test_baseline_is_deterministic(self):
        dev = load_cases("dev")
        self.assertEqual(score(dev), score(dev))

    def test_score_reports_all_cases(self):
        s = score(load_cases("dev"))
        self.assertEqual(s["count"], len(s["results"]))
        self.assertEqual(s["correct"], sum(r["correct"] for r in s["results"]))
        self.assertTrue(0 <= s["accuracy"] <= 1)

    def test_invalid_prediction_fails(self):
        with self.assertRaises(ValueError):
            score(load_cases("dev"), lambda case: "maybe")

if __name__ == "__main__":
    unittest.main()
