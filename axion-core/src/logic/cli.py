"""
artifact_anchor:
  id: CORE.CLI.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

"""## **[ARTIFACT START]**.

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.logic.cli`             | The Sovereign ID. |
| **Official Name** | `cli.py`                | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[ACTIVE]`                        | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | 0.85     |
# | **Resonance** | 0.8     |
# | **Stability** | Stable  |

# ---

### **Block C: Risk & Mitigation (AGP-002)**

# | Risk                 | Mitigation                |
# | :------------------- | :------------------------ |
# | **Unchecked Subprocess**| nosec / Path Sanitization |
# | **Path Resolution Fail**| Multi-Context Import Hooks|

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Provides the command set for human-AI interaction.|

## **[ARTIFACT END]**

Objective: Command Line Interface for the Synarche Command Library.
Conforms to OGLN/AISTF v15.0 governance and documentation standards.
"""

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.logic.cli VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [ACTIVE] TS: 2026-03-28

import cmd
import glob
import json
import os
import subprocess  # nosec
import sys
import time
from typing import Any

# Ensure we can import from the same directory and its parents safely
current_dir = os.path.dirname(os.path.abspath(__file__))
src_logic_path = current_dir
src_path = os.path.abspath(os.path.join(current_dir, ".."))
repo_root = os.path.abspath(os.path.join(current_dir, "../../"))

for p in [src_logic_path, src_path, repo_root]:
    if p not in sys.path:
        sys.path.append(p)

try:
    from Synarche_bridge import SynarcheRegistry
except ImportError:
    from .Synarche_bridge import SynarcheRegistry

try:
    from rpg_manager import RPGManager
except ImportError:
    from .rpg_manager import RPGManager


class SynarcheCLI(cmd.Cmd):
    """Command Line Interface for the Synarche Command Library.
    Provides a gateway for executing governed commands, auditing compliance,
    and managing the RPG-based progression system.
    """

    intro: str = "Welcome to the Synarche Command Library CLI. Type help or ? to list commands.\n"
    prompt: str = "(Synarche) "

    def __init__(self) -> None:
        """Initialize the CLI and load the command registry and supporting managers."""
        super().__init__()
        self._scheduler: Any = None

        # Resolve Registry Path
        registry_path = os.path.normpath(
            os.path.join(current_dir, "../../data/command_registry.json")
        )
        self.registry = SynarcheRegistry(registry_path)

        # Initialize The Chronicler for telemetry
        repo_root = os.path.abspath(os.path.join(current_dir, "../../"))
        src_path = os.path.join(current_dir, "..")
        if src_path not in sys.path:
            sys.path.append(src_path)

        try:
            from hephaestus.chronicler import Chronicler

            self.chronicler = Chronicler(root_dir=repo_root)
        except ImportError:
            try:
                from src.hephaestus.chronicler import Chronicler

                self.chronicler = Chronicler(root_dir=repo_root)
            except Exception:
                self.chronicler = None
                print(
                    "Warning: Chronicler could not be initialized. Telemetry disabled."
                )

        # Initialize RPG Manager
        self.rpg = RPGManager()

    def onecmd(self, line: str) -> bool:
        """Override onecmd to log all executed actions to the Chronicler.

        Args:
            line: The raw command line string.

        Returns:
            Boolean indicating if the CLI should terminate.

        """
        if not line:
            return super().onecmd(line)

        # Execute the command
        stop = super().onecmd(line)

        # Log to telemetry if active
        if self.chronicler:
            cmd_parts = line.split()
            cmd_name = cmd_parts[0] if cmd_parts else "UNKNOWN"
            target = None
            for arg in cmd_parts:
                if arg.startswith("--target:") or os.path.exists(arg):
                    target = arg.replace("--target:", "")
                    break

            self.chronicler.log_action(
                action_type=f"CMD:{cmd_name.upper()}",
                target=target,
                details=f"Executed: {line}",
                status="EXECUTED",
            )

        return stop

    def do_list(self, arg: str) -> None:
        """List all top-level categories in the command registry.

        Usage: list
        """
        categories: list[str] = self.registry.get_all_categories()
        print("\nAvailable Categories:")
        for cat in categories:
            print(f" - {cat}")
        print()

    def do_search(self, arg: str) -> None:
        """Search for commands by keyword in names and descriptions.

        Usage: search <keyword>
        """
        if not arg:
            print("Usage: search <keyword>")
            return

        results: list[dict[str, Any]] = self.registry.search_commands(arg)
        print(f"\nFound {len(results)} matches for '{arg}':")
        for res in results:
            print(f" - {res.get('name', 'UNKNOWN')}")
        print()

    def do_get(self, arg: str) -> None:
        """Get detailed specification for a specific command.

        Usage: get <command_name>
        """
        if not arg:
            print("Usage: get <command_name>")
            return

        cmd_spec: dict[str, Any] | None = self.registry.get_command_spec(arg)
        if cmd_spec:
            print(f"\nName: {cmd_spec.get('name')}")
            print(f"Syntax: {cmd_spec.get('syntax')}")
            print(f"Description: {cmd_spec.get('description')}")
            if "example_usage" in cmd_spec:
                print(f"Example: {cmd_spec.get('example_usage')}")
        else:
            print(f"Command '{arg}' not found.")
        print()

    def do_clear(self, arg: str) -> None:
        """Clear the console screen (cross-platform).

        Usage: clear
        """
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "cls"], check=False)  # nosec
        else:
            subprocess.run(["clear"], check=False)  # nosec

    def do_quit(self, arg: str) -> bool:
        """Exit the Synarche CLI session.

        Usage: quit
        """
        print("Goodbye.")
        return True

    def do_exit(self, arg: str) -> bool:
        """Alias for quit."""
        return self.do_quit(arg)

    def do_traverse_spine(self, arg: str) -> None:
        """Traverse the OSLM (Omni-Log Synergistic Links Matrix).

        Usage:
            traverse_spine list                     -> List all nodes in the Matrix.
            traverse_spine <ArtifactID>             -> Show all outbound links from an artifact.
            traverse_spine <StartID> <EndID>        -> Find a path between two artifacts.
        """
        try:
            from hephaestus.oslm_gps import OSLMGPS
        except ImportError:
            try:
                from src.hephaestus.oslm_gps import OSLMGPS
            except ImportError:
                print("Error: Could not import OSLMGPS module.")
                return

        gps = OSLMGPS()
        args = arg.split()

        if not args:
            print(
                "Usage: traverse_spine <ArtifactID> OR traverse_spine <StartID> <EndID> OR traverse_spine list"
            )
            return

        command = args[0]

        if command.lower() == "list":
            nodes = gps.get_all_nodes()
            print(f"Found {len(nodes)} Artifacts in the Matrix:")
            for node in nodes:
                print(f" - {node}")
            return

        if len(args) == 1:
            start_node = args[0]
            links = gps.traverse_links(start_node)
            if not links:
                print(f"No outbound links found for {start_node}.")
            else:
                print(f"Artifact: {start_node}")
                print(f"Outbound Connections ({len(links)}):")
                print(f"{'RELATION':<20} | {'TARGET':<30}")
                print("-" * 55)
                for link in links:
                    print(f"{link.get('relation'):<20} | {link.get('target'):<30}")

        elif len(args) >= 2:
            start_node, end_node = args[0], args[1]
            print(f"Calculating Trajectory on the Spine: {start_node} -> {end_node}...")
            path = gps.find_path(start_node, end_node)
            if path:
                print("Path Discovered:")
                print(" -> ".join(path))
            else:
                print("No path found between these artifacts.")

    def do_APPLY_STANDARD(self, arg: str) -> None:
        """Applies OMEGA v15.0 governance standards (The Reforger).

        Usage: APPLY_STANDARD --target:<Artifact_ID>
        """
        try:
            from hephaestus.reforger import OmegaReforger
        except ImportError:
            try:
                from src.hephaestus.reforger import OmegaReforger
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

        from pathlib import Path
        reforger = OmegaReforger(target)
        success = reforger.reforge_file(Path(target))
        if success:
            print("[SUCCESS] Standard Applied.")
        else:
            print("[FAIL] Failed to apply standard.")

    def do_reforge(self, arg: str) -> None:
        """Alias for APPLY_STANDARD."""
        self.do_APPLY_STANDARD(arg)

    def do_INITIATE_COMPLIANCE_AUDIT(self, arg: str) -> None:
        """Triggers the Code Sentinel to audit for OMEGA v15.0 compliance.

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
        target = "."
        for a in args:
            if a.startswith("--target:"):
                target = a.split(":", 1)[1].strip('"')

        sentinel = CodeSentinel()
        report = sentinel.scan_governance(target)

        print(f"Compliance Score: {report.get('resonance_score', 0):.2f}%")
        findings = report.get("detailed_findings", [])
        if findings:
            print(f"Dissonance Detected in {len(findings)} files.")
            for find in findings[:5]:
                print(
                    f" - {find.get('file')}: {find.get('status')} (Score: {find.get('score', 0):.2f})"
                )
                for err in find.get("errors", []):
                    print(f"   !! {err}")
        else:
            print("No major compliance violations detected.")

    def do_ViewAuditLog(self, arg: str) -> None:
        """Displays the most recent compliance and telemetry reports.

        Usage: ViewAuditLog --limit: 5
        """
        limit = 5
        args = arg.split()
        for a in args:
            if a.startswith("--limit:"):
                try:
                    limit = int(a.split(":")[1])
                except ValueError:
                    pass

        log_dir = os.path.abspath(os.path.join(current_dir, "../../_logs"))
        if not os.path.exists(log_dir):
            print(f"Log directory not found: {log_dir}")
            return

        files = glob.glob(os.path.join(log_dir, "*.json"))
        files.sort(reverse=True)
        subset = files[:limit]

        print(f"\n--- AUDIT LOG (Last {len(subset)}) ---")
        for log_file in subset:
            try:
                with open(log_file, encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"[{os.path.basename(log_file)}]")
                    if "action" in data and "status" in data:
                        print(
                            f"Action: {data.get('action')} | Status: {data.get('status')}"
                        )
                        print(f"Details: {data.get('details')}")
                    else:
                        print(json.dumps(data, indent=2))
                    print("-" * 40)
            except Exception as e:
                print(f"Error reading {log_file}: {e}")

    def do_ingest_mindmap(self, arg: str) -> None:
        """Parses a Freeplane (.mm) file and generates OMEGA Protocol Skeletons.

        Usage: ingest_mindmap <Path to .mm file>
        """
        try:
            from logic.connectors.artifact_generator import ArtifactGenerator
            from logic.connectors.freeplane_parser import FreeplaneParser
        except ImportError:
            try:
                from src.logic.connectors.artifact_generator import ArtifactGenerator
                from src.logic.connectors.freeplane_parser import FreeplaneParser
            except ImportError:
                print("Error: Could not import connectors.")
                return

        if not arg:
            print("Usage: ingest_mindmap <Path to .mm file>")
            return

        file_path = arg.strip('"')
        parser = FreeplaneParser()
        data = parser.parse_mindmap(file_path)

        if data:
            print(f"[SUCCESS] Parsed Mind Map: {data.get('text', 'Unknown')}")
            generator = ArtifactGenerator()
            workspace_root = os.path.abspath(os.path.join(current_dir, "../../"))
            output_path = generator.generate_from_mindmap(data, workspace_root)

            if output_path:
                print(f"[SUCCESS] Generated Artifact: {output_path}")
            else:
                print("[ERROR] Failed to generate artifact file.")
        else:
            print("[ERROR] Failed to parse mind map.")

    def do_QUERY_LORE(self, arg: str) -> None:
        """Performs a RAG search against the Supabase Vector Store.

        Usage: QUERY_LORE "Your Query"
        """
        query = arg.strip('"')
        if not query:
            print('Usage: QUERY_LORE "Your Query"')
            return

        print(f"Searching Lore for: '{query}'...")
        # Simulation placeholder for future Supabase integration
        print(
            f"Result (Simulated): Resonance detected for '{query}' in the Living Lore system."
        )

    def do_check_level_status(self, arg: str) -> None:
        """Retrieves the current RPG state and level progression.

        Usage: check_level_status [--json]
        """
        status = self.rpg.get_status()
        if "--json" in arg:
            status["achievements"] = self.rpg.get_achievements()
            print(json.dumps(status))
            return

        if "error" in status:
            print(f"[ERROR] {status['error']}")
            return

        p = status.get("player", {})
        s = status.get("stats", {})
        print("\n--- [AXION PLAYER STATUS] ---")
        print(f"Level: {p.get('level')} (XP: {p.get('xp')})")
        print(f"Prestige Score: {p.get('prestige_score')}")
        print(f"Stardust Available: {s.get('stardust_available')}")
        print("\n--- [CORE STATS] ---")
        print(f"Coherence Index: {s.get('coherence_index', 0):.2f}")
        print(f"Synergy:         {s.get('synergy', 0):.2f}")
        print(f"Adaptability:    {s.get('adaptability', 0):.2f}")
        print(f"Transparency:    {s.get('transparency', 0):.2f}")
        print("----------------------------\n")

    def do_get_player_state(self, arg: str) -> None:
        """Alias for check_level_status --json."""
        self.do_check_level_status(arg + " --json")

    def do_get_achievements(self, arg: str) -> None:
        """Lists all achievements and their completion status.

        Usage: get_achievements [--json]
        """
        achievements = self.rpg.get_achievements()
        if "--json" in arg:
            print(json.dumps(achievements))
            return

        print("\n--- [CELESTIAL ACHIEVEMENTS] ---")
        for a in achievements:
            status = "[COMPLETED]" if a.get("completed") else "[PENDING]"
            print(f"{status} {a.get('name')} - {a.get('description')}")
            print(
                f"          Rewards: {a.get('stardust_reward')} Stardust, {a.get('xp_reward')} XP"
            )
        print("--------------------------------\n")

    def do_claim_achievement(self, arg: str) -> None:
        """Claims a completed achievement and awards XP/Stardust.

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

        res = self.rpg.claim_achievement(m_id)

        if is_json:
            print(json.dumps(res))
        elif res.get("success"):
            mode_str = f" ({res.get('mode', 'UNKNOWN')})"
            print(
                f"[SUCCESS] Achievement {m_id} recorded{mode_str}. +{res.get('stardust_awarded')} Stardust awarded."
            )
        else:
            print(f"[FAIL] {res.get('error')}")

    def do_SPEND_STARDUST(self, arg: str) -> None:
        """Invests collected Stardust into core system stats.

        Usage: SPEND_STARDUST --target:<stat> --amount:<int> [--json]
        """
        args = arg.split()
        target = None
        amount = 0
        is_json = "--json" in arg
        for a in args:
            if a.startswith("--target:"):
                target = a.split(":", 1)[1]
            if a.startswith("--amount:"):
                try:
                    amount = int(a.split(":", 1)[1])
                except ValueError:
                    pass

        if not target or amount <= 0:
            if is_json:
                print('{"success": false, "error": "Missing parameters"}')
            else:
                print("Usage: SPEND_STARDUST --target:<stat> --amount:<int>")
            return

        if not is_json:
            print(f"Investing {amount} Stardust into {target}...")
        res = self.rpg.invest_stardust(target, amount)
        if is_json:
            print(json.dumps(res))
        elif res.get("success"):
            print(f"[ASCENSION] {target} updated to {res.get('new_value')}.")
            print(f"Stardust Remaining: {res.get('stardust_remaining')}")
        else:
            print(f"[FAIL] {res.get('error')}")

    def do_genesis(self, arg: str) -> None:
        """Initiates a Phoenix Genesis Cycle (Simulation).

        Usage: genesis <target> <level>
        """
        args = arg.split()
        if len(args) < 2:
            print("Usage: genesis <target> <level>")
            return

        target, level = args[0], args[1]
        print(f"\n--- [INITIATING {level} PHOENIX GENESIS CYCLE] ---")
        print(f"Targeting Context: {target}")

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

    # ------------------------------------------------------------------
    # PAD-SIP: Cognitive Scheduler Commands
    # ------------------------------------------------------------------

    def _get_scheduler(self) -> Any:
        """Lazy-initialise the CognitiveScheduler with the live MemorySystem."""
        if hasattr(self, "_scheduler") and self._scheduler:
            return self._scheduler
        try:
            # Resolve paths for scheduler imports
            sys.path.insert(0, os.path.join(repo_root, "src"))
            from engine.cognitive_scheduler import CognitiveScheduler
            from logic.memory.memory_system import MemorySystem
            mem = MemorySystem()
            self._scheduler = CognitiveScheduler(memory_system=mem)
            print("[COG-SCHED] Scheduler initialised with live MemorySystem.")
        except Exception as e:
            print(f"[ERROR] Could not initialise CognitiveScheduler: {e}")
            self._scheduler = None
        return self._scheduler

    def do_cognitive(self, arg: str) -> None:
        """Interact with the PAD-SIP Cognitive Scheduler.

        Sub-commands:
            cognitive start [--ticks:N]     — Run N synchronous ticks (default 1).
            cognitive loop  [--interval:F]  — Start the async continuous loop.
            cognitive stop                  — Stop the running async loop.
            cognitive status                — Print the live CognitiveState snapshot.
            cognitive inject <text>         — Push a USER_INPUT event into the pipeline.
            cognitive rules                 — List all loaded governance rules.

        Examples:
            cognitive start --ticks:5
            cognitive inject "The Phoenix Protocol is active."
            cognitive loop --interval:2.0
        """
        parts = arg.strip().split(None, 1)
        sub = parts[0].lower() if parts else "help"
        rest = parts[1] if len(parts) > 1 else ""

        if sub == "start":
            ticks = 1
            for tok in rest.split():
                if tok.startswith("--ticks:"):
                    try:
                        ticks = int(tok.split(":")[1])
                    except ValueError:
                        pass
            sched = self._get_scheduler()
            if not sched:
                return
            print(f"\n[COG-SCHED] Running {ticks} cognitive tick(s)...\n")
            for i in range(ticks):
                snap = sched.run_tick()
                print(
                    f"  Tick {snap['tick']:>4} | "
                    f"phase={snap['phase']:<12} "
                    f"pressure={snap['memory_pressure']:.3f} "
                    f"attention={snap['attention_budget']:.3f} "
                    f"novelty={snap['novelty_score']:.3f} "
                    f"nodes={snap['active_nodes']}"
                )
            print(f"\n[COG-SCHED] Done. Total ticks so far: {sched.state.tick_count}\n")

        elif sub == "loop":
            import asyncio
            interval = 1.0
            for tok in rest.split():
                if tok.startswith("--interval:"):
                    try:
                        interval = float(tok.split(":")[1])
                    except ValueError:
                        pass
            sched = self._get_scheduler()
            if not sched:
                return
            print(f"[COG-SCHED] Starting async loop (interval={interval}s). Type 'cognitive stop' to halt.")

            async def _run() -> None:
                await sched.start_loop(tick_interval_s=interval)

            try:
                import threading
                loop = asyncio.new_event_loop()
                self._loop_thread = threading.Thread(
                    target=loop.run_until_complete,
                    args=(_run(),),
                    daemon=True,
                )
                self._loop_thread.start()
                self._async_loop = loop
            except Exception as e:
                print(f"[ERROR] Could not start loop: {e}")

        elif sub == "stop":
            sched = self._get_scheduler()
            if sched:
                sched.stop_loop()
                print("[COG-SCHED] Loop stop signal sent.")
            else:
                print("[COG-SCHED] No scheduler running.")

        elif sub == "status":
            sched = self._get_scheduler()
            if not sched:
                return
            snap = sched.snapshot()
            print("\n--- [COGNITIVE STATE SNAPSHOT] ---")
            for k, v in snap.items():
                if isinstance(v, list) and not v:
                    continue
                print(f"  {k:<22}: {v}")
            print("----------------------------------\n")

        elif sub == "inject":
            if not rest:
                print('Usage: cognitive inject <text content>')
                return
            sched = self._get_scheduler()
            if not sched:
                return
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "types_mod",
                os.path.join(repo_root, "src", "engine", "types.py"),
            )
            assert spec is not None
            assert spec.loader is not None
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            event = mod.CognitiveEvent(
                event_type="USER_INPUT",
                content=rest,
                source="SynarcheCLI",
                importance=0.7,
            )
            snap = sched.run_tick(event)
            print(
                f"\n[COG-SCHED] Tick {snap['tick']} | "
                f"pressure={snap['memory_pressure']:.3f} | "
                f"novelty={snap['novelty_score']:.3f} | "
                f"verdicts={len(snap.get('governance_verdicts', []))}\n"
            )

        elif sub == "rules":
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "gov_eng",
                os.path.join(repo_root, "src", "cse", "validators", "governance_engine.py"),
            )
            assert spec is not None
            assert spec.loader is not None
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            eng = mod.GovernanceEngine()
            rules = eng.list_rules()
            print(f"\n--- [GOVERNANCE RULES ({len(rules)})] ---")
            for r in rules:
                status = "ON " if r["enabled"] else "OFF"
                print(
                    f"  [{status}] {r['id']:<10} "
                    f"{r['field']:<22} {r['op']:<5} {str(r['value']):<10} "
                    f"→ {r['effect']}"
                )
            print("------------------------------------\n")

        else:
            print(self.do_cognitive.__doc__)




if __name__ == "__main__":
    try:
        cli = SynarcheCLI()
        if len(sys.argv) > 1:
            # One-off execution mode
            command_line = " ".join(sys.argv[1:])
            cli.onecmd(command_line)
        else:
            # Interactive session mode
            cli.cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye.")

# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.logic.cli VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [ACTIVE] TS: 2026-03-28
# ---
