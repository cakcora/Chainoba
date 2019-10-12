from flask_restful import Resource
from models.models import Transaction
from models.models import db_session


class TransactionEndpoint(Resource):
    """Resource class endpoint to serve transaction related requests

    TODO: Complete the API
    """

    def get(self):
        print(db_session.query(Transaction).first())
        return {'hello': 'world'}
