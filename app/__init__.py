"""Flask application factory."""

import os

from flask import Flask

from .config import Config
from .extensions import db


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure data directory exists
    os.makedirs(os.path.dirname(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")), exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from .blueprints.main import bp as main_bp

    app.register_blueprint(main_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
