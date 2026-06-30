# Antigravity Kit Architecture

> Comprehensive AI Agent Capability Expansion Toolkit (OMEGA v15.0 Compliant)

---

I. ## 📋 Overview

---

Antigravity Kit is a modular agentic platform consisting of:

- **20 Specialist Agents** (+ 3 Core Agents: Axion, Sophia, and Sentinel)
- **60 Custom Skills** - Combined Developer capability modules (37) & Governance/Integrity modules (23)
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
├── skills/                  # 60 Custom capability modules (Dev & Integrity)
├── workflows/               # 13 Slash command procedures
├── .shared/                 # Shared assets and configuration states
└── substrate/               # The Sovereign Substrate (Implementation Layer)
    ├── agents/              # 23 Agent profiles (Specialist & Core)
    ├── bin/                 # 6 Master validation scripts
    ├── governance/          # Substrate-level protocols
    ├── ide/                 # IDE and Tool configurations
    ├── identity/            # 14 Triad Soul Seeds and Eternal Law profiles
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
| Agent | Focus | Primary Substrate Alignment |
| :--- | :--- | :--- |
| `orchestrator` | Multi-agent coordination | parallel-agents, behavioral-modes |
| `project-planner` | Discovery, task planning | brainstorming, plan-writing |
| `frontend-specialist` | Web UI/UX | frontend-design, nextjs-react-expert, tailwind-patterns |
| `backend-specialist` | API, business logic | api-patterns, nodejs-best-practices, database-design |
| `database-architect` | Schema, SQL | database-design, prisma-expert, supabase-transmuter |
| `mobile-developer` | iOS, Android, RN | mobile-design |
| `game-developer` | Game logic, mechanics | game-development |
| `devops-engineer` | CI/CD, Docker | deployment-procedures, docker-expert |
| `security-auditor` | Security compliance | vulnerability-scanner, red-team-tactics |
| `penetration-tester` | Offensive security | red-team-tactics |
| `test-engineer` | Testing strategies | testing-patterns, tdd-workflow, webapp-testing |
| `debugger` | Root cause analysis | systematic-debugging |
| `performance-optimizer` | Speed, Web Vitals | performance-profiling |
| `seo-specialist` | Ranking, visibility | seo-fundamentals, geo-fundamentals |
| `documentation-writer` | Manuals, docs | documentation-templates |
| `product-manager` | Requirements, user stories | plan-writing, brainstorming |
| `product-owner` | Strategy, backlog, MVP | plan-writing, brainstorming |
| `qa-automation-engineer` | E2E testing, CI pipelines | webapp-testing, testing-patterns |
| `code-archaeologist` | Legacy code, refactoring | clean-code, code-review-checklist |
| `explorer-agent` | Codebase analysis | lint-and-validate |

---

IV. ## 🧩 Skills (60)

---

Modular knowledge domains loaded on-demand by agents. Path: `.agent/skills/`

### 1. Developer Capabilities (37)
| Skill | Category | Description |
| :--- | :--- | :--- |
| `nextjs-react-expert` | Frontend | React & Next.js performance optimizations (Vercel-certified) |
| `web-design-guidelines` | Frontend | Web UI audit rules for UX, performance, and accessibility |
| `tailwind-patterns` | Frontend | Tailwind CSS v4 layout patterns |
| `frontend-design` | Frontend | UI/UX visual systems, grids, and design tokens |
| `api-patterns` | Backend | REST, GraphQL, tRPC, and API design principles |
| `nodejs-best-practices` | Backend | Node.js asynchronous architecture and design patterns |
| `python-patterns` | Backend | Python best practices, standard libraries, and FastAPI |
| `rust-pro` | Backend | Async Rust 1.75+, Tokio, and system development |
| `database-design` | Database | Schema design, indexing, and Postgres optimization |
| `mcp-builder` | Tooling | Model Context Protocol servers and tool schemas |
| `vulnerability-scanner` | Security | Security auditing, OWASP rules, and vulnerability checks |
| `red-team-tactics` | Security | Offensive security and adversary simulations |
| `mobile-design` | Mobile | Mobile-first UI/UX thinking and platform conventions |
| `game-development` | Creative | Game logic, mechanics, and loop structures |
| `seo-fundamentals` | SEO | Technical SEO, Google Web Vitals, and E-E-A-T |
| `geo-fundamentals` | SEO | Generative Engine Optimization patterns |
| `server-management` | Cloud | CI/CD pipelines, Docker, and infrastructure controls |
| `systematic-debugging` | QA | Root cause analysis and evidence-based verification |
| `testing-patterns` | QA | Vitest, Jest, and integration test patterns |
| `webapp-testing` | QA | Playwright E2E automation structures |
| ... *and 17 additional developer runtime modules.* |

