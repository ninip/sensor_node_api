import unittest
from src.database import db
from src.models.sensor import Sensor, ModalityType
from tests.test_base import BaseTestCase


class TestSensorsAPI(BaseTestCase):
    def setUp(self):
        super().setUp()
        Sensor.query.delete()
        db.session.commit()

    def test_create_sensor(self):
        response = self.client.post('/api/sensors', json={
            'serial_number': 'SN123456',
            'manufacturer': 'Acme Corp',
            'model': 'ACM-2000',
            'modality': 'temperature'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['serial_number'], 'SN123456')
        self.assertEqual(data['manufacturer'], 'Acme Corp')
        self.assertEqual(data['modality'], 'Temperature')

    def test_create_sensor_invalid_modality(self):
        response = self.client.post('/api/sensors', json={
            'serial_number': 'SN123456',
            'manufacturer': 'Acme Corp',
            'model': 'ACM-2000',
            'modality': 'INVALID_TYPE'  # Not in ModalityType
        })
        self.assertEqual(response.status_code, 400)

    def test_create_sensor_invalid_data(self):
        # Test missing required fields
        response = self.client.post('/api/sensors', json={
            'model': 'ACM-2000'
        })
        self.assertEqual(response.status_code, 400)

    def test_create_sensor_missing_modality(self):
        response = self.client.post('/api/sensors', json={
            'serial_number': 'SN123456',
            'manufacturer': 'Acme Corp',
            'model': 'ACM-2000'
            # Missing required modality
        })
        self.assertEqual(response.status_code, 400)

    def test_get_sensor(self):
        # Create a sensor first
        create_response = self.client.post('/api/sensors', json={
            'serial_number': 'SN789012',
            'manufacturer': 'Acme Corp',
            'model': 'ACM-2000',
            'modality': 'HUMIDITY'
        })
        sensor_id = create_response.get_json()['id']

        # Get the created sensor
        response = self.client.get(f'/api/sensors/{sensor_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['serial_number'], 'SN789012')
        self.assertEqual(data['manufacturer'], 'Acme Corp')
        self.assertEqual(data['modality'], 'Humidity')  # Check title case

    def test_update_sensor(self):
        # Create a sensor first
        create_response = self.client.post('/api/sensors', json={
            'serial_number': 'SN345678',
            'manufacturer': 'Acme Corp',
            'model': 'ACM-2000',
            'modality': 'TEMPERATURE'
        })
        sensor_id = create_response.get_json()['id']

        # Update the sensor
        response = self.client.put(f'/api/sensors/{sensor_id}', json={
            'modality': 'PRESSURE',  # Must be uppercase
            'model': 'ACM-2001'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['modality'], 'Pressure')  # Check title case
        self.assertEqual(data['model'], 'ACM-2001')
        self.assertEqual(data['serial_number'], 'SN345678')


def test_delete_sensor(self):
    # Create a sensor first
    response = self.client.post('/api/sensors', json={
        'serial_number': 'SN901234',
        'manufacturer': 'Acme Corp',
        'model': 'ACM-2000',
        'modality': 'WIND'
    })
    self.assertEqual(response.status_code, 201)
    sensor_id = response.get_json()['id']

    # Delete the sensor
    response = self.client.delete(f'/api/sensors/{sensor_id}')
    self.assertEqual(response.status_code, 204)

    # Verify sensor is deleted
    get_response = self.client.get(f'/api/sensors/{sensor_id}')
    self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
