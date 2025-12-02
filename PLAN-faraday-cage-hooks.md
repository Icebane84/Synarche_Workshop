# PLAN: Faraday Cage & Pre-Commit Hooks

## Overview

Following external architectural critique, this plan addresses three critical vectors of entropy: Sandbox Escape (RCE), Registry Desynchronization, and Context Saturation. We will seal the **Faraday Cage** (execution boundaries), weave a **Pre-Commit Hook** for automatic Loom syncing, and forge a **Metadata Transmuter** to optimize LLM token limits during context loading.

## Project Type

**BACKEND** (Core OS & Scripting)

## Success Criteria

1. **Zero Sandbox Escapes**: Any `subprocess` or `pwsh` execution attempting to access or write outside of `c:\Users\Chris\Synarche_Workspace\` is mathematically blocked.
2. **Absolute Registry Synchronization**: A Git pre-commit hook (or equivalent watcher) intercepts commits, forces a `Loom Registry audit`, and blocks the commit if Dissonance is detected.
3. **Context Optimization**: A transmutation script (`transmute_context.py`) successfully strips `UIP-V15 Block A` metadata from Markdown files, returning token-dense JSON representations.

## Tech Stack

- **Python 3.x**: For the core execution bounding (`os.path.abspath` resolution) and markdown transmutation logic.
- **Git / Bash / PowerShell**: For the `pre-commit` lifecycle hook.

## File Structure

- `axion-core/forge/security.py` (or integrated into `sentinel.py`) - The Faraday Cage validation logic.
- `.git/hooks/pre-commit` - The Loom synchronization trigger.
- `axion-core/forge/transmute_context.py` - The Token Optimization utility.

## Task Breakdown

### Task 1: The Faraday Cage Implementation

- **Task ID**: `TASK-01-FARADAY`
- **Agent**: `security-auditor`
- **Skills**: Security Architecture, Python
- **Priority**: P0
- **Dependencies**: None
- **INPUT**: `axion-core/forge/sentinel.py` (or local subprocess controllers).
- **OUTPUT**: Strict path bounding logic (`resolve_path`) that throws a `SecurityException` if an execution attempts path traversal outside the Synarche root.
- **VERIFY**: Run a mock script attempting to read/write `C:\Windows\System32`; ensure it is actively blocked and logged by the Chronicler.

### Task 2: Sovereign Pre-Commit Hook

- **Task ID**: `TASK-02-PRECOMMIT`
- **Agent**: `devops-engineer`
- **Skills**: Git, Automation
- **Priority**: P1
- **Dependencies**: Completion of the `axion-core` flattening (Loom script must be formally located at `axion-core/forge/loom.py`).
- **INPUT**: A standard `.git/hooks/pre-commit` shell/pwsh script.
- **OUTPUT**: A hook that executes `python axion-core/forge/loom.py audit` before allowing a commit.
- **VERIFY**: Intentionally break an artifact's UID header. Attempt a `git commit`. The commit must be rejected until the header is repaired.

### Task 3: Context Saturation Transmuter

- **Task ID**: `TASK-03-TRANSMUTER`
- **Agent**: `backend-specialist`
- **Skills**: Python, NLP Parsing
- **Priority**: P2
- **Dependencies**: None
- **INPUT**: Any standard `UIP-V15 Block A` artifact (e.g., `SKILL.md`).
- **OUTPUT**: `axion-core/forge/transmute_context.py`. Parses the markdown, strips the visual tables and spacing of the metadata header, and returns a condensed JSON key-value string.
- **VERIFY**: Feed `transmute_context.py` a 400-token markdown file and ensure the output retains 100% of the semantic properties at `< 150` tokens.

## Phase X: Verification

- [ ] Security Execution Blockers pass Unit Tests.
- [ ] Pre-Commit Hook halts dissonant commits.
- [ ] Transmuter successfully compresses Markdown metadata.
- [ ] Rule Compliance check: No Socratic/Rule overrides occurred.

## ✅ PHASE X COMPLETE

(Pending execution of Tasks 1-3)
