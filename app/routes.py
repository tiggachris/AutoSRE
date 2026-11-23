"""HTTP Route definitions for AutoSRE."""
from flask import Blueprint, jsonify, current_app
from app.db import check_db_health

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def index():
    """Homepage endpoint providing platform info and available endpoints."""
    return jsonify({
        "service": "AutoSRE",
        "description": "Autonomous Site Reliability Engineering Platform",
        "message": "Welcome to AutoSRE - Autonomous Site Reliability Engineering",
        "status": "online",
        "version": current_app.config.get("VERSION", "0.1.0"),
        "endpoints": {
            "homepage": "/",
            "health": "/health",
        },
    }), 200


@bp.route("/health", methods=["GET"])
def health():
    """System health check endpoint validating service and database connectivity."""
    app_config = current_app.config.get("APP_CONFIG")
    db_health = check_db_health(app_config)

    is_healthy = db_health.get("status") == "healthy"
    status_code = 200 if is_healthy else 503

    payload = {
        "status": "healthy" if is_healthy else "unhealthy",
        "service": "AutoSRE",
        "database": db_health,
    }
    return jsonify(payload), status_code
