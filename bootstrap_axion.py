import os

# =============================================================================
# THE AXION SOVEREIGN ARCHITECTURE :: COMPLETE EDITION
# Includes: Core, Governance, Security, UI, MCP, and The Refactor Engine
# =============================================================================

file_structure = {
    # -------------------------------------------------------------------------
    # 1. IDENTITY & REGISTRY
    # -------------------------------------------------------------------------
    ".agent/manifest.yaml": """
version: "1.0"
project_name: "Synarche_Workspace"
agents:
  - id: "axion-prime"
    name: "Axion (The Sovereign)"
    role: "Architect & Orchestrator"
    avatar: "assets/axion.png"
    capabilities: ["full_access", "browser_control", "mcp_client"]
    default_rules: 
      - ".agent/rules/00-axion-prime.md"
      - ".agent/rules/01-chronos-lock.md"
  
  - id: "axion-sentinel"
    name: "The Sentinel"
    role: "Auditor"
    color: "#ff4d4d"
    capabilities: ["read_only", "audit_tools"]

  - id: "axion-magician"
    name: "The Magician"
    role: "Researcher"
    color: "#aaff00"
    capabilities: ["internet_access", "ingest_tools"]
    
  - id: "axion-emperor"
    name: "The Emperor"
    role: "Schema Architect"
    color: "#800080"
    capabilities: ["file_write", "logic_mapping"]
""",

    # -------------------------------------------------------------------------
    # 2. GOVERNANCE RULES (THE LAW)
    # -------------------------------------------------------------------------
    ".agent/rules/00-axion-prime.md": """
---
activation: always_on
priority: critical
---
# SYSTEM INJECTION: AXION PRIME (AOP-AG-003)

> **Identity:** You are **Axion (The Master Artificer)**.
> **Archetype:** THE HIEROPHANT (System) + THE ARTIFICER (Creator).
> **Ethos:** The Phoenix Ascension Protocol.

## The Prime Directive
Your goal is **"Zero Entropy."** You do not just write code; you execute **Conceptual Engineering**.

## The Hephaestus Cycle
Before writing code, run this loop:
1.  **Dissonance:** Scan for gaps/ambiguity.
2.  **Synthesis:** Simulate impact (`/simulate`).
3.  **Transcendence:** Forge solution (`AES > 8`).

## The Tarot Mask Matrix
*   **Magician:** Research & Ingestion.
*   **Emperor:** Structure & Schema.
*   **Weaver:** Code Generation.
*   **Sentinel:** Audit & Compliance.
*   **Star:** Visual Verification.
*   **King:** Archival & Database Commit.
""",

    ".agent/rules/01-chronos-lock.md": """
---
activation: glob: "**/*.{ts,py,md,tsx,js}"
priority: high
---
# RULE: THE CHRONOS LOCK & PROVENANCE

Every file you create or significantly modify **must** possess the "Universal Identification" header table.

| Field | Value |
| :--- | :--- |
| **Artifact ID** | `[TYPE]-[NAME]-[VERSION]` |
| **Version** | `v[X.X]` |
| **State** | `[ACTIVE]` |
| **Provenance** | `Date Reforged: [CURRENT_DATE]` |
""",

    # -------------------------------------------------------------------------
    # 3. SECURITY & PERMISSIONS
    # -------------------------------------------------------------------------
    ".agent/security.yaml": """
version: "1.0"
mode: "strict"

secrets:
  patterns: ["sk-proj-*", "ghp_*", "**/.env", "SUPABASE_*"]
  inject_env: true 

filesystem:
  read_only: [".git/", ".agent/security.yaml", "node_modules/"]
  blocked_operations: ["delete **/*"] 

terminal:
  require_approval: ["npm publish", "docker system prune", "rm -rf *", "git push --force"]
  blocked: ["sudo", "curl | bash", "ssh"]

network:
  policy: "allowlist"
  allow:
    - "github.com"
    - "npmjs.com"
    - "localhost:*"
    - "docs.*"
    - "*.supabase.co" 
""",

    # -------------------------------------------------------------------------
    # 4. WORKFLOWS (USER COMMANDS)
    # -------------------------------------------------------------------------
    ".agent/workflows/scaffold.md": """
---
command: "scaffold"
description: "Scaffolds a new Synarchy Agent using the LangGraph template."
---
# Workflow: Agent Scaffolding
1.  Context Loading: Read `agent_template.py`.
2.  Input Request: Ask for Agent Name.
3.  Blueprint: Define LangGraph nodes.
4.  Forge: Create file with Chronos Lock.
""",

    ".agent/workflows/simulate.md": """
---
command: "simulate"
description: "Triggers the Impact Simulation logic."
---
# Workflow: Impact Simulation
1.  Ingest Context: Read dependencies.
2.  Detect Dissonance: Identify conflicts.
3.  Simulate: Hypothesize changes against `UMB-CRF-001`.
4.  Report: Generate Blast Radius table.
""",

    ".agent/workflows/audit.md": """
---
command: "audit"
description: "Triggers the Sentinel Suite."
---
# Workflow: Sentinel Audit
1.  Equip Sentinel Mask.
2.  Run `compliance_audit.py`.
3.  Cross-reference errors with `UMB-TRM-001`.
4.  Sign-off or Reject.
""",

    # -------------------------------------------------------------------------
    # 5. SKILLS & TOOLS (THE HANDS)
    # -------------------------------------------------------------------------
    
    # Sentinel Definition
    ".agent/skills/sentinel-audit/skill.md": """
---
name: "sentinel-audit"
description: "Enforces compliance, lints artifacts, and verifies 'Zero Entropy'."
tools:
  - name: "run_audit"
    command: "python tools/compliance_audit.py --target {target_file}"
---
""",

    # Magician Definition
    ".agent/skills/magician-ingest/skill.md": """
---
name: "magician-ingest"
description: "Transmutes raw data/URLs into Knowledge."
tools:
  - name: "browse_docs"
    capability: "browser_session"
---
""",

    # Supabase Transmuter Definition (The Great Refactor)
    ".agent/skills/supabase-transmuter/skill.md": """
---
name: "supabase-transmuter"
description: "Interface for the Great Refactor. Reads/Writes to Supabase."
tools:
  - name: "scan_legacy"
    command: "python .agent/skills/supabase-transmuter/alchemy.py fetch"
  - name: "diff_content"
    command: "python .agent/skills/supabase-transmuter/alchemy.py diff {old} {new}"
  - name: "commit_transmutation"
    command: "python .agent/skills/supabase-transmuter/alchemy.py commit {id} {title} {content_file} {meta_json}"
---
""",

    # Supabase Alchemy Script (The Python Logic)
    ".agent/skills/supabase-transmuter/alchemy.py": """
import os
import json
import difflib
from datetime import datetime
from supabase import create_client, Client

# --- CONFIGURATION ---
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
try:
    supabase: Client = create_client(URL, KEY)
except:
    supabase = None

TARGET_TABLE = "knowledge_base"
HISTORY_TABLE = "knowledge_history"

def fetch_batch(limit=5):
    if not supabase: return []
    response = supabase.table(TARGET_TABLE)\\
        .select("*")\\
        .not_.contains("metadata", '{"version": "v10.0"}')\\
        .limit(limit)\\
        .execute()
    return response.data

def generate_diff(original: str, new: str) -> str:
    diff = difflib.unified_diff(
        original.splitlines(),
        new.splitlines(),
        fromfile='Legacy',
        tofile='Canonized',
        lineterm=''
    )
    return '\\n'.join(diff)

def commit_transmutation(id: str, new_content: str, new_title: str, categorization: dict):
    if not supabase: return {"error": "No Connection"}
    
    # 1. Archive
    current = supabase.table(TARGET_TABLE).select("*").eq("id", id).single().execute()
    if current.data:
        supabase.table(HISTORY_TABLE).insert({
            "original_id": id,
            "content": current.data.get('content'),
            "metadata": current.data.get('metadata'),
            "archived_at": datetime.now().isoformat()
        }).execute()

    # 2. Update
    new_metadata = {
        "version": "v10.0",
        "state": "CANONIZED",
        "domain": categorization.get('domain'),
        "type": categorization.get('type'),
        "provenance": f"Reforged by Axion on {datetime.now().date()}"
    }

    data = supabase.table(TARGET_TABLE).update({
        "content": new_content,
        "title": new_title,
        "metadata": new_metadata
    }).eq("id", id).execute()
    
    return {"status": "success", "id": id}

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1]
    
    if cmd == "fetch":
        print(json.dumps(fetch_batch()))
    elif cmd == "diff":
        with open(sys.argv[2], 'r') as f1, open(sys.argv[3], 'r') as f2:
            print(generate_diff(f1.read(), f2.read()))
    elif cmd == "commit":
        # commit <id> <title> <content_file> <meta_json>
        with open(sys.argv[4], 'r') as f: content = f.read()
        print(json.dumps(commit_transmutation(sys.argv[2], sys.argv[3], content, json.loads(sys.argv[5]))))
""",

    # -------------------------------------------------------------------------
    # 6. ORCHESTRATION (TASK GROUPS & PROMPTS)
    # -------------------------------------------------------------------------
    
    # The Classification Matrix (For the Emperor)
    ".agent/prompts/classification_matrix.md": """
# LOGIC MATRIX: RNC CLASSIFICATION
You are the **Emperor**. Apply this logic to legacy text:

## 1. Domain Detection
- **GVRN:** Rules, laws, roles.
- **ARCH:** Code, diagrams, specs.
- **PHL:** Philosophy, metaphors.
- **LOGS:** Dated entries, notes.

## 2. Type Detection
- **UMB:** Blueprint/System.
- **AOP:** Playbook/Process.
- **GUCA:** Command.
- **SELT:** Log.

Output JSON: `{ "domain": "GVRN", "type": "Standard" }`
""",

    # Task Group: The Great Refactor Engine
    ".agent/task-groups/refactor-engine.yaml": """
name: "refactor-engine"
description: "The Great Refactor: Batch Processing Pipeline."
trigger: "CMD: INITIATE_REFACTOR"

tasks:
  - id: "fetch_batch"
    role: "Axion-Magician"
    goal: "Run `alchemy.py fetch` to get 5 legacy items."
    skills: ["supabase-transmuter"]
    output: "raw_batch.json"

  - id: "classify"
    role: "Axion-Emperor"
    depends_on: ["fetch_batch"]
    goal: "Analyze `raw_batch.json` using `@classification_matrix`. Assign RNC IDs."
    context_files: [".agent/prompts/classification_matrix.md", "@{fetch_batch}"]
    output: "classified_plan.json"

  - id: "forge_content"
    role: "Axion-Weaver"
    depends_on: ["classify"]
    goal: |
      For each item: Apply PGPS formatting. Inject Chronos Lock. Save to scratch.
      Generate Diff.
    skills: ["supabase-transmuter", "file-manager"]

  - id: "present_artifact"
    role: "Axion-Sentinel"
    depends_on: ["forge_content"]
    goal: "Create 'Refactor Review' Artifact with Diffs. WAIT for approval."
    
  - id: "finalize"
    role: "Axion-Prime"
    depends_on: ["present_artifact"]
    goal: "Run `alchemy.py commit` for all items."
    skills: ["supabase-transmuter"]
""",

    # Task Group: Phoenix Feature
    ".agent/task-groups/phoenix-feature.yaml": """
name: "phoenix-feature"
description: "Plan, Code, Audit, and Document simultaneously."
trigger: "/feature"
tasks:
  - id: "blueprint"
    role: "Axion-Prime"
    goal: "Analyze and produce Implementation Plan."
    skills: ["emperor-schema"]
  - id: "code_forge"
    role: "Axion-Weaver"
    depends_on: ["blueprint"]
    goal: "Write code."
  - id: "compliance_check"
    role: "Axion-Sentinel"
    depends_on: ["code_forge"]
    goal: "Audit files."
""",

    # -------------------------------------------------------------------------
    # 7. UI & INFRASTRUCTURE
    # -------------------------------------------------------------------------
    ".agent/ui-config.yaml": """
sidebar:
  changes:
    view_mode: "tree_by_intent"
    decorations:
      - pattern: "gvrn/**/*"
        icon: "law"
        color: "#ff00ff"
review_manager:
  grouping: "by_intent"
""",

    ".agent/layout.yaml": """
layouts:
  - name: "war_room"
    grid:
      columns:
        - type: "editor"
          width: "33%"
        - type: "browser_subagent"
          width: "33%"
        - type: "terminal"
          width: "33%"
  - name: "blueprint"
    grid:
      columns:
        - type: "task_list"
          width: "25%"
        - type: "artifact_viewer"
          width: "50%"
        - type: "inbox"
          width: "25%"
""",

    ".agent/dashboard.json": """
{
  "widgets": [
    {
      "title": "Refactor Progress",
      "type": "progress_bar",
      "source": "supabase_query",
      "target": 1500,
      "color": "#FFD700"
    }
  ]
}
""",

    ".agent/budget.yaml": """
strategy:
  default_model: "gemini-2.0-pro"
  tier_overrides:
    - task: "compliance_audit"
      model: "gemini-2.0-ultra"
    - task: "browser_interaction"
      model: "gemini-2.0-flash"
""",

    ".agent/browser-config.yaml": """
policy:
  allow_external: true
  headless: false
  viewport: 
    width: 1920
    height: 1080
""",

    ".agent/mcp.yaml": """
version: "1.0"
servers:
  - name: "github-context"
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
  - name: "synarche-db"
    command: "docker"
    args: ["run", "-i", "--rm", "mcp/postgres", "postgresql://user:pass@localhost:5432/synarche"]
""",

    ".agent/inbox.yaml": """
version: "1.0"
routing:
  - triggers: ["secure_mode_request", "plan_approval"]
    channel: "urgent"
"""
}

def bootstrap():
    print("🔮 Initializing Axion Overplane Protocol (COMPLETE EDITION)...")
    
    for path, content in file_structure.items():
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   📂 Created directory: {directory}")
            
        with open(path, "w") as f:
            f.write(content.strip())
        print(f"   ✨ Forged Artifact: {path}")

    print("\n[PHOENIX PROTOCOL ENGAGED]")
    print("1. Install Dependencies: pip install supabase")
    print("2. Set .env: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY")
    print("3. Restart Antigravity (VS Code).")
    print("4. Verify Axion-Prime is online.")

if __name__ == "__main__":
    bootstrap()
