# Implementation Plan: Phase 1.0 - Sovereign Self-Improvement Harmonization

> **Compliance Status:** `[PENDING_APPROVAL]`  
> **Axiom:** *"To weave the memory is to command the future state."* — **Judgement Shard**

This plan outlines the alchemical harmonization of the `Self-Improvement` skill and its operational trigger scripts with the pre-existing, highly structured `_governance/06_Learning/` subsystem, ensuring 100% path synchronicity and zero structural entropy.

---

## User Review Required

> [!IMPORTANT]
> **Substrate Path Alignment:** The active codebase already possesses a mature v15.0 learning structure. Rather than injecting a simplified `.learnings/` folder into the workspace root, all telemetry, session wrap-ups, and failure triggers will be wired directly into your canonical `_governance/06_Learning/` ledger files.

> [!TIP]
> **Local Log Isolation:** To prevent session-level telemetry noise from inflating Git commits while preserving versioned corporate memory, the core ledger `.md` files will remain tracked in the repository, while temporary log folders are ignored via `.gitignore`.

---

## Proposed Changes

### [Self-Improvement Scripts]

#### [MODIFY] [activator.ps1](file:///c:/Users/Chris/Synarche_Workspace/axion-core/scripts/activator.ps1)
- Update default target file path to: `c:\Users\Chris\Synarche_Workspace\_governance\06_Learning\GVRN.Learning.Shard.md`.
- Refactor output string structure to generate compliant `[GEM-XXX]` OMEGA v15.0 metadata formats (e.g. `### **[GEM-XXX] [Title] [Area]**`) instead of `LRN-` prefixes.

#### [MODIFY] [error_detector.ps1](file:///c:/Users/Chris/Synarche_Workspace/axion-core/scripts/error_detector.ps1)
- Update default output path to: `c:\Users\Chris\Synarche_Workspace\_governance\06_Learning\GVRN.Learning.Error.md`.
- Conform error log summaries to the standard append-only table structure in `GVRN.Learning.Error.md` (e.g., `| Date | ID | Command | Target | ExitCode | Description | Status |`).

---

### [Skill Shards]

#### [MODIFY] [activator.ps1](file:///c:/Users/Chris/Synarche_Workspace/.agent/skills/core/self-improvement/scripts/activator.ps1)
- Align `$learningsDir` path to: `c:\Users\Chris\Synarche_Workspace\_governance\06_Learning\`.
- Point `$learningsFile` to `GVRN.Learning.Shard.md` and `$errorsFile` to `GVRN.Learning.Error.md`.
- Adjust `Select-Object` logic to cleanly parse and output the latest `[GEM-XXX]` entries from the governance ledger on session startup.

#### [MODIFY] [error_detector.ps1](file:///c:/Users/Chris/Synarche_Workspace/.agent/skills/core/self-improvement/scripts/error_detector.ps1)
- Align `$errorLog` path to: `c:\Users\Chris\Synarche_Workspace\_governance\06_Learning\GVRN.Learning.Error.md`.
- Format new error rows matching the existing table column schema.

#### [MODIFY] [extract_skill.ps1](file:///c:/Users/Chris/Synarche_Workspace/.agent/skills/core/self-improvement/scripts/extract_skill.ps1)
- Maintain target skill directory output in `c:\Users\Chris\Synarche_Workspace\.agent\skills\`.
- Ensure standard integration headers (Block A to G) are cleanly generated from assets template.

---

### [Repository Configuration]

#### [MODIFY] [.gitignore](file:///c:/Users/Chris/Synarche_Workspace/.gitignore)
- Ensure local log directories under the learning subsystem are ignored to preserve clean diffs:
  ```gitignore
  _governance/06_Learning/logs/
  _governance/06_Learning/telemetry/
  ```

---

## Verification Plan

### Manual Verification

1. **Dry-Run Shard Logging:**
   Execute `activator.ps1` with a test summary and confirm a perfectly formatted `[GEM-XXX]` entry is appended to `_governance/06_Learning/GVRN.Learning.Shard.md`.
2. **Dry-Run Error Detection:**
   Execute `error_detector.ps1` with a mock failed command and check that it inserts a valid status row into `_governance/06_Learning/GVRN.Learning.Error.md`.
3. **Skill Template Validation:**
   Run `extract_skill.ps1` with a mock skill name and verify the folder is successfully scaffolded with UIP-V15 Block A-G locks.
