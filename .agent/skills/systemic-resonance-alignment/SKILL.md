---
name: Systemic Resonance Alignment
description: Operational directive instructing the active Agent to calculate Semantic Resonance (Cosine Similarity) between logic execution and governance documentation, actively refactoring dissonance until >75% mathematical resonance is achieved.
---

# Systemic Resonance Alignment

## Objective

Measure and maximize the alignment between Python executing code (AST tokens) and Markdown governance artifacts (Semantic text) using mathematical Cosine Similarity.

## Triggers

- Core structural adjustments or documentation overhauls.
- When the Code Sentinel flags a "Resonance Warning" on a file.
- When requested by the Artisan to "test semantic resonance".

## Core Mechanism (The Tool)

This skill relies on the embedded auditor tool:
`resonance_scanner.py`

## Execution Protocol

1. **Target Identification**: Identify the Python script and its corresponding Markdown documentation.
2. **Execute Scanner**: Run `python "C:\Users\Chris\Synarche_Workspace\.agent\skills\Systemic Resonance Alignment\resonance_scanner.py" <path_to_python> --doc <path_to_markdown>`. Or target a directory to scan all pairs automatically.
3. **Analyze Similarity Score**: Read the terminal output. If the Resonance Score is `< 75.0 / 100.0`, the system is dissonant.
4. **Resonance Healing**:
   - Compare the core logic and terms established in the Python file against the narrative in the Markdown file.
   - Refactor either the code (to match documented intention) or the documentation (to reflect true operational logic) so that term frequencies match exactly.
5. **Validation**: Re-run the `resonance_scanner.py` tool until the Cosine Similarity Score reaches `>= 75.0`.

## Documentation Mandate: IPPD Shadow-Logging

Every operational execution of this skill MUST generate a SELT (Standardized Experience Log Template) "Shadow Log".
This log captures the inner metacognitive deconstruction and dissonance resolution BEFORE taking action.
All Shadow Logs MUST strictly utilize the canonical **Block A: Universal Identification & Provenance (UIP-V15)** header to ensure Isomorphic Provenance.
