from flask_restful import Resource


class Address(Resource):
    """Resource class endpoint to serve address related requests

    TODO: Complete the API
    """

    def get(self):
        return {'hello': 'world'}
