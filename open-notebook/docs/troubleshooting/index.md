---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `INDEX` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# index.md

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-02** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

### **Block A: The Identification Lock (UIP-V13)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `GVRN-INDEX-001`              | The Sovereign ID. |
| **Official Name**   | `index.md`                    | The Filename.     |
| **Version**         | **v13.1 [OMEGA]**             | The Standard.     |
| **Domain**          | `GVRN`                        | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Omega Ascension`             | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |

# Troubleshooting Guide

Welcome to the Open Notebook troubleshooting guide. This section provides comprehensive solutions for common issues, debugging techniques, and best practices for getting the most out of your Open Notebook installation.

## 📋 Quick Navigation

### 🔧 Common Issues

- [Installation Problems](./common-issues.md#installation-problems)
- [Runtime Errors](./common-issues.md#runtime-errors)
- [Performance Issues](./common-issues.md#performance-issues)
- [Configuration Problems](./common-issues.md#configuration-problems)

### ❓ Frequently Asked Questions

- [General Usage](./faq.md#general-usage)
- [AI Models and Providers](./faq.md#ai-models-and-providers)
- [Data Management](./faq.md#data-management)
- [Best Practices](./faq.md#best-practices)

### 🐛 Debugging and Analysis

- [Log Analysis](./debugging.md#log-analysis)
- [Error Diagnosis](./debugging.md#error-diagnosis)
- [Performance Profiling](./debugging.md#performance-profiling)
- [Support Information](./debugging.md#support-information)

## 🚨 Emergency Quick Fixes

### Service Not Starting

```bash
# Check all services
make status

# Restart everything
make stop-all
make start-all
```

### Database Connection Issues

```bash
# Restart database
docker compose restart surrealdb

# Check database logs
docker compose logs surrealdb
```

### API Errors

```bash
# Check API logs
docker compose logs open_notebook

# Restart API only
pkill -f "run_api.py"
make api
```

### Memory Issues

```bash
# Check resource usage
docker stats

# Increase Docker memory limit
# Docker Desktop → Settings → Resources → Memory
```

### Windows & Python 3.14 Specific Issues

**1. "surreal" command not found/recognized:**

- **Cause:** The installer didn't add the binary to your PATH, or the installation failed.
- **Fix:** Open PowerShell as Administrator and run:
  ```powershell
  iwr https://windows.surrealdb.com -useb | iex
  ```
- **Check:** Verify it exists at `C:\Users\Chris\AppData\Local\SurrealDB\surreal.exe`. You may need to use the full path if the command still fails.

**2. RuntimeError: Timeout should be used inside a task:**

- **Cause:** Conflict between `nest_asyncio` and Python 3.14's strict asyncio implementation.
- **Fix:** Comment out `nest_asyncio.apply()` in `app_home.py` and `pages/stream_app/utils.py`.

**3. API Server shuts down immediately / WinError 10061:**

- **Cause:** The `uvicorn` auto-reloader crashes on Windows with Python 3.14.
- **Fix:** Disable auto-reload when starting the API:
  ```powershell
  $env:API_RELOAD="false"; python run_api.py
  ```

## 🔍 First Steps for Any Issue

1. **Check Service Status**

   ```bash
   make status
   ```

2. **Review Recent Logs**

   ```bash
   docker compose logs --tail=50 -f
   ```

3. **Verify Configuration**

   ```bash
   # Check environment variables
   cat .env | grep -v "API_KEY"

   # For Docker
   cat docker.env | grep -v "API_KEY"
   ```

4. **Test Basic Connectivity**

   ```bash
   # Database
   curl http://localhost:8000/health

   # API
   curl http://localhost:5055/health

   # UI
   curl http://localhost:8502/healthz
   ```

## 📞 Getting Help

### Community Support

- **Discord**: [https://discord.gg/37XJPXfz2w](https://discord.gg/37XJPXfz2w)
- **GitHub Issues**: [https://github.com/lfnovo/open-notebook/issues](https://github.com/lfnovo/open-notebook/issues)
- **Installation Assistant**: [ChatGPT Assistant](https://chatgpt.com/g/g-68776e2765b48191bd1bae3f30212631-open-notebook-installation-assistant)

### Before Asking for Help

1. Check this troubleshooting guide
2. Search existing GitHub issues
3. Collect relevant logs and error messages
4. Note your installation method and environment
5. Include steps to reproduce the issue

### Information to Include

- Installation method (Docker/source)
- Operating system and version
- Error messages and logs
- Configuration (without API keys)
- Steps to reproduce the issue

## 🛠️ Advanced Troubleshooting

For complex issues that aren't covered in the basic guides:

1. **Enable Debug Logging**

   ```bash
   # Add to .env or docker.env
   LOG_LEVEL=DEBUG
   ```

2. **Use Development Mode**

   ```bash
   # For more detailed error information
   make dev
   ```

3. **Check System Resources**

   ```bash
   # Monitor resource usage
   htop
   docker stats
   ```

4. **Test Individual Components**

   ```bash
   # Test database connection
   uv run python -c "from open_notebook.database.repository import repo_query; import asyncio; print(asyncio.run(repo_query('SELECT * FROM system')))"

   # Test AI providers
   uv run python -c "from esperanto import AIFactory; model = AIFactory.create_language('openai', 'gpt-4o-mini'); print(model.chat_complete([{'role': 'user', 'content': 'Hello'}]))"
   ```

## 📚 Related Documentation

- [Installation Guide](../getting-started/installation.md)
- [Docker Deployment](../deployment/docker.md)
- [Architecture Overview](../development/architecture.md)
- [API Reference](../development/api-reference.md)

---

_This troubleshooting guide is continuously updated based on user feedback and common issues. If you encounter a problem not covered here, please contribute by opening an issue on GitHub._

### V. RPG Framework Integration (BLK-RPG-001)

- **System Slot:** `Passive Knowledge`
- **Synergy Set:** `N/A`
- **Primary Stat Buff:** `Adaptability`
- **Passive Ability:** `The Forge's Heart`
- **Cognitive Load Cost:** `Low`
- **XP Award Value:** `50 XP`

---

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
