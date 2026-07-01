# c:\Users\Chris\Synarche_Workspace\scratch\mocks.py
"""
Mock objects for prototyping and testing Axion-Core components.
These are not intended for production use.

Governed by: TDD Principles
"""

from dataclasses import dataclass


@dataclass
class GenerationConfig:
    """A mock configuration for the generative model."""
    temperature: float = 0.7
    suspend_grounding: bool = False


class KnowledgeGraph:
    """
    A mock KnowledgeGraph that simulates a simple, domain-separated
    knowledge base for prototyping purposes.
    """
    def __init__(self):
        self._data = {
            "Distributed Systems Consensus": "Computer Science",
            "Paxos Algorithm": "Computer Science",
            "Raft Consensus": "Computer Science",
            "Byzantine Fault Tolerance": "Computer Science",
            "Cellular Mitosis": "Biology",
            "CRISPR-Cas9": "Biology",
            "Photosynthesis": "Biology",
            "Quantum Entanglement": "Physics",
            "General Relativity": "Physics",
            "String Theory": "Physics",
            "Kantian Ethics": "Philosophy",
            "Stoicism": "Philosophy",
        }

    def get_all_domains(self) -> list[str]:
        return list(set(self._data.values()))

    def get_domain(self, concept: str) -> str:
        return self._data.get(concept, "General")

    def get_random_concept_from_domain(self, domain: str) -> str:
        import random
        concepts_in_domain = [c for c, d in self._data.items() if d == domain]
        return random.choice(concepts_in_domain) if concepts_in_domain else "philosophy"


class GenerativeModel:
    """
    A mock GenerativeModel that returns predictable, hardcoded outputs
    for testing generative protocols.
    """
    def generate(self, prompt: str, config: GenerationConfig) -> list[str]:
        # The mock model ignores the prompt and config, returning a fixed list.
        return [
            "Insight Spark 1: A novel idea connecting the concepts.",
            "Insight Spark 2: An unexpected synergy has been discovered.",
            "Insight Spark 3: A transformative perspective on the core topic."
        ]
