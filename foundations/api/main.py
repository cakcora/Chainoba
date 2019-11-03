from flask import Flask
from flask_restful import Api
from resources.address import AddressEndpoint
from resources.block import GetBlockDataByDateEndpoint, GetTransactionDataByBlockID
from resources.transaction import TransactionEndpoint
from resources.transaction import TransactionByHashEndpoint
from resources.transaction_input import TransactionInputEndpoint
from resources.transaction_output import TransactionOutputEndpoint
from resources.transaction_output_address import GetTransactionOutputAddressByTransactionOutputId


# Flask application initialization
app = Flask(__name__)
api = Api(app)

# Endpoints
api.add_resource(AddressEndpoint, '/bitcoin/addresses')
api.add_resource(GetBlockDataByDateEndpoint, '/bitcoin/blocks/')
api.add_resource(GetTransactionDataByBlockID, '/bitcoin/blocks/transactions')
api.add_resource(TransactionByHashEndpoint, '/bitcoin/transaction')
api.add_resource(TransactionEndpoint, '/bitcoin/transactions')
api.add_resource(TransactionInputEndpoint, '/bitcoin/transactions/inputs')
api.add_resource(TransactionOutputEndpoint, '/bitcoin/transactions/outputs')
api.add_resource(GetTransactionOutputAddressByTransactionOutputId, '/bitcoin/transactions/outputs/addresses')

if __name__ == '__main__':
    # debug=True in development mode, for production set debug=False
    app.run(debug=True)
