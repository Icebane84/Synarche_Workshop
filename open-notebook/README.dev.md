---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `README.DEV` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# README.dev.md
> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-02** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN-README.DEV-001` | The Sovereign ID. |
| **Official Name** | `README.dev.md` | The Filename.     |
| **Version**       | **v13.1 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |






---

## 1. Local Development (Recommended)

**Best for:** Daily development, hot reload, debugging

### Setup

```bash
# Start database
make database

# Start all services (DB + API + Worker + Frontend)
make start-all
```

### What This Does

1. Starts SurrealDB in Docker (port 8000)
2. Starts FastAPI backend (port 5055)
3. Starts background worker (surreal-commands)
4. Starts Next.js frontend (port 3000)

### Individual Services

```bash
# Just the database
make database

# Just the API
make api

# Just the frontend
make frontend

# Just the worker
make worker
```

### Checking Status

```bash
# See what's running
make status

# Stop everything
make stop-all
```

### Advantages
- ✅ Fastest iteration (hot reload)
- ✅ Easy debugging (direct process access)
- ✅ Low resource usage
- ✅ Direct log access

### Disadvantages
- ❌ Doesn't test Docker build
- ❌ Environment may differ from production
- ❌ Requires local Python/Node setup

---

## 2. Docker Compose Development

**Best for:** Testing containerized setup, CI/CD verification

```bash
# Start with dev profile
make dev

# Or full stack
make full
```

### Configuration Files

- `docker-compose.dev.yml` - Development setup
- `docker-compose.full.yml` - Full stack setup
- `docker-compose.yml` - Base configuration

### Advantages
- ✅ Closer to production environment
- ✅ Isolated dependencies
- ✅ Easy to share exact environment

### Disadvantages
- ❌ Slower rebuilds
- ❌ More complex debugging
- ❌ Higher resource usage

---

## 3. Testing Production Docker Images

**Best for:** Verifying Dockerfile changes before publishing

### Build Locally

```bash
# Build production image for your platform only
make docker-build-local
```

This creates two tags:
- `lfnovo/open_notebook:<version>` (from pyproject.toml)
- `lfnovo/open_notebook:local`

### Run Locally

```bash
docker run -p 5055:5055 -p 3000:3000 lfnovo/open_notebook:local
```

### When to Use
- ✅ Before pushing to registry
- ✅ Testing Dockerfile changes
- ✅ Debugging production-specific issues
- ✅ Verifying build process

---

## 4. Publishing Docker Images

### Workflow

```bash
# 1. Test locally first
make docker-build-local

# 2. If successful, push version tag (no latest update)
make docker-push

# 3. Test the pushed version in staging/production

# 4. When ready, promote to latest
make docker-push-latest
```

### Available Commands

| Command | What It Does | Updates Latest? |
|---------|--------------|-----------------|
| `make docker-build-local` | Build for current platform only | No registry push |
| `make docker-push` | Push version tags to registries | ❌ No |
| `make docker-push-latest` | Push version + update v1-latest | ✅ Yes |
| `make docker-release` | Full release (same as docker-push-latest) | ✅ Yes |

### Publishing Details

- **Platforms:** `linux/amd64`, `linux/arm64`
- **Registries:** Docker Hub + GitHub Container Registry
- **Image Variants:** Regular + Single-container (`-single`)
- **Version Source:** `pyproject.toml`

### Creating Git Tags

```bash
# Create and push git tag matching pyproject.toml version
make tag
```

---

## Code Quality

```bash
# Run linter with auto-fix
make ruff

# Run type checking
make lint

# Run tests
uv run pytest tests/

# Clean cache directories
make clean-cache
```

---

## Common Development Tasks

### Adding a New Feature

1. Create feature branch
2. Develop using `make start-all`
3. Write tests
4. Run `make ruff` and `make lint`
5. Test with `make docker-build-local`
6. Create PR

### Fixing a Bug

1. Reproduce locally with `make start-all`
2. Add test case demonstrating bug
3. Fix the bug
4. Verify test passes
5. Check with `make docker-build-local`

### Updating Dependencies

```bash
# Add Python dependency
uv add package-name

# Update dependencies
uv sync

