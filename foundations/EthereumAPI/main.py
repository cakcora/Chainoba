from flask import Flask
from flask_restful import Api
from foundations.EthereumAPI.resources.transaction import GetTransactionDataByDateEndpoint
from foundations.EthereumAPI.resources.transaction import GetTransactionDataByNodeEndpoint


# Flask application initialization
app = Flask(__name__)
api = Api(app)

# Endpoints
api.add_resource(GetTransactionDataByDateEndpoint, '/ethereum/transactions')
api.add_resource(GetTransactionDataByNodeEndpoint, '/ethereum/node/transactions')


if __name__ == '__main__':
    # debug=True in development mode, for production set debug=False
    app.run(debug=True)
