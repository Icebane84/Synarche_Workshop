---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `DOCKER-COMPOSE` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# docker-compose.md

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-02** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                         | Description       |
| :---------------- | :---------------------------- | :---------------- |
| **Artifact ID**   | `GVRN-DOCKER-COMPOSE-001`     | The Sovereign ID. |
| **Official Name** | `docker-compose.md`           | The Filename.     |
| **Version**       | **v13.1 [OMEGA]**             | The Standard.     |
| **Domain**        | `GVRN`                        | The Subject.      |
| **Status**        | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |

---

## Step 2: Create Configuration (2 min)

Create a folder `open-notebook` and add this file:

**docker-compose.yml**:

```yaml
services:
  surrealdb:
    image: surrealdb/surrealdb:v2
    command: start --user root --pass password --bind 0.0.0.0:8000 rocksdb:/mydata/mydatabase.db
    ports:
      - "8000:8000"
    volumes:
      - ./surreal_data:/mydata

  open_notebook:
    image: lfnovo/open_notebook:v1-latest
    pull_policy: always
    ports:
      - "8502:8502" # Web UI
      - "5055:5055" # API
    environment:
      # AI Provider (choose ONE)
      - OPENAI_API_KEY=sk-... # Your OpenAI key
      # - ANTHROPIC_API_KEY=sk-ant-...  # Or Anthropic
      # - GOOGLE_API_KEY=...  # Or Google

      # Database
      - SURREAL_URL=ws://surrealdb:8000/rpc
      - SURREAL_USER=root
      - SURREAL_PASSWORD=password
      - SURREAL_NAMESPACE=open_notebook
      - SURREAL_DATABASE=open_notebook
    volumes:
      - ./notebook_data:/app/data
    depends_on:
      - surrealdb
    restart: always
```

**Edit the file:**

- Replace `sk-...` with your actual OpenAI API key
- (Or use Anthropic, Google, Groq keys instead)
- If you have multiple keys, uncomment the ones you want

---

## Step 3: Start Services (2 min)

Open terminal in the `open-notebook` folder:

```bash
docker compose up -d
```

Wait 15-20 seconds for all services to start:

```
✅ surrealdb running on :8000
✅ open_notebook running on :8502 (UI) and :5055 (API)
```

Check status:

```bash
docker compose ps
```

---

## Step 4: Verify Installation (1 min)

**API Health:**

```bash
curl http://localhost:5055/health
# Should return: {"status": "healthy"}
```

**Frontend Access:**
Open browser to:

```
http://localhost:8502
```

You should see the Open Notebook interface!

---

## Step 5: First Notebook (2 min)

1. Click **New Notebook**
2. Name: "My Research"
3. Description: "Getting started"
4. Click **Create**

Done! You now have a fully working Open Notebook instance. 🎉

---

## Configuration

### Using Different AI Providers

Change `environment` section in `docker-compose.yml`:

```yaml
# For Anthropic (Claude)
- ANTHROPIC_API_KEY=sk-ant-...

# For Google Gemini
- GOOGLE_API_KEY=...

# For Groq (fast, free tier available)
- GROQ_API_KEY=...

# For local Ollama docker container (free, offline) --> Virtual machine
- OLLAMA_API_BASE=http://ollama:11434
# For localhost Ollama (free, offline) --> Real machine
# - OLLAMA_API_BASE=http://host.docker.internal:11434
```

### Adding Ollama container (Free Local Models)

Add to `docker-compose.yml`:

```yaml
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    restart: always

volumes:
  surreal_data:
  ollama_models:
```

Then update API service:

```yaml
environment:
  - OLLAMA_API_BASE=http://ollama:11434
```

Restart and pull a model:

```bash
docker compose restart
docker exec open_notebook-ollama-1 ollama pull mistral
```

---

## Environment Variables Reference

| Variable              | Purpose              | Example                   |
| --------------------- | -------------------- | ------------------------- |
| `OPENAI_API_KEY`      | OpenAI API key       | `sk-proj-...`             |
| `ANTHROPIC_API_KEY`   | Anthropic/Claude key | `sk-ant-...`              |
| `SURREAL_URL`         | Database connection  | `ws://surrealdb:8000/rpc` |
| `SURREAL_USER`        | Database user        | `root`                    |
| `SURREAL_PASSWORD`    | Database password    | `password`                |
| `API_URL`             | API external URL     | `http://localhost:5055`   |
| `NEXT_PUBLIC_API_URL` | Frontend API URL     | `http://localhost:5055`   |

---

## Common Tasks

### Stop Services

```bash
docker compose down
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f api
```

### Restart Services

```bash
docker compose restart
```

### Update to Latest Version

```bash
docker compose down
docker compose pull
docker compose up -d
```

### Remove All Data

```bash
docker compose down -v
```

---

## Troubleshooting

### "Cannot connect to API" Error

1. Check if Docker is running:

```bash
docker ps
```

2. Check if services are running:

```bash
docker compose ps
```

3. Check API logs:

```bash
docker compose logs api
```

4. Wait longer - services can take 20-30 seconds to start on first run

---

### Port Already in Use

If you get "Port 8502 already in use", change the port:

```yaml
ports:
  - "8503:8502" # Use 8503 instead
  - "5055:5055" # Keep API port same
```

Then access at `http://localhost:8503`

---

### API Key Not Working

1. Double-check your API key in the file (no extra spaces)
2. Verify key is valid at provider's website
3. Check you added credits to your account
4. Restart: `docker compose restart api`

---

### Database Connection Issues

Check SurrealDB is running:

```bash
docker compose logs surrealdb
```

Reset database:

```bash
docker compose down -v
docker compose up -d
```

---

## Next Steps

1. **Add Content**: Sources, notebooks, documents
2. **Configure Models**: Settings → Models (choose your preferences)
3. **Explore Features**: Chat, search, transformations
4. **Read Guide**: [User Guide](../3-USER-GUIDE/index.md)

---

## Production Deployment

For production use, see:

- [Security Hardening](https://github.com/lfnovo/open-notebook/blob/main/docs/deployment/security.md)
- [Reverse Proxy](https://github.com/lfnovo/open-notebook/blob/main/docs/deployment/reverse-proxy.md)

---

## Getting Help

- **Discord**: [Community support](https://discord.gg/37XJPXfz2w)
- **Issues**: [GitHub Issues](https://github.com/lfnovo/open-notebook/issues)
- **Docs**: [Full documentation](../index.md)

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
