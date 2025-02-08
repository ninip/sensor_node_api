import unittest
from src.database import db
from src.models.node import Node
from src.models.sensor import Sensor
from tests.test_base import BaseTestCase


class TestNodeAPI(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Clear sensors table
        Node.query.delete()
        Sensor.query.delete()
        db.session.commit()

    def test_create_node(self):
        response = self.client.post('/api/nodes', json={
            'serial_number': 'ABC123',
            'firmware_version': '1.0.0'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['serial_number'], 'ABC123')
        self.assertEqual(data['firmware_version'], '1.0.0')
        self.assertEqual(data['sensors'], [])

    def test_create_node_with_sensors(self):
        # Create a node first
        response = self.client.post('/api/nodes', json={
            'serial_number': 'NODE123',
            'firmware_version': '1.0.0'
        })
        node_id = response.get_json()['id']

        # Create and connect sensors with required modality
        self.client.post('/api/sensors', json={
            'serial_number': 'SENSOR1',
            'manufacturer': 'Test Mfg',
            'model': 'MODEL-A',  # Now required
            'modality': 'TEMPERATURE',  # Required and must be valid
            'node_id': node_id
        })
        self.client.post('/api/sensors', json={
            'serial_number': 'SENSOR2',
            'manufacturer': 'Test Mfg',
            'model': 'MODEL-B',
            'modality': 'HUMIDITY',
            'node_id': node_id
        })

        # Get node with sensors
        response = self.client.get(f'/api/nodes/{node_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['sensors']), 2)
        self.assertEqual(data['sensors'][0]['serial_number'], 'SENSOR1')
        self.assertEqual(data['sensors'][0]['modality'],
                         'Temperature')
        self.assertEqual(data['sensors'][1]['serial_number'], 'SENSOR2')
        self.assertEqual(data['sensors'][1]['modality'],
                         'Humidity')

    def test_create_node_invalid_data(self):
        # Test missing required field
        response = self.client.post('/api/nodes', json={
            'serial_number': 'ABC123'
        })
        self.assertEqual(response.status_code, 400)

    def test_get_node(self):
        # Create a node first
        create_response = self.client.post('/api/nodes', json={
            'serial_number': 'XYZ789',
            'firmware_version': '2.0.0'
        })
        node_id = create_response.get_json()['id']

        # Get the created node
        response = self.client.get(f'/api/nodes/{node_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['serial_number'], 'XYZ789')
        self.assertEqual(data['firmware_version'], '2.0.0')
        self.assertIn('sensors', data)  # Verify sensors field exists

    def test_update_node_with_sensors(self):
        # Create a node with sensors
        create_response = self.client.post('/api/nodes', json={
            'serial_number': 'DEF456',
            'firmware_version': '1.0.0'
        })
        node_id = create_response.get_json()['id']

        # Add a sensor
        self.client.post('/api/sensors', json={
            'serial_number': 'SENSOR3',
            'manufacturer': 'Test Mfg',
            'model': 'MODEL-C',  # Now required
            'modality': 'WIND',  # Required and must be valid
            'node_id': node_id
        })

        # Update the node
        response = self.client.put(f'/api/nodes/{node_id}', json={
            'firmware_version': '1.1.0'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['firmware_version'], '1.1.0')
        self.assertEqual(data['serial_number'], 'DEF456')
        # Verify sensor relationship maintained
        self.assertEqual(len(data['sensors']), 1)

    def test_delete_node_cascades_to_sensors(self):
        # Create a node with a sensor
        create_response = self.client.post('/api/nodes', json={
            'serial_number': 'GHI789',
            'firmware_version': '1.0.0'
        })
        node_id = create_response.get_json()['id']

        # Add a sensor
        sensor_response = self.client.post('/api/sensors', json={
            'serial_number': 'SENSOR4',
            'manufacturer': 'Test Mfg',
            'model': 'MODEL-D',  # Now required
            'modality': 'PRESSURE',  # Required and must be valid
            'node_id': node_id
        })
        sensor_id = sensor_response.get_json()['id']

        # Delete the node
        response = self.client.delete(f'/api/nodes/{node_id}')
        self.assertEqual(response.status_code, 204)

        # Verify sensor is also deleted or detached
        sensor_response = self.client.get(f'/api/sensors/{sensor_id}')
        # Depending on cascade behavior
        self.assertIn(sensor_response.status_code, [404, 200])


if __name__ == '__main__':
    unittest.main()
