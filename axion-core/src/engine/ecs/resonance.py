"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-ECS-RES-001`             | The Sovereign ID. |
| **Official Name**   | `resonance.py`                | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-ECS`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Domain Resonance (Law 33)**
> Implemented from Blueprint `GVRN.REG.EcsResonance.md`.
> Ethos: Security through Isolation.
"""

import logging
from enum import Enum, auto
from typing import Dict, Type


class ResonanceDomain(Enum):
    """
    Functional domains that define the architectural boundaries of the engine.
    Used to categorize components and systems into secure operational zones.
    """

    CORE = auto()  # Identity, Lifecycle, Metadata
    MOTION = auto()  # Physics, Transform, Spatial
    COMBAT = auto()  # Health, Status, Moral Alignment
    SENSORY = auto()  # AI Perception, Environmental Triggers
    ADMIN = auto()  # Privileged access for meta-systems


class ResonanceRegistry:
    """
    The Sovereign Rulebook: Maps Component Types to Resonance Domains.
    Acts as the source of truth for domain-based access control.
    """

    def __init__(self) -> None:
        """Initializes the registry with an empty mapping set."""
        # Component Class -> ResonanceDomain
        self.mappings: Dict[Type, ResonanceDomain] = {}

    def register(self, component_type: Type, domain: ResonanceDomain) -> None:
        """
        Maps a component type to a specific functional domain.

        Args:
            component_type (Type): The class of the component.
            domain (ResonanceDomain): The target domain for this component.
        """
        self.mappings[component_type] = domain

    def get_domain(self, component_type: Type) -> ResonanceDomain:
        """
        Retrieves the domain for a component type. Defaults to CORE.

        Args:
            component_type (Type): The class of the component.

        Returns:
            ResonanceDomain: The mapped domain or ResonanceDomain.CORE if unmapped.
        """
        return self.mappings.get(component_type, ResonanceDomain.CORE)


class ResonanceAuditor:
    """
    The Security Layer: Monitors and validates data access patterns.
    Identifies 'Semantic Dissonance'—when a system tries to cross
    unauthorized domain boundaries (e.g., a Motion System touching Combat stats).
    """

    def __init__(self, registry: ResonanceRegistry) -> None:
        """
        Initializes the auditor with a registry and a logger.

        Args:
            registry (ResonanceRegistry): The rulebook to audit against.
        """
        self.registry = registry
        self.logger = logging.getLogger("PhoenixLogger")

    def validate_access(self, system_name: str, system_domain: ResonanceDomain, component_type: Type) -> bool:
        """
        Verifies if a system is authorized to access a specific component type.
        Logs an error and returns False if a domain violation is detected.

        Args:
            system_name (str): The name of the requesting system.
            system_domain (ResonanceDomain): The domain the system belongs to.
            component_type (Type): The class of the component being accessed.

        Returns:
            bool: True if access is granted, False otherwise.
        """
        if system_domain == ResonanceDomain.ADMIN:
            return True

        required_domain = self.registry.get_domain(component_type)

        if system_domain != required_domain:
            # We log this as a critical architectural dissonance event
            self.logger.error(
                f"🚨 [SYSTEMIC DISSONANCE] 🚨\n"
                f"Source: System '{system_name}' (Domain: {system_domain.name})\n"
                f"Violation: Attempted access to '{component_type.__name__}'\n"
                f"Restriction: Component is locked to {required_domain.name}."
            )
            return False

        return True

    def __repr__(self) -> str:
        """Returns a string representation of the auditor state."""
        return f"<ResonanceAuditor mappings={len(self.registry.mappings)}>"
