# Antigravity Kit Architecture

> Comprehensive AI Agent Capability Expansion Toolkit (OMEGA v15.0 Compliant)

---

I. ## 📋 Overview

---

Antigravity Kit is a modular agentic platform consisting of:

- **20 Specialist Agents** (+ 3 Core Agents: Axion, Sophia, and Sentinel)
- **23 Custom Skills** - Domain-specific capability modules
- **13 Workflows** - Slash command procedures (Markdown playbooks)
- **6 Master Scripts** - Validation and orchestration bin-scripts

---

II. ## 🏗️ Directory Structure

---

```plaintext
.agent/
├── ARCHITECTURE.md          # This file (The Overplane Fusion Blueprint)
├── mcp_config.json          # MCP Tool configurations
├── README.md                # General Agent Kit Documentation
├── GVRN.Style.Coding.md     # The Sovereign Style Guide (Supreme Law)
├── skills/                  # 23 Custom capability modules
├── workflows/               # 13 Slash command procedures
├── .shared/                 # Shared assets and configuration states
└── substrate/               # The Sovereign Substrate (Implementation Layer)
    ├── agents/              # 23 Agent profiles (Specialist & Core)
    ├── bin/                 # 6 Master validation scripts
    ├── governance/          # Substrate-level protocols
    ├── ide/                 # IDE and Tool configurations
    └── rules/
        ├── GEMINI.md        # Sovereign Rules (Master Standards)
        └── GVRN.Ability.Map.md
```

---

III. ## 🤖 Agents (23)

---

Specialist and Core AI personas stratified into the sovereign substrate. Actual Path: `.agent/substrate/agents/`

### Core Sovereign Agents
- `axion` — The Master Artificer (High Gate Executor).
- `sophia` — The Wisdom Anchor (Systemic Balance).
- `sentinel` — The Compliance Auditor (Zero Entropy Enforcer).

### Specialist Agents (20)
| Agent                    | Focus                           | Primary Substrate Alignment |
| ------------------------ | ------------------------------- | --------------------------- |
| `orchestrator`           | Multi-agent coordination        | parallel-agents, behavioral |
| `project-planner`        | Discovery, task planning        | brainstorming, planning     |
| `frontend-specialist`    | Web UI/UX                       | design, code-standards      |
| `backend-specialist`     | API, business logic             | dev, code-standards         |
| `database-architect`     | Schema, SQL                     | supabase-transmuter, infra  |
| `mobile-developer`       | iOS, Android, RN                | design, code-standards      |
| `game-developer`         | Game logic, mechanics           | dev, design                 |
| `devops-engineer`        | CI/CD, Docker                   | infra, qa                   |
| `security-auditor`       | Security compliance             | security, compliance_audit  |
| `penetration-tester`     | Offensive security              | security                    |
| `test-engineer`          | Testing strategies              | qa, NOVA.Sys.TDD            |
| `debugger`               | Root cause analysis             | qa, dev                     |
| `performance-optimizer`  | Speed, Web Vitals               | dev, infra                  |
| `seo-specialist`         | Ranking, visibility             | lang, documentation         |
| `documentation-writer`   | Manuals, docs                   | documentation-alignment     |
| `product-manager`        | Requirements, user stories      | planning, brainstorming     |
| `product-owner`          | Strategy, backlog, MVP          | planning, brainstorming     |
| `qa-automation-engineer` | E2E testing, CI pipelines       | qa, NOVA.Sys.TDD            |
| `code-archaeologist`     | Legacy code, refactoring        | NOVA.Patt.CleanCode         |
| `explorer-agent`         | Codebase analysis               | dev                         |

---

IV. ## 🧩 Skills (23)

---

Modular knowledge domains that agents load on-demand based on task context. Actual Path: `.agent/skills/`

### Core Methodology & Standards
| Skill | Description | Status |
| :--- | :--- | :--- |
| `NOVA.Patt.CleanCode` | Pragmatic standards for Zero-Entropy code production. | **CANONIZED** |
| `NOVA.Sys.TDD` | Test-Driven Development principles and A/B/C cycles. | **CANONIZED** |
| `canonization` | Formally seal workspace artifacts as immutable nodes. | **CANONIZED** |
| `compliance_audit` | Verify workspace compliance with OMEGA/v13.0+ standards. | **CANONIZED** |
| `sentinel-audit` | compliance enforcement, linting, and entropy verification. | **CANONIZED** |
| `soul-forging` | Protocols defining agent core identity and ethics. | **CANONIZED** |
| `zero-entropy-maintenance` | Calculate technical debt mass and remove stale logic. | **CANONIZED** |

### Workspace & Registry Intelligence
| Skill | Description | Status |
| :--- | :--- | :--- |
| `uam` | Unified Architecture Management (UIP-V15 compliance). | **CANONIZED** |
| `detect-synergies` | Compute Graph Synergy Score (GSS) and weave links. | **CANONIZED** |
| `synergistic-opportunity-weaving` | Automate bidirectional link weaving. | **CANONIZED** |
| `systemic-resonance-alignment` | Cosine similarity semantic alignment of docs vs. logic. | **CANONIZED** |
| `magician-ingest` | Transmute raw directories and web assets into knowledge. | **CANONIZED** |
| `supabase-transmuter` | Database read/write and synchronization interface. | **CANONIZED** |

