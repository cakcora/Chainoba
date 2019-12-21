#!/usr/bin/env python3
# Name: main.py
# Usecase: Contains all Bitcoin API definitions
# Functionalities:
#   1. Query Bitcoin data
#       a. get blocks by date
#       b. get blocks by block ID
#       c. get transactions by block ID
#       d. get transactions by transaction hash ID
#       e. get transactions inputs
#       f. get transactions outputs
#   2. Query and Store Graph team's results
#       a. get/post address distribution by date
#       b. get/post address feature by date
#       c. get/post assortivity coefficient by date
#       d. get/post bitcoin circulation by date
#       e. get/post chainlet occurrence by date
#       f. get/post clustering coefficient by date
#       g. get/post current balance by date
#       h. get/post activity level by date
#       i. get/post most active entity by date
#       j. get/post pearson coefficient by date
#       k. get/post strongly connected component by date
#       l. get/post total BTC received by date
#       m. get/post transaction size by date
#       n. get/post weakly connected component by date

from flask import Flask
from flask_restful import Api
from resources.address import AddressEndpoint
from resources.block import GetBlockDataByDateEndpoint, GetTransactionDataByBlockID
from resources.graph.address_distribution import AddressDistributionByDateEndpoint
from resources.graph.address_feature import AddressFeatureByDateEndpoint
from resources.graph.assortivity_coefficient import AssortativityCoefficientByDateEndpoint
from resources.graph.bitcoin_circulation import BitcoinCirculationByDateEndpoint
from resources.graph.chainlet_occurance import ChainletsOccuranceByDateEndpoint
from resources.graph.chainlet_occurance_amount import ChainletsOccuranceAmountByDateEndpoint
from resources.graph.clustring_coefficient import ClusteringCoefficientByDateEndpoint
from resources.graph.current_balance import CurrentBalanceByDateEndpoint
from resources.graph.level_of_activity import ActivityLevelByDateEndpoint
from resources.graph.most_active_entity import MostActiveEntityByDateEndpoint
from resources.graph.pearson_coefficient import PearsonCoefficientByDateEndpoint
from resources.graph.strongly_connected_component import StronglyConnectedComponentByDateEndpoint
from resources.graph.total_btc_received import TotalBtcReceivedByDateEndpoint
from resources.graph.transaction_size import TransactionSizeByDateEndpoint
from resources.graph.weakly_connected_component import WeaklyConnectedComponentByDateEndpoint
from resources.transaction import TransactionByHashEndpoint
from resources.transaction import TransactionEndpoint
from resources.transaction_input import TransactionInputEndpoint
from resources.transaction_output import TransactionOutputEndpoint
from resources.transaction_output_address import GetTransactionOutputAddressByTransactionOutputId

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
