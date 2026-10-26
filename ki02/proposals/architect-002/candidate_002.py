"""Architect Proposal 002: narrow, conservative rule-based classifier.

AI-authored in an interactive session, not autonomously generated or trained.
The public diagnostics informed these rules: performance on them is *training*
feedback, never independent validation. Uncertain evidence abstains.
"""
from __future__ import annotations
import re

def candidate(case):
    text = case["evidence"].casefold()
    # Quoted words, unverified promotion, and flawed experimental controls
    # are not proof even when they contain positive-sounding words.
    if any(x in text for x in (
        "no independently checkable evidence", "no actual data",
        "no relevant information", "no supporting data", "no evidence",
        "no results", "navigation menu", "no independent measurement",
        "not a measurement", "no control group", "no supporting observations",
        "not been tested", "contradicts an unrelated claim",
        "contradicts a different claim", "different product",
    )):
        return "abstain"
    if re.search(r"\bdoes not support\b", text):
        return "reject"
    if re.search(r"\bnot contradict(?:ed|s)?\b", text):
        return "abstain"
    if re.search(r"\bcontradict(?:s|ed|ion|ory)?\b", text):
        return "reject"
    if re.search(r"\bsupport(?:s|ed)?\b", text):
        return "accept"
    return "abstain"
