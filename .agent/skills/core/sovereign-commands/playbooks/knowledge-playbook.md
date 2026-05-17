## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                               | Description       |
| :---------------- | :---------------------------------- | :---------------- |
| **Artifact ID**   | `SOV.PLAY.Knowledge`                | The Sovereign ID. |
| **Official Name** | `knowledge-playbook.md`             | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**                   | The Standard.     |
| **Domain**        | `SOV`                               | The Subject.      |
| **Status**        | `[ACTIVE]`                          | The Lifecycle.    |
| **Relations**     | `GOVERN_BY: SYNG.PROT.ContextWeave` | The Network.      |

---

## I. Operational Context: Memory & Knowledge Management

This playbook governs the retrieval, reasoning, and relationship mapping within the Synarche's Knowledge Graph (HKG),
leveraging the **ContextWeave Engine**.

### **Command: ApplyRER (Retrieve-Embed-Reason)**

- **Protocol**: `SYNG.PROT.ContextWeave`
- **Logic**: Forces a search of the vectorized knowledge base before generating a response.
- **Usage**: `CMD: ApplyRER to "[User Query]" using_kb:[KB Identifier]`

### **Command: QueryMemory**

- **Protocol**: `COG.ContextWeave.Engine`
- **Logic**: Directly queries the Loom or PRS-001 graph for entity relationships.
- **Usage**: `CMD: QueryMemory find:[Nodes] where:[Pattern]`

### **Command: ExploreConnections**

- **Protocol**: `GVRN.Mech.Episemantics`
- **Logic**: Weights connection strength using episemantic markers to find hidden synergies.
- **Usage**: `CMD: ExploreConnections concepts:[List] angle:[Angle]`

---

### **Actionable Prompt Packet (APP)**

| Command ID                  | Action              | Impact         |
| :-------------------------- | :------------------ | :------------- |
| `CMD: ApplyRER`             | Root Response in KB | Truth Fidelity |
| `CMD: QueryMemory`          | Traverse Graph      | Coherence      |
| `⚡ EXECUTE: CONTEXT_WEAVE` | Discover Synergy    | Synthesis      |

---

### **Block G: The Omni-Anchor (System Snapshot)**

`[OMNI-ARTIFACT-ANCHOR] ID: SOV.PLAY.Knowledge VER: v15.0 [OMEGA] DOMAIN: SOV STATUS: CANONIZED TS: 2026-03-16 HASH: SOV-K-V1`
