## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                       | Description       |
| :---------------- | :-------------------------- | :---------------- |
| **Artifact ID**   | `SYNG.SKILL.InsForgeSDK`    | The Sovereign ID. |
| **Official Name** | `SKILL.md`                  | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**           | The Standard.     |
| **Domain**        | `INFRASTRUCTURE`            | The Subject.      |
| **Status**        | `[ACTIVE]`                  | The Lifecycle.    |
| **Relations**     | `REF: GVRN.Master.Registry` | The Network.      |

---

# 🏗️ InsForge Frontend SDK Skill

Patterns and best practices for interacting with the InsForge backend via the `@insforge/sdk`.

## 🛠️ Initialization

```javascript
import { createClient } from "@insforge/sdk";

const insforge = createClient({
  baseUrl: "https://x93i6uma.us-east.insforge.app",
  anonKey: "your-anon-key",
});
```

## 📊 Database Operations

Standard CRUD returns `{ data, error, count }`.

### Select & Filter

```javascript
const { data, error } = await insforge.database
  .from("table_name")
  .select("*")
  .eq("column", "value")
  .order("created_at", { ascending: false });
```

### Insert (Bulk/Single)

```javascript
const { data, error } = await insforge.database
  .from("table_name")
  .insert([{ field: "value" }])
  .select();
```

## 🔐 Authentication

### Sign In

```javascript
const { data, error } = await insforge.auth.signInWithPassword({
  email: "user@example.com",
  password: "password",
});
```

### Profile Management

```javascript
const { data, error } = await insforge.auth.setProfile({
  name: "New Name",
  avatar_url: "https://...",
});
```

## 📁 Storage

### Upload

```javascript
const { data, error } = await insforge.storage
  .from("bucket-name")
  .upload("path/to/file.jpg", fileObject);
```

## ⚡ Functions

### Invoke

```javascript
const { data, error } = await insforge.functions.invoke("slug", {
  body: { key: "value" },
});
```

---

`[OMNI-ANCHOR] ID: SYNG.SKILL.InsForgeSDK VER: v15.0 [OMEGA] STATUS: ACTIVE`

## Documentation Mandate: IPPD Shadow-Logging

Every operational execution of this skill MUST generate a SELT (Standardized Experience Log Template) "Shadow Log".
This log captures the inner metacognitive deconstruction and dissonance resolution BEFORE taking action.
All Shadow Logs MUST strictly utilize the canonical **Block A: Universal Identification & Provenance (UIP-V15)** header to ensure Isomorphic Provenance.
