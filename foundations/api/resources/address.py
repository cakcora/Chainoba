from flask_restful import Resource
from models.models import Address
from models.models import db_session


class AddressEndpoint(Resource):

    def get(self):
        print(db_session.query(Address).first())
        return {'hello': 'world'}
