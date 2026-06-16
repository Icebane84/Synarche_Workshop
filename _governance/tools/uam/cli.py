"""
artifact_anchor:
  id: GVRN.CLI.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: GVRN
  celestial_class: STAR
  tier: GOVERNANCE
  state: ACTIVE
  ethos: SOVEREIGN_GOVERNANCE_COMPONENT
  relations: []
"""

# UAM Orchestrator CLI
# Combines all modular modules into the 9-stage verification/enforcement pipeline

import os
import sys
from .crawler import WorkspaceCrawler
from .parser import ArtifactParser
from .validator import ArtifactValidator
from .compiler import TopologyCompiler
from .analyzer import TopologicalAnalyzer
from .reporter import DiagnosticReporter
from .reconciler import Reconciler


def execute_pipeline(target_dir: str, mode: str = "lint", scope: str = None) -> bool:
    """Orchestrates the formal 9-stage Architectural Governance compiler sequence."""

    # Instantiate Pipeline Core classes
    crawler = WorkspaceCrawler(target_dir, tier_scope=scope)
    parser = ArtifactParser()
    validator = ArtifactValidator()
    compiler = TopologyCompiler(target_dir)
    reconciler = Reconciler()

    DiagnosticReporter.print_section_header("UIP-V15 GOVERNANCE COMPILER")
    print(f"Target Directory: {target_dir}")
    print(f"Execution Mode:   {mode.upper()}")
    print(f"Tier Scope:       {scope or 'Standard Workspace (Tier 1-3)'}\n")

    # Phase 1: Discovery
    matched_files = crawler.discover_files()

    processed_count = 0
    modified_count = 0
    local_errors = 0
    local_warnings = 0
    failures = []

    for file_path in matched_files:
        processed_count += 1
        rel_path = os.path.relpath(file_path, target_dir)
        _, ext = os.path.splitext(file_path)

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Phase 2: Extraction
            anchor_data, docstring_text, raw_block = parser.extract_anchor(
                file_path, content
            )

            new_content = content
            diagnostics = []
            final_metadata = None

            if anchor_data:
                # Phase 3 & 4: Validation and Semantic Analysis
                fixed_data, corrections = validator.propose_auto_corrections(
                    anchor_data
                )
                final_metadata = fixed_data

                # Check Schema shapes
                schema_errors = validator.run_schema_validation(fixed_data)
                for se in schema_errors:
                    diagnostics.append({"severity": "ERROR", "msg": se})

                # Check bidirectional imports
                drifts = validator.run_semantic_drift_analysis(
                    file_path, content, fixed_data.get("relations", [])
                )
                for d in drifts:
                    diagnostics.append({"severity": "WARNING", "msg": d})

                for c in corrections:
                    diagnostics.append({"severity": "INFO", "msg": c})

                # Check for missing prettier-ignore safety wrapper
                lacks_ignore = False
                if ext in (".js", ".ts") and "// prettier-ignore" not in raw_block:
                    lacks_ignore = True
                    diagnostics.append(
                        {
                            "severity": "INFO",
                            "msg": "Propose: Add prettier-ignore formatting safety flag",
                        }
                    )
                elif ext == ".html" and "prettier-ignore" not in raw_block:
                    lacks_ignore = True
                    diagnostics.append(
                        {
                            "severity": "INFO",
                            "msg": "Propose: Add prettier-ignore formatting safety flag",
                        }
                    )

                # Compute potential modifications
                if corrections or schema_errors or drifts or lacks_ignore:
                    wrapped = reconciler.wrap_anchor_block(fixed_data, ext)
                    if ext == ".py" and raw_block:
                        new_content = content.replace(raw_block, wrapped)
                    else:
                        match = parser.anchor_regex.search(content)
                        if match:
                            new_content = content.replace(match.group(0), wrapped)
            else:
                # Missing Anchor Block
                diagnostics.append(
                    {
                        "severity": "ERROR",
                        "msg": "Missing mandatory artifact_anchor block",
                    }
                )
                inferred = crawler.infer_metadata(file_path)
                final_metadata = inferred
                wrapped = reconciler.wrap_anchor_block(inferred, ext)
                new_content = f"{wrapped}\n\n{content}"
                diagnostics.append(
                    {"severity": "INFO", "msg": f"Inferred block layout: {inferred}"}
                )

            # Phase 5: Register Node for Global compiling
            if final_metadata and "id" in final_metadata:
                compiler.register_node(final_metadata["id"], final_metadata, rel_path)

            file_has_errors = any(d["severity"] == "ERROR" for d in diagnostics)
            file_has_warnings = any(d["severity"] == "WARNING" for d in diagnostics)

            if file_has_errors:
                local_errors += 1
            if file_has_warnings:
                local_warnings += 1

            # Phase 7: Diagnostics (Structured file-level reporting)
            if diagnostics:
                DiagnosticReporter.print_file_diagnostics(rel_path, diagnostics)

                # Phase 8: Reconciliation
                if mode == "interactive":
                    if reconciler.prompt_interactive_reconciliation(
                        file_path, diagnostics
                    ):
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        modified_count += 1
                        print("  ✅ Applied changes permanently.")
                elif mode == "write-all":
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    modified_count += 1
                    print("  ✅ Auto-applied changes permanently.")

        except Exception as e:
            failures.append((rel_path, str(e)))
            print(f"[CRITICAL FAIL] {rel_path} | Error: {e}")

    # Phase 6: Topological & Semantic Verification (Ref target check, Tarjan's SCC, Tier layering, Ontological Lexicon)
    analyzer = TopologicalAnalyzer(target_dir, compiler.registry)
    global_errors = analyzer.validate_referential_integrity()
    global_errors.extend(analyzer.validate_tier_crossings())

    # Run V3/V4 Semantic Boundary Checks
    semantic_leaks = analyzer.validate_semantic_boundaries()
    global_errors.extend(semantic_leaks)

    scc_cycles = analyzer.detect_cycle_clusters_tarjan()

    DiagnosticReporter.print_global_audit_results(global_errors, scc_cycles)

    # Phase 9: Export compiled Intermediate Representation topology JSON (with embedded Lexicon)
    try:
        compiler.export_ir_json(global_errors, scc_cycles)
    except Exception as e:
        print(f"[EXPORT ERROR] Graph serialization failed: {e}")

    # Output total diagnostics run summary block
    DiagnosticReporter.print_execution_summary(
        processed=processed_count,
        errors=local_errors,
        warnings=local_warnings,
        sccs=len(scc_cycles),
        modified=modified_count,
        fails=len(failures),
        mode=mode,
    )

    success = local_errors == 0 and len(global_errors) == 0 and len(failures) == 0
    return success


def find_workspace_root(start_path: str) -> str:
    """Recursively walks upwards from a start path to locate the true workspace root containing .agent or .git."""
    curr = os.path.abspath(start_path)
    for _ in range(10):
        if os.path.exists(os.path.join(curr, ".git")) or os.path.exists(
            os.path.join(curr, ".agent")
        ):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    # Fallback default
    return os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(start_path)))
    )


def main():
    target_directory = find_workspace_root(__file__)
    exec_mode = "lint"
    scope = None

    args = sys.argv[1:]
    if "--write-all" in args:
        exec_mode = "write-all"
        args.remove("--write-all")
    elif "--interactive" in args:
        exec_mode = "interactive"
        args.remove("--interactive")

    for i, arg in enumerate(args):
        if arg == "--scope" and i + 1 < len(args):
            scope = args[i + 1]
            break

    success = execute_pipeline(target_directory, mode=exec_mode, scope=scope)
    sys.exit(0 if success else 1)
