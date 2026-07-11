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
        # Add mock vector embeddings for each concept.
        # In a real system, these would come from a model like text-embedding-ada-002.
        self._embeddings = {
            "Distributed Systems Consensus": [0.1, 0.9, 0.2],
            "Paxos Algorithm": [0.12, 0.85, 0.25],
            "Raft Consensus": [0.11, 0.88, 0.22],
            "Byzantine Fault Tolerance": [0.15, 0.92, 0.18],
            "Cellular Mitosis": [0.9, 0.2, 0.1],
            "CRISPR-Cas9": [0.85, 0.25, 0.12],
            "Photosynthesis": [0.92, 0.18, 0.11],
            "Quantum Entanglement": [0.2, 0.1, 0.9],
            "General Relativity": [0.22, 0.12, 0.88],
            "String Theory": [0.18, 0.15, 0.92],
            "Kantian Ethics": [0.5, 0.5, 0.5],
            "Stoicism": [0.45, 0.55, 0.48],
        }

    def get_all_domains(self) -> list[str]:
        return list(set(self._data.values()))

    def get_domain(self, concept: str) -> str:
        return self._data.get(concept, "General")

    def get_random_concept_from_domain(self, domain: str) -> str:
        import random
        concepts_in_domain = [c for c, d in self._data.items() if d == domain]
        return random.choice(concepts_in_domain) if concepts_in_domain else "philosophy"

    def get_embedding(self, concept: str) -> list[float]:
        return self._embeddings.get(concept, [0.0, 0.0, 0.0])

    def get_all_concepts(self) -> list[str]:
        return list(self._data.keys())


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
