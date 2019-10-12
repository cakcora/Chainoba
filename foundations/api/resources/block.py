from flask_restful import Resource
from models.models import Block
from models.models import db_session


class BlockEndpoint(Resource):
    """Resource class endpoint to serve block related requests

    TODO: Complete the API
    """

    def get(self):
        print(db_session.query(Block).first())
        return {'hello': 'world'}
