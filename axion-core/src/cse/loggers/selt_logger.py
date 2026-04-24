import json
import os
from datetime import datetime


class SeltLogger:
    """
    WHAT: Generates Standardized Experience Logs (SELT).
    HOW: Appends formatted JSON strings to the repository audit_log.txt.
    WHY: To provide an immutable history of System Entropy for AI ingestion.
    """

    def __init__(self, root_dir: str):
        self.log_path = os.path.join(root_dir, "audit_log.txt")

    def record_synthesis(self, status: str, entropy: float, findings: list):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = {"timestamp": timestamp, "status": status, "entropy": entropy, "findings": findings}

        with open(self.log_path, "a", encoding="utf-8") as l:
            l.write(f"\n[SELT] {timestamp} | {json.dumps(log_entry)}")
