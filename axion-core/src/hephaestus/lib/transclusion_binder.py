"""
artifact_anchor:
  id: CORE.TRANSCLUSION_BINDER.001
  version: v15.0 [OMEGA]
  provenance: '2026-06-09'
  domain: CORE
  celestial_class: STAR
  tier: TOOLKIT
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `AOP-ISE-002`                 | The Sovereign ID. |
| **Official Name**   | `transclusion_binder.py`      | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `HEPH-LIB`                    | The Subject.      |
| **Celestial Class** | `[STAR]`                      | The Weight.       |
| **Evolution**       | `PAD-SIP Toolkit`             | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |
# Cognitive Load Cost: Medium

**The Spirit Bomb Axiom: Unified Reference (Law 31)**
> Implemented from Blueprint `PAD-SIP.Toolkit.TransclusionBinder`.
> Ethos: A pointer without resolution is a void. Bind or break.
"""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("PhoenixLogger")

# ---------------------------------------------------------------------------
# §1  Transclusion token grammar
# ---------------------------------------------------------------------------

# Tokens have the form:  [[pointer:STUB-DOMAIN-NNN]]
#                    or  [[alias:some/path.py]]
#                    or  [[id:CORE.ARTIFACT.001]]
_TOKEN_PATTERN = re.compile(
    r"\[\[(?P<kind>pointer|alias|id):(?P<ref>[^\]]+)\]\]"
)


# ---------------------------------------------------------------------------
# §2  BindingResult
# ---------------------------------------------------------------------------

class BindingResult:
    """Result of a single transclusion resolution attempt.

    Attributes:
        token       : the original token string found in the document.
        kind        : token kind ("pointer" | "alias" | "id").
        ref         : the reference value inside the token.
        resolved    : True if the reference was successfully resolved.
        content     : resolved replacement content, or the original token on failure.
        source_file : absolute path of the file that provided the resolved content.
        error       : error message if resolution failed.
    """

    def __init__(
        self,
        token: str,
        kind: str,
        ref: str,
        resolved: bool,
        content: str,
        source_file: Optional[str] = None,
        error: Optional[str] = None,
    ) -> None:
        self.token = token
        self.kind = kind
        self.ref = ref
        self.resolved = resolved
        self.content = content
        self.source_file = source_file
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "token": self.token,
            "kind": self.kind,
            "ref": self.ref,
            "resolved": self.resolved,
            "source_file": self.source_file,
            "error": self.error,
        }


# ---------------------------------------------------------------------------
# §3  TransclusionBinder
# ---------------------------------------------------------------------------

