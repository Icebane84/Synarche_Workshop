#!/usr/bin/env python3
"""# TOOL-SENT-006: Weaver CLI (Celestial Interface).

## I. Universal Identification & Provenance
| Attribute | Value |
| :--- | :--- |
| **Artifact ID** | `TOOL-SENT-006` |
| **Official Name** | `weaver_cli.py` |
| **Version** | **v1.0** |
| **Celestial Class** | `[PLANET]` |
| **Governance** | `GVRN-SYNERGY-001` |
"""

import argparse
import json
import logging
import sys

from weaver_engine import ASLWeaverEngine

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Synarche Celestial Weaver CLI")
    parser.add_argument(
        "--config", default="asl_weaver_config.json", help="Path to config JSON"
    )
    parser.add_argument("--root", default=".", help="Workspace root directory")
    parser.add_argument(
        "--mode",
        choices=["check", "forge", "audit"],
        default="check",
        help="check: passive audit, forge: active links, audit: LIS only",
    )
    parser.add_argument("--output", help="Path to save JSON report")

    args = parser.parse_args()

    try:
        engine = ASLWeaverEngine(args.config, args.root)
        engine.scan()

        report = {
            "mode": args.mode,
            "timestamp": None,  # Could add if needed
            "forge_plan": {},
            "audit_results": {},
        }

        if args.mode in ["check", "forge"]:
            plan = engine.plan_weave()
            report["forge_plan"] = plan

            if not plan:
                logger.info("✅ Zero entropy detected. All artifacts are coherent.")
            else:
                logger.info(f"🔍 Found {len(plan)} artifacts with missing relations.")
                for art_id, suggestions in plan.items():
                    logger.info(f"  - {art_id}: {', '.join(suggestions)}")

            if args.mode == "forge" and plan:
                logger.info("\n⚡ Initiating Forge sequence...")
                updated_count = engine.execute_forge(plan)
                logger.info(
                    f"✨ Successfully forged links in {updated_count} artifacts."
                )

        if args.mode == "audit" or (args.mode in ["check", "forge"]):
            audit = engine.audit_lis()
            report["audit_results"] = audit
            logger.info(f"\n📊 Sentinel LIS: {audit['lis_score']}")
            logger.info(
                f"   (Valid Links: {audit['metrics']['valid_links']} / Total: {audit['metrics']['total_links']})"
            )

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4)
            logger.info(f"\n💾 Report saved to {args.output}")

    except Exception:
        logger.exception("Celestial Weaver encountered a critical failure")
        sys.exit(1)


if __name__ == "__main__":
    main()
