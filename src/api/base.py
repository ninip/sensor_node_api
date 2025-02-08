from flask import jsonify, request


class BaseAPI:
    ''' Base API class for CRUD operations on services'''''

    def __init__(self, service, name):
        self.service = service
        self.name = name

    def get_all(self):
        """Get all items of this type."""
        items = self.service.get_all()
        return jsonify(items), 200

    def get_one(self, identifier: str):
        item_dict = self.service.get_by_identifier(identifier)
        if not item_dict:
            return jsonify({'error': f'{self.name} not found'}), 404
        return jsonify(item_dict), 200

    def create(self):
        data = request.get_json()
        try:
            item_dict = self.service.create(**data)
            return jsonify(item_dict), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    def update(self, identifier: str):
        """Update an item by its identifier."""
        item_dict = self.service.get_by_identifier(identifier)
        if not item_dict:
            return jsonify({'error': f'{self.name} not found'}), 404

        data = request.get_json()
        try:
            updated_dict = self.service.update(item_dict, **data)
            return jsonify(updated_dict), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    def delete(self, identifier: str):
        """Delete an item by its identifier."""
        item = self.service.get_by_identifier(identifier)
        if not item:
            return jsonify({'error': f'{self.name} not found'}), 404

        success = self.service.delete(item)
        if not success:
            return jsonify({'error': f'Failed to delete {self.name}'}), 500

        return '', 204
