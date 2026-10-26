import tempfile
import unittest
from pathlib import Path
from ki02.evaluate import evaluate, validate_cases
from ki02.challenge_pack import generate

class EvaluationTests(unittest.TestCase):
    def test_reports_comparable_counts(self):
        report = evaluate(generate(2026, 30))
        self.assertEqual(report["count"], 30)
        self.assertEqual(report["delta_correct"], report["candidate_correct"] - report["baseline_correct"])
        self.assertEqual(report["baseline_abstentions"] >= 0, True)
        self.assertEqual(len(report["candidate_source_sha256"]), 64)

    def test_repeatability(self):
        self.assertEqual(evaluate(generate(42)), evaluate(generate(42)))

    def test_rejects_duplicate_ids(self):
        cases = generate(42)
        cases[1]["id"] = cases[0]["id"]
        with self.assertRaises(ValueError):
            validate_cases(cases)

    def test_rejects_invalid_label(self):
        cases = generate(42)
        cases[0]["expected"] = "unknown"
        with self.assertRaises(ValueError):
            validate_cases(cases)

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([])

if __name__ == "__main__":
    unittest.main()
