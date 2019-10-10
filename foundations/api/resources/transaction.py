from flask_restful import Resource


class Transaction(Resource):
    """Resource class endpoint to serve transaction related requests

    TODO: Complete the API
    """

    def get(self):
        return {'hello': 'world'}
