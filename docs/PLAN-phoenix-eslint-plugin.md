# PLAN: Comprehensive Governance Consolidation (ESLint, CSpell, Markdownlint)

## 🔴 Phase -1: Context Check
**Goal**: Integrate all custom local governance rules—currently scattered in `.agent/substrate/rules`—into the `axion-core/standards` directory to create an immutable Single Source of Truth (SSOT). This includes ESLint plugins, CSpell custom dictionaries, and Markdownlint custom rules (`axion-rules.cjs`).

**Current State**:
- **ESLint**: Local custom rules (`phoenix-logger`, `artifact-anchor`, `sovereign-aliases`) exist in `.agent/substrate/rules/`.
- **CSpell**: Custom dictionaries (`master.json`, `master.jsonc`) exist in `.agent/substrate/rules/cspell/`. The central `standards/cspell.jsonc` currently relies on a hardcoded `"words"` array.
- **Markdownlint**: Custom rules (`axion-rules.cjs`) exist in `.agent/substrate/rules/markdownlint/`. The central `standards/.markdownlint.cjs` currently attempts to require `tools/rules/axion-rules.cjs` (which is a broken/non-existent path).

## 🟢 Phase 1: Task Breakdown & Strategy

We will proceed with **Approach B** (Copy & Formalize) to fully canonize these rules within the `axion-core/standards` directory. 

### 1. ESLint Plugin Consolidation
- Scaffold `axion-core/standards/eslint-plugin-phoenix/` to hold custom ESLint rules.
- **Copy** (non-destructively) all plugin files from `.agent/substrate/rules/` to this new directory:
  - `eslint-plugin-index.js` -> renamed to `index.js`
  - `eslint-plugin-phoenix-logger.js` -> `rules/phoenix-logger.js`
  - `eslint-plugin-require-artifact-anchor.js` -> `rules/require-artifact-anchor.js`
  - `eslint-plugin-enforce-sovereign-aliases.js` -> `rules/enforce-sovereign-aliases.js`
- **Refactor**: Update relative import paths within the copied `index.js`.
- **Link**: Modify `axion-core/standards/eslint.config.mjs` to import and register the local plugin.

### 2. Markdownlint Consolidation
- Scaffold `axion-core/standards/markdownlint-rules/` to house custom Markdown logic.
- **Copy**: `.agent/substrate/rules/markdownlint/axion-rules.cjs` to the new directory.
- **Link**: Update `axion-core/standards/.markdownlint.cjs` to fix the broken `customRules` path:
  ```javascript
  customRules: [require("./markdownlint-rules/axion-rules.cjs")],
  ```

### 3. CSpell Consolidation
- Scaffold `axion-core/standards/dictionaries/` to hold domain-specific vocabulary.
- **Copy**: `.agent/substrate/rules/cspell/master.json` and `master.jsonc` into this new directory.
- **Link**: Refactor `axion-core/standards/cspell.jsonc` to use the `import` array to load the master dictionaries, migrating away from hardcoding everything in the central config.
  ```jsonc
  "import": ["./dictionaries/master.jsonc"]
  ```

### 4. Implementation Validation
- **ESLint**: Run `npx eslint --config axion-core/standards/eslint.config.mjs` to verify plugin registration.
- **Markdownlint**: Verify that `axion-rules.cjs` loads successfully without module resolution errors.
- **CSpell**: Verify the spellchecker recognizes words from the newly linked master dictionaries.

## 📋 Verification Checklist
- [ ] `eslint-plugin-phoenix/` created and wired to `eslint.config.mjs`.
- [ ] `markdownlint-rules/axion-rules.cjs` created and wired to `.markdownlint.cjs`.
- [ ] `dictionaries/master.jsonc` created and wired to `cspell.jsonc`.
- [ ] No files in `.agent/substrate/rules` were deleted (non-destructive).

---
**Agent Assignments**: 
- **Antigravity (Execution)**: To copy the files across all three domains (ESLint, Markdown, CSpell), refactor relative paths, and link them to their respective master configuration files in the `standards/` directory.
