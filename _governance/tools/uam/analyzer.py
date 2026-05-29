"""
artifact_anchor:
  id: GVRN.ANALYZER.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: GVRN
  celestial_class: STAR
  tier: GOVERNANCE
  state: ACTIVE
  ethos: SOVEREIGN_GOVERNANCE_COMPONENT
  relations: []
"""

# Phase 6: Topological & Semantic Verification Engine
# Validates graph integrity, cycle clusters via Tarjan's SCC, layer crossings, and ontological semantic boundaries

import os
from .config import FORBIDDEN_TIER_CROSSINGS
from .lexicon import ONTOLOGICAL_LEXICON

class TopologicalAnalyzer:
    def __init__(self, target_dir: str, registry: dict):
        self.target_dir = os.path.abspath(target_dir)
        self.registry = registry

    def validate_referential_integrity(self) -> list[str]:
        """Checks if declared relationships point to active IDs or valid files in the workspace."""
        errors = []
        for node_id, node_data in self.registry.items():
            rel_path = node_data.get("rel_path")
            for rel in node_data.get("relations", []):
                target = rel.get("node")
                if target not in self.registry:
                    # Fallback check: is it an existing path relative to target_dir?
                    target_file_path = os.path.join(self.target_dir, target)
                    # Or relative to the source file's own directory?
                    local_dir = os.path.dirname(os.path.join(self.target_dir, rel_path))
                    local_target_path = os.path.join(local_dir, target)
                    
                    if not os.path.exists(target_file_path) and not os.path.exists(local_target_path):
                        errors.append(
                            f"[REFERENTIAL INTEGRITY VIOLATION] '{node_id}' ({rel_path}) declares target '{target}' "
                            f"which does not exist in the workspace as a registered ID or file path."
                        )
        return errors

    def validate_tier_crossings(self) -> list[str]:
        """Enforces clean structural layers by catching forbidden tier-crossing dependencies."""
        violations = []
        for node_id, node_data in self.registry.items():
            node_tier = node_data.get("tier")
            rel_path = node_data.get("rel_path")
            if node_tier in FORBIDDEN_TIER_CROSSINGS:
                forbidden = FORBIDDEN_TIER_CROSSINGS[node_tier]
                for rel in node_data.get("relations", []):
                    target = rel.get("node")
                    if target in self.registry:
                        target_tier = self.registry[target].get("tier")
                        if target_tier in forbidden:
                            violations.append(
                                f"[TIER CROSSING VIOLATION] '{node_id}' ({node_tier} tier) is not allowed to depend on "
                                f"'{target}' ({target_tier} tier) in file '{rel_path}'."
                            )
        return violations

    def validate_semantic_boundaries(self) -> list[str]:
        """Enforces Ontological Semantic Boundaries by checking if a file's declared ethos
        contains vocabulary terms that violate its architectural context rules.
        """
        leaks = []
        for node_id, node_data in self.registry.items():
            ethos = str(node_data.get("ethos", "")).lower()
            tier = node_data.get("tier", "").upper()
            domain = node_data.get("domain", "").upper()
            rel_path = node_data.get("rel_path")

            for lex_id, term_data in ONTOLOGICAL_LEXICON.items():
                term_name = term_data["term"].lower()
                aliases = [a.lower() for a in term_data.get("aliases", [])]
                
                # Check if file ethos references this conceptual abstraction
                matches_term = (term_name in ethos) or any(a in ethos for a in aliases)
                if matches_term:
                    forbidden = [f.upper() for f in term_data.get("forbidden_contexts", [])]
                    # Verify if the node exists in a forbidden tier or domain context
                    if tier in forbidden or domain in forbidden:
                        leaks.append(
                            f"[SEMANTIC BOUNDARY LEAK] '{node_id}' ({rel_path}) has ethos '{node_data.get('ethos')}' "
                            f"referencing concept '{term_data['term']}' ({lex_id}), which is strictly forbidden "
                            f"in {tier}/{domain} contexts."
                        )
        return leaks

    def detect_cycle_clusters_tarjan(self) -> list[list[str]]:
        """Finds circular dependency clusters using Tarjan's Strongly Connected Components algorithm."""
        index_counter = 0
        indices = {}
        lowlinks = {}
        on_stack = set()
        stack = []
        sccs = []

        def strongconnect(curr_id):
            nonlocal index_counter
            indices[curr_id] = index_counter
            lowlinks[curr_id] = index_counter
            index_counter += 1
            stack.append(curr_id)
            on_stack.add(curr_id)

            curr_data = self.registry.get(curr_id, {})
            for rel in curr_data.get("relations", []):
                target = rel.get("node")
                if target in self.registry:
                    if target not in indices:
                        strongconnect(target)
                        lowlinks[curr_id] = min(lowlinks[curr_id], lowlinks[target])
                    elif target in on_stack:
                        lowlinks[curr_id] = min(lowlinks[curr_id], indices[target])

            if lowlinks[curr_id] == indices[curr_id]:
                scc = []
                while True:
                    node = stack.pop()
                    on_stack.remove(node)
                    scc.append(node)
                    if node == curr_id:
                        break
                if len(scc) > 1:
                    sccs.append(scc)
                else:
                    node = scc[0]
                    node_data = self.registry.get(node, {})
                    for rel in node_data.get("relations", []):
                        if rel.get("node") == node:
                            sccs.append(scc)
                            break

        for node_id in self.registry:
            if node_id not in indices:
                strongconnect(node_id)

        return sccs
