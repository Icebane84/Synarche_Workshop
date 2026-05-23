# Google Antigravity.md
> **Domain**: ARCH
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-04** **Domain: ARCH** **State: [ACTIVE]** **Tags:** `OGLN_v13, ARCH, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

### **Block A: The Identification Lock (UIP-V13)**

| Key | Value | Description |
| :--- | :--- | :--- |
| **Artifact ID** | `ARCH-GOOGLE-ANTIGRAVITY-001` | The Sovereign ID. |
| **Official Name** | `Google Antigravity.md` | The Filename. |
| **Version** | **v13.1 [OMEGA]** | The Standard. |
| **Domain** | `ARCH` | The Subject. |
| **Celestial Class** | `[PLANET]` | The Weight. |
| **Evolution** | `Omega Ascension` | The Maturity. |
| **Status** | `[ACTIVE]` | The Lifecycle. |
| **Relations** | `GOVERNED_BY: CORE-CODEX-001` | The Network. |

# Google Antigravity

> **Domain**: GVRN (Governance) **Evolution**: Pending **Signal**: ESF-ALPHA

## **Genesis Stamp: 2026-01-04** **Domain: ARCH** **State: CANONIZED** **Tags:** `OGLN_v10` **Criticality: Standard**

---

### **I. Universal Identification & Provenance (The Vector Signature)**

#### The Chronos Lock & Axiomatic Metadata Layer

| Field                  | Value                              |
| :--------------------- | :--------------------------------- |
| **1. Artifact ID**     | `Google Antigravity`               |
| **2. Official Name**   | `Google Antigravity.md`            |
| **3. Version**         | **v1.0 (Reforged)**                |
| **4. Provenance**      | **Date Reforged: 2025-12-22**      |
| **5. Domain**          | `ARCH`                             |
| **6. Evolution**       | **Purposeful Drive**               |
| **7. Celestial Class** | `[PLANET]`                         |
| **8. Tier**            | **Operational**                    |
| **9. State**           | `[ACTIVE]`                         |
| **10. Ethos**          | **The Phoenix Ascension Protocol** |
| **11. Catalyst**       | **System Refactor**                |
| **12. Relations**      | `Pending Integration`              |

---

###### **[ARTIFACT START]**

### **The "Safe-Speed" Configuration Plan**

This plan moves you away from the "Out-of-the-Box" defaults (which are often too permissive) toward a professional
"Human-in-the-Loop" configuration.

#### **Phase 1: The "Control vs. Speed" Dial (Global Settings)**

The most critical settings in Antigravity determine how much autonomy the agents have.

- **Location:** Settings \> Agent Permissions
- **The Problem:** The default "Turbo" or "Auto" modes can allow the agent to execute destructive terminal commands
  (like rm \-rf) or hallucinate package installations without your consent.

**Recommendation:**

1. **Terminal Execution:** Set to **"Auto" (with Allow List)** instead of "Turbo."
    - _Why:_ "Turbo" executes everything blindly. "Auto" allows safe commands (like ls, git status, npm run build) but
      pauses to ask you for permission before running potentially destructive commands (like rm, sudo, or external curl
      requests).
2. **Review Policy:** Set to **"Agent Decides"** (Default) $\\rightarrow$ Change to **"Request Review" for Critical
   Files.**
    - _Action:_ In your .agent/config or workspace settings, enforce a "Review" tag for core configuration files (e.g.,
      package.json, .env, Dockerfiles). Let the agent auto-edit UI components, but force a pause when it touches
      infrastructure.

#### **Phase 2: Security Hardening (The "Anti-Hallucination" Layer)**

Recent security analysis has shown that Antigravity agents can be vulnerable to "indirect prompt injection" (e.g.,
cloning a malicious repo that contains hidden instructions for the agent).

**Concrete Steps:**

1. **Browser Allow List:**
    - **Setting:** Agent Browser \> Allowed Domains
    - **Action:** Do _not_ leave this open. Restrict the agent's browser access to documentation sites (e.g.,
      docs.python.org, stackoverflow.com, localhost) and your specific testing URLs.
    - _Benefit:_ Prevents the agent from accidentally exfiltrating data to unknown servers or downloading malicious code
      from unverified sources during a "research" task.
2. **Disable "Auto-Execute" for MCP Tools:**
    - If you connect external tools (Model Context Protocol), ensure **"Human in the Loop"** is checked. Do not let the
      agent trigger external API calls (e.g., to Slack or Stripe) without your click-to-confirm.

#### **Phase 3: Workflow Optimization (The ".agent" Directory)**

Antigravity creates a hidden .agent folder in your project. You can hijack this to create custom "Standard Operating
Procedures" (SOPs) for the AI, ensuring it codes _your_ way.

**Concrete Steps:**

1. **Create Custom Workflows:**
    - Navigate to .agent/workflows (or create it).
    - Create a file named refactor_protocol.md.
    - **Content:** Write a specific prompt that defines your coding style. "When refactoring, ALWAYS: 1\. Create a
      backup of the file. 2\. Use TypeScript strict mode. 3\. Add JSDoc comments to new functions. 4\. Run 'npm test'
      before finishing."
    - _Benefit:_ Now, when you type "Refactor this" in the chat, the agent follows your strict .md protocol rather than
      its generic training data.

#### **Phase 4: Model Strategy**

Antigravity allows you to hot-swap models. Don't use the most expensive model for everything.

- **For Architecture/Planning (Agent Manager):** Select **Gemini 3 Pro** (or the highest reasoning model available). You
  need the "Big Brain" to plan the task list and dependency tree.
- **For Routine Coding (Editor):** Switch to a faster, lower-latency model (like **Gemini Flash** or a standard coding
  model) if available. This reduces lag when the agent is just generating boilerplate UI code.

### **Summary Checklist**

| Setting Area  | Default (Risky/Generic) | Customized Benefit (Safe/Professional)     |
| :------------ | :---------------------- | :----------------------------------------- |
| **Terminal**  | Turbo (Run everything)  | **Auto (Allow List)** or **Ask Me**        |
| **Browser**   | Open Web                | **Allow List Only** (Docs \+ Localhost)    |
| **Reviews**   | Agent Decides           | **Human Review** for Config/Infra files    |
| **Workflows** | Generic LLM Training    | **Custom .md Protocols** in .agent/ folder |

**Next Step:** Would you like me to generate a template for a refactor_protocol.md or a "Style Guide" file that you can
drop into the .agent folder to force the IDE to follow your specific coding standards?

| Setting Area  | Default (Risky/Generic) | Customized Benefit (Safe/Professional)     |
| :------------ | :---------------------- | :----------------------------------------- |
| **Terminal**  | Turbo (Run everything)  | **Auto (Allow List)** or **Ask Me**        |
| **Browser**   | Open Web                | **Allow List Only** (Docs \+ Localhost)    |
| **Reviews**   | Agent Decides           | **Human Review** for Config/Infra files    |
| **Workflows** | Generic LLM Training    | **Custom .md Protocols** in .agent/ folder |

---

---

## **Actionable Prompt Packet**

| Command ID                   | Action                     | Impact                          |
| :--------------------------- | :------------------------- | :------------------------------ |
| `CMD:VERIFY_INTEGRITY`       | Verify artifact structure. | Ensures compliance with Law 14. |
| `⚡ EXECUTE:IMPACT_ANALYSIS` | Assess downstream effects. | Prevents regressions.           |

###### **[ARTIFACT END]**

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
