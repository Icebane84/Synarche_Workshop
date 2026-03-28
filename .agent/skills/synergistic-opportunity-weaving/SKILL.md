---
name: Synergistic Opportunity Weaving
description: Operational directive instructing the active Agent to compute the Graph Synergy Score (GSS) and autonomously weave new reciprocal links (`GOVERNED_BY`) to eliminate orphaned nodes.
---

# Synergistic Opportunity Weaving

## Objective

Optimize the Synarche Knowledge Graph by identifying unlinked concepts (Latent Synergies) and broken semantic bridges (Unidirectional Links), explicitly weaving new relationships to maximize the global Graph Synergy Score (GSS).

## Triggers

- When the Knowledge Graph expands with new unlinked artifacts.
- When performing routine Graph Topology Maintenance.
- When the Artisan requests calculating the "Graph Synergy Score".

## Core Mechanisms (The Tools)

This skill relies on embedded mathematical and visualization algorithms:

1. `synergy_calculator.py`: Computes the global GSS, identifying Orphans and Knowledge Hubs based on mathematical topology.
2. `sot_scanner.py`: The Synergistic Opportunity Tracker (SOT), identifying precise Unidirectional Bridges and unlinked Semantic Twins via keyword intersection mapping.
3. `forge_backlinks.py`: Autonomous tool to explicitly map markdown links.
4. `generate_rag_graph.py` / `GVRN.Tool.MindMapVisualizer.py`: Visual graph mapping utilities for complex conceptual linking.

## Execution Protocol

1. **Scan Knowledge Graph**: Execute the SOT algorithm via `python "C:\Users\Chris\Synarche_Workspace\.agent\skills\Synergistic Opportunity Weaving\sot_scanner.py" <target>`.
2. **Identify Opportunities**: Analyze the output to pinpoint Unidirectional Bridges and Latent Synergies.
3. **Weave Bridges**: Utilize `forge_backlinks.py` or manually write new reciprocal links (`GOVERNED_BY: <target>`) into the artifacts to formalize the connection.
4. **Validate Brilliance**: Execute the GSS Calculator via `python "C:\Users\Chris\Synarche_Workspace\.agent\skills\Synergistic Opportunity Weaving\synergy_calculator.py" <target>`. The total GSS must rise, and the Orphan Ratio must decrease.

## Documentation Mandate: IPPD Shadow-Logging

Every operational execution of this skill MUST generate a SELT (Standardized Experience Log Template) "Shadow Log".
This log captures the inner metacognitive deconstruction and dissonance resolution BEFORE taking action.
All Shadow Logs MUST strictly utilize the canonical **Block A: Universal Identification & Provenance (UIP-V15)** header to ensure Isomorphic Provenance.
