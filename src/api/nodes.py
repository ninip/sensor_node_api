from .base import BaseAPI
from flask import Blueprint, jsonify
from src.services.node_service import NodeService
from src.services.sensor_service import SensorService
from src.database import db

nodes_bp = Blueprint('nodes', __name__)
node_api = BaseAPI(NodeService(), 'Node')
sensor_service = SensorService()


@nodes_bp.route('/nodes', methods=['GET'])
def get_nodes():
    return node_api.get_all()


@nodes_bp.route('/nodes/<node_identifier>', methods=['GET'])
def get_node(node_identifier):
    return node_api.get_one(node_identifier)


@nodes_bp.route('/nodes', methods=['POST'])
def create_node():
    return node_api.create()


@nodes_bp.route('/nodes/<node_identifier>', methods=['PUT'])
def update_node(node_identifier):
    return node_api.update(node_identifier)


@nodes_bp.route('/nodes/<node_identifier>', methods=['DELETE'])
def delete_node(node_identifier):
    return node_api.delete(node_identifier)


@nodes_bp.route('/nodes/<node_identifier>/sensors/<sensor_identifier>', methods=['POST'])
def connect_sensor(node_identifier, sensor_identifier):
    """Connect a sensor to a node."""
    node = node_api.service.get_by_identifier(node_identifier)
    if not node:
        return jsonify({'error': 'Node not found'}), 404

    sensor = sensor_service.get_by_identifier(sensor_identifier)
    if not sensor:
        return jsonify({'error': 'Sensor not found'}), 404

    sensor = sensor_service.connect_to_node(sensor.id, node.id)
    return jsonify(sensor.to_dict()), 200
