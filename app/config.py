#File: app/config.py
"""
Settings configuration module.

Loads environment variables and provides centralized access to application settings.
"""
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    """Application configuration settings loaded from environment variables."""
    WGAI_BASE_URL = os.getenv("WGAI_SERVER_URL")
    API_KEY_PHASE1 = os.getenv("WGAI_API_KEY_PHASE1")
    API_KEY_PHASE2 = os.getenv("WGAI_API_KEY_PHASE2")


settings = Settings()