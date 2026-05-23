"""## **[ARTIFACT START]**.

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.utils.debug_env`                    | The Sovereign ID. |
| **Official Name** | `debug_env.py`                     | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[ACTIVE]`                        | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | {resonance}     |
# | **Resonance** | {resonance}     |
# | **Stability** | Stable  |

## **[ARTIFACT END]**

Diagnostic script for verifying environment variable loading and Supabase connectivity parameters.
Conforms to OGLN/AISTF v15.0 documentation standards.
"""

import os

from dotenv import load_dotenv

# Load environment variables from the .env file in the current working directory
load_dotenv()


def print_env_status() -> None:
    """Prints the status of critical Supabase environment variables."""
    print(f"[DEBUG] SUPABASE_URL: {os.environ.get('SUPABASE_URL')}")
    print(
        f"[DEBUG] SUPABASE_SERVICE_ROLE_KEY: {'[SET]' if os.environ.get('SUPABASE_SERVICE_ROLE_KEY') else '[NOT SET]'}"
    )


if __name__ == "__main__":
    print_env_status()

# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.utils.debug_env VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [ACTIVE] TS: 2026-03-28
# ---
