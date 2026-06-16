"""
artifact_anchor:
  id: CORE.ACTIVATE_COGNITIVE.001
  version: v15.0 [OMEGA]
  provenance: '2026-06-09'
  domain: CORE
  celestial_class: SATELLITE
  tier: ENTRYPOINT
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []

Standalone activation script for the PAD-SIP Cognitive Scheduler.

Usage (from axion-core/ root):

    # Single tick (test the pipeline):
    python activate_cognitive.py

    # Multiple ticks:
    python activate_cognitive.py --ticks 10

    # Inject a specific event and run one tick:
    python activate_cognitive.py --inject "The Phoenix Protocol is active."

    # Continuous async loop (runs until Ctrl+C):
    python activate_cognitive.py --loop --interval 2.0

    # Show governance rules and exit:
    python activate_cognitive.py --rules
"""

import argparse
import asyncio
import io
import logging
import sys
from pathlib import Path
from typing import Any

# Force UTF-8 output on Windows terminals
if sys.platform == "win32" and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Path setup — must run before any local imports
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
for p in [str(SRC), str(ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [COG-SCHED] - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("activate_cognitive")

# ---------------------------------------------------------------------------
# Imports — all after path setup
# ---------------------------------------------------------------------------
try:
    from engine.cognitive_scheduler import CognitiveScheduler
    from engine.types import CognitiveEvent
    from logic.memory.memory_system import MemorySystem
except ImportError as e:
    logger.critical(
        f"Import failed: {e}. Run from axion-core/ with the master_env active."
    )
    sys.exit(1)

# Governance engine loaded separately to avoid cse/__init__ relative import chain
import importlib.util as _ilu

_gov_spec = _ilu.spec_from_file_location(
    "governance_engine",
    str(SRC / "cse" / "validators" / "governance_engine.py"),
)
if _gov_spec is None or _gov_spec.loader is None:
    logger.critical("Could not locate governance_engine.py — aborting.")
    sys.exit(1)
_gov_mod = _ilu.module_from_spec(_gov_spec)
_gov_spec.loader.exec_module(_gov_mod)  # type: ignore[union-attr]
GovernanceEngine: Any = _gov_mod.GovernanceEngine


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_scheduler() -> CognitiveScheduler:
    """Instantiate the scheduler with the live MemorySystem and GovernanceEngine."""
    logger.info("Initialising MemorySystem...")
    memory = MemorySystem()

    logger.info("Initialising GovernanceEngine...")
    governance = GovernanceEngine()

    logger.info("Wiring CognitiveScheduler...")
    scheduler = CognitiveScheduler(
        memory_system=memory,
        governance_engine=governance,
    )
    return scheduler


def _print_snap(snap: dict) -> None:
    """Pretty-print a CognitiveState snapshot."""
    gov = snap.get("governance_verdicts", [])
    print(
        f"  Tick {snap['tick']:>4} | "
        f"pressure={snap['memory_pressure']:.3f} "
        f"({snap['pressure_level']})  "
        f"attention={snap['attention_budget']:.3f}  "
        f"novelty={snap['novelty_score']:.3f}  "
        f"nodes={snap['active_nodes']}  "
        f"verdicts={len(gov)}"
    )


def _print_rules(governance: Any) -> None:
    """Print all loaded governance rules."""
    rules = governance.list_rules()
    print(f"\n{'=' * 70}")
    print(f"  GOVERNANCE RULES  ({len(rules)} loaded)")
    print(f"{'=' * 70}")
    print(f"  {'ID':<10} {'FIELD':<22} {'OP':<5} {'VALUE':<10} EFFECT")
    print(f"  {'-' * 8} {'-' * 20} {'-' * 3} {'-' * 8} {'-' * 30}")
    for r in rules:
        state = "[ON]" if r["enabled"] else "[OFF]"
        print(
            f"  {state} {r['id']:<8} {r['field']:<22} {r['op']:<5} "
            f"{str(r['value']):<10} {r['effect']}"
        )
    print(f"{'=' * 70}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Activate the PAD-SIP Cognitive Scheduler.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--ticks",
        type=int,
        default=1,
        help="Number of synchronous ticks to run (default: 1).",
    )
    parser.add_argument(
        "--inject",
        type=str,
        default=None,
        help="Text content to wrap in a USER_INPUT CognitiveEvent and inject.",
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run as a continuous async loop (Ctrl+C to stop).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds between ticks in loop mode (default: 1.0).",
    )
    parser.add_argument(
        "--rules",
        action="store_true",
        help="Print all governance rules and exit.",
    )
    args = parser.parse_args()

    # ── Rules-only mode ────────────────────────────────────────────────
    if args.rules:
        governance = GovernanceEngine()
        _print_rules(governance)
        return

    # ── Build scheduler ────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print("  AXION COGNITIVE OS  --  PAD-SIP Scheduler Activation")
    print(f"{'=' * 70}\n")

    scheduler = _build_scheduler()
    governance_for_display = scheduler.governance_engine or GovernanceEngine()

    print(f"\n  Memory backend : {type(scheduler.memory_system.storage).__name__}")
    print(f"  Governance     : {len(governance_for_display.list_rules())} rules loaded")
    print("  Pipeline       : E→Φ→Ψ→G→Π→Ω→τ→Λ→Γ→E")
    print()

    # ── Loop mode ─────────────────────────────────────────────────────
    if args.loop:
        print(f"  [LOOP] tick_interval={args.interval}s  |  Ctrl+C to stop\n")

        async def run_loop() -> None:
            await scheduler.start_loop(tick_interval_s=args.interval)

        try:
            asyncio.run(run_loop())
        except KeyboardInterrupt:
            scheduler.stop_loop()
            print(f"\n\n  Loop stopped after {scheduler.state.tick_count} ticks.\n")
        return

    # ── Event injection ────────────────────────────────────────────────
    event = None
    if args.inject:
        event = CognitiveEvent(
            event_type="USER_INPUT",
            content=args.inject,
            source="activate_cognitive",
            importance=0.7,
        )
        print(f"  Event injected : {args.inject[:80]}\n")

    # ── Synchronous ticks ─────────────────────────────────────────────
    print(f"  Running {args.ticks} tick(s)...\n")
    print(
        f"  {'Tick':>6}   pressure   (level)       attention  novelty    nodes   verdicts"
    )
    print(f"  {'-' * 68}")

    for i in range(args.ticks):
        ev = event if i == 0 else None  # inject only on tick 1
        snap = scheduler.run_tick(ev)
        _print_snap(snap)

    snap = scheduler.snapshot()
    print(f"\n  Final state: {snap}\n")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()