# Frontend dependencies
cd frontend && npm install package-name
```

### Adding a New Language (i18n)

Open Notebook supports internationalization. To add a new language:

1. **Create locale file**: Copy an existing locale as template
   ```bash
   cp frontend/src/lib/locales/en-US/index.ts frontend/src/lib/locales/pt-BR/index.ts
   ```

2. **Translate all strings** in the new file. The structure includes:
   - `common`: Shared UI elements (buttons, labels)
   - `notebooks`, `sources`, `notes`: Feature-specific strings
   - `chat`, `search`, `podcasts`: Module-specific strings
   - `apiErrors`: Error message translations

3. **Register the locale** in `frontend/src/lib/locales/index.ts`:
   ```typescript
   import { ptBR } from './pt-BR'

   export const locales = {
     'en-US': enUS,
     'zh-CN': zhCN,
     'zh-TW': zhTW,
     'pt-BR': ptBR,  // Add your locale
   }
   ```

4. **Add date-fns locale** in `frontend/src/lib/utils/date-locale.ts`:
   ```typescript
   import { zhCN, enUS, zhTW, ptBR } from 'date-fns/locale'

   const LOCALE_MAP: Record<string, Locale> = {
     'zh-CN': zhCN,
     'zh-TW': zhTW,
     'en-US': enUS,
     'pt-BR': ptBR,  // Add your locale
   }
   ```

5. **Test**: Switch languages using the language toggle in the UI header.

### Database Migrations

Database migrations run **automatically** when the API starts.

1. Create migration file: `migrations/XXX_description.surql`
2. Write SurrealQL schema changes
3. (Optional) Create rollback: `migrations/XXX_description_down.surql`
4. Restart API - migration runs on startup

---

## Troubleshooting

### Services Won't Start

```bash
# Check status
make status

# Check database
docker compose ps surrealdb

# View logs
docker compose logs surrealdb

# Restart everything
make stop-all
make start-all
```

### Port Already in Use

```bash
# Find process using port
lsof -i :5055
lsof -i :3000
lsof -i :8000

# Kill stuck processes
make stop-all
```

### Database Connection Issues

```bash
# Verify SurrealDB is running
docker compose ps surrealdb

# Check connection settings in .env
cat .env | grep SURREAL
```

### Docker Build Fails

```bash
# Clean Docker cache
docker builder prune

# Reset buildx
make docker-buildx-reset

# Try local build first
make docker-build-local
```

---

## Project Structure

```
open-notebook/
├── api/                    # FastAPI backend
├── frontend/               # Next.js React frontend
├── open_notebook/          # Python core library
│   ├── domain/            # Domain models
│   ├── graphs/            # LangGraph workflows
│   ├── ai/                # AI provider integration
│   └── database/          # SurrealDB operations
├── migrations/             # Database migrations
├── tests/                  # Test suite
├── docs/                   # User documentation
└── Makefile               # Development commands
```

See component-specific CLAUDE.md files for detailed architecture:
- [frontend/CLAUDE.md](frontend/CLAUDE.md)
- [api/CLAUDE.md](api/CLAUDE.md)
- [open_notebook/CLAUDE.md](open_notebook/CLAUDE.md)

---

## Environment Variables

### Required for Local Development

```bash
# .env file
SURREAL_URL=ws://localhost:8000
SURREAL_USER=root
SURREAL_PASS=root
SURREAL_DB=open_notebook
SURREAL_NS=production

# AI Provider (at least one required)
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...
# OR configure other providers (see docs/5-CONFIGURATION/)
```

See [docs/5-CONFIGURATION/](docs/5-CONFIGURATION/) for complete configuration guide.

---

## Performance Tips

### Speed Up Local Development

1. **Use `make start-all`** instead of Docker for daily work
2. **Keep SurrealDB running** between sessions (`make database`)
3. **Use `make docker-build-local`** only when testing Dockerfile changes
4. **Skip multi-platform builds** until ready to publish

### Reduce Resource Usage

```bash
# Stop unused services
make stop-all

# Clean up Docker
docker system prune -a

# Clean Python cache
make clean-cache
```

---

## TODO: Sections to Add

- [ ] Frontend development guide (hot reload, component structure)
- [ ] API development guide (adding endpoints, services)
- [ ] LangGraph workflow development
- [ ] Testing strategy and coverage
- [ ] Debugging tips (VSCode/PyCharm setup)
- [ ] CI/CD pipeline overview
- [ ] Release process checklist
- [ ] Common error messages and solutions

---

## Resources

- **Documentation:** https://open-notebook.ai
- **Discord:** https://discord.gg/37XJPXfz2w
- **Issues:** https://github.com/lfnovo/open-notebook/issues
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Maintainer Guide:** [MAINTAINER_GUIDE.md](MAINTAINER_GUIDE.md)

---

**Last Updated:** January 2025

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
