"""Architect proposal 001 — experimental structured evidence classifier.

Authored in a ChatGPT session; not produced by an autonomous background agent.
Never execute unreviewed generated code in a privileged environment.
"""
from __future__ import annotations
import re

NO_EVIDENCE = (
    "no independently checkable evidence",
    "no actual data",
    "no supporting data",
    "no relevant information",
    "no results",
    "navigation menu",
)
IRRELEVANT_CONTRADICTION = (
    "contradicts a different claim",
    "contradictory note concerns a different product",
)
SUPPORTED = re.compile(r"\bsupport(?:s|ed)?\b")
CONTRADICTED = re.compile(r"\bcontradict(?:s|ed|ory|ion)\b")

def candidate(case):
    text = case["evidence"].casefold()
    if any(phrase in text for phrase in NO_EVIDENCE):
        return "abstain"
    if any(phrase in text for phrase in IRRELEVANT_CONTRADICTION):
        return "abstain"
    if CONTRADICTED.search(text):
        return "reject"
    if SUPPORTED.search(text):
        return "accept"
    return "abstain"
