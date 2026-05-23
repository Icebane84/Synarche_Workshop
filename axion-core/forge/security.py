"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-HEPH-SECURITY-001`      | The Sovereign ID. |
| **Official Name**   | `security.py`                 | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-HEPH`                   | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Faraday Cage Implementation` | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Sentinel`          | The Sovereign.    |

**The Spirit Bomb Axiom: Defensive Execution Boundaries (Law 29)**
> Implemented to mitigate Sandbox Escape (RCE) via path traversal.
"""

import subprocess
from pathlib import Path
from typing import Any

from exceptions import SovereigntyViolationError

WORKSPACE_ROOT = Path("c:/Users/Chris/Synarche_Workspace").resolve()


def resolve_path(target_path: str | Path) -> Path:
    """Resolves a path to its absolute form and verifies it exists strictly
    within the Synarche Workspace bounds (The Faraday Cage).
    """
    resolved = Path(target_path).resolve()

    if not resolved.is_relative_to(WORKSPACE_ROOT):
        raise SovereigntyViolationError(
            f"Faraday Cage Violation: Attempted to access '{resolved}' which is outside the Sanctuary ({WORKSPACE_ROOT})."
        )

    return resolved


def execute_safe(
    cmd: list[str], cwd: str | Path | None = None, **kwargs: Any
) -> subprocess.CompletedProcess:
    """A Faraday Cage wrapper for subprocess.run. Validates the command's execution
    directory and referenced script paths before allowing execution.
    """
    if cwd:
        resolve_path(cwd)
    else:
        # Default to ensuring the current working directory isn't already outside
        resolve_path(Path.cwd())

    # If the command executes a local script, validate the script path
    # e.g., ["python", "../../../System32/evil.py"]
    for part in cmd:
        if isinstance(part, str) and (
            "/" in part
            or "\\" in part
            or part.endswith(".py")
            or part.endswith(".ps1")
            or part.endswith(".sh")
        ):
            # Attempt to resolve it if it looks like a path.
            # If it's just a raw system binary name, it won't resolve successfully relative to CWD if it relies on PATH,
            # but we catch explicit relative/absolute malicious path traversals.
            # Only check if it actually exists to avoid failing on arbitrary string arguments.
            potential_path = (
                Path(cwd or Path.cwd()) / part
                if not Path(part).is_absolute()
                else Path(part)
            )
            if potential_path.exists():
                resolve_path(potential_path)

    return subprocess.run(cmd, cwd=cwd, **kwargs)
