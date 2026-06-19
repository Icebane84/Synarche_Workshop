## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                       | Description       |
| :---------------- | :-------------------------- | :---------------- |
| **Artifact ID**   | `SYNG.SKILL.InsForgeCLI`    | The Sovereign ID. |
| **Official Name** | `SKILL.md`                  | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**           | The Standard.     |
| **Domain**        | `INFRASTRUCTURE`            | The Subject.      |
| **Status**        | `[ACTIVE]`                  | The Lifecycle.    |
| **Relations**     | `REF: GVRN.Master.Registry` | The Network.      |

---

# 🛠️ InsForge CLI Skill

Patterns for managing InsForge backend infrastructure via `npx @insforge/cli`.

## 🏗️ Core Commands

### Database Schema

Run raw SQL for migrations and RLS policies.

```bash
npx @insforge/cli run-raw-sql --query "CREATE TABLE test..."
```

### Storage Buckets

```bash
npx @insforge/cli create-bucket --name my-bucket --public true
```

### Edge Functions

```bash
npx @insforge/cli create-function --name my-func --slug func-slug --codeFile ./path/to/code.js
```

### Frontend Deployment

```bash
npx @insforge/cli create-deployment --sourceDirectory ./dist
```

## 🛡️ Metadata Retrieval

Get project keys and URLs.

```bash
npx @insforge/cli get-backend-metadata
```

---

`[OMNI-ANCHOR] ID: SYNG.SKILL.InsForgeCLI VER: v15.0 [OMEGA] STATUS: ACTIVE`

## Documentation Mandate: IPPD Shadow-Logging

Every operational execution of this skill MUST generate a SELT (Standardized Experience Log Template) "Shadow Log".
This log captures the inner metacognitive deconstruction and dissonance resolution BEFORE taking action.
All Shadow Logs MUST strictly utilize the canonical **Block A: Universal Identification & Provenance (UIP-V15)** header to ensure Isomorphic Provenance.
