# High-priority findings

1. **`_safe_path` can crash on mixed absolute/relative input and may miss canonicalization checks.**
    - `os.path.commonpath([base, target])` should compare canonical absolute paths for both values.
    - Recommended hardening:
        - `base_abs = os.path.realpath(base)`
        - `target_abs = os.path.realpath(os.path.join(base_abs, filename))`
        - then compare `commonpath([base_abs, target_abs]) == base_abs`.

2. **`verify_block_integrity` silently skips verification when manifest is missing.**
    - For strict integrity, missing checksum sidecars should fail in strict mode (or always, depending on policy).
    - Current behavior allows unsigned/unchecked blocks to be transcluded.

3. **`resolve_transclusions` dependency graph keying is inconsistent for nested blocks.**
    - Uses `stack[-1] if stack else "root"` as parent key, but values are just `filename` strings.
    - This can mix absolute parent keys with relative child names, which complicates graph analysis and can collide.
    - Prefer normalized node identifiers (all relative to block root or all absolute).

4. **Circular dependency error message leaks full absolute paths.**
    - `RecursionDepthError(f"Circular dependency: {stack}")` can expose internal filesystem layout.
    - Prefer redacted or relative path chain.

5. **CLI `--meta` parsing assumes YAML object; no type guard.**
    - `yaml.safe_load` can return non-dict values (`None`, list, scalar).
    - `metadata.update(meta)` will fail or behave unexpectedly unless `meta` is validated as a mapping.

6. **No explicit encoding for `.sha256` reads/writes and JSON writes.**
    - Use `encoding="utf-8"` consistently to avoid platform-specific defaults.

## Medium-priority findings

1. **Audit log is never populated.**
    - `self.audit_log` is initialized and persisted, but no events are appended.
    - Add lifecycle events (shell read, block include, render success/failure, hash checks).

2. **Template sandboxing is improved but still permissive by default for filters/tests.**
    - Consider explicitly constraining allowed filters/tests/globals if threat model includes hostile templates.

3. **`forge` doesn’t catch template rendering errors to enrich diagnostics.**
    - Wrap render stage to attach shell name and artifact id context.

4. **`--depth` lacks validation for negative values.**
    - Negative depth should reject at argparse/type-validation stage.

5. **Deterministic mode only stabilizes metadata timestamps, not all output-affecting sources.**
    - If manifests, filesystem order, or external metadata can vary, deterministic claims may be overstated.

## Suggested fixes (minimal)

- Harden path checks with `realpath` on both base and target.
- Enforce checksum presence in strict mode.
- Validate `meta` as `dict[str, Any]` before merge.
- Normalize dependency graph node keys/values (e.g., POSIX-style relative paths).
- Add structured audit events for every transclusion and render operation.
- Add explicit file encodings everywhere.

## Positive notes

- Good use of `SandboxedEnvironment` with `StrictUndefined`.
- Recursion/cycle protection is present.
- Integrity hash generation and metadata enrichment are cleanly separated.
- Clear exception taxonomy improves operational handling.
