# PLAN-rosetta-consolidation.md

> **Domain**: ARCH
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-06-30** **Domain: ARCH** **State: [ACTIVE]** **Tags:** `Consolidation, Rosetta, Archive` **Criticality: High**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                               | Description       |
| :---------------- | :---------------------------------- | :---------------- |
| **Artifact ID**   | `PLAN-ROSETTA-CONSOLIDATION-001`    | The Sovereign ID. |
| **Official Name** | `PLAN-rosetta-consolidation.md`     | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**                   | The Standard.     |
| **Domain**        | `ARCH`                              | The Subject.      |
| **Celestial Class** | `[PLANET]`                         | The Weight.       |
| **Evolution**       | `Omega Ascension`                   | The Maturity.     |
| **Status**          | `[ACTIVE]`                          | The Lifecycle.    |
| **Relations**       | `GOVERNED_BY: CORE-CODEX-001`       | The Network.      |

---

# Project Plan: Rosetta Stone Consolidation

This plan outlines the systematic, non-destructive search and consolidation of duplicate `phoenix-rosetta-stone` directories located across the workspace.

## **Phase 1: Deep Diffing & Inventory Scan**
*   **Action**: Scan and inventory all files within the identified directories:
    1.  `C:\Users\Chris\ .dev\phoenix-rosetta-stone`
    2.  `C:\Users\Chris\ .dev\New folder\phoenix-rosetta-stone`
    3.  `C:\Users\Chris\ .dev\OLD PROJECTS\Past Projectx\phoenix-rosetta-stone`
*   **Goal**: Create a master list of all markdown files (`*.md`) and source code files (`*.py`, `*.ts`, `*.js`, `*.json`) across these paths.
*   **Diffing**: Compare each file to those in the active `Synarche_Workspace/` to isolate unique modifications, scripts, or documentation not currently present in the primary repository.

## **Phase 2: Extraction & Safe Merge**
*   **Action**: Copy verified unique assets (code and documentation) into their appropriate directories in `Synarche_Workspace/`.
    *   Unique developer prompts/guidelines -> `.agent/`
    *   Unique source code/scripts -> `packages/` or `axion-core/`
    *   Historical logs -> `_governance/50_Logs/` or `_governance/70_Learnings/`

## **Phase 3: Compress & Purge**
*   **Action**: 
    1.  Compress the three source `phoenix-rosetta-stone` duplicate folders into a single offline archive:
        `C:\Users\Chris\Synarche_Workspace\_governance\60_Archives\phoenix-rosetta-stone-legacy.zip`
    2.  Permanently delete the three original source directories to eliminate IDE indexing pollution.

## **Phase 4: Registry Synchronization**
*   **Action**: Run the Loom controller to calculate SHA-256 hashes of the newly merged assets and commit them to the master registry:
    `C:\DevEnvironments\master_env\Scripts\python.exe axion-core/forge/loom.py pull`

---

## **Verification Checklist**

- [ ] Directory inventory complete.
- [ ] Unique source code/markdown files identified.
- [ ] Unique assets merged into `Synarche_Workspace/`.
- [ ] Duplicate folders compressed to `_governance/60_Archives/phoenix-rosetta-stone-legacy.zip`.
- [ ] Original folders deleted.
- [ ] `loom.py pull` runs successfully and indexes all new files.

###### **[ARTIFACT END]**
