# ARTIFACT_ID: SENTINEL.Models
# VERSION: v1.0
# STATUS: [ACTIVE]

import json
from typing import Any, Dict, List, Optional


class EpistemicVerdict:
    """Structured output of a SentinelPrime verification."""

    def __init__(
        self,
        claim: str,
        observed: str,
        evidence: List[str],
        delta: str,
        verdict: str,
        reason: Optional[str] = None,
        confidence: float = 1.0,
    ):
        self.claim = claim
        self.observed = observed
        self.evidence = evidence
        self.delta = delta
        self.verdict = verdict
        self.reason = reason
        self.confidence = confidence

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2)

    def __str__(self) -> str:
        return self.to_json()


class DeclaredState:
    """Declared state of an artifact, extracted from its own metadata header."""

    def __init__(self, artifact_id: str, version: str, status: str, **kwargs: Any) -> None:
        self.artifact_id = artifact_id
        self.version = version
        self.status = status
        self.metadata = kwargs


class ObservedState:
    """Observed state of an artifact, derived from verifier execution."""

    def __init__(self, verifier_results: Dict[str, Any]):
        self.verifier_results = verifier_results
