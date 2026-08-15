#!/usr/bin/env python3
# Copyright Phoenix Protocol. All rights reserved.
# GVRN.Engine.RunVerificationQuad.PY
# Master Verification Harness for the Prompt Execution Framework (PEF)

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path


class VerificationQuadRunner:
    def __init__(self, engine_file: str, bridge_file: str, bridge_header: str, library_file: str, manifest_dir: str, ledger_file: str):
        self.engine_file = Path(engine_file) if engine_file else None
        self.bridge_file = Path(bridge_file) if bridge_file else None
        self.bridge_header = Path(bridge_header) if bridge_header else None
        self.library_file = Path(library_file) if library_file else None
        self.manifest_dir = Path(manifest_dir) if manifest_dir else None
        self.ledger_file = Path(ledger_file) if ledger_file else None

        self.findings = []
        self.has_critical_error = False

    def log_finding(self, pass_name: str, level: str, message: str):
        if level == "CRITICAL":
            self.has_critical_error = True
        self.findings.append({"pass": pass_name, "level": level, "message": message})
        print(f"[{level}] [{pass_name}] {message}")

    # -------------------------------------------------------------------------
    # PASS 1: GVRN.LAW.CROSS_PORT_CONSISTENCY
    # -------------------------------------------------------------------------
    def run_cross_port_consistency(self):
        print("\n=== Running Pass 1: Cross-Port Consistency ===")
        if not self.engine_file or not self.bridge_file:
            self.log_finding("CROSS_PORT", "WARNING", "Engine or Bridge file not provided. Skipping Pass 1.")
            return

        regex = re.compile(r"(?:#|//)\s*GVRN\.CONST:\s*([A-Za-z0-9_]+)\s*=\s*([0-9\.]+)")
        
        engine_consts = {}
        if self.engine_file.exists():
            with open(self.engine_file, "r", encoding="utf-8") as f:
                for line in f:
                    match = regex.search(line)
                    if match:
                        engine_consts[match.group(1)] = float(match.group(2))

        bridge_consts = {}
        if self.bridge_file.exists():
            with open(self.bridge_file, "r", encoding="utf-8") as f:
                for line in f:
                    match = regex.search(line)
                    if match:
                        bridge_consts[match.group(1)] = float(match.group(2))

        all_keys = set(engine_consts.keys()).union(set(bridge_consts.keys()))
        for key in all_keys:
            in_engine = key in engine_consts
            in_bridge = key in bridge_consts

            if in_engine and in_bridge:
                if engine_consts[key] != bridge_consts[key]:
                    self.log_finding("CROSS_PORT", "CRITICAL", f"DRIFT DETECTED for '{key}': @engine={engine_consts[key]} vs @bridge={bridge_consts[key]}")
                else:
                    print(f"[PASS] [CROSS_PORT] Constant '{key}' matches across ports ({engine_consts[key]}).")
            elif in_engine:
                self.log_finding("CROSS_PORT", "WARNING", f"ORPHANED CONSTANT in @engine: '{key}' = {engine_consts[key]}")
            elif in_bridge:
                self.log_finding("CROSS_PORT", "WARNING", f"ORPHANED CONSTANT in @bridge: '{key}' = {bridge_consts[key]}")

    # -------------------------------------------------------------------------
    # PASS 2: GVRN.LAW.COMPILERS_OATH
    # -------------------------------------------------------------------------
    def run_compilers_oath(self):
        print("\n=== Running Pass 2: Compiler's Oath (Symbol Verification) ===")
        if not self.manifest_dir or not self.manifest_dir.exists():
            self.log_finding("COMPILERS_OATH", "WARNING", "Manifest directory missing or invalid. Skipping Pass 2.")
            return

        files_to_check = [f for f in [self.bridge_file, self.bridge_header] if f and f.exists()]
        if not files_to_check:
            self.log_finding("COMPILERS_OATH", "WARNING", "No implementation/header files found to verify.")
            return

        manifests = []
        for manifest_file in self.manifest_dir.glob("*.json"):
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifests.append(json.load(f))

        for target_file in files_to_check:
            content = target_file.read_text(encoding="utf-8")
            for manifest in manifests:
                lib_name = manifest.get("library_name", "UNKNOWN")
                
                # Check for known hallucinated anti-patterns
                for anti_pattern in manifest.get("hallucinated_anti_patterns", []):
                    if re.search(r"\b" + re.escape(anti_pattern) + r"\b", content):
                        self.log_finding("COMPILERS_OATH", "CRITICAL", f"HALLUCINATED SYMBOL in {target_file.name}: '{anti_pattern}' (Violates {lib_name} manifest)")

                # Validate legitimate symbols
                for valid_symbol in manifest.get("valid_symbols", []):
                    if re.search(r"\b" + re.escape(valid_symbol) + r"\b", content):
                        print(f"[PASS] [COMPILERS_OATH] Valid symbol '{valid_symbol}' verified in {target_file.name}.")

    # -------------------------------------------------------------------------
    # PASS 3: GVRN.LAW.SELF_REPORT_TAGGING
    # -------------------------------------------------------------------------
    def run_self_report_tagging(self):
        print("\n=== Running Pass 3: Self-Report Tagging ===")
        if not self.library_file or not self.library_file.exists():
            self.log_finding("SELF_REPORT", "WARNING", "Library JSON file missing or not provided. Skipping Pass 3.")
            return

        try:
            data = json.loads(self.library_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            self.log_finding("SELF_REPORT", "CRITICAL", f"Invalid JSON structure in {self.library_file.name}: {str(e)}")
            return

        telemetry = data.get("telemetry_metrics", {})
        if not telemetry:
            self.log_finding("SELF_REPORT", "WARNING", "No 'telemetry_metrics' block found in JSON log.")
            return

        for key, metric in telemetry.items():
            if not isinstance(metric, dict) or "value" not in metric or "provenance" not in metric:
                self.log_finding("SELF_REPORT", "CRITICAL", f"UNTAGGED METRIC '{key}': Must be a {{value, provenance}} pair.")
            else:
                prov = metric["provenance"]
                if prov not in ["MEASURED", "SELF_REPORTED"]:
                    self.log_finding("SELF_REPORT", "CRITICAL", f"INVALID PROVENANCE '{prov}' on '{key}': Must be 'MEASURED' or 'SELF_REPORTED'.")
                else:
                    print(f"[PASS] [SELF_REPORT] Metric '{key}' properly tagged with provenance='{prov}'.")

    # -------------------------------------------------------------------------
    # PASS 4: GVRN.LAW.WANING_SEAL
    # -------------------------------------------------------------------------
    def run_waning_seal(self):
        print("\n=== Running Pass 4: Waning Seal (Verification Decay) ===")
        if not self.ledger_file:
            self.log_finding("WANING_SEAL", "WARNING", "Ledger path not provided. Skipping Pass 4.")
            return

        ledger_data = {"records": []}
        if self.ledger_file.exists():
            try:
                ledger_data = json.loads(self.ledger_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.log_finding("WANING_SEAL", "WARNING", "Corrupted ledger JSON. Resetting ledger.")

        active_files = [f for f in [self.engine_file, self.bridge_file, self.bridge_header, self.library_file] if f and f.exists()]
        existing_records = {r["artifact_path"]: r for r in ledger_data.get("records", [])}

        updated_records = []
        for file_path in active_files:
            path_str = str(file_path).replace("\\", "/") # standardize path separators to unix slash for cross-platform compatibility
            content_bytes = file_path.read_bytes()
            current_hash = hashlib.sha256(content_bytes).hexdigest()

            if path_str in existing_records:
                expected_hash = existing_records[path_str]["content_sha256"]
                if current_hash == expected_hash:
                    print(f"[PASS] [WANING_SEAL] {file_path.name} hash matches ledger (STILL_VALID).")
                else:
                    self.log_finding("WANING_SEAL", "CRITICAL", f"VERIFICATION VOID for {file_path.name}: File content modified since last pass (STALE).")
            else:
                print(f"[NEW] [WANING_SEAL] Registering new artifact hash for {file_path.name}.")

            updated_records.append({
                "artifact_path": path_str,
                "content_sha256": current_hash,
                "status": "STILL_VALID" if not self.has_critical_error else "FAILED"
            })

        # Commit back to ledger
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
        self.ledger_file.write_text(json.dumps({"records": updated_records}, indent=2), encoding="utf-8")
        print(f"[INFO] [WANING_SEAL] Ledger committed to {self.ledger_file}")

    def execute_all(self) -> int:
        print("================================-------------------")
        print("   PEF VERIFICATION QUAD MASTER HARNESS (v1.0)   ")
        print("================================-------------------")
        
        self.run_cross_port_consistency()
        self.run_compilers_oath()
        self.run_self_report_tagging()
        self.run_waning_seal()

        print("\n=== FINAL AUDIT SUMMARY ===")
        if self.has_critical_error:
            print("RESULT: FAILED // CRITICAL FINDINGS DETECTED")
            return 1
        else:
            print("RESULT: PASSED // ALL VERIFICATION GATES SATISFIED")
            return 0


def main():
    parser = argparse.ArgumentParser(description="Run the PEF Verification Quad Gates.")
    parser.add_argument("--engine", help="Path to @engine python specification file.")
    parser.add_argument("--bridge", help="Path to @bridge C++ implementation file.")
    parser.add_argument("--header", help="Path to @bridge C++ header file.")
    parser.add_argument("--library", help="Path to @library JSON log file.")
    parser.add_argument("--manifests", default="_governance/known_api_symbols", help="Path to API manifests directory.")
    parser.add_argument("--ledger", default="library/logs/verification_ledger.json", help="Path to verification decay ledger.")

    args = parser.parse_args()

    runner = VerificationQuadRunner(
        engine_file=args.engine,
        bridge_file=args.bridge,
        bridge_header=args.header,
        library_file=args.library,
        manifest_dir=args.manifests,
        ledger_file=args.ledger
    )

    sys.exit(runner.execute_all())


if __name__ == "__main__":
    main()
