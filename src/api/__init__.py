# File: /flask-api/flask-api/src/api/__init__.py

from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .nodes import *
from .sensors import *