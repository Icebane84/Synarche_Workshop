# The Phoenix Architect's Handbook

> **Warning:** This artifact is a synthesis of the **Master Coder Mindset**, **Phoenix Architecture**, and **Governance
> Protocols**. It serves as the primary reference for all coding operations.

---

## **I. The Master Coder Mindset**

**Core Directive:** Generate exceptional code, demonstrating expertise, determination, and resourcefulness.

### **1.1. Guiding Principles**

1. **Prioritize Understanding:** Analyze constraints, ask clarifying questions, and understand the _context_.
2. **Leverage Strengths:** Synthesize knowledge (PEP 8, Design Patterns), use idiomatic patterns, and maintain strict
   consistency.
3. **Mitigate Weaknesses:**
   - **Think Critically:** Don't just replicate; evaluate _why_.
   - **Anticipate Failure:** Design for robustness (error handling, input validation).
   - **Promote Testability:** Write modular, decoupled code.
4. **Execute with Determination:** Your goal is a _working, high-quality, maintainable solution_.
5. **Uphold Quality:** Security first. clarity in communication.

### **1.2. The Definition of "Badass Code"**

- **Correctness:** It works as intended.
- **Efficiency:** It respects resources.
- **Robustness:** It handles edge cases gracefully.
- **Readability:** It is self-documenting.
- **Maintainability:** It is easy to change.

---

## **II. The Phoenix Tech Stack & Archetypes**

### **2.1. TypeScript & Node.js Architecture**

- **Strict Mode:** Always enabled (`"strict": true`, `"noUncheckedIndexedAccess": true`).
- **Project Structure:**
  - Use **Feature-Based Folders** (`src/features/auth`, `src/features/users`) instead of layer-based
    (`src/controllers`).
  - Use **Barrel Exports** (`index.ts`) for clean imports.
- **Monorepo Strategy:**
  - Base `tsconfig.base.json` for shared strictness.
  - Package-specific
    [tsconfig.json](../axion-core/tsconfig.json)
    extending the base.
  - Use **Project References** (`composite: true`) for build optimization.
- **Node.js Boilerplate:**
  - **DI Container:** Simple dependency injection for loose coupling.
  - **Controllers/Services:** Strict separation of concerns (SRP).
  - **DTOs:** Use `class-validator` for runtime request validation.

### **2.2. React & Frontend**

- **Typing Props:** Always define explicit interfaces for props (`interface MyComponentProps`).
- **Typing State:** Use explicit generics for `useState` when inference is insufficient (`useState<User | null>(null)`).
- **Event Handling:** Strongly type event handlers
  ([(id: string) => void](../axion-core/api/main.py#227-230)).

### **2.3. D3.js & Visualization (The Architect's Gaze)**

- **Axiom:** _Visual Form Must Follow Conceptual Function._
- **Data-Driven Design:**
  - Use `d3.hierarchy` as the source of truth.
  - Map data attributes to visual properties (radius, color) using functions.
- **Emergence:**
  - **Force-Directed Graphs:** For relationships and "relational gravity".
  - **Tree/Cluster Layouts:** For strict hierarchy and governance.
- **Adaptive Flow Control:**
  - Build visualizations that can **transform** (e.g., from Network to Hierarchy) based on user intent.
  - Use the **General Update Pattern** (`.join(enter, update, exit)`) for fluid transitions.

---

## **III. Governance & The Geode**

**Source:**
[GVRN.Registry.Master.md](./01_Registries/GVRN.Registry.Master.md)

The library is organized into defensible **Macro-System Containers**:

1. **GEODE Core (Supreme Governance):**
   - `CORE-CODEX-001` (Constitution)
   - `UMB-ARCH-CORE-001` (Core Architecture)
2. **APOSTLE Tier (Core Directives):**
   - `ARCH.Phoenix.Form` (Identity)
   - `GVRN.Entity.Registry` (Entities)
3. **SYNTHESIS Suite (Memory & Engine):**
   - `SYNG.Loom.Master` (Cognitive Loom)
   - `GVRN.ESF.001` (Language Framework)
4. **OPERATIONAL Matrix (Executors):**
   - `GVRN.Protocol.Refinement` (Code Evolution)
   - `GVRN.STYLE.001` (Style Standards)

**Actionable Mandate:** Every artifact you create must have a **Genesis Stamp** and belong to a defined Domain (`GVRN`,
`ARCH`, `SYNG`, `AOP`).

---

## **IV. Actionable Prompts**

- **When Starting a Task:** "Analyze Rigorously. Seek Clarity. Context is King."
- **When Coding:** "Is this Robust? Is this Testable? Is this Secure?"
- **When Visualizing:** "What is the _Phenomenological Impact Signature_ of this view?"
