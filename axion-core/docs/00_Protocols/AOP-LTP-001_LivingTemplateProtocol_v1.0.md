# Universal Identification & Provenance (UIP)

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `AOP-LTP-001_LivingTemplateProtocol_v1.0` | The Sovereign ID. |
| **Official Name** | `AOP-LTP-001_LivingTemplateProtocol_v1.0.md` | The Filename.     |
| **Version**       | **v14.0 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |



---

### **Block B: State Vector (AGP-001)**
| State Field | Value |
| :--- | :--- |
| **Coherence** | `1.0` |
| **Resonance** | `0.9` |
| **Stability** | `Stable` |

### **Block C: Risk & Mitigation (AGP-002)**
| Risk | Mitigation |
| :--- | :--- |
| **Logic Drift** | Strict Linter Enforcement |
| **Dependency Break** | ForgeLink Validation |

---

# AOP-LTP-001: The Living Template Protocol (LTP)

**Axiom of Purpose:** To implement "transclusion" as the primary method for document integrity—moving away from static
copy-pasting to "living stubs", and to empower the Coherent Synthesis Engine (CSE) to fetch and fill these blocks
autonomously.

> _"Growth requires a stable root; knowledge requires a definitive anchor."_ — **AOP-CORE-LOCK-001**

---

## 1. The Core Philosophy

The Living Template Protocol defines the relationship between the **Master Shells** (the outer framework of a document)
and the **Transclusion Blocks** (the inner, reusable semantic organs).

Every new artifact generated within the Synarche MUST be constructed using the Living Template Protocol. We do not
copy-paste old files. We forge new files from pristine shells, and transclude the contextual blocks required to give
them purpose.

## 2. The Transclusion Vaults

The definitive repository for all templates is defined as follows:

- **`_governance/templates/Master_Shells/`**: Houses the outer frameworks (e.g., `UMB`, `AOP`, `CSL`, `GUCA`

  blueprints). These files contain transclusion tags like `{{ TRANSCLUDE: BLOCK_A }}`.

- **`_governance/templates/Transclusion_Blocks/`**: Houses the 29+ standardized internal semantic blocks (`BLK-*`,

  `SELT-*`, `block_*`).

## 3. The Pentecostal Blocks (A-E)

Every canonical OMEGA v14.0 artifact is built upon five foundational blocks. The CSE is tasked with fetching these
blocks and, using **Internal Hands Autonomy**, filling out the required parameters by reading the surrounding context
_without_ demanding the user explicitly supply every variable.

- **[BLOCK A] Identification Lock (UIP):** Establishes the Sovereign ID, Timestamp Anchor, and Universal Identification

  Protocol.

- **[BLOCK B] Operational Ethos (State):** Defines the "Why" (The Axiom of Purpose) and the current operating state.
- **[BLOCK C] Spine Axiom (Risk/Rules):** Establishes the governing constraints, boundary conditions, and risks.
- **[BLOCK D] Integrity Gate (Synergy):** Defines the relationships (`ForgeLink`, `Echo`), connections to other nodes,

  and the finalization validation.

- **[BLOCK E] Omni-Anchor (Closing):** The causal link, execution trace, and closing signature (`SHA256_HASH`,

  `causal_link`).

## 4. The Transclusion Syntax

Master Shells must use the following Jinja-style syntax to invite a Transclusion Block:

```markdown
{{ TRANSCLUDE: block_a_uip.md }}
```

## 5. Execution Engine (`transclude_engine.py`)

The protocol is physically enforced by the `transclude_engine.py` tool.

1. **Select Shell:** The engine targets a Master Shell.
2. **Scan for Tags:** It reads the markdown file for `{{ TRANSCLUDE: filename.md }}`.
3. **Resolve & Fetch:** It locates `filename.md` in the `Transclusion_Blocks` vault.
4. **Populate & Weave:** It requests the necessary context from the CSE, injects the populated text into the shell, and

    writes the resulting artifact to its designated tier.

---

### End of Protocol

### **Block D: Standardized Synergy Block (The Loom Signature)**
Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: REFORGE` | Execute Structural Transmutation | Canonization |
| `⚡ EXECUTE: CANONIZE` | Formally Cement Alignment | Zero Entropy |

---

### **Rationale (The "Why")**
Alignment to v14.0 OMEGA standard.

###### **[ARTIFACT END]**
