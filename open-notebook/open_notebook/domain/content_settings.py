# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

from typing import ClassVar, List, Literal, Optional

from pydantic import Field

from open_notebook.domain.base import RecordModel


class ContentSettings(RecordModel):
    record_id: ClassVar[str] = "open_notebook:content_settings"
    default_content_processing_engine_doc: Literal["auto", "docling", "simple"] | None = Field(
        "auto", description="Default Content Processing Engine for Documents"
    )
    default_content_processing_engine_url: Literal["auto", "firecrawl", "jina", "simple"] | None = Field(
        "auto", description="Default Content Processing Engine for URLs"
    )
    default_embedding_option: Literal["ask", "always", "never"] | None = Field(
        "ask", description="Default Embedding Option for Vector Search"
    )
    auto_delete_files: Literal["yes", "no"] | None = Field("yes", description="Auto Delete Uploaded Files")
    youtube_preferred_languages: list[str] | None = Field(
        ["en", "pt", "es", "de", "nl", "en-GB", "fr", "de", "hi", "ja"],
        description="Preferred languages for YouTube transcripts",
    )
