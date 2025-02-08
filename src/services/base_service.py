from src.database import db
from typing import List, Optional
from contextlib import contextmanager


@contextmanager
def session_scope():
    '''
    Context manager for database session to ensure connection is closed'''
    session = db.session()  # connect to db
    try:
        yield session  # run function
        session.commit()  # commit any changes
    except Exception as e:
        session.rollback()  # remove any changes that resulted in an exception
        raise e
    finally:
        session.close()  # close the db connection


class BaseService:
    ''' Base service class for CRUD operations on database models'''

    def __init__(self, model):
        self.model = model


    def get_all(self, query_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        with session_scope() as session:
            query = session.query(self.model)

            if query_params:
                try:
                    # Apply filters if query parameters exist
                    for key, value in query_params.items():
                        if hasattr(self.model, key):
                            query = query.filter(
                                getattr(self.model, key) == value)
                except Exception as e:
                    raise ValueError(f"Invalid query parameters: {str(e)}")

            items = query.all()
            return [item.to_dict() for item in items] if items else []

    def get_by_identifier(self, identifier: str):
        ''' identifier can be either an ID or a serial number
        if it is a digit, it is an ID, otherwise it is a serial number'''
        if identifier.isdigit():
            return self.get_by_id(int(identifier))
        else:
            return self.get_by_serial(identifier)

    def get_by_id(self, id):
        with session_scope() as session:
            item = session.query(self.model).get(id)
            return item.to_dict() if item else None

    def get_by_serial(self, serial_number):
        with session_scope() as session:
            item = session.query(self.model).filter_by(
                serial_number=serial_number).first()
            return item.to_dict() if item else None

    def create(self, **kwargs):
        with session_scope() as session:
            try:
                instance = self.model(**kwargs)
                session.add(instance)
                session.flush()  # Flush to get the ID while in session
                return instance.to_dict()
            except ValueError as e:
                raise ValueError(str(e))
            except Exception as e:
                raise ValueError(
                    f"Failed to create {self.model.__name__}: {str(e)}")

    def update(self, instance_dict: dict, **kwargs):
        with session_scope() as session:
            # Get the actual instance from database
            instance = session.query(self.model).get(instance_dict['id'])
            if not instance:
                raise ValueError(f"{self.model.__name__} not found")

            # Update attributes
            for key, value in kwargs.items():
                setattr(instance, key, value)

            session.flush()
            return instance.to_dict()

    def delete_by_id(self, id: int) -> bool:
        with session_scope() as session:
            instance = session.query(self.model).get(id)
            if not instance:
                return False
            session.delete(instance)
            return True

    def delete(self, instance_dict: dict) -> bool:
        return self.delete_by_id(instance_dict['id'])
