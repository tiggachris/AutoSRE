"""Configuration management for AutoSRE."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration with environment-driven values and sensible defaults."""

    def __init__(self):
        self.FLASK_ENV = os.getenv("FLASK_ENV", "development")
        self.DEBUG = self.FLASK_ENV == "development"
        self.SECRET_KEY = os.getenv("SECRET_KEY", "autosre-default-insecure-secret-key")

        # Server port
        raw_port = os.getenv("PORT", "5000")
        try:
            self.PORT = int(raw_port)
        except ValueError:
            self.PORT = 5000

        # Database configuration
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        raw_db_port = os.getenv("DB_PORT", "5432")
        try:
            self.DB_PORT = int(raw_db_port)
        except ValueError:
            self.DB_PORT = 5432

        self.DB_NAME = os.getenv("DB_NAME", "autosre_db")
        self.DB_USER = os.getenv("DB_USER", "autosre_user")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "autosre_password")

    @property
    def db_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
