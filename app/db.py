"""Database connection and health check module."""
import time
from typing import Any, Dict, Optional
import psycopg2
from app.config import Config


def get_db_connection(config: Optional[Config] = None):
    """Establish and return a connection to PostgreSQL."""
    if config is None:
        config = Config()

    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        connect_timeout=3,
    )


def check_db_health(config: Optional[Config] = None) -> Dict[str, Any]:
    """Check connectivity to PostgreSQL database and calculate response latency."""
    if config is None:
        config = Config()

    start_time = time.perf_counter()
    conn = None
    try:
        conn = get_db_connection(config)
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        latency = (time.perf_counter() - start_time) * 1000.0
        return {
            "status": "healthy",
            "database": "connected",
            "latency_ms": round(latency, 2),
        }
    except psycopg2.OperationalError as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e),
        }
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
