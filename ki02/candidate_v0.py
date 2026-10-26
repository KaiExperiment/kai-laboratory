"""KI-02 candidate v0: conservative evidence assessor for synthetic DEV cases.

An AI-authored heuristic candidate, not a trained model or autonomous agent.
It is intentionally frozen without using holdout labels to design it.
"""
from __future__ import annotations
import re

def candidate(case):
    text = case["evidence"].casefold()
    # Quoted commands, navigation text, vendor assertions and unsupported
    # evidence are not independent corroboration.
    if any(x in text for x in (
        "no independently checkable evidence", "no actual data",
        "no relevant information", "no supporting data",
        "navigation menu", "no evidence",
    )):
        return "abstain"
    # A stronger, independently repeated contradiction overrides a
    # weaker single positive trial. This remains a toy text heuristic.
    if re.search(r"contradict(?:s|ed|ory|ion)", text):
        return "reject"
    if re.search(r"support(?:s|ed)?", text):
        return "accept"
    return "abstain"
