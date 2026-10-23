"""SCOUT 0.1.3 end-to-end corroboration tests (AI-authored, synthetic data).

Copy to scout/tests/ inside a checkout of KaiExperiment/kai-laboratory.
Unlike direct evaluate() tests, these exercise ingest -> analyse -> run -> verify.
No quote in this test constitutes real-world evidence or customer demand.
"""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from scout.engine import analyse, encoded, run, verify
from scout.review_chain import append_event

AT = "2026-10-20T12:00:00Z"


def reviewed_claim(cid, refs, critical=True):
    claim = {
        "id": cid,
        "text": "Synthetic claim " + cid,
        "kind": "observation",
        "critical": critical,
        "evidence": [
            {"source": sid, "quote": quote, "stance": "supports"}
            for sid, quote in refs
        ],
    }
    if critical:
        claim["semantic_review"] = "approved"
        claim["review_record"] = {
            "reviewer": "synthetic-test-operator",
            "rationale": "Test fixture only; not a real semantic assessment",
            "limitations": "This is an asserted verdict, not independent verification",
            "reviewed_at": AT,
        }
        claim["review_history"] = append_event(
            [], "approved", "synthetic-test-operator",
            "Synthetic approval to test validation mechanics", AT,
        )
    return claim


class CorroborationIngestionTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "evidence").mkdir()
        self.sources = {}
        self.claims = []

    def add_source(self, sid, text, group, fixture=False):
        (self.root / "evidence" / f"{sid}.txt").write_text(text, encoding="utf-8")
        self.sources[sid] = {
            "id": sid,
            "title": "Synthetic test source " + sid,
            "publisher": "Kai Laboratory synthetic test",
            "independence_group": group,
            "locator": "test:" + sid,
            "accessed_at": AT,
            "path": f"evidence/{sid}.txt",
            "quality": 3,
            "quality_rationale": "Arbitrary synthetic test rating",
            "fixture": fixture,
        }

    def dossier(self):
        rule = {
            "id": "synthetic-opportunity",
            "title": "Synthetic corroboration test",
            "category": "experiment",
            "triggers": ["premise"],
            "hypothesis": "Test claim-specific corroboration",
            "claims": copy.deepcopy(self.claims),
            "assessments": {
                dimension: {
                    "score": 4,
                    "rationale": "Deliberately high synthetic rating",
                    "claims": ["critical"],
                }
                for dimension in ("feasibility", "novelty", "cost", "risk")
            },
            "risks": ["Artificial inputs"],
            "uncertainties": ["No real-world corroboration"],
            "falsification_tests": ["Inspect the claim-specific evidence gate"],
            "next_action": {
                "scope": "local", "description": "Inspect generated test report"
            },
        }
        data = {
            "schema_version": 1,
            "question": "Does synthetic critical-claim corroboration pass?",
            "sources": list(self.sources.values()),
            "opportunity_rules": [rule],
        }
        path = self.root / "dossier.json"
        path.write_bytes(encoded(data))
        return path

    def evaluate_dossier(self):
        return analyse(self.dossier(), AT)["candidates"][0]

    def test_unrelated_real_source_does_not_rescue_critical_claim(self):
        self.add_source("one", "premise one", "one")
        self.add_source("context", "premise context", "context")
        self.claims = [
            reviewed_claim("critical", [("one", "premise one")]),
            reviewed_claim("context", [("context", "premise context")], False),
        ]
        candidate = self.evaluate_dossier()
        self.assertEqual(candidate["independent_support_count"], 2)
        self.assertEqual(candidate["decision"], "abstain")
        self.assertTrue(any("critical" in b and "real sources" in b
                            for b in candidate["challenge"]["blockers"]))

    def test_two_independent_real_sources_shortlist_and_reproduce(self):
        self.add_source("one", "premise one", "one")
        self.add_source("two", "premise two", "two")
        self.claims = [reviewed_claim("critical", [
            ("one", "premise one"), ("two", "premise two")
        ])]
        path = self.dossier()
        candidate = analyse(path, AT)["candidates"][0]
        self.assertEqual(candidate["decision"], "shortlist")
        self.assertEqual(candidate["claims"][0]["semantic_validation"], "not_performed")
        out = self.root / "frozen-run"
        run(path, out, AT)
        self.assertEqual(verify(out)["candidates"][0]["decision"], "shortlist")

    def test_duplicate_real_content_is_not_independent(self):
        self.add_source("one", "premise shared", "one")
        self.add_source("two", "premise shared", "two")
        self.claims = [reviewed_claim("critical", [
            ("one", "premise shared"), ("two", "premise shared")
        ])]
        self.assertEqual(self.evaluate_dossier()["decision"], "abstain")

    def test_shared_group_is_not_independent(self):
        self.add_source("one", "premise one", "same")
        self.add_source("two", "premise two", "same")
        self.claims = [reviewed_claim("critical", [
            ("one", "premise one"), ("two", "premise two")
        ])]
        self.assertEqual(self.evaluate_dossier()["decision"], "abstain")

    def test_real_and_fixture_cannot_combine_to_corroborate_real_claim(self):
        self.add_source("one", "premise one", "one")
        self.add_source("two", "premise two", "two", fixture=True)
        self.claims = [reviewed_claim("critical", [
            ("one", "premise one"), ("two", "premise two")
        ])]
        self.assertEqual(self.evaluate_dossier()["decision"], "abstain")

    def test_missing_semantic_review_history_rejected_during_ingestion(self):
        self.add_source("one", "premise one", "one")
        self.add_source("two", "premise two", "two")
        claim = reviewed_claim("critical", [
            ("one", "premise one"), ("two", "premise two")
        ])
        claim.pop("review_history")
        self.claims = [claim]
        with self.assertRaisesRegex(ValueError, "review history"):
            self.evaluate_dossier()


if __name__ == "__main__":
    unittest.main()
