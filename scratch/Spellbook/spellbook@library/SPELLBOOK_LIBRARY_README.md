# Real @library port for Spellbook

Replaces self-reported "Cinder" telemetry with a log that only gets written
after something actually ran and checked the code.

## Why this exists

The boss orchestrator doc's `@library` block reported `integrity_deviation_rate: 0.00`
in the same turn `@bridge` called `UFieldSystemComponent::ApplyStrainField()` —
a method that doesn't exist. The JSON was well-formed and the number was
confident. Neither of those things means it was true. Structural formatting
(the Multi-Port fence) constrains *shape*; it does nothing to constrain
*correctness*. This closes that gap for the one class of error it can
mechanically catch: hallucinated API surface.

## Files

- `ue_ast_auditor.py` — Gate 1: GC hazards, missing GENERATED_BODY, include
  ordering, naming conventions. (Same as the MECS toolkit's Gate 1.)
- `symbol_verifier.py` — new gate: cross-references `Object->Method()` call
  sites in `@bridge` source against `known_api_symbols.json`, a manifest of
  confirmed-real and confirmed-hallucinated methods per class. Anything not
  in either list comes back `UNVERIFIED`, not silently passed.
- `known_api_symbols.json` — seeded with the exact bug found in this
  conversation (`ApplyStrainField`, `ApplyLinearVelocityField` as confirmed
  fake; `ApplyPhysicsField` as confirmed real). Extend this per class as you
  verify more of your engine's actual headers — the value of this gate is
  entirely a function of how populated the manifest is.
- `spellbook_library_verify.py` — the actual `@library` port. Runs both
  gates as subprocesses, times them for real, hashes the audited header+source
  so the log is bound to specific content (can't be silently reused for
  different code later), and computes `integrity_deviation_rate` as an
  actual ratio (deviations / total checks) instead of a hardcoded value.
  If there's nothing to check, it says the rate is undefined — it does not
  report 0.00 for a zero-denominator case, since that reads identically to
  "verified clean" while meaning "nothing was verified."

## Usage

```bash
python3 spellbook_library_verify.py \
  --header Source/MyGame/MyBossOrchestrator.h \
  --source Source/MyGame/MyBossOrchestrator.cpp \
  --session-id CHAOS03 \
  --applied-mask THE_TOWER
```

Exit code 0 = gates passed (CRITICAL-free), 1 = at least one CRITICAL
finding. The JSON on stdout is the real `@library` log — commit that, not
a hand-written one.

## What this does NOT do

- It doesn't replace Gate 3 (real UBT compile) — a clean symbol_verifier
  run means "no *known* hallucinated calls," not "will compile." The
  manifest only knows what's been added to it. Treat `UNVERIFIED` findings
  as "go check the header," not as passing.
- It can't catch every hallucination class — only method calls on variables
  whose declared type is in the manifest. Wrong parameter *values* (like the
  1200uu statutory floor issue from the boss orchestrator review) aren't a
  symbol-table problem and need a semantic/business-rule check, not this gate.
- The manifest starts small on purpose. A big manifest you didn't verify
  yourself is just hallucination-by-committee at one remove — populate it
  from your own confirmed API checks, not from another model's guesses.