### 2. Core Governance & Integrity (23)
| Skill | Category | Description |
| :--- | :--- | :--- |
| `NOVA.Patt.CleanCode` | Standards | Code clarity, formatting rules, and style standards |
| `NOVA.Sys.TDD` | Standards | Triple-pass TDD cycle guidelines and test patterns |
| `canonization` | Integrity | Sealing and hashing active files into registry manifests |
| `compliance_audit` | Integrity | Compliance engine checks for workspace resonance |
| `sentinel-audit` | Integrity | Linting execution, compliance checks, and error audits |
| `soul-forging` | Identity | Behavioral specifications for core agents (Axion, Sophia, Sentinel) |
| `zero-entropy-maintenance` | Integrity | Calculating technical debt mass and pruning code rot |
| `uam` | Architecture | Unified Architecture Management (UIP-V15 compliance checking) |
| `detect-synergies` | Architecture | Weaving links between workspace components |
| `supabase-transmuter` | Database | Interfacing reads/writes directly to database backends |
| `systemic-resonance-alignment` | Integrity | Calculating Cosine Similarity semantic alignment |

---

V. ## 🔄 Workflows (13)

---

Slash command procedures. Invoke via `/command`. Actual Path: `.agent/workflows/`

| Command | Description | File |
| :--- | :--- | :--- |
| `/audit` | Runs the compliance audit checks on the workspace. | [audit.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/audit.md) |
| `/canonize` | Formally seals and hashes workspace changes to registry. | [canonize.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/canonize.md) |
| `/create` | Scaffolds a new project or custom application template. | [create.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/create.md) |
| `/debug` | Investigates runtime errors using systematic debugging. | [debug.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/debug.md) |
| `/enhance` | Progressively adds features or updates existing files. | [enhance.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/enhance.md) |
| `/game_creation` | Invokes specialist subagents to prototype game code. | [game_creation.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/game_creation.md) |
| `/migrate_tasks` | Executes task-store tracking migration. | [migrate_tasks.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/migrate_tasks.md) |
| `/plan` | Creates detailed project implementation blueprints. | [plan.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/plan.md) |
| `/scaffold` | Generates a LangGraph agent scaffold template. | [scaffold.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/scaffold.md) |
| `/simulate` | Runs impact simulations across system boundaries. | [simulate.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/simulate.md) |
| `/status` | Details goals, progress boards, and current targets. | [status.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/status.md) |
| `/tdd_cycle` | Performs the A/B/C triple-pass TDD cycle. | [tdd_cycle.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/tdd_cycle.md) |
| `/test` | Runs test suites and creates unit test specs. | [test.md](file:///c:/Users/Chris/Synarche_Workspace/.agent/workflows/test.md) |

---

VI. ## 📜 Scripts (6)

---

Validation scripts inside `.agent/substrate/bin/`:

| Script | Purpose |
| :--- | :--- |
| `checklist.py` | Priority-based validation (security checks, lint, code metrics). |
| `verify_all.py` | Comprehensive test execution suite including E2E and audits. |
| `session_manager.py` | Persistent workspace context and session memory tracking. |
| `auto_preview.py` | Real-time state visualization and UI previews. |
| `refresh_registry.py` | Synchronize workspace file indices with registry keys. |
| `update_nav_hubs.py` | Maintain dynamic markdown navigation maps. |

---

VII. ## 📊 Statistics

---

| Metric | Count | Details |
| :--- | :--- | :--- |
| **Total Agents** | 23 | 20 Specialist + 3 Core Substrate Profiles |
| **Total Skills** | 60 | Combined Developer (37) & Compliance (23) Packages |
| **Total Workflows** | 13 | Slash command playbooks |
| **Total Binaries** | 6 | Python scripts inside `substrate/bin/` |
| **Registry Size** | 4,673 | Fully aligned workspace artifacts |
