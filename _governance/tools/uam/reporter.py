"""
artifact_anchor:
  id: GVRN.REPORTER.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: GVRN
  celestial_class: STAR
  tier: GOVERNANCE
  state: ACTIVE
  ethos: SOVEREIGN_GOVERNANCE_COMPONENT
  relations: []
"""

# Phase 7: Diagnostics Engine
# Formats, prints, and logs unified structural diagnostics

import sys

# Reconfigure stdout/stderr to UTF-8 for cross-platform unicode safety
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

class DiagnosticReporter:
    @staticmethod
    def print_section_header(title: str):
        print("==================================================")
        print(f"{title:^50}")
        print("==================================================")

    @staticmethod
    def print_file_diagnostics(rel_path: str, diagnostics: list[dict]):
        """Prints a structured group of warnings/errors for an individual processed file."""
        file_has_errors = any(d["severity"] == "ERROR" for d in diagnostics)
        file_has_warnings = any(d["severity"] == "WARNING" for d in diagnostics)
        
        status_tag = "FAIL" if file_has_errors else "DRIFT" if file_has_warnings else "INFO"
        print(f"\n[{status_tag}] {rel_path}")
        
        for diag in diagnostics:
            # Resilient ASCII tags to guarantee CP1252 / terminal safety on Windows
            severity_tag = f"[{diag['severity']}]"
            print(f"  {severity_tag:<9} {diag['msg']}")

    @staticmethod
    def print_global_audit_results(global_errors: list[str], scc_cycles: list[list[str]]):
        """Prints compiled topology cycle warnings and target verification errors."""
        DiagnosticReporter.print_section_header("V3 GLOBAL GRAPH COMPILATION")
        
        if global_errors:
            print(f"\n[FAIL] Found {len(global_errors)} Global Graph Architecture Errors:")
            for ge in global_errors:
                print(f"  - {ge}")
        else:
            print("\n[PASS] Referential integrity and layer directionality: PASS")

        if scc_cycles:
            print(f"\n[WARNING] Found {len(scc_cycles)} Entangled Cycle Clusters (Strongly Connected Components):")
            for cycle in scc_cycles:
                print(f"  - Loop Cluster: {' ↔ '.join(cycle)}")
        else:
            print("[PASS] Cycle cluster analysis: PASS (Zero circular dependency loops)")

    @staticmethod
    def print_execution_summary(processed: int, errors: int, warnings: int, sccs: int, modified: int, fails: int, mode: str):
        """Prints a standard, deterministically structured run summary block."""
        DiagnosticReporter.print_section_header("ENFORCEMENT RUN SUMMARY")
        print(f"Total files matched:       {processed}")
        print(f"Files with Local Errors:   {errors}")
        print(f"Files with Local Warnings: {warnings}")
        print(f"Entangled Cycle Clusters:  {sccs}")
        print(f"Files written/updated:     {modified}")
        print(f"Failures (system errors):  {fails}")
        
        if mode == "lint":
            print("\nLint audit complete. Run with '--interactive' or '--write-all' to reconcile.")
