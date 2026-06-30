# c:\Users\Chris\Synarche_Workspace\axion-core\src\esf\esf_core.py
"""
This module contains the core implementation of the Episemantic Framework (ESF),
the system responsible for annotating artifacts with machine-readable markers
to define their state of knowledge.

Governed by: UMB-ESF-001, OGLN.Architecture.LayerProtocol
"""

import re
from dataclasses import dataclass, asdict, fields
from enum import Enum
from typing import Optional, Dict, Type


# --- GVRN-STD-ENUM-001: ESF Marker Definitions ---

class Veracity(Enum):
    """Explicitly marks the truthfulness of information."""
    VERIFIED = "verified"
    DISPUTED = "disputed"
    HALLUCINATION = "hallucination"
    THEORETICAL = "theoretical"


class Nexus(Enum):
    """Defines the artifact's relationship to the core system logic."""
    ALIGNED = "aligned"
    DEPRECATED = "deprecated"
    CANON = "canon"
    REFACTOR = "refactor"


class Tempus(Enum):
    """Defines the temporal relevance of the information."""
    EVERGREEN = "evergreen"
    SNAPSHOT = "snapshot"
    VOLATILE = "volatile"


# --- Core ESF Data Structure ---

@dataclass
class EpisemanticSignature:
    """
    A structured container for all episemantic markers associated with an artifact.
    Provides a clean, type-safe interface for the Sentinel and other systems.
    """
    veracity: Optional[Veracity] = None
    nexus: Optional[Nexus] = None
    tempus: Optional[Tempus] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        """Serializes the signature to a dictionary, converting enums to strings."""
        return {
            field.name: getattr(self, field.name).value if getattr(self, field.name) else None
            for field in fields(self)
        }


# --- ESF Utility Engine ---

class ESFEngine:
    """Provides utility functions for parsing and manipulating ESF markers."""

    # Regex to find any [κ-...] marker
    _MARKER_REGEX = re.compile(r"\[κ-(?P<key>\w+):(?P<value>\w+)\]")
    _ENUM_MAP: Dict[str, Type[Enum]] = {
        "veracity": Veracity,
        "nexus": Nexus,
        "tempus": Tempus,
    }

    @classmethod
    def parse_from_text(cls, text: str) -> EpisemanticSignature:
        """
        Parses a string (e.g., file content) and extracts all valid ESF markers
        into a structured EpisemanticSignature object.

        Args:
            text: The text content to parse.

        Returns:
            An EpisemanticSignature instance.
        """
        signature = EpisemanticSignature()
        matches = cls._MARKER_REGEX.finditer(text)

        for match in matches:
            key = match.group("key").lower()
            value_str = match.group("value").lower()

            if key in cls._ENUM_MAP:
                enum_class = cls._ENUM_MAP[key]
                try:
                    enum_value = enum_class(value_str)
                    setattr(signature, key, enum_value)
                except ValueError:
                    # Ignore invalid enum values to maintain robustness
                    print(f"[ESF/WARN]: Invalid value '{value_str}' for marker '{key}'.")

        return signature

    @classmethod
    def generate_marker_string(cls, signature: EpisemanticSignature) -> str:
        """
        Generates a standardized, formatted string of ESF markers from a signature.

        Args:
            signature: The EpisemanticSignature to serialize.

        Returns:
            A formatted string, e.g., "[κ-veracity:verified] [κ-nexus:aligned]".
        """
        parts = []
        sig_dict = signature.to_dict()
        for key, value in sig_dict.items():
            if value:
                parts.append(f"[κ-{key}:{value}]")
        return " ".join(parts)


# --- Example Usage (Conceptual) ---

if __name__ == '__main__':
    # 1. Simulate reading an artifact with embedded markers
    markdown_content = """
    # UMB-DEMO-001: A Canonized Blueprint
    This document is considered absolute truth. [κ-veracity:verified] [κ-nexus:canon]

    It is also designed to be timeless. [κ-tempus:evergreen]

    An invalid marker [κ-color:blue] will be ignored.
    """

    # 2. Parse the content to create a structured signature
    print("--- [Parsing Artifact] ---")
    engine = ESFEngine()
    parsed_signature = engine.parse_from_text(markdown_content)
    print(f"Parsed Signature: {parsed_signature}")
    print(f"Serialized to Dict: {parsed_signature.to_dict()}")

    # 3. Create a new signature and generate its string representation
    print("\n--- [Generating New Marker String] ---")
    new_signature = EpisemanticSignature(
        veracity=Veracity.THEORETICAL,
        nexus=Nexus.REFACTOR
    )
    marker_string = engine.generate_marker_string(new_signature)
    print(f"Generated String: {marker_string}")
