"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-AGT-CFG-001`            | The Sovereign ID. |
| **Official Name**   | `config.py`                   | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-AGT`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Parameter Purity (Law 36)**
> Implemented from Blueprint `GVRN.REG.AgentConfig.md`.
> Ethos: Stability through Configuration.
"""

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the Axion Agent."""

    PROJECT_NAME: str = "Axion Core"
    VERSION: str = "v15.0 [OMEGA]"

    # API Keys & Endpoints
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")

    # Agent Logic Config
    MAX_MEMORY_RECALL: int = 5
    ENABLE_SENTINEL: bool = True

    class Config:
        """Pydantic configuration for the settings model."""

        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
