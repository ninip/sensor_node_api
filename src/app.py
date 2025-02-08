from src.config import Config
from src.database import db, init_db

from flask import Flask
import os


def create_app():
    instance_path = os.path.abspath(os.path.join(os.getcwd(), 'instance'))
    os.makedirs(instance_path, exist_ok=True)
    app = Flask(__name__)

    # Use absolute path for database
    db_path = os.path.join(instance_path, 'sensor_node.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    # Initialize database
    with app.app_context():
        db.create_all()

    # Register blueprints
    from src.api.health import health_bp
    from src.api.nodes import nodes_bp
    from src.api.sensors import sensors_bp
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(nodes_bp, url_prefix='/api')
    app.register_blueprint(sensors_bp, url_prefix='/api')

    return app


# Create the application instance
application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000, debug=True)
