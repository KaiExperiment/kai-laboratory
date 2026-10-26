"""KI-02 transparent failure analysis on public diagnostic cases.

This suite is intentionally not a pass/fail accuracy gate. It prints a
diagnostic comparison so weaknesses can be recorded before proposing fixes.
Labels are operator-authored, not independently adjudicated.
"""
from __future__ import annotations
import json
from pathlib import Path
from .compare_proposals import compare

PATH = Path(__file__).parent / "diagnostics" / "adversarial-v1.json"

def diagnose():
    cases = json.loads(PATH.read_text(encoding="utf-8"))
    result = compare(cases)
    result["kind"] = "public operator-labelled adversarial diagnostics"
    result["warning"] = "Not blind; diagnostic labels are operator-authored and available to the proposal author."
    return result

if __name__ == "__main__":
    print(json.dumps(diagnose(), indent=2))
