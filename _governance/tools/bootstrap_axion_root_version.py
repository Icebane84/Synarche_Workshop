import hashlib
import json
import os
from typing import Any, Dict, List

# cspell:ignore npmjs synarchy tofile lineterm modelcontextprotocol

# =============================================================================
# THE AXION SOVEREIGN ARCHITECTURE :: COMPLETE EDITION
# Includes: Core, Governance, Security, UI, MCP, and The Refactor Engine
# =============================================================================

SKILL_PATH = ".agent/skills/supabase-transmuter/skill.md"
ALCHEMY_PATH = ".agent/skills/supabase-transmuter/alchemy.py"
ALCHEMY_COMMAND = f"python {ALCHEMY_PATH}"

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
    SKILL_PATH: f"""
---
name: "supabase-transmuter"
description: "Interface for the Great Refactor. Reads/Writes to Supabase."
tools:
  - name: "scan_legacy"
    command: "{ALCHEMY_COMMAND} fetch"
  - name: "diff_content"
    command: "{ALCHEMY_COMMAND} diff {{old}} {{new}}"
  - name: "commit_transmutation"
    command: "{ALCHEMY_COMMAND} commit {{id}} {{title}} {{content_file}} {{meta_json}}"
---
""",
    # Supabase Alchemy Script (The Python Logic)
    ALCHEMY_PATH: """
import os
import json
import difflib
from datetime import datetime
from typing import Any, Optional

from supabase import Client, create_client

# --- CONFIGURATION ---
URL = os.environ.get("SUPABASE_URL", "")
KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")


def _build_client() -> Optional[Client]:
    if not URL or not KEY or "your-supabase" in KEY.lower():
        return None

    try:
        return create_client(URL, KEY)
    except Exception:
        return None


supabase: Optional[Client] = _build_client()

TARGET_TABLE = "knowledge_base"
HISTORY_TABLE = "knowledge_history"


def fetch_batch(limit: int = 5) -> list[dict[str, Any]]:
    if supabase is None:
        return []

    response = (
        supabase.table(TARGET_TABLE)
        .select("*")
        .not_.contains("metadata", '{"version": "v10.0"}')
        .limit(limit)
        .execute()
    )
    data = getattr(response, "data", None)
    return data if isinstance(data, list) else []


def generate_diff(original: str, new: str) -> str:
    diff = difflib.unified_diff(
        original.splitlines(),
        new.splitlines(),
        fromfile="Legacy",
        tofile="Canonized",
        lineterm="",
    )
    return "\\n".join(diff)


def commit_transmutation(
    id: str, new_content: str, new_title: str, categorization: dict[str, Any]
) -> dict[str, Any]:
    if supabase is None:
        return {"error": "No Connection"}

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
""",
}


def blake3_hash(content: str) -> str:
    """Computes a stable hash for a string content."""
    blake3_impl = getattr(hashlib, "blake3", None)
    if blake3_impl is not None:
        result = blake3_impl(content.encode("utf-8")).hexdigest()
        return str(result)
    return hashlib.blake2b(content.encode("utf-8"), digest_size=32).hexdigest()


def _write_text_file(path: str, content: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def calculate_stcp_version(artifact_id: str, artifacts: Dict[str, Dict[str, Any]], versions: Dict[str, str]) -> str:
    """
    Calculates the STCP version for an artifact based on its content and dependencies.
    This is a direct implementation of the principles in stcp-final-audited-spec.md.
    """
    if artifact_id in versions:
        return versions[artifact_id]

    if artifact_id not in artifacts:
        raise KeyError(f"Missing artifact definition for {artifact_id}")

    artifact = artifacts[artifact_id]

    # Step 1: Resolve dependencies and get their versions recursively.
    # This ensures we build from the bottom of the dependency graph up.
    dep_versions: List[str] = []
    for dep_id in sorted(artifact.get("dependencies", [])):
        dep_version = calculate_stcp_version(dep_id, artifacts, versions)
        dep_versions.append(f"{dep_id}:{dep_version}")

    # Step 2: Calculate M_local (local content hash)
    # This includes the artifact's own content and the content hash of any
    # external code it verifies/uses (the §2.2 fix).
    local_content_parts: List[str] = [f"id:{artifact_id}", f"content:{artifact['content']}"]
    if "target_content_hash" in artifact:
        local_content_parts.append(f"target_content_hash:{artifact['target_content_hash']}")

    m_local = blake3_hash("\n".join(local_content_parts))

    # Step 3: Final hash combines M_local with sorted dependency versions.
    # This ensures that any change in a dependency propagates up the chain.
    final_hash_input = [m_local] + dep_versions
    version = blake3_hash("\n".join(final_hash_input))

    versions[artifact_id] = version
    return version


def forge_system(artifacts: Dict[str, Dict[str, Any]]) -> None:
    """
    The new bootstrap function, acting as a Constitutional Forge.
    It calculates verifiable versions for all artifacts before writing them.
    """
    print("🔥 Initiating Constitutional Forge: Applying STCP and Phoenix Codex...")

    # --- Pre-computation Step: Calculate content hashes for external code ---
    # This implements the critical §2.2 fix from the STCP spec.
    alchemy_py_content = artifacts[ALCHEMY_PATH]["content"]
    artifacts[SKILL_PATH]["target_content_hash"] = blake3_hash(alchemy_py_content)

    # --- STCP Hashing Step: Calculate all artifact versions ---
    versions: Dict[str, str] = {}
    sorted_artifacts = sorted(artifacts.keys())  # Process in a deterministic order
    for artifact_id in sorted_artifacts:
        calculate_stcp_version(artifact_id, artifacts, versions)

    print("✅ STCP Hashing Complete. All artifact versions are verified.")

    # --- Manifest Generation & File Writing ---
    nodes: List[Dict[str, Any]] = []
    manifest: Dict[str, Any] = {
        "graph_id": "axion-prime-genesis-v1.0",
        "codex_version": "Phoenix Codex v17.0",
        "stcp_version": "6.3",
        "nodes": nodes,
    }

    for path, version in versions.items():
        artifact_data = artifacts[path]
        content = artifact_data["content"]

        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"   📂 Created directory: {directory}")

        _write_text_file(path, content)
        print(f"   ✨ Forged Artifact: {path} (Version: {version[:12]})")

        nodes.append({"id": path, "version": version, "dependencies": artifact_data.get("dependencies", [])})

    _write_text_file(".agent/manifest.json", json.dumps(manifest, indent=2))
    print("   ✨ Forged Manifest: .agent/manifest.json")

    print("\n[PHOENIX PROTOCOL ENGAGED: SYSTEM STATE IS VERIFIABLE]")
    print("1. Install Dependencies: pip install supabase")
    print("2. Set .env: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY")
    print("3. Restart Antigravity (VS Code).")
    print("4. Verify Axion-Prime is online.")


if __name__ == "__main__":
    # Deconstruct the monolithic dictionary into a graph-ready format
    artifacts_graph = {
        path: {"content": content.strip(), "dependencies": []} for path, content in file_structure.items()
    }

    # Manually define dependencies based on the system's logic
    artifacts_graph[".agent/task-groups/refactor-engine.yaml"]["dependencies"] = [
        SKILL_PATH,
        ".agent/prompts/classification_matrix.md",
    ]
    artifacts_graph[SKILL_PATH]["dependencies"] = [ALCHEMY_PATH]

    forge_system(artifacts_graph)
