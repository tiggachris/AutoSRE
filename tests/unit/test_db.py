"""Unit tests for database connection and health check utilities."""
from unittest import mock
import psycopg2
import pytest
from app.config import Config


def test_get_db_connection_success():
    """Verify get_db_connection successfully connects with config params."""
    from app.db import get_db_connection

    config = Config()
    mock_conn = mock.MagicMock()

    with mock.patch("psycopg2.connect", return_value=mock_conn) as mock_connect:
        conn = get_db_connection(config)
        assert conn == mock_conn
        mock_connect.assert_called_once_with(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            connect_timeout=3,
        )


def test_get_db_connection_default_config():
    """Verify get_db_connection falls back to default config if none provided."""
    from app.db import get_db_connection
    mock_conn = mock.MagicMock()

    with mock.patch("psycopg2.connect", return_value=mock_conn) as mock_connect:
        conn = get_db_connection(None)
        assert conn == mock_conn
        assert mock_connect.called


def test_get_db_connection_operational_error():
    """Verify get_db_connection propagates OperationalError when DB is down."""
    from app.db import get_db_connection

    config = Config()

    with mock.patch("psycopg2.connect", side_effect=psycopg2.OperationalError("Connection refused")):
        with pytest.raises(psycopg2.OperationalError, match="Connection refused"):
            get_db_connection(config)


def test_check_db_health_healthy():
    """Verify check_db_health returns healthy status when SELECT 1 succeeds."""
    from app.db import check_db_health

    config = Config()
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)

    with mock.patch("app.db.get_db_connection", return_value=mock_conn):
        result = check_db_health(config)
        assert result["status"] == "healthy"
        assert result["database"] == "connected"
        assert "latency_ms" in result
        assert isinstance(result["latency_ms"], float)
        mock_conn.close.assert_called_once()


def test_check_db_health_unhealthy_operational_error():
    """Verify check_db_health returns unhealthy status when connection fails."""
    from app.db import check_db_health

    config = Config()

    with mock.patch("app.db.get_db_connection", side_effect=psycopg2.OperationalError("Server not responding")):
        result = check_db_health(config)
        assert result["status"] == "unhealthy"
        assert result["database"] == "disconnected"
        assert "Server not responding" in result["error"]


def test_check_db_health_query_failure():
    """Verify check_db_health handles cursor/query execution errors cleanly."""
    from app.db import check_db_health

    config = Config()
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = psycopg2.DatabaseError("Query failed")

    with mock.patch("app.db.get_db_connection", return_value=mock_conn):
        result = check_db_health(config)
        assert result["status"] == "unhealthy"
        assert result["database"] == "error"
        assert "Query failed" in result["error"]
        mock_conn.close.assert_called_once()


def test_check_db_health_close_exception_handled():
    """Verify check_db_health handles connection close exceptions silently."""
    from app.db import check_db_health

    mock_conn = mock.MagicMock()
    mock_conn.close.side_effect = Exception("Close failed")

    with mock.patch("app.db.get_db_connection", return_value=mock_conn):
        result = check_db_health(None)
        assert result["status"] == "healthy"
