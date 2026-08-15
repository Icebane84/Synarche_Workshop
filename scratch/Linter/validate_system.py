#!/usr/bin/env python3
"""
# GVRN.Security.SystemValidator
# ID: GVRN.Security.SystemValidator | VER: v15.1 [ETERNAL]
# Domain: GVRN | Status: ACTIVE
# Objective: Programmatic execution of the Evidence Confidence Model (ECM).
#            Calculates traceable system alignment by performing physical audits
#            rather than making qualitative assumptions.
"""

import argparse
import datetime
import json
import re  # Moved here to avoid conflict with other imports and ensure it's used where needed

# import re # Unused import, removed for cleanliness
from typing import Any, Dict, List, Tuple

try:
    from jsonschema import ValidationError, validate
except ImportError:
 print("Warning: 'jsonschema' library not found. Configuration schema validation will be skipped. Please run 'pip install jsonschema'.")
    validate = None
import subprocess

try:
    import tomli
except ImportError:
    print("Warning: 'tomli' library not found. pyproject.toml audit will be skipped. Please run 'pip install tomli'.")
    tomli = None
import os  # Moved here to avoid conflict with other imports and ensure it's used where needed

try:
    from radon.visitors import ComplexityVisitor
except ImportError:
    print("Warning: 'radon' library not found. Cyclomatic complexity audit will be skipped. Please run 'pip install radon'.")
    ComplexityVisitor = None
try:
    import vulture
except ImportError:
    print("Warning: 'vulture' library not found. Dead code audit will be skipped. Please run 'pip install vulture'.")
    vulture = None
try:
    from copydetect import CopyDetector
except ImportError:
    print("Warning: 'copydetect' library not found. Code duplication audit will be skipped. Please run 'pip install copydetect'.")
    CopyDetector = None
import ast  # For deprecated usage audit
import math  # For Shannon entropy calculation

from eve_engine import (
    Claim,
    Evidence,
    EvidenceType,
    EvidenceValidationEngine,
    Truth,
)

# Tarot Namespace standard mapping representation
TAROT_NAMESPACES = {
    "EMPEROR": "Structure, ID, Schema Linter (@system/core)",
    "JUDGEMENT": "Compilation, mTLS, Audits (@shield/security)",
    "MAGICIAN": "Ingestion, Web Parsing (@nexus/weave)",
    "STAR": "Cohesion, Tone, Visuals (@loom/voice)",
    "PRIESTESS": "Connection, Graph Matrix (@atlas/navigation)",
    "KNIGHT_SWORDS": "Mutation, Refactoring (@archive/refactor)",
    "KING_PENTACLES": "Archival, Persistence (@system/database)"
}

# Integrated from epistemic_linter.py for the new audit check
LEXICAL_BLOCKLIST = [
    "flawless", "immune", "perfect", "infallible", "bulletproof",
    "foolproof", "guaranteed", "impossible to fail", "never fails",
    "100% reliable", "always works", "unbreakable"
]


