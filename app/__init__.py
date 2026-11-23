"""AutoSRE Application Factory."""
from typing import Optional
from flask import Flask, jsonify
from app.config import Config

__version__ = "0.1.0"


def create_app(config: Optional[Config] = None) -> Flask:
    """Create and configure Flask application instance."""
    app = Flask(__name__)

    if config is None:
        config = Config()

    app.config["APP_CONFIG"] = config
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["DEBUG"] = config.DEBUG
    app.config["VERSION"] = __version__

    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": "The requested resource does not exist"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

    return app
