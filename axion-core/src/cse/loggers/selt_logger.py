"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-CSE-LOG-001`            | The Sovereign ID. |
| **Official Name**   | `selt_logger.py`              | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-CSE`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Accountable Logging (Law 31)**
> Implemented from Blueprint `GVRN.REG.SeltLogger.md`.
> Ethos: Transparency through Logging.
"""

import json
import os
from datetime import datetime
from typing import Any, List


class SeltLogger:
    """WHAT: Generates Standardized Experience Logs (SELT).
    HOW: Appends formatted JSON strings to the repository audit_log.txt.
    WHY: To provide an immutable history of System Entropy for AI ingestion.
    """

    def __init__(self, root_dir: str):
        self.log_path = os.path.join(root_dir, "audit_log.txt")

    def record_synthesis(
        self, status: str, entropy: float, findings: List[Any]
    ) -> None:
        """Records a synthesis event to the audit log.

        Args:
            status (str): The status of the synthesis (e.g., STABLE, DEGRADED).
            entropy (float): The calculated entropy level.
            findings (List[Any]): A list of findings or errors discovered during synthesis.

        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = {
            "timestamp": timestamp,
            "status": status,
            "entropy": entropy,
            "findings": findings,
        }

        with open(self.log_path, "a", encoding="utf-8") as l:
            l.write(f"\n[SELT] {timestamp} | {json.dumps(log_entry)}")
