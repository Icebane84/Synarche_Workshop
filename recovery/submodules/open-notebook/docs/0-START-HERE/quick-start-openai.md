---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `QUICK-START-OPENAI` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# quick-start-openai.md
> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-02** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN-QUICK-START-OPENAI-001` | The Sovereign ID. |
| **Official Name** | `quick-start-openai.md` | The Filename.     |
| **Version**       | **v13.1 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |






---

## Step 2: Start Services (1 min)

Open terminal in your `open-notebook` folder:

```bash
docker compose up -d
```

Wait 15-20 seconds for services to start.

---

## Step 3: Access Open Notebook (instant)

Open your browser:
```
http://localhost:8502
```

You should see the Open Notebook interface!

---

## Step 4: Create Your First Notebook (1 min)

1. Click **New Notebook**
2. Name: "My Research"
3. Click **Create**

---

## Step 5: Add a Source (1 min)

1. Click **Add Source**
2. Choose **Web Link**
3. Paste: `https://en.wikipedia.org/wiki/Artificial_intelligence`
4. Click **Add**
5. Wait for processing (30-60 seconds)

---

## Step 6: Chat With Your Content (1 min)

1. Go to **Chat**
2. Type: "What is artificial intelligence?"
3. Click **Send**
4. Watch as GPT responds with information from your source!

---

## Verification Checklist

- [ ] Docker is running
- [ ] You can access `http://localhost:8502`
- [ ] You created a notebook
- [ ] You added a source
- [ ] Chat works

**All checked?** 🎉 You have a fully working AI research assistant!

---

## Using Different Models

In your notebook, go to **Settings** → **Models** to choose:
- `gpt-4o` - Best quality (recommended)
- `gpt-4o-mini` - Fast and cheap (good for testing)

---

## Troubleshooting

### "Port 8502 already in use"

Change the port in docker-compose.yml:
```yaml
ports:
  - "8503:8502"  # Use 8503 instead
```

Then access at `http://localhost:8503`

### "API key not working"

1. Double-check your API key (no extra spaces)
2. Verify you added credits at https://platform.openai.com
3. Restart: `docker compose restart api`

### "Cannot connect to server"

```bash
docker ps  # Check all services running
docker compose logs  # View logs
docker compose restart  # Restart everything
```

---

## Next Steps

1. **Add Your Own Content**: PDFs, web links, documents
2. **Explore Features**: Podcasts, transformations, search
3. **Full Documentation**: [See all features](../3-USER-GUIDE/index.md)

---

## Cost Estimate

OpenAI pricing (approximate):
- **Conversation**: $0.01-0.10 per 1K tokens
- **Embeddings**: $0.02 per 1M tokens
- **Typical usage**: $1-5/month for light use, $20-50/month for heavy use

Check https://openai.com/pricing for current rates.

---

**Need help?** Join our [Discord community](https://discord.gg/37XJPXfz2w)!

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
