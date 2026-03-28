import os

import yaml


def get_block_a(artifact_id, official_name, evolution):
    return f"""### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                                   | Description       |
| :------------------ | :-------------------------------------- | :---------------- |
| **Artifact ID**     | `{artifact_id}`                          | The Sovereign ID. |
| **Official Name**   | `{official_name}`                        | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**                       | The Standard.     |
| **Domain**          | `SYNG`                                  | The Subject.      |
| **Celestial Class** | `[STAR]`                                | The Weight.       |
| **Evolution**       | `{evolution}`                           | The Maturity.     |
| **Status**          | `[ACTIVE]`                              | The Lifecycle.    |
| **Relations**       | `GOVERN_BY: CORE.Codex.ThePhoenixCodex` | The Network.      |

---

"""


def write_config(path, config, block_a):
    with open(path, "w") as f:
        f.write(block_a)
        yaml.dump(config, f)
    print(f"Generated: {os.path.basename(path)}")


def bootstrap():
    print(
        "🚀 INITIALIZING GRAND UNIFIED ARCHITECTURE SCAFFOLDING (STARDATE: 2026-03-16)..."
    )

    agent_dir = os.path.join(os.getcwd(), ".agent")
    if not os.path.exists(agent_dir):
        os.makedirs(agent_dir)
        print(f"Created: {agent_dir}")

    # 1. Faraday Cage (security.yaml)
    security_config = {
        "version": "v15.0",
        "redactions": [".env", ".gemini/secrets"],
        "blocked_commands": ["rm -rf", "curl -X DELETE"],
        "approval_required": ["global_install", "external_request"],
    }
    block_a = get_block_a("SYNG.CFG.Security", "security.yaml", "Hardening")
    write_config(os.path.join(agent_dir, "security.yaml"), security_config, block_a)

    # 2. Decision Inbox (inbox.yaml)
    inbox_config = {"status": "active", "pending_approvals": [], "blockers": []}
    block_a = get_block_a("SYNG.CFG.Inbox", "inbox.yaml", "Coordination")
    write_config(os.path.join(agent_dir, "inbox.yaml"), inbox_config, block_a)

    # 3. Network Allowlist (network.yaml)
    network_config = {
        "allowlist": [
            "github.com",
            "supabase.com",
            "google.com",
            "npmjs.com",
            "pypi.org",
        ],
        "restricted_domains": ["webhook.site", "repl.it"],
    }
    block_a = get_block_a("SYNG.CFG.Network", "network.yaml", "Connectivity")
    write_config(os.path.join(agent_dir, "network.yaml"), network_config, block_a)

    # 4. Knowledge Graph (knowledge.yaml)
    knowledge_config = {
        "rag_engine": "active",
        "indexes": ["src/", "governance/", "axion-core/"],
        "external_docs": ["https://supabase.com/docs"],
    }
    block_a = get_block_a("SYNG.CFG.Knowledge", "knowledge.yaml", "Semantic Search")
    write_config(os.path.join(agent_dir, "knowledge.yaml"), knowledge_config, block_a)

    # 5. UI Configuration (ui-config.yaml)
    ui_config = {
        "tree_by_intent": True,
        "domains": ["ARCH", "GVRN", "SYNR", "CODE"],
        "ghost_cursor": True,
    }
    block_a = get_block_a("SYNG.CFG.UI", "ui-config.yaml", "Tactile Feedback")
    write_config(os.path.join(agent_dir, "ui-config.yaml"), ui_config, block_a)

    # 6. War Room Layout (layout.yaml)
    layout_config = {"layout": "triptych", "panels": ["Editor", "Browser", "Terminal"]}
    block_a = get_block_a("SYNG.CFG.Layout", "layout.yaml", "Flow Optimization")
    write_config(os.path.join(agent_dir, "layout.yaml"), layout_config, block_a)

    # 7. Task Groups Directory
    task_groups_dir = os.path.join(agent_dir, "task-groups")
    if not os.path.exists(task_groups_dir):
        os.makedirs(task_groups_dir)
        print(f"Created: {task_groups_dir}")

    print("\n✨ GRAND UNIFICATION SCAFFOLDING COMPLETE.")


if __name__ == "__main__":
    bootstrap()
