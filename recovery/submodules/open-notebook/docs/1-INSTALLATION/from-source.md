---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `FROM-SOURCE` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# from-source.md

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-02** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                         | Description       |
| :---------------- | :---------------------------- | :---------------- |
| **Artifact ID**   | `GVRN-FROM-SOURCE-001`        | The Sovereign ID. |
| **Official Name** | `from-source.md`              | The Filename.     |
| **Version**       | **v13.1 [OMEGA]**             | The Standard.     |
| **Domain**        | `GVRN`                        | The Subject.      |
| **Status**        | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |

---

## Development Workflow

### Code Quality

```bash
# Format and lint Python
make ruff
# or: ruff check . --fix

# Type checking
make lint
# or: uv run python -m mypy .
```

### Run Tests

```bash
uv run pytest tests/
```

### Common Commands

```bash
# Start everything
make start-all

# View API docs
open http://localhost:5055/docs

# Check database migrations
# (Auto-run on API startup)

# Clean up
make clean
```

---

## Troubleshooting

### Python version too old

```bash
python --version  # Check version
uv sync --python 3.11  # Use specific version
```

### npm: command not found

Install Node.js from https://nodejs.org/

### Database connection errors

```bash
docker ps  # Check SurrealDB running
docker logs surrealdb  # View logs
```

### Port 5055 already in use

```bash
# Use different port
uv run uvicorn api.main:app --port 5056
```

---

## Next Steps

1. Read [Development Guide](../7-DEVELOPMENT/quick-start.md)
2. See [Architecture Overview](../7-DEVELOPMENT/architecture.md)
3. Check [Contributing Guide](../7-DEVELOPMENT/contributing.md)

---

## Getting Help

- **Discord**: [Community](https://discord.gg/37XJPXfz2w)
- **Issues**: [GitHub Issues](https://github.com/lfnovo/open-notebook/issues)

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