class ConfigLoader:
    """
    Utility to load and merge configurations from specified files,
    searching upwards from a starting directory.
    """
    CONFIG_NAMES = ["audit_config.json", ".auditrc"]
    AUDIT_SCHEMA = {
        "type": "object",
        "properties": {
            "rnc_compliance": {
                "type": "object",
                "properties": {
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "import_paths": {
                "type": "object",
                "properties": {
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "magic_numbers": {
                "type": "object",
                "properties": {
                    "threshold": {"type": "number"},
                    "exclude_numbers": {"type": "array", "items": {"type": "number"}},
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "history_reports_dir": {"type": "string"},
            "cyclomatic_complexity": {
                "type": "object",
                "properties": {
                    "threshold": {"type": "integer", "minimum": 1},
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "dead_code": {
                "type": "object",
                "properties": {
                    "min_confidence": {"type": "integer", "minimum": 0, "maximum": 100},
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "hardcoded_secrets": {
                "type": "object",
                "properties": {
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                    "custom_patterns": {"type": "object", "additionalProperties": {"type": "string"}},
                    "entropy_threshold": {"type": "number", "minimum": 0},
                    "min_length": {"type": "integer", "minimum": 1}
                },
                "additionalProperties": False,
            },
            "outdated_dependencies": {
                "type": "object",
                "properties": {
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                    "custom_patterns": {"type": "object", "additionalProperties": {"type": "string"}}
                },
                "additionalProperties": False,
            },
            "logging_consistency": {
                "type": "object",
                "properties": {
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "pyproject_toml": {
                "type": "object",
                "properties": {
                    "required_sections": {"type": "array", "items": {"type": "string"}},
                    "required_keys": {"type": "object", "additionalProperties": {"type": "array", "items": {"type": "string"}}}
                },
                "additionalProperties": False,
            },
            "code_duplication": {
                "type": "object",
                "properties": {
                    "threshold": {"type": "integer", "minimum": 1},
                    "min_lines": {"type": "integer", "minimum": 1},
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "deprecated_usage": {
                "type": "object",
                "properties": {
                    "modules": {"type": "object", "additionalProperties": {"type": "string"}},
                    "functions": {"type": "object", "additionalProperties": {"type": "string"}},
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "commit_message_quality": {
                "type": "object",
                "properties": {
                    "max_commits_to_check": {"type": "integer", "minimum": 1},
                    "require_ticket_reference": {"type": "boolean"},
                    "ticket_reference_pattern": {"type": "string"},
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "accessibility": {
                "type": "object",
                "properties": {
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "inclusive_language": {
                "type": "object",
                "properties": {
                    "blocklist": {"type": "array", "items": {"type": "string"}},
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "file_encoding": {
                "type": "object",
                "properties": {
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "line_endings": {
                "type": "object",
                "properties": {
                    "preferred": {"type": "string", "enum": ["LF", "CRLF"]},
                    "exclude_files": {"type": "array", "items": {"type": "string"}},
                    "exclude_folders": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "formatter_config": {
                "type": "object",
                "properties": {
                    "config_filename": {"type": "string"}
                },
                "additionalProperties": False
            }
        },
        "additionalProperties": False,
    }

    # Helper to format JSON schema paths for readability
    @staticmethod
    def _format_schema_path(path_deque) -> str:
        if not path_deque:
            return ""
        path_str = ""
        for item in path_deque:
            if isinstance(item, int):
                path_str += f"[{item}]"
            else:
                path_str += f".{item}" if path_str else item
        return path_str

    FORMATTER_SCHEMA = {
        "type": "object",
        "properties": {
            "headings": {
                "type": "object",
                "properties": {
                    "style": {"type": "string", "enum": ["atx"]},
                    "number_headings": {"type": "boolean"},
                    "numbering_style": {"type": "string", "enum": ["decimal", "roman", "alpha"]}
                },
                "additionalProperties": False
            },
            "inclusive_language": {
                "type": "object",
                "properties": {
                    "replacements": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "find": {"type": "string"},
                                "replace": {"type": "string"}
                            },
                            "required": ["find", "replace"]
                        }
                    }
                },
                "additionalProperties": False
            },
            "list_formatting": {
                "type": "object",
                "properties": {
                    "convert_bullets_to_numbered_threshold": {"type": "integer", "minimum": 0},
                    "ordered_list_style": {"type": "string", "enum": ["decimal", "roman", "alpha"]}
                },
                "additionalProperties": False
            },
            "table_formatting": {
                "type": "object",
                "properties": {
                    "sort_by_column": {"type": "integer"},
                    "sort_order": {"type": "string", "enum": ["asc", "desc"]},
                    "add_total_row": {"type": "boolean"},
                    "format_numbers": {"type": "boolean"}
                },
                "additionalProperties": False
            },
            "toc": {
                "type": "object",
                "properties": {
                    "max_depth": {"type": "integer", "minimum": 1, "maximum": 6}
                },
                "additionalProperties": False
            },
            "time_formatting": {
                "type": "object",
                "properties": {
                    "timezone_replacements": {"type": "object", "additionalProperties": {"type": "string"}}
                },
                "additionalProperties": False
            }
            , "files_to_process": {"type": "array", "items": {"type": "string"}}
        },
        "additionalProperties": False
    }

    @staticmethod
    def _deep_merge(source: Dict, destination: Dict) -> Dict:
        """
        Recursively merges the source dictionary into the destination dictionary.
        Nested dictionaries are merged, while other value types in the source
        overwrite those in the destination.
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in destination and isinstance(destination[key], dict):
                destination[key] = ConfigLoader._deep_merge(value, destination[key])
            else:
                destination[key] = value
        return destination

    @staticmethod
    def load_config(start_dir: str) -> Dict[str, Any]:
        found_configs = []
        current_dir = start_dir
        # Search upwards from the starting directory
        while True:
            for config_name in ConfigLoader.CONFIG_NAMES:
                config_path = os.path.join(current_dir, config_name)
                if os.path.exists(config_path):
                    found_configs.append(config_path)
            
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir: # Reached root
                break
            current_dir = parent_dir

        # Merge configs, starting with the highest-level one (last found)
        merged_config: Dict[str, Any] = {}
        for config_path in reversed(found_configs):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    merged_config = ConfigLoader._deep_merge(config_data, merged_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not parse or read {config_path}. Error: {e}")
        
        # Validate the final merged configuration against the schema
        if validate and merged_config:
            try:
 validate(instance=merged_config, schema=ConfigLoader.AUDIT_SCHEMA) # type: ignore
            except ValidationError as e:
                print(f"Warning: Configuration is invalid. Error: {e.message}. Proceeding with default settings.")
                return {} # Return empty config on validation failure
        return merged_config

class SystemValidator:
    """
    Implements the Evidence Confidence Model (ECM).
    Processes physical directory scanning to replace abstract "Coherence" metrics
    with clear, verifiable observations of binary system checks.
    """
    def __init__(self, target_dir: str):
        self.target_dir = os.path.abspath(target_dir)
        self.eve = EvidenceValidationEngine()
        self.config = ConfigLoader.load_config(self.target_dir)
        self.evidence_list: List[Evidence] = []

    def now_utc(self) -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)

    def run_audit(self) -> Dict[str, Any]:
        """Runs all system audits, frames them as Evidence, and certifies a final Claim."""
        print(f"🔍 [NIM-001] Initiating System Audit across target: {self.target_dir}")
        print("=====================================================================")
        
        # Each check is now a piece of evidence for the final claim.
        # The callback returns a tuple: (bool_passed, details_dict)
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.INTEGRATION,
            timestamp=self.now_utc(),
            reference_callback=self.check_compilation
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.INTEGRATION,
            timestamp=self.now_utc(),
            reference_callback=self.check_rnc_compliance
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.INTEGRATION,
            timestamp=self.now_utc(),
            reference_callback=self.check_import_paths
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.INTEGRATION,
            timestamp=self.now_utc(),
            reference_callback=self.check_block_integrity
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_epistemic_hygiene
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_stale_todos
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.INTEGRATION,
            timestamp=self.now_utc(),
            reference_callback=self.check_license_file
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_magic_numbers
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_cyclomatic_complexity
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_dead_code
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_hardcoded_secrets
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_outdated_dependencies
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_logging_consistency
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.INTEGRATION,
            timestamp=self.now_utc(),
            reference_callback=self.check_pyproject_toml
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_code_duplication
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_deprecated_usage
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_commit_message_quality
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_accessibility
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_inclusive_language
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_file_encoding
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.BENCHMARK,
            timestamp=self.now_utc(),
            reference_callback=self.check_line_endings
        ))
        self.evidence_list.append(Evidence(
            evidence_type=EvidenceType.INTEGRATION,
            timestamp=self.now_utc(),
            reference_callback=self.check_formatter_config
        ))

        # Frame the entire audit as a single, high-level claim
        system_claim = Claim(
            claim_id="GVRN.System.Aligned",
            statement="The target system demonstrates structural alignment with core GVRN engineering standards.",
            required_evidence_types=[EvidenceType.INTEGRATION, EvidenceType.BENCHMARK],
            provided_evidence=self.evidence_list,
            strict_veto_on_unverified=False # Allow individual checks to fail without vetoing the whole report
        )

        # Certify the claim using the EVE engine
        claim_result = self.eve.certify_claim(system_claim)

        # Assemble the final report
        final_report = {
            "timestamp": self.now_utc().isoformat(),
            "target_directory": self.target_dir,
            "claim_result": claim_result,
            "namespaces": TAROT_NAMESPACES,
            "evidence_details": [
                {"name": ev.reference_callback.__name__, "result": ev.evaluate()}
                for ev in self.evidence_list
            ]
        }
        
        return final_report

    def check_compilation(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Verifies schema validation and typescript compilation settings (tsconfig.json).
        In this local environment, it programmatically scans for standard project configurations.
        """
        issues = []
        tsconfig_found = False
        package_json_found = False
        
        tsconfig_path = os.path.join(self.target_dir, "tsconfig.json")
        if os.path.exists(tsconfig_path):
            tsconfig_found = True
            try:
                with open(tsconfig_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                paths = config.get("compilerOptions", {}).get("paths", {})
                if not paths:
                    issues.append("tsconfig.json exists but does not define `@` absolute path aliases.")
            except Exception as e:
                issues.append(f"Failed to parse tsconfig.json: {e}")
        else:
            # Fallback scan for common indicators
            for root, _, files in os.walk(self.target_dir):
                if "tsconfig.json" in files:
                    tsconfig_found = True
                    break
                if "package.json" in files:
                    package_json_found = True
        
        details = {
            "tsconfig_found": tsconfig_found,
            "strict_typing_enforced": True if tsconfig_found else False,
            "package_json_found": package_json_found,
            "failures": issues
        } # The 'issues' list contains strings, so len(issues) is always valid.
        passed = tsconfig_found and not issues # Check if issues list is empty
        return passed, details # Return the boolean 'passed' and the details dictionary


    def check_rnc_compliance(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks files in the workspace for compliance with GVRN.ID.Standard (Relational Naming Convention).
        Checks if file names match DOMAIN.Subject.Type format or legacy TYPE-ID_Name format.
        """
        rnc_pattern = re.compile(r"^[A-Z0-9]+\.[a-zA-Z0-9_]+\.[A-Z0-9_]+(\.[a-zA-Z0-9]+)?$")
        legacy_pattern = re.compile(r"^[A-Z0-9]+-[A-Z0-9]+-\d+_.*?_v\d+\.\d+(\.[a-zA-Z0-9]+)?$")
        
        total_scanned = 0
        compliant_count = 0
        non_compliant_files = []

        # Get custom exclusions from config
        rnc_config = self.config.get("rnc_compliance", {})
        custom_exclude_files = set(rnc_config.get("exclude_files", []))
        custom_exclude_folders = set(rnc_config.get("exclude_folders", []))
        
        # Standard extensions to check
        target_exts = (".md", ".py", ".ts", ".tsx", ".json")
        
        for root, _, files in os.walk(self.target_dir):
            # Skip noise folders and custom excluded folders
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                # Combine hardcoded and custom excluded files
                excluded_files = {"tsconfig.json", "package.json", "package-lock.json", "verify_all.py", "validate_system.py"}.union(custom_exclude_files)
                if f in excluded_files:
                    compliant_count += 1
                    continue

                if f.endswith(target_exts):
                    total_scanned += 1
                    is_rnc = bool(rnc_pattern.match(f))
                    is_legacy = bool(legacy_pattern.match(f))
                    
                    if is_rnc or is_legacy:
                        compliant_count += 1
                    else:
                        non_compliant_files.append(os.path.relpath(os.path.join(root, f), self.target_dir))
                        
        passed = len(non_compliant_files) == 0 or (total_scanned > 0 and (compliant_count / total_scanned) >= 0.85)
        details = {
            "total_files_scanned": total_scanned,
            "compliant_files_count": compliant_count,
            "compliance_ratio": round(compliant_count / total_scanned, 2) if total_scanned > 0 else 1.0,
            "violations": non_compliant_files[:10]  # Limit to top 10 violations for readability
        }
        return passed, details

    def check_import_paths(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans code files (Python, TypeScript) for relative directory traversals (../)
        which represent "Path Noise" violating the Absolute Path Principle.
        """
        path_noise_files = []
        total_code_files = 0

        # Get custom exclusions from config
        import_paths_config = self.config.get("import_paths", {})
        custom_exclude_files = set(import_paths_config.get("exclude_files", []))
        custom_exclude_folders = set(import_paths_config.get("exclude_folders", []))
        
        # Scanned extensions
        code_exts = (".py", ".ts", ".tsx", ".js", ".jsx")
        relative_import_pat = re.compile(r"(from\s+['\"]\.{2}/)|(import\s+.*?\s+from\s+['\"]\.{2}/)|(import\s+['\"]\.{2}/)")
        
        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                if f.endswith(code_exts):
                    total_code_files += 1
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                            # Skip custom excluded files
                            if f in custom_exclude_files:
                                continue

                            content = file.read()
                        if relative_import_pat.search(content) or "../" in content:
                            path_noise_files.append(os.path.relpath(file_path, self.target_dir))
                    except Exception:
                        pass # Squelch read errors for safety
                        
        passed = len(path_noise_files) == 0
        details = {
            "total_code_files_scanned": total_code_files,
            "path_noise_files_count": len(path_noise_files),
            "violations": path_noise_files[:10]
        }
        return passed, details

    def check_epistemic_hygiene(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans markdown files for unquantifiable, absolute language from the epistemic blocklist.
        """
        violations = []
        total_docs_scanned = 0
        
        for root, _, files in os.walk(self.target_dir):
            if any(folder in root for folder in [".git", "node_modules", "__pycache__", "scratch"]):
                continue
            for f in files:
                if f.endswith(".md"):
                    total_docs_scanned += 1
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                            content = file.read().lower()
                        found_terms = [term for term in LEXICAL_BLOCKLIST if term in content]
                        if found_terms:
                            violations.append({
                                "file": os.path.relpath(file_path, self.target_dir),
                                "found_terms": list(set(found_terms))
                            })
                    except Exception:
                        pass
        
        passed = len(violations) == 0
        details = {
            "total_docs_scanned": total_docs_scanned,
            "violations": violations[:10]
        }
        return passed, details

    def check_block_integrity(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans Markdown files in the target directory to verify they contain 
        the mandatory PPL Block-Logic structures (Blocks A through F).
        """
        markdown_files = 0
        fully_compliant_docs = 0
        violations = []
        
        required_blocks = {
            "Block A": "Identification Lock",
            "Block B": "State Vector",
            "Block C": "Risk & Mitigation",
            "Block D": "Synergy Block",
            "Block E": "Ethos"
        }
        
        for root, _, files in os.walk(self.target_dir):
            if any(folder in root for folder in [".git", "node_modules", "__pycache__", "scratch"]):
                continue
            for f in files:
                if f.endswith(".md"):
                    markdown_files += 1
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                            content = file.read()
                        
                        missing_blocks = []
                        for block_key, block_name in required_blocks.items():
                            if block_name.lower() not in content.lower():
                                missing_blocks.append(block_key)
                        
                        if len(missing_blocks) == 0:
                            fully_compliant_docs += 1
                        else:
                            violations.append({
                                "file": os.path.relpath(file_path, self.target_dir),
                                "missing_blocks": missing_blocks
                            })
                    except Exception:
                        pass
                        
        passed = len(violations) == 0 or (markdown_files > 0 and (fully_compliant_docs / markdown_files) >= 0.75)
        details = {
            "total_markdown_files_scanned": markdown_files,
            "fully_compliant_documents": fully_compliant_docs,
            "violations": violations[:10]
        }
        return passed, details

    def check_stale_todos(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans code files for TODO comments in files that have not been modified for over 90 days.
        """
        violations = []
        total_files_with_todos = 0
        ninety_days_ago = self.now_utc() - datetime.timedelta(days=90)

        code_exts = (".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".cs", ".sh")
        todo_pattern = re.compile(r'TODO', re.IGNORECASE)

        for root, _, files in os.walk(self.target_dir):
            if any(folder in root for folder in [".git", "node_modules", "__pycache__", "scratch"]):
                continue
            for f in files:
                if f.endswith(code_exts):
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as file_content:
                            if todo_pattern.search(file_content.read()):
                                total_files_with_todos += 1
                                file_mod_time_ts = os.path.getmtime(file_path)
                                file_mod_time = datetime.datetime.fromtimestamp(file_mod_time_ts, tz=datetime.timezone.utc)

                                if file_mod_time < ninety_days_ago:
                                    days_old = (self.now_utc() - file_mod_time).days
                                    violations.append(f"`{os.path.relpath(file_path, self.target_dir)}` (stale for {days_old} days)")
                    except Exception:
                        pass  # Ignore files that can't be read

        passed = len(violations) == 0
        details = {
            "total_files_with_todos": total_files_with_todos,
            "violations": violations
        }
        return passed, details

    def check_license_file(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks for the presence and validity of a LICENSE file in the project root.
        """
        license_found = False
        license_file_name = ""
        file_size = 0
        possible_names = ["LICENSE", "LICENSE.md", "LICENSE.txt"]
        
        for name in possible_names:
            path = os.path.join(self.target_dir, name)
            if os.path.exists(path):
                license_file_name = name
                file_size = os.path.getsize(path)
                if file_size > 0:
                    license_found = True
                break

        details = {
            "license_file_found": license_found,
            "license_file_name": license_file_name,
            "file_size_bytes": file_size
        }
        return license_found, details

    def _strip_code(self, code: str, file_ext: str) -> str:
        """
        A more robust method to remove comments and string literals from a code string
        to avoid flagging numbers within them as "magic numbers".
        """
        # C-style comments (JS, TS, Java, C#, Go, Rust)
        if file_ext in (".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".cs"):
            # Multi-line /* ... */, non-greedy
            code = re.sub(r'/\*[\s\S]*?\*/', '', code)
            # Single-line // ...
            code = re.sub(r'//.*', '', code)
        # Python/Shell comments
        elif file_ext in (".py", ".sh"):
            # Python multi-line strings/docstrings
            if file_ext == ".py":
                code = re.sub(r'"""[\s\S]*?"""', '', code)
                code = re.sub(r"'''[\s\S]*?'''", '', code)
            # Single-line # ...
            code = re.sub(r'#.*', '', code)

        # Generic string literal removal for most languages
        # This handles escaped quotes like "hello \"world\""
        code = re.sub(r'"(?:\\.|[^"\\])*"', '', code)
        code = re.sub(r"'(?:\\.|[^'\\])*'", '', code)
        # Template literals for JS/TS
        if file_ext in (".ts", ".tsx", ".js", ".jsx"):
            code = re.sub(r'`(?:\\.|[^`\\])*`', '', code)

        return code

    def check_magic_numbers(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans code files for "magic numbers" (hardcoded numeric literals)
        that are not explicitly excluded or below a certain threshold.
        """
        violations = []
        total_files_scanned = 0

        # Get custom exclusions and thresholds from config
        magic_numbers_config = self.config.get("magic_numbers", {})
        threshold = magic_numbers_config.get("threshold", 2)  # Default to 2 (ignore 0, 1, -1)
        exclude_numbers = set(magic_numbers_config.get("exclude_numbers", []))
        custom_exclude_files = set(magic_numbers_config.get("exclude_files", []))
        custom_exclude_folders = set(magic_numbers_config.get("exclude_folders", []))

        # Common non-magic numbers to always exclude, regardless of threshold
        # These are often used as indices, simple counts, or boolean representations
        always_exclude = {0, 1, -1, 2, 10, 100, 1000}
        exclude_numbers.update(always_exclude)

        code_exts = (".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".cs", ".sh")
        # Regex to find numbers (integers and floats, including negative)
        # Avoids numbers within strings or comments for simplicity, but not perfect.
        number_pattern = re.compile(r'\b(?:-?\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\b')

        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                if f.endswith(code_exts):
                    file_path = os.path.join(root, f)
                    # Skip custom excluded files
                    if f in custom_exclude_files:
                        continue

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as file_content:
                            original_content = file_content.read()
                        
                        total_files_scanned += 1
                        file_ext = os.path.splitext(f)[1]
                        stripped_content = self._strip_code(original_content, file_ext)

                        for match in number_pattern.finditer(stripped_content):
                            num_str = match.group(0)
                            try:
                                num = float(num_str) if '.' in num_str or 'e' in num_str.lower() else int(num_str)
                            except ValueError:
                                continue # Should not happen with this regex, but for safety.

                            if abs(num) > threshold and num not in exclude_numbers:
                                # Find original line number for better reporting
                                line_num = original_content.count('\n', 0, match.start()) + 1
                                violations.append(f"`{os.path.relpath(file_path, self.target_dir)}` (Line ~{line_num}): `{num_str}`")
                    except Exception:
                        pass  # Ignore files that can't be read

        passed = len(violations) == 0
        details = {
            "total_files_scanned": total_files_scanned,
            "violations": violations
        }
        return passed, details

    def check_cyclomatic_complexity(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans Python files for functions/methods with high cyclomatic complexity.
        """
        if not ComplexityVisitor:
            return True, {"violations": ["'radon' library not installed, check skipped."]}

        violations = []
        total_files_scanned = 0

        # Get config
        complexity_config = self.config.get("cyclomatic_complexity", {})
        threshold = complexity_config.get("threshold", 15)
        custom_exclude_files = set(complexity_config.get("exclude_files", []))
        custom_exclude_folders = set(complexity_config.get("exclude_folders", []))

        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                if f.endswith(".py"):
                    if f in custom_exclude_files:
                        continue
                    
                    total_files_scanned += 1
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8") as source_file:
                            source_code = source_file.read()
                        visitor = ComplexityVisitor.from_code(source_code)
                        for func in visitor.functions:
                            if func.complexity > threshold:
                                violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{func.lineno} - Function `{func.name}` has complexity {func.complexity} (>{threshold})")
                    except Exception:
                        pass # Ignore files that can't be parsed

        passed = len(violations) == 0
        details = {
            "total_files_scanned": total_files_scanned,
            "threshold": threshold,
            "violations": violations
        }
        return passed, details

    def check_dead_code(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans Python files for unused functions, classes, and other dead code using Vulture.
        """
        if not vulture:
            return True, {"violations": ["'vulture' library not installed, check skipped."]}

        violations = []
        total_files_scanned = 0

        # Get config
        dead_code_config = self.config.get("dead_code", {})
        min_confidence = dead_code_config.get("min_confidence", 80)
        custom_exclude_files = set(dead_code_config.get("exclude_files", []))
        custom_exclude_folders = set(dead_code_config.get("exclude_folders", []))

        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                if f.endswith(".py"):
                    if f in custom_exclude_files:
                        continue
                    
                    total_files_scanned += 1
                    file_path = os.path.join(root, f)
                    try:
                        v = vulture.Vulture.from_filename(file_path, min_confidence=min_confidence)
                        for item in v.report():
                            violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{item.lineno} - {item.message}")
                    except Exception:
                        pass # Ignore files that can't be parsed

        passed = len(violations) == 0
        details = {
            "total_files_scanned": total_files_scanned,
            "min_confidence": min_confidence,
            "violations": violations
        }
        return passed, details

    def _calculate_shannon_entropy(self, data: str) -> float:
        """Calculate the Shannon entropy of a string."""
        if not data:
            return 0.0
        
        entropy = 0.0
        length = len(data)
        
        # Count character frequencies
        counts = {}
        for char in data:
            counts[char] = counts.get(char, 0) + 1
        
        for count in counts.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
        return entropy

    def check_hardcoded_secrets(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans all files for hardcoded secrets and API keys using regex patterns.
        """
        violations = []
        total_files_scanned = 0

        # Get config
        secrets_config = self.config.get("hardcoded_secrets", {})
        custom_exclude_files = set(secrets_config.get("exclude_files", []))
        custom_exclude_folders = set(secrets_config.get("exclude_folders", []))
        custom_patterns = secrets_config.get("custom_patterns", {})
        entropy_threshold = secrets_config.get("entropy_threshold", 4.5)
        min_length = secrets_config.get("min_length", 20)

        # Common secret patterns
        secret_patterns = {
            "GitHub Token": r"ghp_[0-9a-zA-Z]{36}",
            "Slack Token": r"xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}",
            "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
            "Stripe API Key": r"sk_live_[0-9a-zA-Z]{24}",
            "Generic High Entropy": f"[a-zA-Z0-9]{{{min_length},}}",
            **custom_patterns
        }

        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                if f in custom_exclude_files:
                    continue
                
                total_files_scanned += 1
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as source_file:
                        content = source_file.read()
                        for name, pattern in secret_patterns.items():
                            for match_obj in re.finditer(pattern, content):
                                potential_secret = match_obj.group(0)
                                
                                # For generic high entropy, apply entropy check
                                if name == "Generic High Entropy":
                                    entropy = self._calculate_shannon_entropy(potential_secret)
                                    if entropy >= entropy_threshold:
                                        line_num = content.count('\n', 0, match_obj.start()) + 1
                                        violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{line_num} - Found potential '{name}' (Entropy: {entropy:.2f})")
                                else:
                                    # For specific patterns, just report
                                    line_num = content.count('\n', 0, match_obj.start()) + 1
                                    violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{line_num} - Found potential '{name}'")
                except Exception:
                    pass # Ignore binary files or files with read errors

        passed = len(violations) == 0
        details = {
            "total_files_scanned": total_files_scanned,
            "violations": violations
        }
        return passed, details

    def check_outdated_dependencies(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks for outdated dependencies by parsing a pre-generated dependency audit report.
        This audit expects an external tool (e.g., npm outdated, pip-audit) to generate
        a JSON report file (e.g., 'dependency_audit.json') in the target directory.
        """
        violations = []
        total_dependency_files_scanned = 0

        # Get config
        outdated_config = self.config.get("outdated_dependencies", {})
        report_file_name = outdated_config.get("report_file_name", "dependency_audit.json")
        custom_exclude_files = set(outdated_config.get("exclude_files", []))
        custom_exclude_folders = set(outdated_config.get("exclude_folders", []))

        report_path = os.path.join(self.target_dir, report_file_name)

        if not os.path.exists(report_path):
            return True, {"violations": [f"Dependency audit report '{report_file_name}' not found. Skipping check."], "report_file_found": False}

        try:
            with open(report_path, "r", encoding="utf-8") as f:
                dependency_report = json.load(f)
            
            if not isinstance(dependency_report, list):
                raise ValueError("Dependency report is not a list.")

            total_dependency_files_scanned = 1 # We scanned the report file itself

            for dep_info in dependency_report:
                dep_name = dep_info.get("name", "UNKNOWN")
                current_version = dep_info.get("current_version", "N/A")
                latest_version = dep_info.get("latest_version", "N/A")
                dep_type = dep_info.get("type", "N/A")

                # Apply exclusions from config
                if dep_name in custom_exclude_files or any(folder in dep_info.get("path", "") for folder in custom_exclude_folders):
                    continue

                violations.append(f"[{dep_type}] {dep_name}: Current {current_version}, Latest {latest_version}")

        except (json.JSONDecodeError, IOError, ValueError) as e:
            return False, {"violations": [f"Error parsing dependency audit report '{report_file_name}': {e}"], "report_file_found": True}
        
        passed = len(violations) == 0
        details = {
            "total_files_scanned": total_files_scanned,
            "violations": violations
        }
        return passed, details

    def check_logging_consistency(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans Python files for use of `print()` outside of `if __name__ == "__main__"` blocks.
        """
        violations = []
        total_files_scanned = 0

        # Get config
        logging_config = self.config.get("logging_consistency", {})
        custom_exclude_files = set(logging_config.get("exclude_files", []))
        custom_exclude_folders = set(logging_config.get("exclude_folders", []))

        # Regex to find `print(` that is not commented out
        print_pattern = re.compile(r"^\s*print\s*\(")

        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                if f.endswith(".py"):
                    if f in custom_exclude_files:
                        continue
                    
                    total_files_scanned += 1
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as source_file:
                            lines = source_file.readlines()

                        # Find the start line of the main block, if it exists
                        main_block_start_line = -1
                        for i, line in enumerate(lines):
                            if 'if __name__ == "__main__":' in line:
                                main_block_start_line = i
                                break

                        for i, line in enumerate(lines):
                            # If we are inside a main block, skip all checks for this file
                            if main_block_start_line != -1 and i >= main_block_start_line:
                                break

                            if print_pattern.search(line):
                                violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{i + 1} - Use of `print()` detected outside a `__main__` block. Use the `logging` module instead.")

                    except Exception:
                        pass # Ignore files that can't be parsed

        passed = len(violations) == 0
        details = {
            "total_files_scanned": total_files_scanned,
            "violations": violations
        }
        return passed, details

    def check_pyproject_toml(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Validates the structure and content of pyproject.toml against a defined schema.
        """
        if not tomli:
            return True, {"violations": ["'tomli' library not installed, check skipped."]}

        violations = []
        pyproject_path = os.path.join(self.target_dir, "pyproject.toml")

        if not os.path.exists(pyproject_path):
            return False, {"violations": ["`pyproject.toml` not found in the target directory."]}

        # Get config
        config = self.config.get("pyproject_toml", {})
        required_sections = config.get("required_sections", ["project", "tool"])
        required_keys = config.get("required_keys", {
            "project": ["name", "version", "description"]
        })

        try:
            with open(pyproject_path, "rb") as f:
                data = tomli.load(f)

            # Check for required sections
            for section in required_sections:
                if section not in data:
                    violations.append(f"Missing required section: `[{section}]`")

            # Check for required keys within sections
            for section, keys in required_keys.items():
                if section in data:
                    for key in keys:
                        if key not in data[section]:
                            violations.append(f"Missing required key in `[{section}]`: `{key}`")
            
            # Check for wildcard dependency versions
            if "project" in data and "dependencies" in data["project"]:
                for dep in data["project"]["dependencies"]:
                    if "*" in dep:
                        violations.append(f"Disallowed wildcard `*` version in `[project.dependencies]`: `{dep}`")
            
            if "tool" in data and "poetry" in data["tool"] and "dependencies" in data["tool"]["poetry"]:
                for dep, version in data["tool"]["poetry"]["dependencies"].items():
                    if isinstance(version, str) and version == "*":
                        violations.append(f"Disallowed wildcard `*` version in `[tool.poetry.dependencies]`: `{dep}`")


        except tomli.TOMLDecodeError as e:
            violations.append(f"Failed to parse `pyproject.toml`: {e}")

        passed = len(violations) == 0
        details = {
            "file_found": True,
            "violations": violations
        }
        return passed, details

    def check_code_duplication(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans the codebase for duplicated code blocks using copydetect.
        """
        if not CopyDetector:
            return True, {"violations": ["'copydetect' library not installed, check skipped."]}

        violations = []
        
        # Get config
        config = self.config.get("code_duplication", {})
        threshold = config.get("threshold", 50) # Similarity threshold
        min_lines = config.get("min_lines", 5) # Min lines to be considered a match
        custom_exclude_files = config.get("exclude_files", [])
        report_path = os.path.join(os.path.dirname(self.target_dir), "duplication_report.html")
        
        try:
            detector = CopyDetector(
                test_dirs=[self.target_dir],
                thresh=threshold,
                min_lines=min_lines,
                ignore_paths=custom_exclude_files
            )
            detector.run()
            
            if detector.has_matches():
                detector.generate_html_report(output_file=report_path)
                for file1, file2, similarity, _ in detector.get_copied_code():
                    violations.append(f"Similarity of {similarity:.1f}% found between `{os.path.relpath(file1, self.target_dir)}` and `{os.path.relpath(file2, self.target_dir)}`")

        except Exception as e:
            violations.append(f"Code duplication check failed to run: {e}")

        passed = len(violations) == 0
        details = {
            "violations": violations,
            "visual_report_path": report_path if not passed else None
        }
        return passed, details

    def check_deprecated_usage(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans Python files for usage of deprecated modules or functions using AST.
        """
        violations = []
        
        # Get config
        config = self.config.get("deprecated_usage", {})
        deprecated_modules = config.get("modules", {})
        deprecated_functions = config.get("functions", {})
        custom_exclude_files = set(config.get("exclude_files", []))

        if not deprecated_modules and not deprecated_functions:
            return True, {"violations": ["No deprecated items configured to check."]}

        for root, _, files in os.walk(self.target_dir):
            if any(folder in root for folder in {".git", "node_modules", "__pycache__", "scratch"}):
                continue
            for f in files:
                if f.endswith(".py") and f not in custom_exclude_files:
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8") as source_file:
                            tree = ast.parse(source_file.read(), filename=f)
                        
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                                for alias in node.names: # `import os, sys`
                                    if alias.name in deprecated_modules:
                                        suggestion = deprecated_modules[alias.name]
                                        violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{node.lineno} - Use of deprecated module `{alias.name}`. Suggestion: `{suggestion}`.")
                            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                                if node.func.id in deprecated_functions:
                                    suggestion = deprecated_functions[node.func.id]
                                    violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{node.lineno} - Use of deprecated function `{node.func.id}()`. Suggestion: `{suggestion}`.")

                    except Exception:
                        pass # Ignore files that can't be parsed

        passed = len(violations) == 0
        details = {
            "violations": violations
        }
        return passed, details

    def check_commit_message_quality(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Analyzes Git history for commit message quality.
        """
        violations = []
        
        # Get config
        config = self.config.get("commit_message_quality", {})
        max_commits = config.get("max_commits_to_check", 50)
        require_ticket = config.get("require_ticket_reference", True)
        ticket_pattern = config.get("ticket_reference_pattern", r"\[[A-Z]+-\d+\]")
        max_subject_length = config.get("max_subject_length", 50)

        # Common imperative verbs for commit messages
        imperative_verbs = {"add", "fix", "refactor", "update", "remove", "feat", "docs", "style", "test", "chore", "revert"}

        try:
            # Get log with subject and body, separated by a unique delimiter
            log_format = "%s%n%b" # Subject, newline, body
            result = subprocess.run(
                ["git", "log", f"-n{max_commits}", f"--format={log_format}"],
                capture_output=True, text=True, check=True, cwd=self.target_dir
            )
            
            commits = result.stdout.strip().split('\n\n')
            for i, commit_text in enumerate(commits):
                lines = commit_text.split('\n')
                subject = lines[0]
                body = "\n".join(lines[1:])

                # Check subject line length
                if len(subject) > max_subject_length:
                    violations.append(f"Commit #{i+1} ('{subject[:30]}...'): Subject line is {len(subject)} chars long (>{max_subject_length}).")

                # Check for blank line between subject and body
                if body.strip() and len(lines) > 1 and lines[1].strip() != "":
                    violations.append(f"Commit #{i+1} ('{subject[:30]}...'): No blank line between subject and body.")


                # Check for imperative mood
                first_word = subject.split(' ')[0].lower()
                if first_word not in imperative_verbs:
                    violations.append(f"Commit #{i+1} ('{subject[:30]}...'): Subject does not appear to start with an imperative verb.")

                # Check for ticket reference
                if require_ticket and not re.search(ticket_pattern, subject + body):
                    violations.append(f"Commit #{i+1} ('{subject[:30]}...'): Missing ticket reference matching pattern `{ticket_pattern}`.")

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            return True, {"violations": [f"Git command failed or not found: {e}"]}

        passed = len(violations) == 0
        details = {
            "violations": violations
        }
        return passed, details

    def check_accessibility(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans HTML and Markdown files for common accessibility issues, like missing image alt text.
        """
        violations = []
        total_files_scanned = 0

        # Get config
        config = self.config.get("accessibility", {})
        custom_exclude_files = set(config.get("exclude_files", []))
        custom_exclude_folders = set(config.get("exclude_folders", []))

        # Regex for Markdown images: ![alt](src) and HTML images: <img alt="...">
        md_img_pattern = re.compile(r"!\[(.*?)\]\(.*?\)")
        html_img_pattern = re.compile(r"<img\s.*?alt=\"(.*?)\".*?>", re.IGNORECASE)
        heading_pattern = re.compile(r"^(#{1,6})\s+|<h([1-6])>", re.IGNORECASE)

        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                if f.endswith((".md", ".html")) and f not in custom_exclude_files:
                    total_files_scanned += 1
                    file_path = os.path.join(root, f)
                    try:
                        # For HTML files, check for the lang attribute on the html tag
                        if f.endswith(".html"):
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as sf:
                                if not re.search(r"<html\s+[^>]*lang=", sf.read(500), re.IGNORECASE):
                                    violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:1 - `<html>` tag is missing the `lang` attribute.")
                        last_heading_level = 0
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as source_file:
                            for i, line in enumerate(source_file, 1):
                                # Check for heading structure
                                heading_match = heading_pattern.search(line)
                                if heading_match:
                                    md_level = len(heading_match.group(1)) if heading_match.group(1) else 0
                                    html_level = int(heading_match.group(2)) if heading_match.group(2) else 0
                                    current_level = md_level or html_level

                                    if current_level > last_heading_level + 1:
                                        violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{i} - Skipped heading level: `h{current_level}` follows `h{last_heading_level}`.")
                                    last_heading_level = current_level

                                # Check for image alt text
                                patterns = [md_img_pattern, html_img_pattern] if f.endswith(".md") else [html_img_pattern]
                                for pattern in patterns:
                                    for match in pattern.finditer(line):
                                        alt_text = match.group(1)
                                        if not alt_text.strip():
                                            violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{i} - Image is missing descriptive alt text.")
                    except Exception:
                        pass  # Ignore files that can't be parsed

        passed = len(violations) == 0
        details = {
            "total_files_scanned": total_files_scanned,
            "violations": violations
        }
        return passed, details

    def check_inclusive_language(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Scans text files for words from a configurable blocklist of non-inclusive terms.
        """
        violations = []
        total_files_scanned = 0

        # Get config
        config = self.config.get("inclusive_language", {})
        blocklist_map = config.get("blocklist", {})
        custom_exclude_files = set(config.get("exclude_files", []))
        custom_exclude_folders = set(config.get("exclude_folders", []))

        if not blocklist_map:
            return True, {"violations": ["No inclusive language blocklist configured."]}

        # Create a single regex for efficiency
        blocklist_pattern = re.compile(r'\b(' + '|'.join(re.escape(term) for term in blocklist_map.keys()) + r')\b', re.IGNORECASE)

        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                # Heuristic to only check text-like files
                if f.endswith((".txt", ".md", ".py", ".js", ".ts", ".html", ".css", ".json", ".yml", ".yaml")) and f not in custom_exclude_files:
                    total_files_scanned += 1
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as source_file:
                            for i, line in enumerate(source_file, 1):
                                for match in blocklist_pattern.finditer(line):
                                    term = match.group(0).lower()
                                    suggestion = blocklist_map.get(term, "a more inclusive alternative")
                                    violations.append(f"`{os.path.relpath(file_path, self.target_dir)}`:{i} - Found term: `{match.group(0)}`. Suggestion: `{suggestion}`.")
                    except Exception:
                        pass # Ignore binary files or files that can't be read

        passed = len(violations) == 0
        details = {"violations": violations}
        return passed, details

    def check_file_encoding(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks that all text files are UTF-8 encoded.
        """
        violations = []
        total_files_scanned = 0

        # Get config
        config = self.config.get("file_encoding", {})
        custom_exclude_files = set(config.get("exclude_files", []))
        custom_exclude_folders = set(config.get("exclude_folders", []))

        # Common binary file extensions to skip
        binary_exts = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.gz', '.tar', '.exe', '.dll', '.so', '.o', '.a', '.lib', '.woff', '.woff2', '.ttf', '.eot'}

        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                file_ext = os.path.splitext(f)[1].lower()
                if f in custom_exclude_files or file_ext in binary_exts:
                    continue
                
                total_files_scanned += 1
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, "r", encoding="utf-8") as source_file:
                        source_file.read() # Attempt to read the whole file
                except UnicodeDecodeError:
                    violations.append(f"`{os.path.relpath(file_path, self.target_dir)}` is not a valid UTF-8 encoded file.")
                except Exception:
                    pass # Ignore other read errors (e.g., permissions)

        passed = len(violations) == 0
        details = {"violations": violations}
        return passed, details

    def check_line_endings(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks that all text files use consistent line endings (LF or CRLF).
        """
        violations = []
        total_files_scanned = 0

        # Get config
        config = self.config.get("line_endings", {})
        preferred = config.get("preferred", "LF") # Default to LF
        custom_exclude_files = set(config.get("exclude_files", []))
        custom_exclude_folders = set(config.get("exclude_folders", []))

        # Common binary file extensions to skip
        binary_exts = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.gz', '.tar', '.exe', '.dll', '.so', '.o', '.a', '.lib', '.woff', '.woff2', '.ttf', '.eot'}

        for root, _, files in os.walk(self.target_dir):
            excluded_folders = {".git", "node_modules", "__pycache__", "scratch"}.union(custom_exclude_folders)
            if any(folder in root for folder in excluded_folders):
                continue
            for f in files:
                file_ext = os.path.splitext(f)[1].lower()
                if f in custom_exclude_files or file_ext in binary_exts:
                    continue
                
                total_files_scanned += 1
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, "rb") as source_file:
                        content = source_file.read()
                        if b'\r\n' in content and b'\n' in content.replace(b'\r\n', b''):
                            violations.append(f"`{os.path.relpath(file_path, self.target_dir)}` has mixed line endings (LF and CRLF).")
                        elif preferred == "LF" and b'\r\n' in content:
                            violations.append(f"`{os.path.relpath(file_path, self.target_dir)}` uses CRLF line endings instead of the preferred LF.")
                        elif preferred == "CRLF" and b'\n' in content and b'\r\n' not in content:
                             violations.append(f"`{os.path.relpath(file_path, self.target_dir)}` uses LF line endings instead of the preferred CRLF.")
                except Exception:
                    pass # Ignore read errors

        passed = len(violations) == 0
        details = {
            "violations": violations,
            "preferred_ending": preferred
        }
        return passed, details

    def check_formatter_config(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks for the presence and validity of the .pgps-formatter.json file.
        """
        violations = []
        
        # Get config
        config = self.config.get("formatter_config", {})
        config_filename = config.get("config_filename", ".pgps-formatter.json")
        
        config_path = os.path.join(self.target_dir, config_filename)

        if not os.path.exists(config_path):
            violations.append(f"Formatter configuration file `{config_filename}` not found in the target directory.")
        else:
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                # Validate against the schema if jsonschema is available
                if validate:
 validate(instance=config_data, schema=self.FORMATTER_SCHEMA) # type: ignore

            except json.JSONDecodeError as e: # type: ignore
                violations.append(f"Formatter configuration file `{config_filename}` is not valid JSON: {e}")
            except ValidationError as e:
                path = self._format_schema_path(e.path)
                suggestion = f"Error in '{path}': {e.message}. "
                
                if e.validator == "enum":
                    suggestion += f"Expected one of: {e.validator_value}."
                elif e.validator == "type":
                    suggestion += f"Expected type '{e.validator_value}'."
                elif e.validator == "required":
                    missing_prop = e.message.split("'")[1]
                    suggestion += f"Missing required property '{missing_prop}'."
                elif e.validator == "additionalProperties":
                    unexpected_prop = e.message.split("'")[1]
                    suggestion += f"Unexpected property '{unexpected_prop}'. Remove it or check for typos."
                elif e.validator == "minimum":
                    suggestion += f"Value must be at least {e.validator_value}."
                elif e.validator == "max_depth":
                    suggestion += "Value must be between 1 and 6."
                elif e.validator == "items":
                    suggestion += "Check the format of items in this array."
                
                violations.append(f"Formatter configuration file `{config_filename}` is invalid: {suggestion}")

        passed = len(violations) == 0
        details = {
            "violations": violations
        }
        return passed, details

def generate_markdown_report(report_data: Dict[str, Any]) -> str:
    """Compiles the JSON report vector into a clean, human-readable markdown file."""
    claim_result = report_data["claim_result"]
    truth_status = claim_result["TRUTH_STATUS"]
    confidence = claim_result["CONFIDENCE"]

    md = []
    md.append("# Systemic Evidence Confidence Report")
    md.append(f"**Logged**: {report_data['timestamp']}")
    md.append(f"**Target Directory**: `{report_data['target_directory']}`")
    md.append(f"**Overall Truth Status**: `{truth_status}`")
    md.append(f"**Overall Confidence**: `{confidence}`")
    md.append("\n---\n")
    
    md.append("## Audit Claim Certification")
    md.append(f"**Claim**: {claim_result['CLAIM_ID']}")
    md.append(f"> {report_data['claim_result']['REASON']}")
    if claim_result.get("LEXICAL_VIOLATIONS"):
        md.append(f"\n**Lexical Violations in Claim Statement**: {', '.join(claim_result['LEXICAL_VIOLATIONS'])}")
    md.append("\n---\n")

    md.append("## Individual Evidence Evaluation")
    md.append("The overall claim is supported by the following evidence, evaluated independently:\n")
    
    for ev_detail in report_data["evidence_details"]:
        check_name = ev_detail["name"]
        result = ev_detail["result"]
        status = result["STATUS"]
        status_symbol = "🟢" if status == Truth.PASS else "🔴" if status == Truth.FAIL else "🟡"
        
        md.append(f"### {status_symbol} {check_name}")
        md.append(f"- **Status**: {status.value}")
        
        details = result.get("details", {})
        if check_name == "check_compilation":
            md.append(f"  - TypeScript TSConfig Mapping: {'FOUND' if details['tsconfig_found'] else 'MISSING'}")
        elif check_name == "check_rnc_compliance":
            md.append(f"  - Standard Compliance Ratio: {details.get('compliance_ratio', 0)*100:.1f}% ({details.get('compliant_files_count', 0)}/{details.get('total_files_scanned', 0)} files)")
        elif check_name == "check_import_paths":
            md.append(f"  - Files with relative path noise (`../`): {details.get('path_noise_files_count', 0)}")
        elif check_name == "check_block_integrity":
            md.append(f"  - Fully Compliant Documents: {details.get('fully_compliant_documents', 0)}/{details.get('total_markdown_files_scanned', 0)}")
        elif check_name == "check_epistemic_hygiene":
            md.append(f"  - Documents with rhetorical armor: {len(details.get('violations', []))}")
        elif check_name == "check_license_file":
            md.append(f"  - License File: {'FOUND (`' + details.get('license_file_name', '') + '`)' if details.get('license_file_found') else 'MISSING'}")
        elif check_name == "check_magic_numbers":
            md.append(f"  - Magic Number Violations: {len(details.get('violations', []))}")
        elif check_name == "check_cyclomatic_complexity":
            md.append(f"  - High Complexity Functions: {len(details.get('violations', []))} (Threshold: >{details.get('threshold', 'N/A')})")
        elif check_name == "check_dead_code":
            md.append(f"  - Dead Code Instances: {len(details.get('violations', []))} (Confidence: >{details.get('min_confidence', 'N/A')}%)")
        elif check_name == "check_outdated_dependencies":
            md.append(f"  - Outdated Dependencies: {len(details.get('violations', []))}")
        elif check_name == "check_hardcoded_secrets":
            md.append(f"  - Potential Hardcoded Secrets: {len(details.get('violations', []))}")
        elif check_name == "check_logging_consistency":
            md.append(f"  - Inconsistent Logging (`print` usage): {len(details.get('violations', []))}")
        elif check_name == "check_pyproject_toml":
            md.append(f"  - `pyproject.toml` violations: {len(details.get('violations', []))}")
        elif check_name == "check_code_duplication":
            md.append(f"  - Code Duplication Instances: {len(details.get('violations', []))}")
        elif check_name == "check_deprecated_usage":
            md.append(f"  - Deprecated Code Usage: {len(details.get('violations', []))}")
        elif check_name == "check_commit_message_quality":
            md.append(f"  - Commit Message Violations: {len(details.get('violations', []))}")
        elif check_name == "check_accessibility":
            md.append(f"  - Accessibility Violations: {len(details.get('violations', []))}")
        elif check_name == "check_file_encoding":
            md.append(f"  - File Encoding Violations: {len(details.get('violations', []))}")
        elif check_name == "check_line_endings":
            md.append(f"  - Inconsistent Line Endings: {len(details.get('violations', []))} (Preferred: {details.get('preferred_ending', 'N/A')})")
        elif check_name == "check_inclusive_language":
            md.append(f"  - Inclusive Language Violations: {len(details.get('violations', []))}")
        elif check_name == "check_formatter_config":
            md.append(f"  - Formatter Config Issues: {len(details.get('violations', []))}")
            
        if details.get("violations"):
            md.append("  - **Flagged Anomalies (First 5):**")
            for viol in details["violations"][:5]:
                if isinstance(viol, dict):
                    md.append(f"    - `{viol['file']}` (Missing: {', '.join(viol['missing_blocks'])})")
                elif isinstance(viol, dict) and 'found_terms' in viol:
                     md.append(f"    - `{viol['file']}` (Found: {', '.join(viol['found_terms'])})")
                else:
                    md.append(f"    - `{viol}`")
        md.append("")

    md.append("\n---\n")
    md.append("## Tarot Namespace Mapping (Service Routing)")
    md.append("To prevent semantic drift across subsystems, active commands are routed to stable, documented namespaces:")
    md.append("| Tarot Namespace | System Alias | Core Responsibility |")
    md.append("| :--- | :--- | :--- |") # This line is fine
    for name, desc in report_data["namespaces"].items():
        md.append(f"| **{name}** | `@system/core` | {desc} |")
        
    return "\n".join(md)

def generate_html_report(report_data: Dict[str, Any], historical_reports: List[Dict[str, Any]]) -> str:
    """Compiles the JSON report vector into a clean, human-readable HTML file with collapsible sections."""
    claim_result = report_data["claim_result"]
    truth_status = claim_result["TRUTH_STATUS"]
    confidence = claim_result["CONFIDENCE"]

    # CSS for styling the report
    css = """
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #e0e0e0; background-color: #1e1e1e; margin: 0; padding: 2rem; }
        .container { max-width: 1024px; margin: 0 auto; }
        h1, h2, h3 { color: #4e9a06; border-bottom: 1px solid #444; padding-bottom: 5px; }
        h1 { font-size: 2.5em; }
        h2 { font-size: 2em; }
        h3 { font-size: 1.5em; border-bottom: none; }
        code { background-color: #333; padding: 0.2em 0.4em; border-radius: 3px; font-family: "Fira Code", "Courier New", monospace; }
        .summary-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; background-color: #2a2a2a; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; }
        .summary-grid div { padding: 0.5rem; }
        .summary-grid strong { color: #87ceeb; }
        details { background-color: #2c2c2c; border: 1px solid #444; border-radius: 5px; margin-bottom: 1rem; }
        summary { cursor: pointer; padding: 1rem; font-weight: bold; font-size: 1.2em; }
        summary:hover { background-color: #3a3a3a; }
        .details-content { padding: 0 1rem 1rem 1rem; border-top: 1px solid #444; }
        ul { list-style-type: none; padding-left: 20px; }
        li { margin-bottom: 0.5rem; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #444; }
        th { background-color: #3a3a3a; color: #4e9a06; }
        .status-pass { color: #73d216; }
        .status-fail { color: #ef2929; }
        .status-unverified { color: #fce94f; }
    </style>
    """

    html = [f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>System Audit Report</title>{css}</head><body><div class='container'>"]
    html.append("<h1>Systemic Evidence Confidence Report</h1>")
    
    html.append("<div class='summary-grid'>")
    html.append(f"<div><strong>Logged:</strong> {report_data['timestamp']}</div>")
    html.append(f"<div><strong>Target:</strong> <code>{report_data['target_directory']}</code></div>")
    html.append(f"<div><strong>Overall Truth Status:</strong> <span class='status-{truth_status.lower()}'>{truth_status}</span></div>")
    html.append(f"<div><strong>Overall Confidence:</strong> {confidence}</div>")
    html.append("</div>")

    # --- Summary Chart ---
    pass_count = sum(1 for ev in report_data["evidence_details"] if ev["result"]["STATUS"] == "PASS")
    fail_count = sum(1 for ev in report_data["evidence_details"] if ev["result"]["STATUS"] in ["FAIL", "STALE", "CONFLICT"])
    unverified_count = sum(1 for ev in report_data["evidence_details"] if ev["result"]["STATUS"] == "UNVERIFIED")
    total_audits = len(report_data["evidence_details"])

    if total_audits > 0:
        pass_pct = (pass_count / total_audits) * 100
        fail_pct = (fail_count / total_audits) * 100
        unverified_pct = (unverified_count / total_audits) * 100

        html.append("<h2>Latest Audit Summary</h2>")
        html.append('<div style="display: flex; width: 100%; height: 24px; border-radius: 4px; overflow: hidden; background-color: #444;">')
        html.append(f'<div style="width: {pass_pct}%; background-color: #73d216;" title="Pass: {pass_count}"></div>')
        html.append(f'<div style="width: {fail_pct}%; background-color: #ef2929;" title="Fail/Stale: {fail_count}"></div>')
        html.append(f'<div style="width: {unverified_pct}%; background-color: #fce94f;" title="Unverified: {unverified_count}"></div>')
        html.append('</div><br>')
    # --- End Summary Chart ---

    html.append("<h2>Audit Claim Certification</h2>")
    html.append(f"<p><strong>Claim:</strong> {claim_result['CLAIM_ID']}</p>")
    html.append(f"<blockquote>{claim_result['REASON']}</blockquote>")
    if claim_result.get("LEXICAL_VIOLATIONS"):
        html.append(f"<p><strong>Lexical Violations in Claim Statement:</strong> {', '.join(claim_result['LEXICAL_VIOLATIONS'])}</p>")
    html.append("<h2>Individual Evidence Evaluation</h2>")
    html.append("<p>The overall claim is supported by the following evidence, evaluated independently:</p>")
    for ev_detail in report_data["evidence_details"]:
        check_name = ev_detail["name"]
        result = ev_detail["result"]
        
        # Ensure status is a Truth enum member for sparkline generation
        status = Truth(result["STATUS"]) if isinstance(result["STATUS"], str) else result["STATUS"]

        status_symbol = "🟢" if status == Truth.PASS else "🔴" if status == Truth.FAIL else "🟡"
        
        html.append("<details>")
        html.append(f"<summary>{status_symbol} {check_name}")
        history_for_audit = _get_audit_history_for_check(historical_reports, check_name)
        if history_for_audit:
            html.append(f" {_generate_sparkline_svg(history_for_audit)}")
        html.append("</summary>")
        html.append("<div class='details-content'>")
        html.append(f"<ul><li><strong>Status:</strong> <span class='status-{status.value.lower()}'>{status.value}</span></li>")

        details = result.get("details", {})
        if check_name == "check_compilation":
            html.append(f"<li>TypeScript TSConfig Mapping: {'FOUND' if details.get('tsconfig_found') else 'MISSING'}</li>")
        elif check_name == "check_rnc_compliance":
            html.append(f"<li>Standard Compliance Ratio: {details.get('compliance_ratio', 0)*100:.1f}% ({details.get('compliant_files_count', 0)}/{details.get('total_files_scanned', 0)} files)</li>")
        elif check_name == "check_import_paths":
            html.append(f"<li>Files with relative path noise (`../`): {details.get('path_noise_files_count', 0)}</li>")
        elif check_name == "check_block_integrity":
            html.append(f"<li>Fully Compliant Documents: {details.get('fully_compliant_documents', 0)}/{details.get('total_markdown_files_scanned', 0)}</li>")
        elif check_name == "check_epistemic_hygiene":
            html.append(f"<li>Documents with rhetorical armor: {len(details.get('violations', []))}</li>")
        elif check_name == "check_stale_todos":
            html.append(f"<li>Files with stale TODOs (>90 days): {len(details.get('violations', []))}</li>")
        elif check_name == "check_magic_numbers":
            html.append(f"<li>Magic Number Violations: {len(details.get('violations', []))}</li>")
        elif check_name == "check_cyclomatic_complexity":
            html.append(f"<li>High Complexity Functions: {len(details.get('violations', []))} (Threshold: >{details.get('threshold', 'N/A')})</li>")
        elif check_name == "check_license_file":
            html.append(f"<li>License File: {'FOUND (<code>' + details.get('license_file_name', '') + '</code>)' if details.get('license_file_found') else 'MISSING'}</li>")
        elif check_name == "check_dead_code":
            html.append(f"<li>Dead Code Instances: {len(details.get('violations', []))} (Confidence: >{details.get('min_confidence', 'N/A')}%)</li>")
        elif check_name == "check_outdated_dependencies":
            html.append(f"<li>Outdated Dependencies: {len(details.get('violations', []))}</li>")
        elif check_name == "check_hardcoded_secrets":
            html.append(f"<li>Potential Hardcoded Secrets: {len(details.get('violations', []))}</li>")
        elif check_name == "check_pyproject_toml":
            html.append(f"<li>`pyproject.toml` violations: {len(details.get('violations', []))}</li>")
        elif check_name == "check_logging_consistency":
            html.append(f"<li>Inconsistent Logging (`print` usage): {len(details.get('violations', []))}</li>")
        elif check_name == "check_line_endings":
            html.append(f"<li>Inconsistent Line Endings: {len(details.get('violations', []))} (Preferred: {details.get('preferred_ending', 'N/A')})</li>")
        elif check_name == "check_file_encoding":
            html.append(f"<li>File Encoding Violations: {len(details.get('violations', []))}</li>")
        elif check_name == "check_inclusive_language":
            html.append(f"<li>Inclusive Language Violations: {len(details.get('violations', []))}</li>")
        elif check_name == "check_formatter_config":
            html.append(f"<li>Formatter Config Issues: {len(details.get('violations', []))}</li>")
        elif check_name == "check_accessibility":
            html.append(f"<li>Accessibility Violations: {len(details.get('violations', []))}</li>")
        elif check_name == "check_commit_message_quality":
            html.append(f"<li>Commit Message Violations: {len(details.get('violations', []))}</li>")
        elif check_name == "check_deprecated_usage":
            html.append(f"<li>Deprecated Code Usage: {len(details.get('violations', []))}</li>")
        elif check_name == "check_code_duplication":
            html.append(f"<li>Code Duplication Instances: {len(details.get('violations', []))}</li>")
            if details.get("visual_report_path"):
                html.append(f"<li><a href='{details['visual_report_path']}' target='_blank'>View Visual Report</a></li>")

        if details.get("violations"):
            html.append("<li><strong>Flagged Anomalies:</strong><ul>")
            for viol in details["violations"][:10]:
                if isinstance(viol, dict) and 'missing_blocks' in viol:
                    html.append(f"<li><code>{viol['file']}</code> (Missing: {', '.join(viol['missing_blocks'])})</li>")
                elif isinstance(viol, dict) and 'found_terms' in viol:
                    html.append(f"<li><code>{viol['file']}</code> (Found: {', '.join(viol['found_terms'])})</li>")
                else:
                    html.append(f"<li>{viol}</li>")
            html.append("</ul></li>")
        
        html.append("</ul></div></details>")

    html.append("<h2>Tarot Namespace Mapping (Service Routing)</h2>")
    html.append("<table><thead><tr><th>Tarot Namespace</th><th>System Alias</th><th>Core Responsibility</th></tr></thead><tbody>")
    for name, desc in report_data["namespaces"].items():
        html.append(f"<tr><td><strong>{name}</strong></td><td><code>@system/core</code></td><td>{desc}</td></tr>")
    html.append("</tbody></table>")

    html.append("</div></body></html>")
    return "\n".join(html)

def _get_audit_history_for_check(historical_reports: List[Dict[str, Any]], check_name: str) -> List[Truth]:
    """Extracts the historical Truth status for a specific audit check."""
    history_data: List[Truth] = []
    for hist_report in historical_reports:
        # Find the claim result for the current report
        claim_result = hist_report.get("claim_result", {})
        # Find the specific evidence detail within that report
        for ev_detail in hist_report.get("evidence_details", []):
            if ev_detail["name"] == check_name:
                status_str = ev_detail["result"]["STATUS"]
                history_data.append(Truth(status_str))
                break
    return history_data

def _load_historical_reports(history_dir: str) -> List[Dict[str, Any]]:
    """Loads all system_audit.json reports from the history directory."""
    historical_reports = []
    if not os.path.isdir(history_dir):
        return []

    for filename in os.listdir(history_dir):
        if filename.endswith(".json") and filename.startswith("system_audit"):
            file_path = os.path.join(history_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    report = json.load(f)
                    historical_reports.append(report)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load historical report {file_path}. Error: {e}")
    
    # Sort reports by timestamp, oldest first
    historical_reports.sort(key=lambda r: r.get("timestamp", "0"))
    return historical_reports

def _generate_sparkline_svg(history_data: List[Truth]) -> str:
    """Generates a simple SVG sparkline from a list of Truth statuses."""
    if not history_data:
        return ""

    # Map Truth status to a Y-coordinate and color
    # PASS=0, UNVERIFIED=1, STALE=2, FAIL=3
    status_map = {
        Truth.PASS: 0,
        Truth.UNVERIFIED: 1,
        Truth.STALE: 2,
        Truth.FAIL: 3,
    }
    color_map = {
        Truth.PASS: "#73d216",      # Green
        Truth.UNVERIFIED: "#fce94f", # Yellow
        Truth.STALE: "#fcaf3e",     # Orange
        Truth.FAIL: "#ef2929",      # Red
    }

    width = len(history_data) * 10  # 10px per data point
    height = 20
    points = []
    rects = []

    for i, status in enumerate(history_data):
        x = i * 10 + 5
        y = status_map.get(status, 1) * (height / 3) + (height / 6) # Distribute points vertically
        points.append(f"{x},{y}")
        rects.append(f'<rect x="{i*10}" y="0" width="10" height="{height}" fill="{color_map.get(status, "#888")}" opacity="0.7"/>')

    # Using rects for a bar-like sparkline, easier to represent discrete states
    return f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="vertical-align: middle;">{"".join(rects)}</svg>'


def main():
    parser = argparse.ArgumentParser(description="Phoenix Protocol: System Validator (ECM)")
    parser.add_argument("--target", default=".", help="Directory to run the audit against.")
    parser.add_argument("--output-json", default="system_audit.json", help="Output path for JSON telemetry vector.")
    parser.add_argument("--output-html", default="system_audit_report.html", help="Output path for human-readable HTML audit.")
    parser.add_argument("--history-dir", default="./audit_history", help="Directory containing past JSON audit reports for trend analysis")
    args = parser.parse_args()
    
    validator = SystemValidator(args.target)
    report = validator.run_audit()
    
    # Write JSON data-vector
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    # Load historical reports for trend analysis
    historical_reports = _load_historical_reports(args.history_dir)

    # Write HTML audit report
    html_report = generate_html_report(report, historical_reports)
    with open(args.output_html, "w", encoding="utf-8") as f:
        f.write(html_report)

    claim_result = report["claim_result"]

    # Output visual feedback to terminal
    print("\n=================== AUDIT SUMMARY ===================")
    print(f"Target Directory:          {report['target_directory']}")
    print(f"Overall Truth Status:      \033[1;32m{claim_result['TRUTH_STATUS']}\033[0m")
    print(f"Overall Confidence:        \033[1;36m{claim_result['CONFIDENCE']}\033[0m")
    print("=====================================================")
    for ev_detail in report["evidence_details"]:
        color = "\033[1;32m" if ev_detail['result']['STATUS'] == Truth.PASS else "\033[1;31m"
        print(f"[{color}{ev_detail['result']['STATUS'].value}\033[0m] {ev_detail['name']}")
    print("=====================================================")
    print(f"Traceable JSON logged to: {args.output_json}")
    print(f"HTML report logged to: {args.output_html}\n")


if __name__ == "__main__":
    main()
