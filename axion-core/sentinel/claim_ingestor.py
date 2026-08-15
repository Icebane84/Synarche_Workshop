# ARTIFACT_ID: SENTINEL.ClaimIngestor
# VERSION: v1.0
# STATUS: [ACTIVE]

import logging
import re
from pathlib import Path
from typing import Any, Dict, Optional

from .models import DeclaredState

logger = logging.getLogger(__name__)

# Header block format ClaimIngestor looks for, e.g.:
#   # ARTIFACT_ID: CORE.oathkeeper
#   # VERSION: v15.0 [OMEGA]
#   # STATUS: [CANONIZED]
#   # TS: 2026-03-28
#   # HASH: 8b27d7dd96329230
_HEADER_FIELD_RE = re.compile(r"^#\s*(ARTIFACT_ID|VERSION|STATUS|TS|HASH)\s*:\s*(.*)", re.IGNORECASE)
_HEADER_SCAN_LINES = 40  # only look near the top of the file


class ClaimIngestor:
    """
    SP-CLAIM-001: Parses declared state directly from an artifact's own
    metadata header.
    """

    def ingest_metadata(self, artifact_path: str) -> Optional[DeclaredState]:
        """
        Parses artifact metadata to extract its declared state.
        """
        path = Path(artifact_path)
        if not path.is_file():
            logger.debug("ClaimIngestor: %s is not a file, skipping.", artifact_path)
            return None

        fields: Dict[str, str] = {}
        try:
            with path.open("r", encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f):
                    if i >= _HEADER_SCAN_LINES:
                        break
                    match = _HEADER_FIELD_RE.match(line)
                    if match:
                        key, value = match.group(1).upper(), match.group(2).strip()
                        fields[key] = value
        except OSError as e:
            logger.warning("ClaimIngestor: could not read %s: %s", artifact_path, e)
            return None

        if "ARTIFACT_ID" not in fields or "STATUS" not in fields:
            return None

        return DeclaredState(
            artifact_id=fields["ARTIFACT_ID"],
            version=fields.get("VERSION", "UNVERSIONED"),
            status=fields["STATUS"],
            ts=fields.get("TS"),
            hash=fields.get("HASH"),
        )
