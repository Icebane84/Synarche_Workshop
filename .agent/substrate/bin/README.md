## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                       | Description       |
| :---------------- | :-------------------------- | :---------------- |
| **Artifact ID**   | `SYNG.BIN.Master`           | The Sovereign ID. |
| **Official Name** | `README.md`                 | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**           | The Standard.     |
| **Domain**        | `SUBSTRATE`                 | The Subject.      |
| **Status**        | `[ACTIVE]`                  | The Lifecycle.    |
| **Relations**     | `REF: GVRN.Master.Registry` | The Network.      |

---

# ⚡ Master Substrate Binaries (.agent/substrate/bin)

This directory contains the core Python scripts used for workspace maintenance, registry synchronization, and systematic validation.

## 🛠️ Binary Catalog

| Script                | Purpose                                  | Usage                                             |
| :-------------------- | :--------------------------------------- | :------------------------------------------------ |
| `checklist.py`        | Priority-based validation (Core checks). | `python .agent/substrate/bin/checklist.py`        |
| `verify_all.py`       | Comprehensive verification (All checks). | `python .agent/substrate/bin/verify_all.py`       |
| `session_manager.py`  | Persistent context & memory tracking.    | Internal / Automated                              |
| `auto_preview.py`     | Real-time UI/State visualization.        | Internal / Automated                              |
| `refresh_registry.py` | Artifact & Index synchronization.        | `python .agent/substrate/bin/refresh_registry.py` |
| `update_nav_hubs.py`  | Dynamic Navigation Hub maintenance.      | `python .agent/substrate/bin/update_nav_hubs.py`  |

---

`[OMNI-ANCHOR] ID: SYNG.BIN.Master VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-03-20`
