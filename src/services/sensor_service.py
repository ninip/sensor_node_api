from src.database import db
from src.models.sensor import Sensor
from src.services.base_service import BaseService


class SensorService(BaseService):
    def __init__(self):
        super().__init__(Sensor)

    def connect_to_node(self, sensor_id: int, node_id: int):
        sensor = self.get_by_id(sensor_id)
        if sensor:
            sensor.node_id = node_id
            db.session.commit()
        return sensor
