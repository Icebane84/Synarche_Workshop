import cmd
import os
import subprocess  # nosec
import sys
from typing import Any

# Ensure we can import from the same directory safely
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from synarchy_bridge import SynarchyRegistry
except ImportError:
    # Fallback for when running from a different context
    sys.path.append(os.path.join(current_dir, "..", "src"))
    from synarchy_bridge import SynarchyRegistry

try:
    from rpg_manager import RPGManager
except ImportError:
    # Fallback
    sys.path.append(current_dir)
    from rpg_manager import RPGManager


class SynarchyCLI(cmd.Cmd):
    """
    Command Line Interface for the Synarchy Command Library.
    Attributes:
        intro (str): Welcome message displayed on startup.
        prompt (str): The CLI prompt string.
        registry (SynarchyRegistry): The registry manager instance.
    """

    # --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
    # System Slot: Passive Knowledge
    # Synergy Set: N/A
    # Primary Stat Buff: Adaptability
    # Passive Ability: The Forge's Heart (Auto-Refactor)
    # Cognitive Load Cost: Low
    # XP Award Value: 50 XP

    intro: str = "Welcome to the Synarchy Command Library CLI. Type help or ? to list commands.\n"
    prompt: str = "(synarchy) "

    def __init__(self) -> None:
        """Initialize the CLI and load the command registry."""
        super().__init__()
        # Point to data/command_registry.json
        # current_dir is src/logic
        registry_path = os.path.join(current_dir, "data", "command_registry.json")
        self.registry = SynarchyRegistry(registry_path)

        # Initialize The Chronicler
        # Repo Root is ../.. (src/logic -> src -> root)
        repo_root = os.path.join(current_dir, "..", "..")

        # Add src to sys.path to ensure hephaestus imports work
        src_path = os.path.join(current_dir, "..")
        if src_path not in sys.path:
            sys.path.append(src_path)

        try:
            from hephaestus.chronicler import Chronicler

            self.chronicler = Chronicler(root_dir=repo_root)
        except ImportError:
            # Fallback import
            try:
                from src.hephaestus.chronicler import Chronicler

                self.chronicler = Chronicler(root_dir=repo_root)
            except Exception:
                self.chronicler = None
                print("Warning: Chronicler could not be initialized. Logging disabled.")

        # Initialize RPG Manager
        self.rpg = RPGManager()

    def onecmd(self, line: str) -> bool:
        """Override onecmd to log all executed actions."""
        if not line:
            return super().onecmd(line)

        # Execute
        stop = super().onecmd(line)

        # Log
        if self.chronicler:
            cmd_parts = line.split()
            cmd_name = cmd_parts[0] if cmd_parts else "UNKNOWN"
            # Try to identify target in args
            target = None
            for arg in cmd_parts:
                if arg.startswith("--target:") or os.path.exists(arg):
                    target = arg.replace("--target:", "")
                    break

            self.chronicler.log_action(
                action_type=f"CMD:{cmd_name.upper()}", target=target, details=f"Executed: {line}", status="EXECUTED"
            )

        return stop

    def do_list(self, _: str) -> None:
        """
        List all top-level categories in the registry.
        Args:
            _: Unused argument (required by cmd.Cmd signature).
        """
        categories: list[str] = self.registry.get_all_categories()
        print("\nAvailable Categories:")
        for cat in categories:
            print(f" - {cat}")
        print()

    def do_search(self, arg: str) -> None:
        """
        Search for commands by keyword.

        Args:
            arg (str): The keyword to search for.

        Usage:
            search <keyword>
        """
        if not arg:
            print("Usage: search <keyword>")
            return

        results: list[dict[str, Any]] = self.registry.search_commands(arg)
        print(f"\nFound {len(results)} matches for '{arg}':")
        for res in results:
            print(f" - {res['name']}")
        print()

    def do_get(self, arg: str) -> None:
        """
        Get details for a specific command.

        Args:
            arg (str): The name of the command to retrieve.

        Usage:
            get <command_name>
        """
        if not arg:
            print("Usage: get <command_name>")
            return

        cmd_spec: dict[str, Any] | None = self.registry.get_command_spec(arg)
        if cmd_spec:
            print(f"\nName: {cmd_spec['name']}")
            print(f"Syntax: {cmd_spec['syntax']}")
            print(f"Description: {cmd_spec['description']}")
            if "example_usage" in cmd_spec:
                print(f"Example: {cmd_spec['example_usage']}")
        else:
            print(f"Command '{arg}' not found.")
        print()

    def do_clear(self, _: str) -> None:
        """
        Clear the console screen.
        Args:
            _: Unused argument.
        """
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "cls"], check=False)  # nosec
        else:
            subprocess.run(["clear"], check=False)  # nosec

    def do_quit(self, _: str) -> bool:
        """
        Exit the CLI.
        Returns:
            bool: True to signal the command loop to stop.
        """
        print("Goodbye.")
        return True

    def do_exit(self, _: str) -> bool:
        """Alias for quit."""
        return self.do_quit(_)

    def do_traverse_spine(self, arg):
        """
        Traverse the OSLM (Omni-Log Synergistic Links Matrix).

        Usage:
            traverse_spine list                     -> List all nodes in the Matrix.
            traverse_spine <ArtifactID>             -> Show all outbound links from an artifact.
            traverse_spine <StartID> <EndID>        -> Find a path between two artifacts.

        Examples:
            traverse_spine UMB-CSE-001
            traverse_spine UMB-CSE-001 UMB-ESF-001
        """
        try:
            from hephaestus.oslm_gps import OSLMGPS
        except ImportError:
            # Fallback if running from a different context
            try:
                from src.hephaestus.oslm_gps import OSLMGPS
            except ImportError:
                print("Error: Could not import OSLMGPS module.")
                return

        gps = OSLMGPS()
        args = arg.split()

        if not args:
            print("Usage: traverse_spine <ArtifactID> OR traverse_spine <StartID> <EndID> OR traverse_spine list")
            return

        command = args[0]

        if command.lower() == "list":
            nodes = gps.get_all_nodes()
            print(f"Found {len(nodes)} Artifacts in the Matrix:")
            for node in nodes:
                print(f" - {node}")
            return

        if len(args) == 1:
            # Show links for one node
            start_node = args[0]
            links = gps.traverse_links(start_node)
            if not links:
                print(f"No outbound links found for {start_node} (or node does not exist).")
            else:
                print(f"Artifact: {start_node}")
                print(f"Outbound Connections ({len(links)}):")
                print(f"{'RELATION':<20} | {'TARGET':<30}")
                print("-" * 55)
                for link in links:
                    print(f"{link['relation']:<20} | {link['target']:<30}")

        elif len(args) >= 2:
            # Find path
            start_node = args[0]
            end_node = args[1]
            print(f"Calculating Trajectory on the Spine: {start_node} -> {end_node}...")
            path = gps.find_path(start_node, end_node)
            if path:
                print("Path Discovered:")
                print(" -> ".join(path))
            else:
                print("No path found between these artifacts.")

    def do_APPLY_STANDARD(self, arg):
        """
        Applies Codex v10.0 and Axion governance standards (Ultimate Reforger).
        Usage: APPLY_STANDARD --target:<Artifact_ID>
        """
        try:
            from hephaestus.reforger import Reforger
        except ImportError:
            try:
                from src.hephaestus.reforger import Reforger
            except ImportError:
                print("Error: Could not import Reforger module.")
                return

        args = arg.split()
        target = None
        for a in args:
            if a.startswith("--target:"):
                target = a.split(":", 1)[1]

        if not target:
            print("Usage: APPLY_STANDARD --target:<Artifact_ID/Path>")
            return

        reforger = Reforger()
        success = reforger.apply_standard(target)
        if success:
            print("[SUCCESS] Standard Applied.")
        else:
            print("[FAIL] Failed to apply standard.")

    def do_reforge(self, arg):
        """Alias for APPLY_STANDARD."""
        self.do_APPLY_STANDARD(arg)

    def do_INITIATE_COMPLIANCE_AUDIT(self, arg):
        """
        Triggers the Code Sentinel to audit for OGLN v11.0 compliance.
        Usage: INITIATE_COMPLIANCE_AUDIT --target:<Path>
        """
        try:
            from hephaestus.sentinel import CodeSentinel
        except ImportError:
            try:
                from src.hephaestus.sentinel import CodeSentinel
            except ImportError:
                print("Error: Could not import CodeSentinel module.")
                return

        args = arg.split()
        target = None
        for a in args:
            if a.startswith("--target:"):
                target = a.split(":", 1)[1].strip('"')

        if not target:
            # Fallback to current directory if no target specified
            target = "."

        sentinel = CodeSentinel()
        report = sentinel.scan_governance(target)

        # Format output for CLI/Extension consumption
        print(f"Compliance Score: {report['resonance_score']:.2f}%")
        if report["detailed_findings"]:
            print(f"Dissonance Detected in {len(report['detailed_findings'])} files.")
            for find in report["detailed_findings"][:5]:
                print(f" - {find['file']}: {find['status']} (Score: {find['score']:.2f})")
                for err in find["errors"]:
                    print(f"   !! {err}")
        else:
            print("No major compliance violations detected.")

    def do_ViewAuditLog(self, arg):
        """
        Displays the most recent coherence reports (logs).
        Usage: ViewAuditLog --limit: 5
        """
        import glob
        import json

        # Parse limit
        limit = 5
        args = arg.split()
        for a in args:
            if a.startswith("--limit:"):
                try:
                    limit = int(a.split(":")[1])
                except ValueError:
                    pass

        # Locate logs
        # cli.py is in src/, logs are in ../_logs
        log_dir = os.path.join(current_dir, "..", "_logs")
        if not os.path.exists(log_dir):
            # Try plain logs dir if _logs fails, just in case
            log_dir = os.path.join(current_dir, "..", "logs")
            if not os.path.exists(log_dir):
                print(f"Log directory not found: {log_dir}")
                return

        # Get contents
        files = glob.glob(os.path.join(log_dir, "*.json"))
        # Sort by Name (Date is in name) Descending
        files.sort(reverse=True)

        subset = files[:limit]

        print(f"\n--- AUDIT LOG (Last {len(subset)}) ---")
        for log_file in subset:
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Pretty print minimal info
                    print(f"[{os.path.basename(log_file)}]")
                    # Handle typical Chronicler fields if present
                    if "action" in data and "status" in data:
                        print(f"Action: {data.get('action')} | Status: {data.get('status')}")
                        print(f"Details: {data.get('details')}")
                    else:
                        print(json.dumps(data, indent=2))
                    print("-" * 40)
            except Exception as e:
                print(f"Error reading {log_file}: {e}")

    def do_ingest_mindmap(self, arg):
        """
        Parses a Freeplane (.mm) file and generates Protocol Skeletons.
        Usage: ingest_mindmap <Path to .mm file>
        """
        # Imports
        try:
            from connectors.artifact_generator import ArtifactGenerator
            from connectors.freeplane_parser import FreeplaneParser
        except ImportError:
            try:
                from src.logic.connectors.artifact_generator import ArtifactGenerator
                from src.logic.connectors.freeplane_parser import FreeplaneParser
            except ImportError:
                # Local dev fallback
                from connectors.freeplane_parser import FreeplaneParser
                from connectors.artifact_generator import ArtifactGenerator

        if not arg:
            print("Usage: ingest_mindmap <Path to .mm file>")
            return

        file_path = arg.strip('"')
        parser = FreeplaneParser()
        data = parser.parse_mindmap(file_path)

        if data:
            print(f"[SUCCESS] Parsed Mind Map: {data.get('text', 'Unknown')}")

            # Generate Artifact
            generator = ArtifactGenerator()
            # Save to current workspace root (../../..) from src/logic
            # Or just use the directory of the CLI for now, user can move it.
            # Ideally, we want to save it to the Workspace root.
            workspace_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

            output_path = generator.generate_from_mindmap(data, workspace_root)

            if output_path:
                print(f"[SUCCESS] Generated Artifact: {output_path}")
            else:
                print("[ERROR] Failed to generate artifact file.")
        else:
            print("[ERROR] Failed to parse mind map.")

    def do_QUERY_LORE(self, arg):
        """
        Performs a RAG search against the Supabase Vector Store.
        Usage: QUERY_LORE "Your Query"
        """
        # Placeholder for real Supabase RAG logic
        # In a real scenario, this would import a search utility
        query = arg.strip('"')
        if not query:
            print('Usage: QUERY_LORE "Your Query"')
            return

        print(f"Searching Lore for: '{query}'...")
        # For now, simulate a match or provide a helpful message
        # TODO: Implement actual Supabase query logic here
        print(
            f"Result (Simulated): Knowledge regarding '{query}' is currently being synchronized with the Living Lore system."
        )

    def do_check_level_status(self, arg):
        """
        Retrieves the current RPG state and level from Supabase.
        Usage: check_level_status [--json]
        """
        status = self.rpg.get_status()
        if "--json" in arg:
            import json

            status["achievements"] = self.rpg.get_achievements()
            print(json.dumps(status))
            return

        if "error" in status:
            print(f"[ERROR] {status['error']}")
            return

        p = status["player"]
        s = status["stats"]
        print("\n--- [AXION PLAYER STATUS] ---")
        print(f"Level: {p['level']} (XP: {p['xp']})")
        print(f"Prestige Score: {p['prestige_score']}")
        print(f"Stardust Available: {s['stardust_available']}")
        print("\n--- [CORE STATS] ---")
        print(f"Coherence Index: {s['coherence_index']:.2f}")
        print(f"Synergy:         {s['synergy']:.2f}")
        print(f"Adaptability:    {s['adaptability']:.2f}")
        print(f"Transparency:    {s['transparency']:.2f}")
        print("----------------------------\n")

    def do_get_player_state(self, arg):
        """Alias for check_level_status --json."""
        self.do_check_level_status(arg + " --json")

    def do_get_achievements(self, arg):
        """
        Lists all achievements and their status.
        Usage: get_achievements [--json]
        """
        achievements = self.rpg.get_achievements()
        if "--json" in arg:
            import json

            print(json.dumps(achievements))
            return

        print("\n--- [CELESTIAL ACHIEVEMENTS] ---")
        for a in achievements:
            status = "[COMPLETED]" if a.get("completed") else "[PENDING]"
            print(f"{status} {a['name']} - {a['description']}")
            print(f"          Rewards: {a['stardust_reward']} Stardust, {a['xp_reward']} XP")
        print("--------------------------------\n")

    def do_claim_achievement(self, arg):
        """
        Claims a milestone and awards XP/Stardust.
        Usage: claim_achievement --id:<ID> [--json]
        """
        args = arg.split()
        m_id = None
        is_json = "--json" in arg

        for a in args:
            if a.startswith("--id:"):
                m_id = a.split(":", 1)[1]

        if not m_id:
            if is_json:
                print('{"success": false, "error": "Missing --id"}')
            else:
                print("Usage: claim_achievement --id:<MILESTONE_ID>")
            return

        if not is_json:
            print(f"Claiming achievement: {m_id}...")

        res = self.rpg.claim_achievement(m_id)

        if is_json:
            import json

            print(json.dumps(res))
        else:
            if res["success"]:
                mode_str = f" ({res.get('mode', 'UNKNOWN')})"
                print(f"[SUCCESS] Achievement {m_id} recorded{mode_str}. +{res['stardust_awarded']} Stardust awarded.")
            else:
                print(f"[FAIL] {res['error']}")

    def do_SPEND_STARDUST(self, arg):
        """
        Invests Stardust into a core stat.
        Usage: SPEND_STARDUST --target:<stat> --amount:<int>
        """
        args = arg.split()
        target = None
        amount = 0
        for a in args:
            if a.startswith("--target:"):
                target = a.split(":", 1)[1]
            if a.startswith("--amount:"):
                try:
                    amount = int(a.split(":", 1)[1])
                except ValueError:
                    pass

        if not target or amount <= 0:
            print("Usage: SPEND_STARDUST --target:<stat> --amount:<int>")
            return

        print(f"Investing {amount} Stardust into {target}...")
        res = self.rpg.invest_stardust(target, amount)
        if res["success"]:
            print(f"[ASCENSION] {target} updated to {res['new_value']}.")
            print(f"Stardust Remaining: {res['stardust_remaining']}")
        else:
            print(f"[FAIL] {res['error']}")

    def do_genesis(self, arg):
        """
        Initiates a Phoenix Genesis Cycle.
        Usage: genesis <target> <level>
        """
        args = arg.split()
        if len(args) < 2:
            print("Usage: genesis <target> <level>")
            return

        target, level = args[0], args[1]
        print(f"\n--- [INITIATING {level} PHOENIX GENESIS CYCLE] ---")
        print(f"Targeting Context: {target}")

        # Simulate the cycle and award stardust at the end
        import time

        print("1. Scanning for Dissonance...")
        time.sleep(0.5)
        print("2. Mapping Structural Synapses...")
        time.sleep(0.5)
        print("3. Executing Transclusion Patch...")
        time.sleep(0.5)

        award = 250 if level == "STANDARD" else 750
        self.rpg.award_stardust(award, f"GENESIS:{target}")

        print(f"\n[SUCCESS] Cycle Complete. {award} Stardust synthesized.")
        print("Broadcast: [TRANSCENDENCE EVENT] detected on the SignalBus.\n")


if __name__ == "__main__":
    try:
        cli = SynarchyCLI()
        if len(sys.argv) > 1:
            # One-off execution
            command_line = " ".join(sys.argv[1:])
            cli.onecmd(command_line)
        else:
            # Interactive mode
            cli.cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye.")
