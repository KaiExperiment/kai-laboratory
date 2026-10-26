import unittest
from ki02.scout_baseline import evaluate_scout

class ScoutIntegrationTests(unittest.TestCase):
    def test_existing_scout_fixture_regression(self):
        report = evaluate_scout()
        self.assertEqual(report["count"], 3)
        self.assertEqual(report["correct"], 3)
        self.assertFalse(report["model_driven"])
        self.assertEqual(
            {r["id"]: r["predicted"] for r in report["records"]},
            {"csv-comparison": "fixture_shortlist", "sensor-experiment": "abstain", "research-service": "abstain"},
        )

    def test_contradiction_blocks_shortlist(self):
        report = evaluate_scout()
        sensor = next(r for r in report["records"] if r["id"] == "sensor-experiment")
        self.assertIn("Unresolved contradictory evidence", sensor["blockers"])

    def test_unsupported_critical_claim_blocks_shortlist(self):
        report = evaluate_scout()
        research = next(r for r in report["records"] if r["id"] == "research-service")
        self.assertIn("Critical claim unsupported or contradicted", research["blockers"])

if __name__ == "__main__":
    unittest.main()
