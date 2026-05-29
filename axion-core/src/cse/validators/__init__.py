"""
artifact_anchor:
  id: CORE.INIT.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

from .law_validator import LawValidator

__all__ = ["LawValidator"]
