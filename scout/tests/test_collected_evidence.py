"""Regression tests for collected-source provenance handoff."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from scout.collected_evidence import prepare

class CollectedEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        data = b"Public sample text\n"
        (self.folder / "source.txt").write_bytes(data)
        self.record = {
            "status": "ok",
            "final_url": "https://www.gutenberg.org/robots.txt",
            "retrieved_at": "2026-10-19T18:00:00+00:00",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()
        }
        self.write_record()

    def write_record(self):
        (self.folder / "provenance.json").write_text(json.dumps(self.record), encoding="utf-8")

    def prepare(self, source_id="test-source"):
        return prepare(self.folder, source_id, "Project Gutenberg", "Test", "gutenberg")

    def test_valid_source(self):
        source = self.prepare()
        self.assertEqual(source["id"], "test-source")
        self.assertFalse(source["fixture"])
        self.assertEqual(source["quality"], 1)

    def test_tampered_snapshot_rejected(self):
        (self.folder / "source.txt").write_text("Tampered", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.prepare()

    def test_failed_collection_rejected(self):
        self.record["status"] = "error"
        self.write_record()
        with self.assertRaises(ValueError):
            self.prepare()

    def test_unsafe_id_rejected(self):
        for bad in ("../outside", "/tmp/evil", "", "two words"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.prepare(bad)

    def test_non_allowlisted_final_url_rejected(self):
        for url in ("https://evil.example/claim", "http://www.gov.uk/set-up-business",
                    "https://www.gov.uk.evil.example/page", "https://user@www.gov.uk/page"):
            with self.subTest(url=url):
                self.record["final_url"] = url
                self.write_record()
                with self.assertRaisesRegex(ValueError, "allowlist"):
                    self.prepare()

    def test_naive_retrieval_time_rejected(self):
        self.record["retrieved_at"] = "2026-10-19T18:00:00"
        self.write_record()
        with self.assertRaisesRegex(ValueError, "timezone"):
            self.prepare()

    def test_missing_snapshot_rejected(self):
        (self.folder / "source.txt").unlink()
        with self.assertRaises(OSError):
            self.prepare()

if __name__ == "__main__":
    unittest.main()
