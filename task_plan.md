# Task Plan: Consolidate Governance Standards

## Phase 1: Planning and Documentation
- [x] Initialize `planning-with-files` workflow
- [ ] Update `axion-core/standards/README.md` with canonical paths

## Phase 2: Configuration Alignment
- [ ] Analyze scattered configs (`tarot-forge/eslint.config.js`, `open-notebook/mypy.ini`) for unique overrides
- [ ] Merge necessary overrides into `axion-core/standards/`
- [ ] Update Global VS Code `settings.json` to point to central standards
- [ ] Update Antigravity `settings.json` to point to central standards
- [ ] Update `ide_sentinel.py` to enforce the correct paths

## Phase 3: Agent Folder Alignment (.agent)
- [ ] Update `.agent/substrate/rules/README.md`
- [ ] Update `lint_runner.py` to use central configs
- [ ] Update `AGENT_AXION_SYNTHESIS.md` references

## Phase 4: Project-Level Migration & Cleanup
- [ ] Delete `nova_forge/playground/tarot-forge/.prettierrc.yaml`
- [ ] Delete `nova_forge/playground/tarot-forge/eslint.config.js`
- [ ] Delete `nova_forge/.markdownlint.json`
- [ ] Delete `open-notebook/mypy.ini`

## Phase 4: Verification
- [ ] Run `ide_sentinel.py`
- [ ] Verify formatting and linting across projects
