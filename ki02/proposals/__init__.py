"""Proposal package; public intake API lives in proposal_intake."""
from ..proposal_intake import intake, validate_manifest

__all__ = ["intake", "validate_manifest"]
