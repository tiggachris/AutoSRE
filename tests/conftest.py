"""Test fixtures for AutoSRE test suite."""
import pytest
from app import create_app
from app.config import Config


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    DEBUG = False


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    test_config = TestConfig()
    app = create_app(test_config)
    return app


@pytest.fixture
def client(app):
    """Test client fixture."""
    return app.test_client()
