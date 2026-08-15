---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `QUICK-START-CLOUD` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# quick-start-cloud.md

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-02** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                         | Description       |
| :---------------- | :---------------------------- | :---------------- |
| **Artifact ID**   | `GVRN-QUICK-START-CLOUD-001`  | The Sovereign ID. |
| **Official Name** | `quick-start-cloud.md`        | The Filename.     |
| **Version**       | **v13.1 [OMEGA]**             | The Standard.     |
| **Domain**        | `GVRN`                        | The Subject.      |
| **Status**        | `[ACTIVE]`                    | The Lifecycle.    |
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

## Step 4: Configure Your Model (1 min)

1. Go to **Settings** (gear icon)
2. Navigate to **Models**
3. Select your provider's model:

| Provider       | Recommended Model             | Notes                  |
| -------------- | ----------------------------- | ---------------------- |
| **OpenRouter** | `anthropic/claude-3.5-sonnet` | Access 100+ models     |
| **Anthropic**  | `claude-3-5-sonnet-latest`    | Best reasoning         |
| **Google**     | `gemini-2.0-flash`            | Large context, fast    |
| **Groq**       | `llama-3.3-70b-versatile`     | Ultra-fast             |
| **Mistral**    | `mistral-large-latest`        | Strong European option |

4. Click **Save**

---

## Step 5: Create Your First Notebook (1 min)

1. Click **New Notebook**
2. Name: "My Research"
3. Click **Create**

---

## Step 6: Add Content & Chat (2 min)

1. Click **Add Source**
2. Choose **Web Link**
3. Paste any article URL
4. Wait for processing
5. Go to **Chat** and ask questions!

---

## Verification Checklist

- [ ] Docker is running
- [ ] You can access `http://localhost:8502`
- [ ] Models are configured for your provider
- [ ] You created a notebook
- [ ] Chat works

**All checked?** You're ready to research!

---

## Provider Comparison

| Provider       | Speed      | Quality   | Context | Cost                 |
| -------------- | ---------- | --------- | ------- | -------------------- |
| **OpenRouter** | Varies     | Varies    | Varies  | Varies (100+ models) |
| **Anthropic**  | Medium     | Excellent | 200K    | $$$                  |
| **Google**     | Fast       | Very Good | 1M+     | $$                   |
| **Groq**       | Ultra-fast | Good      | 128K    | $ (free tier)        |
| **Mistral**    | Fast       | Good      | 128K    | $$                   |
| **DeepSeek**   | Medium     | Very Good | 64K     | $                    |

---

## Using Multiple Providers

You can enable multiple providers simultaneously:

```yaml
environment:
  - OPENROUTER_API_KEY=sk-or-...
  - ANTHROPIC_API_KEY=sk-ant-...
  - GOOGLE_API_KEY=...
  - GROQ_API_KEY=gsk_...
```

Then switch between them in **Settings** > **Models** as needed.

---

## Troubleshooting

### "Model not found" Error

1. Verify your API key is correct (no extra spaces)
2. Check you have credits/access for the model
3. Restart: `docker compose restart api`

### "Cannot connect to server"

```bash
docker ps  # Check all services running
docker compose logs  # View logs
docker compose restart  # Restart everything
```

### Provider-Specific Issues

**Anthropic**: Ensure key starts with `sk-ant-`
**Google**: Use AI Studio key, not Cloud Console
**Groq**: Free tier has rate limits; upgrade if needed

---

## Cost Estimates

Approximate costs per 1K tokens:

| Provider           | Input               | Output  |
| ------------------ | ------------------- | ------- |
| Anthropic (Sonnet) | $0.003              | $0.015  |
| Google (Flash)     | $0.0001             | $0.0004 |
| Groq (Llama 70B)   | Free tier available | -       |
| Mistral (Large)    | $0.002              | $0.006  |

Check provider websites for current pricing.

---

## Next Steps

1. **Add Your Content**: PDFs, web links, documents
2. **Explore Features**: Podcasts, transformations, search
3. **Full Documentation**: [See all features](../3-USER-GUIDE/index.md)

---

**Need help?** Join our [Discord community](https://discord.gg/37XJPXfz2w)!

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
