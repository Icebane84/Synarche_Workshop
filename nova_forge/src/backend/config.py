"""
Artifact ID: CODE-REF-006
Module: Configuration Manager
Context: Nova Forge > Backend
Description: Manages application settings and environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Notion Integration
    NOTION_API_TOKEN: str = ""
    NOTION_BASE_URL: str = "https://api.notion.com/v1"

    # System
    LOG_LEVEL: str = "INFO"

    # Supabase Integration
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    @property
    def is_notion_configured(self) -> bool:
        """Checks if the Notion API token is set."""
        return bool(self.NOTION_API_TOKEN)

    @property
    def is_supabase_configured(self) -> bool:
        """Checks if Supabase credentials are set."""
        return bool(self.SUPABASE_URL and self.SUPABASE_KEY)


# Global settings instance
settings = Settings()
