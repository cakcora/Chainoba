
import anomaly.pump_prediction


"""
----- Pump and Dump prediction -----
Given all information about all the necessary features, apply random forest
to predict which coin is going to be pumped.
"""


# get the pump activities from telegram channels
# # return all the pumps and all the (unique) coins that have been pumped
def get_pump_activities():
    return anomaly.pump_prediction.get_pump_activities()


# get information about the involved exchanges in the known pumps
# return the information about those exchanges
def get_coin_list(pumps):
    return anomaly.pump_prediction.get_coin_list(pumps)


# get the data for all coins listed on Cryptopia.
# return the data so we can train the random forest models with it.
def load_pump_data():
    anomaly.pump_prediction.load_data()


# prepare the data for training and testing
# the data is split with different ratios for different random forest models
# return all these set of X and Y in training data so we can use them to train the models
def split_data(data):
    return anomaly.pump_prediction.split_data(data)


# train a given random forest model with given training data and cross validation
# return the predictions and the scores of the model, using built in sklearn random
# forest library
def train_rf_model(X_data, Y_data, rf_classifier, cross_validation):
    return anomaly.pump_prediction.run_random_forest(X_data, Y_data, rf_classifier, cross_validation)


# given the data, we create, train and test the random forest models
def get_pump_predictions(X_reg, Y_reg, X_1, Y_1, X_2, Y_2):
    return anomaly.pump_prediction.predict_results(X_reg, Y_reg, X_1, Y_1, X_2, Y_2)


# ---- Pump and Dump - Kainth ----
# Main analysis method for pump and dump detection. Returns final dataframe with number of pump and dumps.
# -- EXAMPLE INPUT --
# f_path : 'data/lbank/lbank_AAC-ETH_[2019-11-20 00.00.00]-TO-[2019-12-07 02.00.00].csv'
# volume_thresh : 5 (500%) - volume threshold
# price_thresh : 1.05 (5%) -  price threshold
# window_size : 24 - size of the window for the rolling average (in hours)
# candle_size = '12h' - candlesticks
def pump_dump(f_path, volume_thresh, price_thresh, window_size, candle_size):
    df = analysis_pump_dump.analyse_symbol(f_path, volume_thresh, price_thresh, window_size, candle_size)
    return df


# Ponzi Scheme - Ethereum - Karan
# Extracting Account Features from the existing Smart Contracts
from anomaly.karan_ponzi.graph_comparison_ponzi import graph
def implement_random_forest_ponzi():
    '''graph_comparison() gives the graph analysis of the features of the schemes. random_forest_ponzi_evaluation() is called, which in turn is calling get_account_data(). get_account_data() gets the data from Etherscan.io'''
    return graph.graph_comparison()
