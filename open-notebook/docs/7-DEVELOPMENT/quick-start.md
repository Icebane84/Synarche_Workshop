---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `QUICK-START` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# quick-start.md
> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-02** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN-QUICK-START-001` | The Sovereign ID. |
| **Official Name** | `quick-start.md` | The Filename.     |
| **Version**       | **v13.1 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |






---

## Next Steps

- **First Issue?** Pick a [good first issue](https://github.com/lfnovo/open-notebook/issues?q=label%3A%22good+first+issue%22)
- **Understand the code?** Read [Architecture Overview](architecture.md)
- **Make changes?** Follow [Contributing Guide](contributing.md)
- **Setup details?** See [Development Setup](development-setup.md)

---

## Troubleshooting

### "Port 5055 already in use"
```bash
# Find what's using the port
lsof -i :5055

# Use a different port
uv run uvicorn api.main:app --port 5056
```

### "Can't connect to SurrealDB"
```bash
# Check if SurrealDB is running
docker ps | grep surrealdb

# Restart it
make database
```

### "Python version is too old"
```bash
# Check your Python version
python --version  # Should be 3.11+

# Use Python 3.11 specifically
uv sync --python 3.11
```

### "npm: command not found"
```bash
# Install Node.js from https://nodejs.org/
# Then install frontend dependencies
cd frontend && npm install
```

---

## Common Development Commands

```bash
# Run tests
uv run pytest

# Format code
make ruff

# Type checking
make lint

# Run the full stack
make start-all

# View API documentation
open http://localhost:5055/docs
```

---

Need more help? See [Development Setup](development-setup.md) for details or join our [Discord](https://discord.gg/37XJPXfz2w).

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
