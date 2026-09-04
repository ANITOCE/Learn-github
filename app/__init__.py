"""Math API application package."""

from flask import Flask

from app.routes import register_routes


def create_app() -> Flask:
    """Create and return a configured Flask application instance."""
    app = Flask(__name__)
    register_routes(app)
    return app
