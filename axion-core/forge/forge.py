"""
IDENTIFICATION: TOOL-FORGE-001
VERSION: v15.0 [OMEGA]
STATUS: [CANONIZED]
TIMESTAMP: 2026-03-24
"""

#!/usr/bin/env python3
"""
The Forge CLI (Game Master)
---------------------------
Manages the RPG attributes of the Forge Engine artifact.
Handles XP gain, Level Ups, and Stat modifications.

Usage:
    python forge.py --target "CBM-FORGE-001" --add-xp 100
    python forge.py --target "CBM-FORGE-001" --view-stats
    python forge.py --target "CBM-FORGE-001" --target-b "UMB-CSE-001" --check-synergy
"""

import argparse
import os
import re
import sys

# Add the current directory to sys.path to ensure local imports work
sys.path.append(os.path.dirname(__file__))

try:
    from nova_forge.catalyst_weaver import CatalystWeaver
except ImportError:
    # Fallback or error if not found
    print("Warning: CatalystWeaver not found. Synergy features disabled.")
    CatalystWeaver = None

# Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

if sys.platform == "win32":
    os.system("color")
    sys.stdout.reconfigure(encoding="utf-8")

# Default path relative to this script
ARTIFACT_PATH = os.path.join(os.path.dirname(__file__), "..", "CBM-FORGE-001_The_Forge_Engine.md")


def load_artifact(path=None):
    """Load artifact content from the given path or default path."""
    target_path = path if path else ARTIFACT_PATH

    # If path is just a filename, try to find it in Documentation root
    if path and os.path.sep not in path:
        root_dir = os.path.join(os.path.dirname(__file__), "..")
        potential_path = os.path.join(root_dir, path)
        if os.path.exists(potential_path):
            target_path = potential_path
        # Also try adding .md if missing
        elif os.path.exists(potential_path + ".md"):
            target_path = potential_path + ".md"

    if not os.path.exists(target_path):
        print(f"{RED}Error: Artifact not found at {target_path}{RESET}")
        sys.exit(1)

    with open(target_path, encoding="utf-8") as f:
        return f.read()


def save_artifact(content, path=None):
    """Save content to the artifact."""
    target_path = path if path else ARTIFACT_PATH
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{GREEN}✔ Artifact Updated.{RESET}")


def parse_stats(content):
    """Parse RPG stats from markdown content."""
    stats = {}

    # Extract Level
    lvl_match = re.search(r"\*\s*\*\*Level:\*\*\s*`(\d+)`", content)
    stats["level"] = int(lvl_match.group(1)) if lvl_match else 1

    # Extract XP
    xp_match = re.search(r"\*\s*\*\*Experience \(XP\):\*\*\s*`(\d+)/(\d+)`", content)
    if xp_match:
        stats["xp_current"] = int(xp_match.group(1))
        stats["xp_max"] = int(xp_match.group(2))
    else:
        stats["xp_current"] = 0
        stats["xp_max"] = 1000

    # Extract Stats
    coherence_match = re.search(r"\*\s*\*\*Coherence:\*\*\s*`(\d+)`", content)
    stats["coherence"] = int(coherence_match.group(1)) if coherence_match else 10

    velocity_match = re.search(r"\*\s*\*\*Velocity:\*\*\s*`(\d+)`", content)
    stats["velocity"] = int(velocity_match.group(1)) if velocity_match else 5

    return stats

    return stats


def parse_tags(content):
    """Extract tags from artifact content (YAML frontmatter or inline tags)."""
    tags = []
    # match tags: [tag1, tag2]
    tag_match = re.search(r"^tags:\s*\[(.*?)\]", content, re.MULTILINE)
    if tag_match:
        tags = [t.strip() for t in tag_match.group(1).split(",")]

    # Also look for hashtag style #tag (simplified)
    hashtags = re.findall(r"(?<!#)#(\w+)", content)
    tags.extend(hashtags)

    return tags


def update_artifact_text(content, stats):
    """Update RPG stats in the markdown text."""
    # Update Level
    content = re.sub(r"(\*\s*\*\*Level:\*\*\s*`)(\d+)(`)", f"\g<1>{stats['level']}\g<3>", content)

    # Update XP
    content = re.sub(
        r"(\*\s*\*\*Experience \(XP\):\*\*\s*`)(\d+)/(\d+)(`)",
        f"\g<1>{stats['xp_current']}/{stats['xp_max']}\g<3>",
        content,
    )

    # Update Stats
    content = re.sub(
        r"(\*\s*\*\*Coherence:\*\*\s*`)(\d+)(`)",
        f"\g<1>{stats['coherence']}\g<3>",
        content,
    )
    content = re.sub(
        r"(\*\s*\*\*Velocity:\*\*\s*`)(\d+)(`)",
        f"\g<1>{stats['velocity']}\g<3>",
        content,
    )

    return content

    return content


