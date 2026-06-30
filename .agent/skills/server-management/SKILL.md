---
name: server-management
description:
    Server management principles and decision-making. Process management, monitoring strategy, and scaling
    decisions. Teaches thinking, not commands.
allowed-tools: Read, Glob, Grep, Bash
---

# Server Management System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Runtime Stability** and **Process Resilience** through **PM2 Lifecycle Management** and **Environment Isolation**. This skill mandates that every process be monitored, clustered, and guarded against failure, ensuring the Sovereignty of the application state.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Process & Lifecycle Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `pm2 monit` - Automated CPU/Memory Audit.
- `scripts/omega_audit.py` - Universal Cluster-Wide Health Check.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. "Monitoring-First" Mandate
**MANDATORY**: No process may run without an active PM2 configuration. Every service must have defined CPU/Memory limits and a restart policy.

### 2. Graceful Connection Draining
**MANDATORY**: All process reloads and restarts must use a graceful draining period (30s minimum) to prevent user request failures.

### 3. Clustering & Scaling
All production instances MUST use PM2 Cluster Mode to utilize multi-core architecture and provide high availability.

### 4. Health Check Verification
Mandate a `/health` endpoint for all servers that verifies database and external service connectivity.

---
"Stability is the foundation of the Sovereign. Process health is its breath."
