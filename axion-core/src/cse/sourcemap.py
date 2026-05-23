"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `TOOL-FORGE-MAP-001`          | The Sovereign ID. |
| **Official Name**   | `sourcemap.py`                | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `TOOL-FORGE`                  | The Subject.      |
| **Celestial Class** | `[STAR]`                      | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `SYNERGIZES: GUCA-Command`    | The Sovereign.    |

**The Spirit Bomb Axiom: Traceability (Law 03)**
> Implemented from Blueprint `GVRN.REG.SourceMap.md`.
> Ethos: Truth through Provenance.
"""

import bisect
import re
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class SourceMapping:
    """Represents a single mapping block between generated content and its source.

    Attributes:
        generated_start (int): Start offset in the generated file.
        generated_end (int): End offset in the generated file.
        source_id (str): The MSID of the source block (e.g., "@codex/Auth").
        source_start (int): Offset within the source block itself.

    """

    generated_start: int
    generated_end: int
    source_id: str  # MUST be an MSID (e.g., "@codex/Auth_Protocol")
    source_start: int  # Offset within the source block itself


class ForgeSourceMap:
    """AXION Forge equivalent of Volar's SourceMap.
    Maintains a mathematically strict mapping of generated character offsets
    to their sovereign source blocks using Modular Sovereign IDs (MSIDs).

    Relations:
        UTILIZED_BY: TOOL.Forge.Daemon
        SYNERGIZES_WITH: TOOL.GUCA.Command
    """

    def __init__(self) -> None:
        """Initializes the SourceMap with empty mappings and keys."""
        # Mappings must be strictly sorted by generated_start for binary search
        self._mappings: list[SourceMapping] = []
        self._keys: list[int] = []  # Cached keys for bisect

    def add_mapping(
        self, gen_start: int, gen_end: int, source_id: str, src_start: int = 0
    ) -> None:
        """Registers a new mapping block.
        Enforces MSID normalization (ensuring the source_id uses @alias notation).

        Args:
            gen_start (int): Start offset in generated content.
            gen_end (int): End offset in generated content.
            source_id (str): The MSID/Alias of the source.
            src_start (int): Start offset in the source block.

        """
        # Internal MSID Normalization (Placeholder for more complex logic if needed)
        if not source_id.startswith("@") and "/" in source_id:
            # Logic could go here to auto-map physical paths back to aliases
            pass

        mapping = SourceMapping(gen_start, gen_end, source_id, src_start)
        self._mappings.append(mapping)
        self._keys.append(gen_start)

    def trace_offset(self, generated_offset: int) -> Optional[Tuple[str, int]]:
        """Mimics Volar's translateOffset using binary search.
        Given an absolute character offset in the final compiled Markdown,
        returns the (MSID, Exact Offset Inside Block).
        """
        if not self._mappings:
            return None

        # Binary search to find the closest mapping block
        idx = bisect.bisect_right(self._keys, generated_offset) - 1

        if idx >= 0:
            mapping = self._mappings[idx]
            if mapping.generated_start <= generated_offset < mapping.generated_end:
                delta = generated_offset - mapping.generated_start
                exact_source_offset = mapping.source_start + delta
                return mapping.source_id, exact_source_offset

        return "Master_Shell", generated_offset

    def apply_delta_update(self, offset: int, length_diff: int) -> None:
        """Handles real-time source updates, adjusting generated indices.
        Operates similarly to a Language Server processing document changes.

        Args:
            offset (int): The character offset where the edit occurred.
            length_diff (int): The change in length (+ for insertions, - for deletions).

        """
        if length_diff == 0:
            return

        for mapping in self._mappings:
            if offset <= mapping.generated_start:
                mapping.generated_start += length_diff
                mapping.generated_end += length_diff
            elif mapping.generated_start < offset < mapping.generated_end:
                mapping.generated_end = max(
                    mapping.generated_start, mapping.generated_end + length_diff
                )

        # Re-synchronize the binary search keys
        self._keys = [m.generated_start for m in self._mappings]


class TranscludeEngine:
    """Two-pass transclusion compiler that wraps content in mapping boundaries,
    then strips markers and generates the SourceMap in a single pass.

    Encourages the use of @alias paths for transclusion targets.
    """

    MARKER_START = "\x00MAP_START:{}\x00"
    MARKER_END = "\x00MAP_END\x00"
    MARKER_REGEX = re.compile(r"\x00MAP_START:(.*?)\x00|\x00MAP_END\x00")

    def compile_with_sourcemap(
        self, raw_jinja_output: str
    ) -> Tuple[str, ForgeSourceMap]:
        """The Second Pass: Strips markers, calculates offsets, generates the map.

        Args:
            raw_jinja_output (str): The raw string containing mapping markers.

        Returns:
            Tuple[str, ForgeSourceMap]: The cleaned content and its associated SourceMap.

        """
        sourcemap = ForgeSourceMap()
        final_output = []

        current_gen_offset = 0
        stack = []

        parts = self.MARKER_REGEX.split(raw_jinja_output)
        matches = self.MARKER_REGEX.finditer(raw_jinja_output)

        if parts[0]:
            final_output.append(parts[0])
            current_gen_offset += len(parts[0])

        part_idx = 1
        for match in matches:
            match_str = match.group(0)

            if match_str == self.MARKER_END:
                if stack:
                    block_id, block_start_offset = stack.pop()
                    sourcemap.add_mapping(
                        gen_start=block_start_offset,
                        gen_end=current_gen_offset,
                        source_id=block_id,
                    )
            else:
                # Capture the MSID (e.g., @codex/Law) from the marker
                block_id = match.group(1)
                stack.append((block_id, current_gen_offset))

            text_chunk = parts[part_idx + 1] if part_idx + 1 < len(parts) else ""
            if text_chunk:
                final_output.append(text_chunk)
                current_gen_offset += len(text_chunk)

            part_idx += 2

        compiled_markdown = "".join(final_output)
        return compiled_markdown, sourcemap

    def inject_transclude(self, block_id: str, block_content: str) -> str:
        """Wraps content in strict mapping boundaries.

        Args:
            block_id (str): The MSID (e.g. "@codex/Law") of the source.
            block_content (str): The content to wrap.

        Returns:
            str: The wrapped content with markers.

        """
        start = self.MARKER_START.format(block_id)
        return f"{start}{block_content}{self.MARKER_END}"
