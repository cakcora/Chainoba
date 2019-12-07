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
from resources.Graph.address_distribution import AddressDistributionByDateEndpoint
from resources.Graph.address_feature import AddressFeatureByDateEndpoint
from resources.Graph.assortivity_coefficient import AssortativityCoefficientByDateEndpoint
from resources.Graph.bitcoin_circulation import BitcoinCirculationByDateEndpoint
from resources.Graph.chainlet_occurance import ChainletsOccuranceByDateEndpoint
from resources.Graph.chainlet_occurance_amount import ChainletsOccuranceAmountByDateEndpoint
from resources.Graph.clustring_coefficient import ClusteringCoefficientByDateEndpoint
from resources.Graph.current_balance import CurrentBalanceByDateEndpoint
from resources.Graph.level_of_activity import ActivityLevelByDateEndpoint
from resources.Graph.most_active_entity import MostActiveEntityByDateEndpoint
from resources.Graph.pearson_coefficient import PearsonCoefficientByDateEndpoint
from resources.Graph.strongly_connected_component import StronglyConnectedComponentByDateEndpoint
from resources.Graph.total_btc_received import TotalBtcReceivedByDateEndpoint
from resources.Graph.transaction_size import TransactionSizeByDateEndpoint
from resources.Graph.weakly_connected_component import WeaklyConnectedComponentByDateEndpoint

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

## Graph Analysis API
api.add_resource(AddressFeatureByDateEndpoint, '/bitcoin/address_feature/date')
api.add_resource(AddressDistributionByDateEndpoint, '/bitcoin/address_distribution')
api.add_resource(TotalBtcReceivedByDateEndpoint, '/bitcoin/total_btc_received')
api.add_resource(ActivityLevelByDateEndpoint, '/bitcoin/activity_level')
api.add_resource(StronglyConnectedComponentByDateEndpoint, '/bitcoin/strongly_connected_component')
api.add_resource(WeaklyConnectedComponentByDateEndpoint, '/bitcoin/weakly_connected_component')
api.add_resource(TransactionSizeByDateEndpoint, '/bitcoin/transaction_size')
api.add_resource(CurrentBalanceByDateEndpoint, '/bitcoin/current_balance')
api.add_resource(AssortativityCoefficientByDateEndpoint, '/bitcoin/assortativity_coefficient')
api.add_resource(PearsonCoefficientByDateEndpoint, '/bitcoin/pearson_coefficient')
api.add_resource(ClusteringCoefficientByDateEndpoint, '/bitcoin/clustering_coefficient')
api.add_resource(BitcoinCirculationByDateEndpoint, '/bitcoin/bitcoin_circulation')
api.add_resource(MostActiveEntityByDateEndpoint, '/bitcoin/most_active_entity')
api.add_resource(ChainletsOccuranceByDateEndpoint, '/bitcoin/chainlets_occurance')
api.add_resource(ChainletsOccuranceAmountByDateEndpoint, '/bitcoin/chainlets_occurance_amount')

if __name__ == '__main__':
    # debug=True in development mode, for production set debug=False
    app.run(debug=True)
