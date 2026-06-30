# GUCA: Server Management Command Registry [v15.0]

## 🛠️ Process & Performance Commands

### 🔍 PM2 Lifecycle
- `/start_process_cluster` - Deploy the server in cluster mode.
  - **Automation**: `pm2 start ecosystem.config.js --env production`
- `/monitor_process_health` - Show real-time CPU/Memory usage.
  - **Automation**: `pm2 monit`
- `/graceful_reload` - Reload processes with zero downtime (draining).
  - **Automation**: `pm2 reload all`

### ⚡ Resource Audits
- `/check_memory_restart` - Verify the `max_memory_restart` setting.
- `/audit_process_logs` - Tail the error log for anomalies.
  - **Automation**: `pm2 logs --err --lines 50`
- `/verify_health_endpoint` - Ping `/health` and verify connectivity status.

### 🛡️ Final Verification
- `/run_runtime_sweep` - Scan all active processes for up-time and stability.
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

### 🚀 Reporting
- `/generate_uptime_report` - Show up-time percentage and restart history.
- `/audit_resource_spikes` - Identify peak CPU/Memory events.

---
**Usage**: Server management commands must be executed within the runtime context. No process is Sovereign without active Monitoring and a verified Restart Policy.
