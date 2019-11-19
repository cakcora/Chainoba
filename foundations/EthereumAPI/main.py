from flask import Flask
from flask_restful import Api
from foundations.EthereumAPI.resources.transaction import TransactionEndpoint


# Flask application initialization
app = Flask(__name__)
api = Api(app)

# Endpoints
api.add_resource(TransactionEndpoint, '/ethereum/transactions')


if __name__ == '__main__':
    # debug=True in development mode, for production set debug=False
    app.run(debug=True)
