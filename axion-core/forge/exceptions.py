"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-EXCEPT-001`              | The Sovereign ID. |
| **Official Name** | `exceptions.py`                | The Filename.     |
| **Version**       | **v14.0**                      | The Standard.     |
| **Domain**        | `ARCH`                         | The Subject.      |
| **Evolution**     | **Crystalline Coherence**      | The Alignment.    |
| **Status (State)**| `[ACTIVE]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |.

## Sovereign Ethos
Standardized error models for the Forge Toolkit and Axion Runtime.
Failure is not an end, but a signal for re-calibration.
"""


class ForgeError(Exception):
    """Base exception for all Forge Toolkit errors."""

    pass


class SovereigntyViolationError(ForgeError):
    """Raised when a path resolution attempts to leave the Workspace Sanctuary."""

    pass


class IntegrityError(ForgeError):
    """Raised when metadata or rendering integrity is compromised."""

    pass


class ObsidianConnectionError(ForgeError):
    """Raised when the Obsidian Local REST API is unreachable or authentication fails."""

    pass


class TransmissionError(ForgeError):
    """Raised when data synthesis or transclusion fails."""

    pass
