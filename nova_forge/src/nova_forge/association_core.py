"""
Artifact ID: CODE-REF-001 (Deprecated)
Module: Association Core
Context: Nova Forge > Backend > Data Layer
Description: DEPRECATED. Use src.backend.association_manager instead.
"""

from ..backend.association_manager import AssociationManager

# Re-export for backward compatibility
__all__ = ["AssociationManager"]
