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
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
