"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AXION-CONFIG-001
Official Name: config.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Zero Entropy. Coherence through Confrontation."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AxionConfig(BaseSettings):
    """
    Centralized configuration for the Axion Agent (v15.0 [OMEGA]).
    Handles path resolution, environment variables, and Sovereign YAML ingestion.
    """

    # Environment
    ENV: str = Field(default="dev", description="Operational environment (dev/prod)")

    # Path Resolution
    WORKSPACE_ROOT: Path = Field(default_factory=lambda: _resolve_workspace_root())

    # Tool Paths
    SOPHIA_PATH: Path | None = Field(default=None)
    SENTINEL_PATH: Path | None = Field(default=None)

    # Sovereign Configuration Buffers (L4 Memory)
    SECURITY: dict[str, Any] = Field(default_factory=dict)
    NETWORK: dict[str, Any] = Field(default_factory=dict)
    KNOWLEDGE: dict[str, Any] = Field(default_factory=dict)

    # Constants (v15.0 [OMEGA])
    XP_THRESHOLD_MULTIPLIER: int = 1000
    LEVEL_CHRONOS: int = 100
    LEVEL_GENESIS: int = 50
    LEVEL_VECTOR: int = 25

    # Memory Thresholds
    COHERENCE_THRESHOLD: float = 0.9
    GEM_ACTIVATION_SCORE: float = 1.0

    # InsForge Integration
    INSFORGE_API_KEY: str | None = Field(default=None, description="Admin API Key for InsForge")
    INSFORGE_BASE_URL: str | None = Field(default=None, description="Base URL for InsForge project")
    INSFORGE_MODEL: str = Field(default="anthropic/claude-sonnet-4.5", description="Authoritative AI model for reasoning")

    # Logging
    LOG_LEVEL: str = "INFO"
    STRUCTURED_LOGGING: bool = True

    model_config = SettingsConfigDict(
        env_prefix="AXION_",
        case_sensitive=False,
    )

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(**kwargs)
        # 1. Resolve Tool Paths
        tools_dir = self.WORKSPACE_ROOT / "axion-core" / "tools"
        if not self.SOPHIA_PATH:
            self.SOPHIA_PATH = tools_dir / "sophia_wisdom.py"
        if not self.SENTINEL_PATH:
            self.SENTINEL_PATH = tools_dir / "sentinel_sword.py"

        # 2. Ingest Sovereign YAML Configs
        agent_dir = self.WORKSPACE_ROOT / ".agent"
        if agent_dir.exists():
            self._load_sovereign_config(agent_dir / "security.yaml", "SECURITY")
            self._load_sovereign_config(agent_dir / "network.yaml", "NETWORK")
            self._load_sovereign_config(agent_dir / "knowledge.yaml", "KNOWLEDGE")

    def _load_sovereign_config(self, path: Path, attribute: str) -> None:
        """
        Ingests YAML data from the .agent directory into the config.
        Targeted at SECURITY, NETWORK, and KNOWLEDGE buffers.
        """
        if path.exists():
            try:
                content = path.read_text()
                # Split by document separator and take the functional block
                yaml_part = content.split("---")[-1] if "---" in content else content
                
                data = yaml.safe_load(yaml_part)
                setattr(self, attribute, data or {})
            except Exception:
                # Silent failure to ensure operational continuity under dissonance
                pass

    @property
    def tools_dir(self) -> Path:
        """Returns the absolute path to the axion-core/tools directory."""
        return self.WORKSPACE_ROOT / "axion-core" / "tools"


def _resolve_workspace_root() -> Path:
    """Environment-first workspace resolution."""
    if workspace := os.getenv("AXION_WORKSPACE_ROOT"):
        return Path(workspace).resolve()

    # Marker file traversal
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".axion-root").exists():
            return parent

    # Fallback to relative path (src/agents/axion -> axion-core -> WORKSPACE)
    # 5 levels up from src/agents/axion/config.py
    return Path(__file__).resolve().parents[4]


# Singleton instance
settings = AxionConfig()
