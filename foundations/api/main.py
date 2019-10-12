from flask import Flask
from flask_restful import Api
from resources.address import AddressEndpoint
from resources.block import BlockEndpoint
from resources.transaction import TransactionEndpoint

# Flask application initialization
app = Flask(__name__)
api = Api(app)

# Endpoints
api.add_resource(AddressEndpoint, '/bitcoin/addresses')
api.add_resource(BlockEndpoint, '/bitcoin/blocks')
api.add_resource(TransactionEndpoint, '/bitcoin/transactions')

if __name__ == '__main__':
    # debug=True in development mode, for production set debug=False
    app.run(debug=True)
