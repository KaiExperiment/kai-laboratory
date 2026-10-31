"""Source-bound decision handoff for KI-02.

Unlike the legacy handoff, this function reopens source bytes at decision time.
It cannot authenticate a reviewer or establish truth. The local source tree
must be trusted and protected from concurrent modification.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
from .review_decision import evaluate_reviewed_case

def evaluate_with_source_recheck(case, prepared, decisions, source_root):
    root = Path(source_root).resolve()
    observations = case.get("observations")
    items = prepared.get("review_items")
    if not isinstance(observations, list) or not isinstance(items, list):
        raise ValueError("invalid case or prepared review")
    by_id = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("invalid review item")
        if item["id"] in by_id:
            raise ValueError("duplicate review item")
        by_id[item["id"]] = item
    for observation in observations:
        if not isinstance(observation, dict) or observation.get("id") not in by_id:
            raise ValueError("observation mismatch")
        item = by_id[observation["id"]]
        source = observation.get("source_path")
        quote = observation.get("quote")
        if not isinstance(source, str) or not source.strip() or not isinstance(quote, str) or not quote.strip():
            raise ValueError("source and quote required")
        relative = Path(source)
        if relative.is_absolute():
            raise ValueError("absolute source path prohibited")
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError("source path escapes root")
        if item.get("source_path") != source:
            raise ValueError("source path changed after review preparation")
        try:
            data = path.read_bytes()
            decoded = data.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            raise ValueError("source unavailable at decision time") from exc
        if hashlib.sha256(data).hexdigest() != item.get("source_sha256"):
            raise ValueError("source changed after review preparation")
        if quote not in decoded:
            raise ValueError("quoted text missing at decision time")
    return evaluate_reviewed_case(case, prepared, decisions)
