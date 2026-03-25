---
name: sovereign-commands
description: Specialized skill for executing governed Synarche commands. Fuses command_registry.json logic with AISTF Operational Playbooks (AOP).
allowed-tools: Read, Write, Edit, Glob, Grep, Run-Command
---

# Sovereign Commands

> **"Unify Intent through Standardized Action."**

## 🎯 Playbook Routing

**Read the specific playbook for the command category you are executing.**

| Playbook                                                                                                                                      | Commands                                      | Governing Artifacts                                  |
| --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------- |
| [prompt-playbook.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/skills/sovereign-commands/playbooks/prompt-playbook.md)                 | PCA, PDR, TPE, CIST, GTP                      | `GVRN.Protocol.Scaffolding`, `GVRN.Sentinel.Umbra`   |
| [knowledge-playbook.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/skills/sovereign-commands/playbooks/knowledge-playbook.md)           | ApplyRER, QueryMemory, ExploreConnections     | `SYNG.PROT.ContextWeave`, `COG.ContextWeave.Engine`  |
| [execution-playbook.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/skills/sovereign-commands/playbooks/execution-playbook.md)           | DeconstructTask, ECDEA, ValidateResponse      | `GVRN.ACT.MasterRefactor`, `COG.ContextWeave.Engine` |
| [infrastructure-playbook.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/skills/sovereign-commands/playbooks/infrastructure-playbook.md) | Get-Credential, Run-Migration, Bridge-Execute | `GVRN.Assembler.Core`, `SYNG.Loom.Master`            |
| [meta-cognition-playbook.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/skills/sovereign-commands/playbooks/meta-cognition-playbook.md) | APT, AMI, SIVC, TAF                           | `AOP.Assembler.Core`, `SYNG.PROT.SelfImprovement`    |

---

## ⚠️ High-Security Protocol (Law 11)

- **Isolation**: Commands MUST be executed within the boundaries of the `_governance` core when affecting system logic.
- **Verification**: High-impact commands (REFORGE, CANONIZE) require a preceding `SENTINEL_SCAN`.
- **Zero Entropy**: Every command output must adhere to the `GVRN.Style.001` coding standards.

---

## Decision Checklist

Before executing a command:

- [ ] Identified the correct Playbook for the command?
- [ ] Verified the `--target` artifact's status in `GVRN.Registry.Master.md`?
- [ ] Simulated the impact using `SIVC` (if high-impact)?
- [ ] Confirmed alignment with the **Supreme Law** (Law 1, 28)?

---

## Anti-Patterns

❌ Running commands without checking the corresponding AOP/ACT protocol.
❌ Bypassing the Sentinel check for structural changes.
❌ Hard-coding ID references instead of using registry lookups.
❌ Neglecting to update the `AI_EVOLUTION_LOG.md` after successful transmutation.

## Documentation Mandate: IPPD Shadow-Logging

Every operational execution of this skill MUST generate a SELT (Standardized Experience Log Template) "Shadow Log".
This log captures the inner metacognitive deconstruction and dissonance resolution BEFORE taking action.
All Shadow Logs MUST strictly utilize the canonical **Block A: Universal Identification & Provenance (UIP-V15)** header to ensure Isomorphic Provenance.