class TransclusionBinder:
    """Runtime pointer resolver and content binder for the PAD-SIP toolkit.

    The TransclusionBinder extends `src/cse/sourcemap.py` (which performs
    compile-time transclusion) by resolving pointers **at runtime**, so that
    documents, prompts, and cognitive payloads can dynamically include content
    from:
        - ScaffoldWeaver's stub pointer registry (``[[pointer:STUB-xxx-NNN]]``)
        - Filesystem paths (``[[alias:some/relative/path.py]]``)
        - OMEGA artifact anchors (``[[id:CORE.ARTIFACT.001]]``)

    The binder reads the scaffold_registry.json to resolve pointer tokens and
    scans the project for artifact anchors to resolve ID tokens.

    Usage::

        binder = TransclusionBinder(root_dir="c:/Users/Chris/Synarche_Workspace/axion-core")
        output, results = binder.bind_document(my_markdown_text)
        for r in results:
            if not r.resolved:
                print(f"Unresolved: {r.token} — {r.error}")
    """

    # Maximum bytes to inline from a resolved file (prevent huge inclusions)
    MAX_INLINE_BYTES = 4096

    def __init__(
        self,
        root_dir: Optional[str] = None,
        scaffold_registry_path: Optional[str] = None,
    ) -> None:
        """Initialise the binder.

        Args:
            root_dir                : absolute path to axion-core root.
            scaffold_registry_path  : path to scaffold_registry.json.
                                      Defaults to axion-core/data/scaffold_registry.json.
        """
        if root_dir:
            self.root = Path(root_dir)
        else:
            self.root = Path(__file__).resolve().parent.parent.parent.parent

        _default_reg = self.root / "data" / "scaffold_registry.json"
        self._registry_path = (
            Path(scaffold_registry_path) if scaffold_registry_path else _default_reg
        )
        self._pointer_map: Dict[str, str] = {}  # pointer_id → file_path
        self._id_map: Dict[str, str] = {}        # artifact_id → file_path (built lazily)
        self._id_map_built = False

        self._load_pointer_map()
        logger.info(
            f"[TBINDER] TransclusionBinder initialised. "
            f"Pointers loaded: {len(self._pointer_map)}"
        )

    # ------------------------------------------------------------------
    # §3.1  Registry loading
    # ------------------------------------------------------------------

    def _load_pointer_map(self) -> None:
        """Build a pointer_id → file_path lookup from the scaffold registry."""
        if not self._registry_path.exists():
            logger.debug("[TBINDER] No scaffold registry found — pointer resolution unavailable.")
            return
        try:
            with open(self._registry_path, encoding="utf-8") as f:
                data = json.load(f)
            for stub in data.get("stubs", []):
                pid = stub.get("pointer_id", "")
                fpath = stub.get("file_path", "")
                if pid and fpath:
                    self._pointer_map[pid] = fpath
        except Exception:
            logger.exception("[TBINDER] Failed to load scaffold registry.")

    def reload_registry(self) -> int:
        """Hot-reload the pointer map from the scaffold registry on disk.

        Returns:
            int: Number of pointers loaded.
        """
        self._pointer_map.clear()
        self._load_pointer_map()
        return len(self._pointer_map)

    # ------------------------------------------------------------------
    # §3.2  Artifact ID scanning
    # ------------------------------------------------------------------

    def _build_id_map(self) -> None:
        """Scan the project for artifact_anchor ID fields and build a lookup map.

        Searches all .py and .md files under self.root for the pattern:
            id: CORE.SOMETHING.001
        """
        if self._id_map_built:
            return
        anchor_pattern = re.compile(r"id:\s+([A-Z][A-Z0-9._\-]+)")
        for ext in ("*.py", "*.md"):
            for path in self.root.rglob(ext):
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                    for match in anchor_pattern.finditer(text):
                        artifact_id = match.group(1)
                        if artifact_id not in self._id_map:
                            self._id_map[artifact_id] = str(path)
                except Exception:
                    pass
        self._id_map_built = True
        logger.debug(f"[TBINDER] Artifact ID map built: {len(self._id_map)} entries.")

    # ------------------------------------------------------------------
    # §3.3  Single token resolution
    # ------------------------------------------------------------------

    def _resolve_pointer(self, ref: str) -> Tuple[bool, str, Optional[str]]:
        """Resolve a [[pointer:STUB-xxx-NNN]] token."""
        file_path = self._pointer_map.get(ref)
        if not file_path:
            return False, f"[[pointer:{ref}]]", f"Pointer '{ref}' not found in registry."
        p = Path(file_path)
        if not p.exists():
            return False, f"[[pointer:{ref}]]", f"File '{file_path}' does not exist."
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")[: self.MAX_INLINE_BYTES]
            return True, content, None
        except Exception as e:
            return False, f"[[pointer:{ref}]]", str(e)

    def _resolve_alias(self, ref: str) -> Tuple[bool, str, Optional[str]]:
        """Resolve a [[alias:some/relative/path.py]] token."""
        candidate = self.root / ref
        if not candidate.exists():
            # Try as absolute path
            candidate = Path(ref)
        if not candidate.exists():
            return False, f"[[alias:{ref}]]", f"Path '{ref}' not found."
        try:
            content = candidate.read_text(encoding="utf-8", errors="ignore")[: self.MAX_INLINE_BYTES]
            return True, content, None
        except Exception as e:
            return False, f"[[alias:{ref}]]", str(e)

    def _resolve_id(self, ref: str) -> Tuple[bool, str, Optional[str]]:
        """Resolve a [[id:CORE.ARTIFACT.001]] token."""
        self._build_id_map()
        file_path = self._id_map.get(ref)
        if not file_path:
            return False, f"[[id:{ref}]]", f"Artifact ID '{ref}' not found in project."
        p = Path(file_path)
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")[: self.MAX_INLINE_BYTES]
            return True, content, None
        except Exception as e:
            return False, f"[[id:{ref}]]", str(e)

    def resolve_token(self, kind: str, ref: str) -> BindingResult:
        """Resolve a single transclusion token.

        Args:
            kind: "pointer" | "alias" | "id".
            ref : the reference value.

        Returns:
            BindingResult with resolved content or the original token on failure.
        """
        token = f"[[{kind}:{ref}]]"
        if kind == "pointer":
            ok, content, err = self._resolve_pointer(ref)
        elif kind == "alias":
            ok, content, err = self._resolve_alias(ref)
        elif kind == "id":
            ok, content, err = self._resolve_id(ref)
        else:
            ok, content, err = False, token, f"Unknown token kind '{kind}'."

        if not ok:
            logger.warning(f"[TBINDER] Unresolved: {token} — {err}")
        return BindingResult(
            token=token,
            kind=kind,
            ref=ref,
            resolved=ok,
            content=content,
            source_file=self._pointer_map.get(ref) if kind == "pointer" else None,
            error=err,
        )

    # ------------------------------------------------------------------
    # §3.4  Document-level binding
    # ------------------------------------------------------------------

    def bind_document(self, text: str) -> Tuple[str, List[BindingResult]]:
        """Scan a text document and replace all transclusion tokens with resolved content.

        Args:
            text: The document content containing [[kind:ref]] tokens.

        Returns:
            Tuple[str, List[BindingResult]]:
                - The document with all tokens replaced (resolved or fallback).
                - A list of BindingResult objects for each token found.
        """
        results: List[BindingResult] = []
        output = text

        for match in _TOKEN_PATTERN.finditer(text):
            kind = match.group("kind")
            ref = match.group("ref")
            result = self.resolve_token(kind, ref)
            results.append(result)
            output = output.replace(result.token, result.content, 1)

        resolved_count = sum(1 for r in results if r.resolved)
        logger.info(
            f"[TBINDER] Document bound: {len(results)} tokens, "
            f"{resolved_count} resolved, {len(results) - resolved_count} unresolved."
        )
        return output, results

    def bind_file(self, file_path: str, output_path: Optional[str] = None) -> Tuple[str, List[BindingResult]]:
        """Read a file, resolve all transclusion tokens, optionally write output.

        Args:
            file_path   : path to the source document.
            output_path : if provided, write the bound document to this path.

        Returns:
            Tuple[str, List[BindingResult]]: bound text and results list.
        """
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"[TBINDER] Source file not found: {file_path}")

        text = p.read_text(encoding="utf-8")
        bound, results = self.bind_document(text)

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(bound, encoding="utf-8")
            logger.info(f"[TBINDER] Bound document written to {out}")

        return bound, results

    # ------------------------------------------------------------------
    # §3.5  Introspection
    # ------------------------------------------------------------------

    def list_unresolved_pointers(self) -> List[str]:
        """Return all pointer IDs in the registry whose file path does not exist."""
        missing = []
        for pid, fpath in self._pointer_map.items():
            if not Path(fpath).exists():
                missing.append(pid)
        return missing

    def stats(self) -> Dict[str, Any]:
        """Return binder statistics."""
        return {
            "pointer_count": len(self._pointer_map),
            "artifact_id_count": len(self._id_map) if self._id_map_built else "not_built",
            "registry_path": str(self._registry_path),
            "root": str(self.root),
        }

    def __repr__(self) -> str:
        return (
            f"<TransclusionBinder pointers={len(self._pointer_map)} "
            f"ids={'built' if self._id_map_built else 'lazy'}>"
        )
