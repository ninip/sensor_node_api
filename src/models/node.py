from src.database import db


class Node(db.Model):
    __tablename__ = 'node'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    firmware_version = db.Column(db.String(50), nullable=False)
    sensors = db.relationship('Sensor', back_populates='node', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'serial_number': self.serial_number,
            'firmware_version': self.firmware_version,
            'sensors': [sensor.to_dict() for sensor in self.sensors] if self.sensors else []
        }
