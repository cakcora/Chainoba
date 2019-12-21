#!/usr/bin/env python3
# Name: address.py
# Usecase: Bitcoin transaction address API
# Functionality: GET

from flask_restful import Resource
from models.models import Address
from models.models import db_session


class AddressEndpoint(Resource):
    """
    Class implementing address endpoint
    """

    def get(self):
        """
        Method for GET request
        """
        print(db_session.query(Address).first())
        return {'hello': 'world'}
