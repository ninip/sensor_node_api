from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initialize the database with the Flask app"""
    db.init_app(app)

    # Import models to ensure they're registered with SQLAlchemy
    from src.models.node import Node  # noqa: F401
    from src.models.sensor import Sensor  # noqa: F401

    return app
