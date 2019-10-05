from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


# TODO
# Add a database connection to PostgreSQL

class Address(Resource):
    def get(self):
        return {'hello': 'world'}


class Block(Resource):
    def get(self):
        return {'hello': 'world'}


class Transaction(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(Address, '/bitcoin/address')
api.add_resource(Block, '/bitcoin/block')
api.add_resource(Transaction, '/bitcoin/transaction')

if __name__ == '__main__':
    app.run(debug=True)
