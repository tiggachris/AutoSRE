"""Integration tests against live database instance."""
import os
import pytest
import psycopg2
from app.config import Config
from app.db import get_db_connection, check_db_health


def is_live_db_available():
    """Check if a live PostgreSQL database is reachable."""
    config = Config()
    try:
        conn = get_db_connection(config)
        conn.close()
        return True
    except Exception:
        return False


@pytest.mark.skipif(not is_live_db_available(), reason="Live PostgreSQL database not reachable")
def test_live_postgres_connection_and_query():
    """Verify live PostgreSQL accepts connections, executes queries, and returns health."""
    config = Config()
    health = check_db_health(config)
    assert health["status"] == "healthy"
    assert health["database"] == "connected"
    assert health["latency_ms"] >= 0

    # Test executing a real query and transaction
    conn = get_db_connection(config)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            assert version is not None
            assert "PostgreSQL" in version[0]

            # Test creating a temporary table and inserting a test row
            cursor.execute("""
                CREATE TEMP TABLE _autosre_test (
                    id SERIAL PRIMARY KEY,
                    component VARCHAR(50),
                    status VARCHAR(20)
                );
            """)
            cursor.execute(
                "INSERT INTO _autosre_test (component, status) VALUES (%s, %s) RETURNING id;",
                ("core-service", "active"),
            )
            row_id = cursor.fetchone()[0]
            assert row_id == 1

            cursor.execute("SELECT component, status FROM _autosre_test WHERE id = %s;", (row_id,))
            row = cursor.fetchone()
            assert row[0] == "core-service"
            assert row[1] == "active"
    finally:
        conn.close()
