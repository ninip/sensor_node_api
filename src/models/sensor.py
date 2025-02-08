from src.database import db
from sqlalchemy import TypeDecorator, String


class ModalityType(TypeDecorator):
    ''' Measurement type is used to define the type of value in the table.'''
    impl = String(20)
    cache_ok = True

    TEMPERATURE = "TEMPERATURE"
    WIND = "WIND"
    HUMIDITY = "HUMIDITY"
    PRESSURE = "PRESSURE"

    def process_bind_param(self, value, _):
        ''' 
        Ensures value matches Modelity Type & 
        converts to uppercase before storing in DB
        '''
        if value is None:
            raise ValueError("Modality type cannot be None")

        value = value.upper()
        if value not in {self.TEMPERATURE, self.WIND, self.HUMIDITY,
                         self.PRESSURE}:
            raise ValueError("Invalid modality type value")
        return value

    def process_result_value(self, value, _):
        ''' Convert to title case before returning to API
        '''
        if value is None:
            raise ValueError("Modality type cannot be None")

        if value not in {self.TEMPERATURE, self.WIND, self.HUMIDITY,
                         self.PRESSURE}:
            raise ValueError("Invalid modality type value")
        return value.title()


class Sensor(db.Model):
    __tablename__ = 'sensor'
    __table_args__ = {'extend_existing': True}  # Add this line

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    modality = db.Column(ModalityType, nullable=False)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'), nullable=True)

    node = db.relationship('Node', back_populates='sensors')

    def to_dict(self):
        return {
            'id': self.id,
            'serial_number': self.serial_number,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'modality': self.modality.title(),
            'node_id': self.node_id
        }
