from src.models.node import Node
from src.services.base_service import BaseService


class NodeService(BaseService):
    def __init__(self):
        super().__init__(Node)

    def get_sensors(self, node_identifer: setattr):
        node = self.get_by_identifier(node_identifer)
        return node.sensors if node else []
