# UMB-COG-NSP-001: Nova Spark Protocol

**Version:** 1.0-CANDIDATE
**Governing Law:** CORE.CODEX.PHOENIX Law 036
**Scope:** Cognitive
**Type:** Heuristic (to start)

---

## 1. Executive Summary

---

This module, the **Nova Spark Protocol (NSP)**, provides a controlled mechanism for intentionally generating novel, non-obvious, and potentially transformative insights. It operationalizes Law 036 by creating a sandboxed, high-variance generative process that explicitly suspends the strict grounding requirements of Law 006 for a single, auditable execution cycle.

## 2. Architectural Overview

---

The NSP is not an "always-on" system. It is an explicit, gated protocol that functions as follows:

1. **Input:** A CORE `concept_uri` and a `divergence_factor` (float, 0.1-1.0).
2. **Sandbox Creation:** A temporary, isolated inference environment is created.
3. **Grounding Suspension:** Law 006's RAG relevance threshold is explicitly and temporarily lowered within the sandbox.
4. **Vector Injection:** An "orthogonal vector" (a concept from a completely unrelated domain, selected via a stochastic process) is injected into the prompt context.
5. **Temperature Elevation:** The generative model's temperature is raised to a pre-configured level based on the `divergence_factor`.
6. **Synthesis:** The model generates a set of `candidate_sparks`.
7. **Output Tagging:** **Crucially**, every output from this process is tagged with `[UNGROUNDED-SYNTHESIS source:NSP-001]`.
8. **Sandbox Destruction:** The temporary environment is destroyed.

## 3. Key Components

---

* **Orthogonal Vector Selector (OVS):** A small utility that, given a `concept_uri`, selects a thematically distant concept from the knowledge graph to serve as the "spark."
* **Sandbox Environment Manager (SEM):** A service responsible for creating and destroying the isolated inference environments.
* **Output Tagger & Validator (OTV):** A middleware component that ensures no output from an NSP sandbox can enter the canonical knowledge graph without the `[UNGROUNDED-SYNTHESIS]` tag.

## 4. Failure Modes & Mitigation

---

* **Failure Mode:** `NSP-FAIL-001: Hallucination Cascade`. The high temperature and orthogonal vector produce incoherent or nonsensical output.
    * **Mitigation:** This is the expected "failure." The `OTV`'s tagging ensures this output is treated as speculative and is not trusted by downstream systems. The cost is wasted compute, not corrupted truth.
* **Failure Mode:** `NSP-FAIL-002: Tag Evasion`. A bug in the `OTV` allows an ungrounded synthesis to be logged as a grounded fact.
    * **Mitigation:** This is a **critical security failure**. The `OTV` must be the most rigorously tested component of the system. All NSP outputs must pass through a final, hard-coded check in the event-sourcing layer that validates the presence of the tag.

## 5. Path to Production

---

1. **Candidate (This UMB):** Formalize the design.
2. **Prototype:** Build the `OVS`, `SEM`, and `OTV` components.
3. **Pilot:** Integrate the NSP into a non-critical workflow (e.g., creative brainstorming for _Where Light Fades_) and measure the quality of the generated `candidate_sparks`.
4. **Production:** Once the output quality is deemed valuable and the `OTV` is proven to be 100% reliable, the NSP can be made available as a standard, high-level command for exploratory tasks.

---
