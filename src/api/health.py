from flask import Blueprint, jsonify
from src.database import db
from datetime import datetime
from sqlalchemy import text

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connection with explicit text declaration and execution
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'

    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'version': '1.0.0'
    })
