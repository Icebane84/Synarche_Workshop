"""
Artifact ID: CODE-NEW-001
Module: Supabase Client
Context: Nova Forge > Backend
Description: Manages the connection to the Supabase backend.
"""

from typing import Optional

from backend.config import settings
from supabase import Client, create_client


class SupabaseManager:
    """
    Manages the Supabase client connection.
    """

    _client: Optional[Client] = None

    @classmethod
    def get_client(cls) -> Client:
        """
        Returns the Supabase client instance.
        Initializes it if it hasn't been created yet.
        Raises ValueError if configuration is missing.
        """
        if cls._client is None:
            if not settings.is_supabase_configured:
                raise ValueError(
                    "Supabase is not configured. Please check your .env file."
                )

            cls._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

        return cls._client


# Global accessor
def get_supabase() -> Client:
    """Convenience function to get the Supabase client."""
    return SupabaseManager.get_client()
