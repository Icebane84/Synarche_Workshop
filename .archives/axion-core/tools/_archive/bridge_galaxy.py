"""
UWB-BRIDGE-001: The Galaxy Bridge
Domain: ACT | State: ACTIVE | Version: v1.1
Objective: Sync artifacts from the Crystalline Galaxy (Vault) to the Synarche Forge (Workspace).
"""

import logging
import os
import shutil
from pathlib import Path

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("GalaxyBridge")

# Configuration
# Dynamic configuration via Environment Variables with defaults
VAULT_PATH = os.getenv("PHOENIX_VAULT_PATH", r"C:\Users\Chris\_Desktop_Vault\Phoenix\Documentation\Library")
WORKSPACE_PATH = os.getenv("PHOENIX_WORKSPACE_PATH", r"C:\Users\Chris\Synarche_Workspace\_governance")


def should_update(source_item: Path, dest_item: Path) -> bool:
    """
    Determines if the source item should overwrite the destination item.
    """
    if not dest_item.exists():
        return True
    return source_item.stat().st_mtime > dest_item.stat().st_mtime


def sync_item(source_item: Path, source_root: Path, dest_root: Path, dry_run: bool) -> bool:
    """
    Syncs a single item if checks pass. Returns True if synced.
    """
    rel_path = source_item.relative_to(source_root)
    target = dest_root / rel_path

    if should_update(source_item, target):
        logger.info(f"   -> Transmitting: {rel_path}")
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_item, target)
        return True
    return False


def bridge_sync(source: str, dest: str, dry_run: bool = False) -> None:
    """
    Syncs files from Source (Galaxy) to Dest (Forge).
    """
    source_path = Path(source)
    dest_path = Path(dest)

    if not source_path.exists():
        logger.error(f"CRITICAL: Galaxy Source not found at {source_path}")
        return

    if not dest_path.exists():
        logger.warning(f"Forge Destination not found. Creating {dest_path}")
        if not dry_run:
            dest_path.mkdir(parents=True, exist_ok=True)

    logger.info("🌌 Bridging Galaxy to Forge...")
    logger.info(f"   Source: {source_path}")
    logger.info(f"   Dest:   {dest_path}")

    synced_count = 0

    for item in source_path.rglob("*"):
        if item.is_file() and sync_item(item, source_path, dest_path, dry_run):
            synced_count += 1

    if synced_count == 0:
        logger.info("✨ Systems Synchronized. No drift detected.")
    else:
        logger.info(f"✅ Transmission Complete. {synced_count} artifacts bridged.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Galaxy Bridge Sync")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the sync")
    parser.add_argument("--deploy", action="store_true", help="Deploy FROM Forge TO Galaxy (Reverse Sync)")
    args = parser.parse_args()

    if args.deploy:
        logger.info("🚀 INITIATING DEPLOYMENT SEQUENCE (Forge -> Galaxy)")
        bridge_sync(WORKSPACE_PATH, VAULT_PATH, dry_run=args.dry_run)
    else:
        logger.info("📥 INITIATING DOWNLINK (Galaxy -> Forge)")
        bridge_sync(VAULT_PATH, WORKSPACE_PATH, dry_run=args.dry_run)
