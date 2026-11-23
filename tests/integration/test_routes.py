"""Integration tests for Flask application routes."""
from unittest import mock


def test_homepage_endpoint(client):
    """Verify GET / returns 200 with HTML or JSON welcoming to AutoSRE."""
    response = client.get("/")
    assert response.status_code == 200
    if response.is_json:
        data = response.get_json()
        assert data["service"] == "AutoSRE"
        assert "Autonomous Site Reliability Engineering" in data["message"]
    else:
        assert b"AutoSRE" in response.data


def test_health_endpoint_healthy(client):
    """Verify GET /health returns 200 when database is healthy."""
    mock_health = {
        "status": "healthy",
        "database": "connected",
        "latency_ms": 1.25,
    }
    with mock.patch("app.routes.check_db_health", return_value=mock_health):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["service"] == "AutoSRE"
        assert data["database"]["status"] == "healthy"
        assert data["database"]["database"] == "connected"
        assert data["database"]["latency_ms"] == 1.25


def test_health_endpoint_unhealthy(client):
    """Verify GET /health returns 503 when database is down."""
    mock_health = {
        "status": "unhealthy",
        "database": "disconnected",
        "error": "Connection refused",
    }
    with mock.patch("app.routes.check_db_health", return_value=mock_health):
        response = client.get("/health")
        assert response.status_code == 503
        assert response.is_json
        data = response.get_json()
        assert data["status"] == "unhealthy"
        assert data["service"] == "AutoSRE"
        assert data["database"]["status"] == "unhealthy"
        assert "Connection refused" in data["database"]["error"]


def test_404_not_found(client):
    """Verify 404 response for nonexistent routes."""
    response = client.get("/non-existent-endpoint")
    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert data["error"] == "Not Found"


def test_500_internal_server_error(app):
    """Verify 500 response when an unhandled server error occurs."""
    app.testing = False
    app.config["PROPAGATE_EXCEPTIONS"] = False

    @app.route("/force-error")
    def force_error():
        raise RuntimeError("Simulated internal error")

    test_client = app.test_client()
    response = test_client.get("/force-error")
    assert response.status_code == 500
    assert response.is_json
    data = response.get_json()
    assert data["error"] == "Internal Server Error"
