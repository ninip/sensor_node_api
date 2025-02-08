from src.database import db
from src.models.sensor import Sensor
from src.services.base_service import BaseService, session_scope


class SensorService(BaseService):
    def __init__(self):
        super().__init__(Sensor)
        
    def connect_to_node(self, sensor_id: int, node_id: int):
        with session_scope() as session:
            sensor = session.query(Sensor).get(sensor_id)
            if not sensor:
                return None

            sensor.node_id = node_id
            session.add(sensor)  # Explicitly add the modified instance
            session.flush()
            session.refresh(sensor)
            return sensor.to_dict()
