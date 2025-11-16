"""
Configuration management for the BI Intelligence Agent System.
Handles API keys, model settings, and application configuration.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration for the BI Intelligence Agent System."""
    
    # API Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENABLE_TRACING: bool = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent
    DATA_DIR: Path = BASE_DIR / "data"
    OUTPUT_DIR: Path = BASE_DIR / "outputs"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY not found. Please set it in .env file or environment."
            )
        return True
    
    @classmethod
    def setup_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.REPORTS_DIR.mkdir(exist_ok=True)
        (cls.DATA_DIR / "examples").mkdir(exist_ok=True)


# Validate configuration on import
try:
    Config.validate()
    Config.setup_directories()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please copy .env.example to .env and add your GOOGLE_API_KEY")