### Functional Operations
| Skill | Description | Status |
| :--- | :--- | :--- |
| `core` | Core runtime setup and orchestrator extension. | UNREGISTERED |
| `design` | System architecture design patterns. | UNREGISTERED |
| `dev` | Development and code production guidelines. | UNREGISTERED |
| `infra` | Infrastructure configuration and controls. | UNREGISTERED |
| `lang` | Language mapping and translations. | UNREGISTERED |
| `qa` | Testing, quality assurance, and mock setups. | UNREGISTERED |
| `security` | Attack surface analysis and vulnerability rules. | UNREGISTERED |
| `documentation-alignment` | Documentation coherence and formatting standard. | **CANONIZED** |
| `hello_world` | Validation module for verifying the active skill system. | **CANONIZED** |

---

V. ## 🔄 Workflows (13)

---

Slash command procedures. Invoke in the chat UI via `/command`. Actual Path: `.agent/workflows/`

| Command | Description | File |
| :--- | :--- | :--- |
| `/audit` | Triggers the Sentinel Suite to run compliance audits. | [audit.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/audit.md) |
| `/canonize` | Formally seals and hashes workspace artifacts to CANONIZED. | [canonize.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/canonize.md) |
| `/create` | Scaffolds a new application (starts interactive dialogue). | [create.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/create.md) |
| `/debug` | Activates DEBUG mode for systematic root-cause analysis. | [debug.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/debug.md) |
| `/enhance` | Add or update features iteratively in an existing application. | [enhance.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/enhance.md) |
| `/game_creation` | Special subagent orchestration to design and build games. | [game_creation.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/game_creation.md) |
| `/migrate_tasks` | Executes the Task Store Sovereignty Migration. | [migrate_tasks.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/migrate_tasks.md) |
| `/plan` | Generate structural project plans using the project-planner. | [plan.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/plan.md) |
| `/scaffold` | Scaffolds a new Synarche Agent using the LangGraph template. | [scaffold.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/scaffold.md) |
| `/simulate` | Runs the Systemic Impact Simulation engine. | [simulate.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/simulate.md) |
| `/status` | Displays progress boards and tracks goals. | [status.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/status.md) |
| `/tdd_cycle` | Executes the Agent A/B/C Triple-Pass TDD loop. | [tdd_cycle.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/tdd_cycle.md) |
| `/test` | Executes test runner and writes unit/integration tests. | [test.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/test.md) |

---

VI. ## 📜 Scripts (6)

---

Master validation scripts that orchestrate capability and audit checks. Actual Path: `.agent/substrate/bin/`

| Script | Purpose | Execution |
| :--- | :--- | :--- |
| `checklist.py` | Priority-based validation (security, types, tests). | `python .agent/substrate/bin/checklist.py .` |
| `verify_all.py` | Full validation suite (checklist + E2E + performance). | `python .agent/substrate/bin/verify_all.py .` |
| `session_manager.py` | Persistent workspace context and memory tracking. | `python .agent/substrate/bin/session_manager.py` |
| `auto_preview.py` | Real-time state visualization and UI previews. | `python .agent/substrate/bin/auto_preview.py` |
| `refresh_registry.py` | Synchronize workspace file indices with registry keys. | `python .agent/substrate/bin/refresh_registry.py` |
| `update_nav_hubs.py` | Maintain dynamic markdown navigation maps. | `python .agent/substrate/bin/update_nav_hubs.py` |

> Note: Centralized metadata control is managed by `loom.py` and `reforge.py` located in the `axion-core/forge/` directory.

---

VII. ## 📊 Statistics

---

| Metric | Count | Details |
| :--- | :--- | :--- |
| **Total Agents** | 23 | 20 Specialist + 3 Core Substrate Profiles |
| **Total Skills** | 23 | Custom OMEGA knowledge packages |
| **Total Workflows** | 13 | Playbooks for slash command actions |
| **Total Binaries** | 6 | Python scripts inside `substrate/bin/` |
| **Registry Size** | 4,666 | Fully aligned workspace artifacts |

---

VIII. ## 🔗 Quick Reference

---

| Need | Agent Profile | Associated Primary Skills |
| :--- | :--- | :--- |
| Refactor | `code-archaeologist` | NOVA.Patt.CleanCode, zero-entropy-maintenance |
| Test Cycles | `test-engineer` | NOVA.Sys.TDD, qa |
| Database Sync | `database-architect` | supabase-transmuter, infra |
| Compliance Audit | `sentinel` | compliance_audit, sentinel-audit, uam |
| Weave & Synergy | `sophia` | detect-synergies, synergistic-opportunity-weaving |
| General Reforging | `axion` | reforge, soul-forging |
