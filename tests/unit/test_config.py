"""Unit tests for configuration module."""
import os
from unittest import mock
import pytest


def test_default_config():
    """Verify default configuration values when no env vars are set."""
    with mock.patch.dict(os.environ, {}, clear=True):
        from app.config import Config
        config = Config()
        assert config.FLASK_ENV == "development"
        assert config.DEBUG is True
        assert config.PORT == 5000
        assert config.DB_HOST == "localhost"
        assert config.DB_PORT == 5432
        assert config.DB_NAME == "autosre_db"
        assert config.DB_USER == "autosre_user"
        assert config.DB_PASSWORD == "autosre_password"
        assert config.db_url == "postgresql://autosre_user:autosre_password@localhost:5432/autosre_db"


def test_custom_env_config():
    """Verify custom environment variables override defaults."""
    custom_env = {
        "FLASK_ENV": "production",
        "PORT": "8080",
        "DB_HOST": "postgres-prod",
        "DB_PORT": "5433",
        "DB_NAME": "prod_db",
        "DB_USER": "prod_admin",
        "DB_PASSWORD": "supersecretpassword",
        "SECRET_KEY": "custom-secret-key",
    }
    with mock.patch.dict(os.environ, custom_env, clear=True):
        from app.config import Config
        config = Config()
        assert config.FLASK_ENV == "production"
        assert config.DEBUG is False
        assert config.PORT == 8080
        assert config.DB_HOST == "postgres-prod"
        assert config.DB_PORT == 5433
        assert config.DB_NAME == "prod_db"
        assert config.DB_USER == "prod_admin"
        assert config.DB_PASSWORD == "supersecretpassword"
        assert config.SECRET_KEY == "custom-secret-key"
        assert config.db_url == "postgresql://prod_admin:supersecretpassword@postgres-prod:5433/prod_db"


def test_invalid_port_fallback():
    """Verify invalid port strings fallback gracefully to default port."""
    with mock.patch.dict(os.environ, {"PORT": "invalid-port", "DB_PORT": "not-a-number"}, clear=True):
        from app.config import Config
        config = Config()
        assert config.PORT == 5000
        assert config.DB_PORT == 5432
