import datetime
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

# Path Alignment for Phoenix Core
ROOT = str(Path(__file__).parents[2])
SRC_PATH = os.path.join(ROOT, "axion-core", "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

try:
    from phoenix import PhoenixBase
except ImportError:
    # Fallback for localized testing if package resolution fails
    sys.path.append(os.path.join(ROOT, "axion-core", "src"))
    from phoenix import PhoenixBase

# Constants
FORGE_SCRIPT = os.path.join(ROOT, "axion-core", "scripts", "grand_weave_refactor.py")

class KineticWeaverRitual(PhoenixBase):
    """
    Orchestrates the 'Kinetic Weaving Ritual' as a Phoenix-Class Module.
    Combines static analysis, semantic elegance checks, and atomic execution.
    """

    def __init__(self, target_dir: str, kinetic: bool = True, verbose: bool = False):
        super().__init__(persona_id="KineticWeaver", ethos="Atomic Synthesis", verbose=verbose)
        self.target_dir = os.path.abspath(target_dir)
        self.kinetic = kinetic
        self.forge_path = FORGE_SCRIPT

    def assess_elegance(self, file_path: str) -> float:
        """
        Overrides base elegance assessment with polyglot-friendly parsing.
        Calculates the 'Algorithmic Elegance Score' (AES).
        """
        # Start with base heuristic
        score = super().assess_elegance(file_path)
        
        if score <= 0:
            return 0.0

        ext = os.path.splitext(file_path)[1]
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        except:
            return score

        # Polyglot Specific Refinements
        if ext == ".py":
            # PEP8-ish check: excessive globals
            global_count = len(re.findall(r"^[A-Z_]+ = ", content, re.MULTILINE))
            if global_count > 10:
                score -= 0.5
        elif ext in [".ts", ".js"]:
            # TS check: missing types ('any' usage)
            any_count = content.count(": any") + content.count("as any")
            if any_count > 0:
                score -= min(2.0, 0.2 * any_count)
        elif ext == ".ps1":
            # PowerShell check: Write-Host usage
            if "Write-Host" in content:
                score -= 0.5

        return max(0.0, min(10.0, score))

    def run_vigil(self, script_name: str, args: list[str]) -> dict[str, Any]:
        """Runs a script with elevated monitoring and governance logging."""
        script_path = os.path.abspath(script_name)
        if not os.path.exists(script_path):
            return {"status": "ERROR", "msg": f"Script not found: {script_name}"}

        self._log_event("VIGIL", f"Starting vigil for {os.path.basename(script_name)}")

        try:
            cmd = ["python", script_path] + args
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)

            if result.returncode == 0:
                self._log_event("SUCCESS", f"Vigil for {os.path.basename(script_name)} passed.")
                return {"status": "SUCCESS", "output": result.stdout}
            else:
                self._log_event("DISSONANCE", f"Vigil failed: {result.stderr[:100]}")
                return {"status": "FAIL", "error": result.stderr}
        except Exception as e:
            self._log_event("CRASH", f"Vigil crashed: {e}")
            return {"status": "CRASH", "error": str(e)}

    def execute_ritual(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Executes the 'Kinetic Ritual'—Atomic orchestration of forging and governance.
        """
        self.don_mask("RitualOrchestrator")
        
        # 1. Assessment Phase
        elegance = self.assess_elegance(self.forge_path)
        if elegance < 5.0:
            self._log_event("ABORT", f"Ritual Aborted: AES ({elegance}) < Threshold (5.0)")
            self.finalize("ABORTED_DUE_TO_LOW_ELEGANCE")
            return {"status": "ABORTED", "reason": "Low Elegance", "AES": elegance}

        # 2. Execution (Forge Cycle)
        mode_arg = "--kinetic" if self.kinetic else "--dry-run"
        forge_result = self.run_vigil(self.forge_path, [mode_arg])

        if forge_result["status"] != "SUCCESS":
            self.finalize("FAILED_AT_FORGE")
            return forge_result

        # 3. Finalization
        self.reveal_core()
        self.finalize("SUCCESS")
        return {"status": "COMPLETED", "AES": elegance}

if __name__ == "__main__":
    # Diagnostic Run
    ritual = KineticWeaverRitual(target_dir=ROOT, kinetic=False, verbose=True)
    result = ritual.execute_ritual()
    print(f"\n[FINAL_RESULT] {result}")
