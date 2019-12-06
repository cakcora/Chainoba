from flask import Flask
from flask_restful import Api
from resources.ponzy_schemes import GetPonziAnomalyDataEndpoint
from resources.transaction import GetTransactionDataByDateAndTokenNameEndpoint
from resources.transaction import GetTransactionDataByNodeEndpoint

# Flask application initialization
app = Flask(__name__)
api = Api(app)

# Endpoints
api.add_resource(GetTransactionDataByDateAndTokenNameEndpoint, '/ethereum/transactions')
api.add_resource(GetTransactionDataByNodeEndpoint, '/ethereum/node/transactions')
api.add_resource(GetPonziAnomalyDataEndpoint, '/ethereum/ponzi/data')

if __name__ == '__main__':
    # debug=True in development mode, for production set debug=False
    app.run(debug=True, port=6000)
