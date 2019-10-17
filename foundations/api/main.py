from flask import Flask
from flask_restful import Api
from foundations.api.resources.address import AddressEndpoint
from foundations.api.resources.block import BlockEndpoint
from foundations.api.resources.transaction import TransactionEndpoint
from foundations.api.resources.transaction_input import TransactionInputEndpoint
from foundations.api.resources.transaction_output import TransactionOutputEndpoint
from foundations.api.resources.transaction_output_address import TransactionOutputAddressEndpoint

# Flask application initialization
app = Flask(__name__)
api = Api(app)

# Endpoints
api.add_resource(AddressEndpoint, '/bitcoin/addresses')
api.add_resource(BlockEndpoint, '/bitcoin/blocks')
api.add_resource(TransactionEndpoint, '/bitcoin/transactions')
api.add_resource(TransactionInputEndpoint, '/bitcoin/transactions/inputs')
api.add_resource(TransactionOutputEndpoint, '/bitcoin/transactions/outputs')
api.add_resource(TransactionOutputAddressEndpoint, '/bitcoin/transactions/output_addresses')

if __name__ == '__main__':
    # debug=True in development mode, for production set debug=False
    app.run(debug=True)
