from flask_restful import Resource


class Block(Resource):
    """Resource class endpoint to serve block related requests

    TODO: Complete the API
    """

    def get(self):
        return {'hello': 'world'}
