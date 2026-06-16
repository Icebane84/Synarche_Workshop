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

# cse/managers package
from .guca_parser import GucaParser
from .mcp_injector import McpInjector

__all__ = ["GucaParser", "McpInjector"]
