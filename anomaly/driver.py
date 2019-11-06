# pump and dump prediction
# get the data price for pump and dump prediction
def load_price_data():
    return 0


# pump and dump prediction
# predict the pump possibilities of all the coins in the exchange
def generate_possibilities():
    return []


# pump and dump prediction
# predict the pump possibility of the given coin using Random Forest, 0.0 <= return value <= 1.0
def predict_coin_possibility(given_coin):
    return 0


# pump and dump prediction
# return all the coins with predicted possibilities greater than a chosen threshold (0.0 <= threshold <= 1.0)
def get_predicted_pumped_coins(threshold: float):
    return []


# fifth labor
# get list of transaction within a time period
def get_transaction_list(start_time, end_time):
    return []


# fifth labor
# get list of transactions related to the exchanges within a time period
def get_exchange_transaction(start_time, end_time):
    return []


# fifth labor
# build a local graph with the transaction_list, and markdown the transaction related to the exhchanges
def build_graph(transaction_list, excange_transaction_list):
    return "Graph edges and nodes"


# fifth labor
# detect the loop linking behaviour from the local graph and return the edges and nodes creating the loop
def find_loop(edge_list, nodes):
    return "Subgraph with detected loop"

# fifth labor
# predict the suspicious addresses from the loop subgraph
def suspicious_addresses_from_loop(loop_subgraph):
    return []


# fifth labor
# detect the loop spliting behaviour from the local graph and return the edges and nodes creating the split behaviour
def find_split_nodes(edge_list, nodes):
    return "Subgraph with split behaviour"

# fifth labor
# predict the suspicious addresses from the split subgraph
def suspicious_addresses_from_split_nodes(split_subgraph):
    return []
