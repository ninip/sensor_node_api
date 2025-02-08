from flask import Blueprint
from src.services.sensor_service import SensorService
from .base import BaseAPI

sensors_bp = Blueprint('sensors', __name__)
sensor_api = BaseAPI(SensorService(), 'Sensor')


@sensors_bp.route('/sensors', methods=['GET'])
def get_sensors():
    return sensor_api.get_all()


@sensors_bp.route('/sensors/<sensor_identifier>', methods=['GET'])
def get_sensor(sensor_identifier):
    return sensor_api.get_one(sensor_identifier)


@sensors_bp.route('/sensors', methods=['POST'])
def create_sensor():
    return sensor_api.create()


@sensors_bp.route('/sensors/<sensor_identifier>', methods=['DELETE'])
def delete_sensor(sensor_identifier):
    return sensor_api.delete(sensor_identifier)


@sensors_bp.route('/sensors/<sensor_identifier>', methods=['PUT'])
def update_sensor(sensor_identifier):
    return sensor_api.update(sensor_identifier)
