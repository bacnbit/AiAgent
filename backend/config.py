"""
Application configuration management.
Loads settings from environment variables.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import logging


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "AI Agent - ERP Config Validator"
    app_version: str = "0.1.0"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Logging
    log_level: str = "info"  # info or verbose

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/agent.db"

    # MCP Server Endpoints (to be configured)
    erp_mcp_endpoint: Optional[str] = None
    salesforce_mcp_endpoint: Optional[str] = None

    # API Keys (loaded from secrets)
    erp_api_key: Optional[str] = None
    salesforce_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = False


def setup_logging(log_level: str) -> None:
    """
    Configure application logging.

    Args:
        log_level: 'info' or 'verbose'
    """
    level = logging.DEBUG if log_level.lower() == "verbose" else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# Global settings instance
settings = Settings()
setup_logging(settings.log_level)