def force_level_up(target):
    """Force a level up on the target artifact."""
    content = load_artifact(target)
    stats = parse_stats(content)

    print(f"{BOLD}⚡ Forcing Level Up for {target}...{RESET}")
    # Set XP to max to trigger level up logic in a standardized way if we reused add_xp,
    # but here we just manipulate stats directly for the force command.

    stats["level"] += 1
    stats["coherence"] += 2
    stats["velocity"] += 1
    stats["xp_current"] = 0  # Reset XP on forced level up
    stats["xp_max"] = int(stats["xp_max"] * 1.5)

    print(f"{YELLOW}🎉 LEVEL UP! You are now Level {stats['level']}!{RESET}")
    print("   Coherence +2 | Velocity +1")

    new_content = update_artifact_text(content, stats)
    save_artifact(new_content, target)
    print_hud(stats)


def add_xp(amount, target=None):
    """Add XP to the default artifact."""
    content = load_artifact()
    stats = parse_stats(content)

    print(f"{BOLD}⚡ Adding {amount} XP...{RESET}")
    stats["xp_current"] += amount

    while stats["xp_current"] >= stats["xp_max"]:
        stats["xp_current"] -= stats["xp_max"]
        stats["level"] += 1
        stats["coherence"] += 2
        stats["velocity"] += 1
        stats["xp_max"] = int(stats["xp_max"] * 1.5)  # Harder to level up
        print(f"{YELLOW}🎉 LEVEL UP! You are now Level {stats['level']}!{RESET}")
        print("   Coherence +2 | Velocity +1")

    new_content = update_artifact_text(content, stats)
    new_content = update_artifact_text(content, stats)
    save_artifact(new_content, target)

    # Print HUD
    print_hud(stats)


def check_synergy(target_a, target_b):
    """Check synergy between two artifacts using CatalystWeaver."""
    if not CatalystWeaver:
        print(f"{RED}Error: CatalystWeaver logic not available.{RESET}")
        return

    print(f"{BOLD}🔗 Analyzing Synergy between {target_a} and {target_b}...{RESET}")

    try:
        content_a = load_artifact(target_a)
        content_b = load_artifact(target_b)
    except Exception as e:
        print(f"{RED}Error loading targets: {e}{RESET}")
        return

    # Extract tags
    tags_a = parse_tags(content_a)
    tags_b = parse_tags(content_b)

    # Extract IDs from filenames (simple split by _)
    # e.g. Library/1_Modules/UMB-CSE-001_Coherent... -> UMB-CSE-001
    id_a = os.path.basename(target_a).split("_")[0]
    id_b = os.path.basename(target_b).split("_")[0]

    # Mocking dictionary structure for Weaver
    art_a = {"id": id_a, "content": content_a, "tags": tags_a}
    art_b = {"id": id_b, "content": content_b, "tags": tags_b}

    weaver = CatalystWeaver()
    link = weaver.weave(art_a, art_b)

    if link:
        print(f"{GREEN}✔ Synergy Detected! Score: {link['synergy_score']}{RESET}")
        print(f"   Rationale: {link['rationale']}")
    else:
        print(f"{YELLOW}✖ Low Synergy. No link established.{RESET}")


def print_hud(stats):
    """Print the RPG HUD."""
    print(f"\n{BOLD}🛡️  THE FORGE ENGINE STATUS 🛡️{RESET}")
    print(f"{BOLD}{'=' * 30}{RESET}")
    print(f"   🏆 Level:     {CYAN}{stats['level']}{RESET}")

    # XP Bar
    pct = stats["xp_current"] / stats["xp_max"]
    bar_len = 20
    filled = int(pct * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)

    print(f"   ✨ XP:        [{GREEN}{bar}{RESET}] {stats['xp_current']}/{stats['xp_max']}")
    print(f"   🧠 Coherence: {YELLOW}{stats['coherence']}{RESET}")
    print(f"   🚀 Velocity:  {YELLOW}{stats['velocity']}{RESET}")
    print(f"{BOLD}{'=' * 30}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Forge Gamification CLI")
    parser.add_argument("--target", help="Target Artifact (Primary)")
    parser.add_argument("--target-b", help="Secondary Target Artifact (for Synergy checks)")
    parser.add_argument("--add-xp", type=int, help="Amount of XP to add")
    parser.add_argument("--level-up", action="store_true", help="Force a Level Up event")
    parser.add_argument("--view-stats", action="store_true", help="View current stats")
    parser.add_argument(
        "--check-synergy",
        action="store_true",
        help="Check synergy between two artifacts",
    )

    args = parser.parse_args()

    # Determine target (default to CBM-FORGE-001 if not provided, but some commands need explicit target)
    target = args.target if args.target else ARTIFACT_PATH

    if args.add_xp:
        add_xp(args.add_xp, target)
    elif args.level_up:
        force_level_up(target)
    elif args.view_stats:
        content = load_artifact(target)  # Allow viewing stats of other targets
        stats = parse_stats(content)
        print_hud(stats)
    elif args.check_synergy:
        if not args.target or not args.target_b:
            print(f"{RED}Error: --check-synergy requires --target and --target-b{RESET}")
        else:
            check_synergy(args.target, args.target_b)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
