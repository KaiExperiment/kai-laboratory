import tempfile
from pathlib import Path
"""Adversarial semantic-validity probes for SCOUT.

A matching quote alone does not prove a claim. These tests document the
limitation and ensure insufficient corroboration still blocks promotion.
"""
import unittest
from scout.engine import evaluate, encoded, ingest

def source(text, group, quality=3):
    return {"status": "ok", "text": text, "sha256": group,
            "independence_group": group, "quality": quality, "fixture": False}

def rule():
    return {
        "id": "false-demand", "title": "Misleading citation probe",
        "category": "product", "triggers": ["fee"],
        "hypothesis": "Makers will pay for a tool",
        "claims": [{
            "id": "demand", "text": "Makers will pay for a tool",
            "kind": "observation", "critical": True,
            "evidence": [{"source": "policy", "quote": "A fee exists.", "stance": "supports"}]
        }],
        "assessments": {d: {"score": 4, "rationale": "Deliberately inflated operator rating",
                             "claims": ["demand"]} for d in ("feasibility", "novelty", "cost", "risk")},
        "risks": ["Misleading conclusion"], "uncertainties": ["No demand study"],
        "falsification_tests": ["Interview customers"],
        "next_action": {"scope": "local", "description": "Seek demand evidence"}
    }

class SemanticLimitTests(unittest.TestCase):
    def test_single_irrelevant_quote_cannot_shortlist(self):
        candidate = evaluate(rule(), {"policy": source("A fee exists. A fee applies.", "policy")})
        self.assertEqual(candidate["decision"], "abstain")
        self.assertIn("Fewer than two independent, nonduplicate supporting sources",
                      candidate["challenge"]["blockers"])

    def test_two_independent_irrelevant_quotes_expose_false_shortlist(self):
        candidate_rule = rule()
        candidate_rule["claims"][0]["evidence"].append(
            {"source": "guide", "quote": "Fees are charged.", "stance": "supports"})
        sources = {
            "policy": source("A fee exists.", "policy"),
            "guide": source("Fees are charged.", "guide"),
        }
        candidate = evaluate(candidate_rule, sources)
        # Without explicit semantic review, matching quotes must never be enough.
        self.assertEqual(candidate["decision"], "abstain",
                         "Two irrelevant fee citations must not validate customer demand")

    def test_mixed_fixture_and_real_sources_cannot_bypass_review(self):
        candidate_rule = rule()
        candidate_rule["claims"][0]["evidence"].append(
            {"source": "guide", "quote": "Fees are charged.", "stance": "supports"})
        sources = {
            "policy": source("A fee exists.", "policy"),
            "guide": dict(source("Fees are charged.", "guide"), fixture=True),
        }
        candidate = evaluate(candidate_rule, sources)
        self.assertEqual(candidate["decision"], "abstain")
        self.assertIn("Critical claim lacks explicit semantic review approval",
                      candidate["challenge"]["blockers"])

    def test_review_is_explicit_not_automatic(self):
        candidate_rule = rule()
        candidate_rule["claims"][0]["semantic_review"] = "approved"
        candidate_rule["claims"][0]["evidence"].append(
            {"source": "guide", "quote": "Fees are charged.", "stance": "supports"})
        candidate = evaluate(candidate_rule, {
            "policy": source("A fee exists.", "policy"),
            "guide": source("Fees are charged.", "guide"),
        })
        self.assertEqual(candidate["decision"], "shortlist")
        self.assertEqual(candidate["claims"][0]["semantic_validation"], "not_performed")
        # Approval is an operator assertion; this is not automatic semantic proof.

    def test_unrecorded_semantic_approval_is_rejected_at_ingestion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evidence").mkdir()
            (root / "evidence/policy.txt").write_text("A fee exists.")
            candidate_rule = rule()
            candidate_rule["claims"][0]["semantic_review"] = "approved"
            dossier = {
                "schema_version": 1, "question": "Does a fee prove demand?",
                "sources": [{"id": "policy", "title": "Fee policy", "publisher": "Test",
                             "independence_group": "policy", "locator": "test:policy",
                             "accessed_at": "2026-10-19T18:00:00Z",
                             "path": "evidence/policy.txt", "quality": 3,
                             "quality_rationale": "Test source", "fixture": False}],
                "opportunity_rules": [candidate_rule]
            }
            path = root / "dossier.json"
            path.write_bytes(encoded(dossier))
            with self.assertRaisesRegex(ValueError, "Semantic approval requires"):
                ingest(path)

    def test_critical_approval_without_history_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evidence").mkdir()
            (root / "evidence/policy.txt").write_text("A fee exists.")
            candidate_rule = rule()
            claim = candidate_rule["claims"][0]
            claim["semantic_review"] = "approved"
            claim["review_record"] = {
                "reviewer": "test-reviewer",
                "rationale": "Operator assertion only",
                "limitations": "No independent verification",
                "reviewed_at": "2026-10-19T18:00:00Z",
            }
            dossier = {
                "schema_version": 1, "question": "Does a fee prove demand?",
                "sources": [{"id": "policy", "title": "Fee policy", "publisher": "Test",
                             "independence_group": "policy", "locator": "test:policy",
                             "accessed_at": "2026-10-19T18:00:00Z",
                             "path": "evidence/policy.txt", "quality": 3,
                             "quality_rationale": "Test source", "fixture": False}],
                "opportunity_rules": [candidate_rule]
            }
            path = root / "dossier.json"
            path.write_bytes(encoded(dossier))
            with self.assertRaisesRegex(ValueError, "at least one review history event"):
                ingest(path)

    def test_rejected_and_reopened_review_history_checked(self):
        from scout.review_chain import append_event
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evidence").mkdir()
            (root / "evidence/policy.txt").write_text("A fee exists.")
            candidate_rule = rule()
            claim = candidate_rule["claims"][0]
            claim["semantic_review"] = "rejected"
            claim["review_history"] = append_event(
                [], "rejected", "reviewer-a", "No demand evidence", "2026-10-19T18:00:00Z")
            dossier = {
                "schema_version": 1, "question": "Review rejection?",
                "sources": [{"id": "policy", "title": "Fee policy", "publisher": "Test",
                             "independence_group": "policy", "locator": "test:policy",
                             "accessed_at": "2026-10-19T18:00:00Z",
                             "path": "evidence/policy.txt", "quality": 3,
                             "quality_rationale": "Test source", "fixture": False}],
                "opportunity_rules": [candidate_rule]
            }
            path = root / "dossier.json"
            def check():
                path.write_bytes(encoded(dossier))
                ingest(path)
            check()
            claim["semantic_review"] = "reopened"
            with self.assertRaisesRegex(ValueError, "match current rejection or reopening"):
                check()
            claim["review_history"] = append_event(
                claim["review_history"], "reopened", "reviewer-b", "Reassessment needed",
                "2026-10-19T19:00:00Z")
            check()
            claim["review_history"][0]["rationale"] = "Quietly rewritten"
            with self.assertRaisesRegex(ValueError, "event hash mismatch"):
                check()

    def test_approved_claim_is_invalidated_by_new_contradiction(self):
        candidate_rule = rule()
        claim = candidate_rule["claims"][0]
        claim["semantic_review"] = "approved"
        claim["review_record"] = {
            "reviewer": "test-reviewer",
            "rationale": "Historical approval for regression test",
            "limitations": "May be overturned by new evidence",
            "reviewed_at": "2026-10-19T18:00:00Z",
        }
        claim["evidence"].append(
            {"source": "guide", "quote": "Fees are charged.", "stance": "supports"})
        sources = {
            "policy": source("A fee exists.", "policy"),
            "guide": source("Fees are charged.", "guide"),
            "counter": source("No buyers requested a tool.", "counter"),
        }
        claim["evidence"].append(
            {"source": "counter", "quote": "No buyers requested a tool.", "stance": "contradicts"})
        candidate = evaluate(candidate_rule, sources)
        self.assertEqual(candidate["decision"], "abstain")
        self.assertEqual(candidate["claims"][0]["status"], "contradicted")
        self.assertIn("Previously approved claim invalidated by missing or contradictory evidence",
                      candidate["challenge"]["blockers"])

    def test_review_history_rejects_mismatch_and_reverse_chronology(self):
        from scout.engine import ingest, encoded
        import json
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evidence").mkdir()
            (root / "evidence/policy.txt").write_text("A fee exists.")
            candidate_rule = rule()
            claim = candidate_rule["claims"][0]
            claim["semantic_review"] = "approved"
            claim["review_record"] = {
                "reviewer": "reviewer-b", "rationale": "Approved for test",
                "limitations": "Not semantic proof", "reviewed_at": "2026-10-19T19:00:00Z"
            }
            claim["review_history"] = [
                {"verdict": "rejected", "reviewer": "reviewer-a",
                 "rationale": "Initially rejected", "reviewed_at": "2026-10-19T18:00:00Z"},
                {"verdict": "approved", "reviewer": "reviewer-b",
                 "rationale": "Reconsidered", "reviewed_at": "2026-10-19T19:00:00Z"}
            ]
            dossier = {
                "schema_version": 1, "question": "Review history integrity?",
                "sources": [{"id": "policy", "title": "Policy", "publisher": "Test",
                             "independence_group": "policy", "locator": "test:policy",
                             "accessed_at": "2026-10-19T18:00:00Z",
                             "path": "evidence/policy.txt", "quality": 3,
                             "quality_rationale": "Test source", "fixture": False}],
                "opportunity_rules": [candidate_rule]
            }
            from scout.engine import sha
            previous = "0" * 64
            for event in claim["review_history"]:
                event["previous_hash"] = previous
                event["event_hash"] = sha(encoded({k: v for k, v in event.items() if k != "event_hash"}))
                previous = event["event_hash"]
            path = root / "dossier.json"
            def check():
                path.write_bytes(encoded(dossier))
                ingest(path)
            check()
            claim["review_history"][0]["rationale"] = "Tampered older reasoning"
            with self.assertRaisesRegex(ValueError, "event hash mismatch"):
                check()
            claim["review_history"][0]["rationale"] = "Initially rejected"
            claim["review_history"][-1]["reviewer"] = "other"
            with self.assertRaisesRegex(ValueError, "event hash mismatch"):
                check()
            claim["review_history"][-1]["reviewer"] = "reviewer-b"
            claim["review_history"][0]["reviewed_at"] = "2026-10-19T20:00:00Z"
            with self.assertRaisesRegex(ValueError, "chronological"):
                check()

    def test_quote_is_traceable_not_semantically_proven(self):
        candidate = evaluate(rule(), {"policy": source("A fee exists.", "policy")})
        self.assertEqual(candidate["claims"][0]["status"], "traceable")
        self.assertEqual(candidate["decision"], "abstain")
        # The above traceability is NOT evidence that anyone will pay.
        # Future semantic validation must address this limitation explicitly.

if __name__ == "__main__":
    unittest.main()
