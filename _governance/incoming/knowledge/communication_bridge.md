# Dual-Artifact Communication Protocol (DACP)

To ensure seamless coordination between a Human and an AI Agent, descriptions and plans should be provided in a "Dual Format". This protocol minimizes ambiguity for the AI while providing clear, high-level context for the Human.

## The Dual Format Structure

### 👤 1. Human Perspective: The "Why" and "Impact"

_Focused on intent, outcomes, and business value._

- **Objective**: What are we actually trying to achieve in plain English?
- **Impact**: How does this change the experience or the system?
- **Analogy/Metaphor**: Optional but helpful for complex concepts.
- **Visuals/UX**: Description of the intended visual feel or user flow.

---

### 🤖 2. AI Perspective: The "What" and "How"

_Focused on execution, constraints, and technical state._

- **Technical Goal**: Precise definition of the success state (e.g., "Function X returns Type Y").
- **Dependencies**: Explicit list of files, variables, or MCP tools involved.
- **Constraints**: Security rules, performance limits, or specific syntax standards (e.g., OMEGA 14.0).
- **Automation Markers**: Instructions for `scripts/` or `workflows/` triggers.

---

## 🚀 The Dual-Artifact Generator Prompt

Use this prompt to ask me for a Dual Artifact for any task:

> **"Draft a Dual Artifact for [TASK/CONCEPT]. Provide a Human Perspective segment focused on intent and a separate AI Perspective segment focused on technical specs and constraints. Ensure the AI segment uses precise paths and references to the current `.agent` structure."**

---

## Example Usage

### Human Segment

"We want to make the login button feel 'snappy'. When clicked, it should have a subtle bounce animation and immediately show a loading spinner."

### AI Segment

"Modify `src/components/LoginButton.tsx`. Apply CSS class `.bounce-click`. Use `useState` for `isLoading` state. Ensure `onClick` prevents default and triggers `authService.login()`. Target: OMEGA v14.0 visual standards."
