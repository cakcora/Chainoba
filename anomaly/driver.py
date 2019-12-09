from anomaly.kainth_pump_dump import analysis_pump_dump


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
def get_account_features():
    return None


# Ponzi Scheme - Ethereum - Karan
# Extracting Code Features from Transaction Data
def get_code_features():
    return None


# Ponzi Scheme - Ethereum - Karan
# Build the classification model using Random Forest
def classify_contract_as_ponzi():
    return None


# Ponzi Scheme - Ethereum - Karan
# Apply the model on all Smart Contracts in Ethereum
def ponzi_scheme_detection():
    return None
