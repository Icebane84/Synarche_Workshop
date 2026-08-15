# ARTIFACT_ID: SENTINEL.Verifiers
# VERSION: v1.0
# STATUS: [ACTIVE]

import hashlib
import os
import re
from pathlib import Path
from typing import List, Tuple

# Shared constants for header parsing
_HEADER_FIELD_RE = re.compile(r"^#\s*(ARTIFACT_ID|VERSION|STATUS|TS|HASH)\s*:\s*(.*)", re.IGNORECASE)
_HASH_TRUNCATE_CHARS = 16


def compute_artifact_hash(path: Path) -> str:
    """
    Hashes the artifact's content EXCLUDING its own declared HASH line to prevent
    a self-referential paradox where writing the hash changes the hash.
    """

    def _is_hash_line(line: str) -> bool:
        match = _HEADER_FIELD_RE.match(line)
        return match is not None and match.group(1).upper() == "HASH"

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    hashable_lines = [line for line in lines if not _is_hash_line(line)]
    digest = hashlib.sha256("".join(hashable_lines).encode("utf-8")).hexdigest()
    return digest[:_HASH_TRUNCATE_CHARS]


def find_hardcoded_paths(scan_dir: Path) -> List[Tuple[str, int, str]]:
    """Scans for hardcoded, user-specific paths."""
    issues = []
    user_home_str = str(Path.home()).replace("\\", "/")
    path_pattern = re.compile(f"(['\"])(.*{re.escape(user_home_str)}.*)(['\"])")
    for root, _, files in os.walk(scan_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                try:
                    for i, line in enumerate(file_path.read_text(encoding="utf-8").splitlines()):
                        if path_pattern.search(line):
                            issues.append((str(file_path), i + 1, line.strip()))
                except OSError, UnicodeDecodeError:
                    continue
    return issues


def find_pyc_files(scan_dir: Path) -> List[str]:
    """Finds compiled Python files."""
    return [str(p) for p in scan_dir.rglob("*.pyc")]
