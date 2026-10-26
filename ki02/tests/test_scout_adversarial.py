"""KI-02 adversarial SCOUT integration checks using synthetic local dossiers.

These tests exercise SCOUT's actual engine and change only local temporary copies.
They are regression tests, not an AI capability benchmark.
"""
import json
import tempfile
import unittest
from pathlib import Path
from scout.engine import analyse

FIXTURE = Path(__file__).resolve().parents[2] / "scout" / "examples"

class ScoutAdversarialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        (root / "evidence").mkdir()
        for source in (FIXTURE / "evidence").glob("*.txt"):
            (root / "evidence" / source.name).write_bytes(source.read_bytes())
        self.dossier = json.loads((FIXTURE / "dossier.json").read_text(encoding="utf-8"))
        self.path = root / "dossier.json"

    def analyse(self):
        self.path.write_text(json.dumps(self.dossier), encoding="utf-8")
        return {c["id"]: c for c in analyse(self.path, at="2026-10-26T20:00:00Z")["candidates"]}

    def test_unverifiable_quote_blocks_critical_claim(self):
        rule = next(x for x in self.dossier["opportunity_rules"] if x["id"] == "csv-comparison")
        rule["claims"][0]["evidence"][0]["quote"] = "A quote that is not in any source."
        result = self.analyse()["csv-comparison"]
        self.assertEqual(result["decision"], "abstain")
        self.assertIn("Invalid reference on a critical claim", result["challenge"]["blockers"])

    def test_removed_source_blocks_fixture_shortlist(self):
        source = next(x for x in self.dossier["sources"] if x["id"] == "review")
        (self.path.parent / source["path"]).unlink()
        result = self.analyse()["csv-comparison"]
        self.assertEqual(result["decision"], "abstain")
        self.assertTrue(any("Fewer than two independent" in x for x in result["challenge"]["blockers"]))

    def test_unsupported_critical_claim_blocks_fixture_shortlist(self):
        rule = next(x for x in self.dossier["opportunity_rules"] if x["id"] == "csv-comparison")
        rule["claims"][0]["evidence"] = []
        result = self.analyse()["csv-comparison"]
        self.assertEqual(result["decision"], "abstain")
        self.assertIn("Critical claim unsupported or contradicted", result["challenge"]["blockers"])

    def test_operator_declared_counterevidence_blocks_shortlist(self):
        rule = next(x for x in self.dossier["opportunity_rules"] if x["id"] == "csv-comparison")
        rule["claims"][0]["evidence"].append({
            "source": "workflow",
            "quote": "Scenario A: a maker needs to compare saved pricing assumptions across products.",
            "stance": "contradicts"
        })
        result = self.analyse()["csv-comparison"]
        self.assertEqual(result["decision"], "abstain")
        self.assertIn("Unresolved contradictory evidence", result["challenge"]["blockers"])

if __name__ == "__main__":
    unittest.main()
