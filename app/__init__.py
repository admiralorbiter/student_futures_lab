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

    # Initialize pathway data service
    from .services.pathway_service import pathway_service

    pathway_service.init_app(app)

    # Make pathway_service available in all templates
    @app.context_processor
    def inject_pathway_service():
        return dict(pathway_service=pathway_service)

    # Register blueprints
    from .blueprints.main import bp as main_bp

    app.register_blueprint(main_bp)

    from .blueprints.explore import bp as explore_bp

    app.register_blueprint(explore_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
