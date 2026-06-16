# Task Plan: Consolidate Governance Standards

## Phase 1: Planning and Documentation

- [x] Initialize `planning-with-files` workflow
- [x] Update `axion-core/standards/README.md` with canonical paths

## Phase 2: Configuration Alignment

- [x] Analyze scattered configs (`tarot-forge/eslint.config.js`, `open-notebook/mypy.ini`) for unique overrides
- [x] Merge necessary overrides into `axion-core/standards/`
- [x] Update Global VS Code `settings.json` to point to central standards
- [x] Update Antigravity `settings.json` to point to central standards
- [x] Update `ide_sentinel.py` to enforce the correct paths

## Phase 3: Agent Folder Alignment (.agent)

- [x] Update `.agent/substrate/rules/README.md`
- [x] Update `lint_runner.py` to use central configs
- [x] Update `AGENT_AXION_SYNTHESIS.md` references

## Phase 4: Project-Level Migration & Cleanup

- [x] Delete `nova_forge/playground/tarot-forge/.prettierrc.yaml` (Confirmed: deleted/non-existent)
- [x] Delete `nova_forge/playground/tarot-forge/eslint.config.js` (Confirmed: deleted/non-existent)
- [x] Delete `nova_forge/.markdownlint.json` (Confirmed: deleted/non-existent)
- [x] Delete `open-notebook/mypy.ini` (Confirmed: deleted/non-existent)

## Phase 5: Verification

- [x] Run `ide_sentinel.py` (Confirmed: SYSTEM STATUS: COHERENT [OK])
- [x] Verify formatting and linting across projects (ESLint ignores added; tests passing)
