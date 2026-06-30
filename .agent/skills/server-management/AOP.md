# AOP: Server & Process Playbook [v15.0]

## 🏗️ RUNTIME STABILITY & PROCESSES
**Vitality is the Primary Structural Property of Execution.**

### 🚦 PM2 Lifecycle Management [CRITICAL]
- **Cluster Mode**: Enable `instances: 'max'` for load-balanced production scaling.
- **Restart Policy**: Use `exp_backoff_restart_delay` to prevent rapid failure loops.
- **Auto-Reload**: Only use `watch: true` in `dev`. Never in `stage/prod`.
- **Termination**: Use `stop_timeout` to allow graceful connection closing (Draining).

### 🚦 Resource & Monitoring [CRITICAL]
- **CPU Threshold**: Alert on >80% sustained usage.
- **Memory Limit**: Mandate `max_memory_restart` to prevent system-wide lockups.
- **Logs**: Mandate `rotate-logs` to prevent disk exhaustion.

### 🛡️ ENVIRONMENT & VAULTING [HIGH]
- **Isolation**: Use `ecosystem.config.js` to strictly separate `development` and `production` vars.
- **Secrets**: PROHIBITED: Hardcoded secrets in config files. Use environment injection from a secure vault.
- **Health Checks**: Mandate a `/health` endpoint that checks DB connectivity and critical service status.

---

## 🏰 DECOMPOSITION PROTOCOL (PROCESS PRE-WORK)
**Before any deployment or runtime change, perform this scan:**
```
UI/TASK: [Deploy/Change Task]
├── INSTANCES: [Is cluster mode required?] (Scaling check)
├── SECRETS: [Are env vars injected from vault?] (Security check)
├── LIMITS: [Is max_memory_restart set?] (Stability check)
└── HEALTH: [Is the /health endpoint updated?] (Uptime check)
```

---

## 📜 STABILITY STANDARDS (MANDATORY)
1. **Draining**: Always allow 30s-60s for connections to close before hard process termination.
2. **Backoff**: Never restart a failing process more than 10 times consecutively without a delay increase.
3. **Immutability**: Once deployed, the environment configuration must be immutable.

---
**Protocol**: "Vitality is the foundation of the Sovereign. Trust the process state."
