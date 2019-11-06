

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
# Pulls the raw data from exchanges. Returns list of fetched symbols.
# -- EXAMPLE INPUT --
# exchange = 'binance'
# from_date = '2019-04-20 00:00:00'
# number_candles = 240 - number of candles
# candle_size = '12h' - candlesticks
# f_path = '../data' - CSV OHLCV file path for output
def pull_data(exchange, from_date, number_candles, candle_size, f_path):
    return 1


# ---- Pump and Dump - Kainth ----
# Gets symbol name from the csv file.
def get_symbol(f_path):
    return "XRP-BTC"  # Example


# ---- Pump and Dump - Kainth ----
# Main analysis method for pump and dump detection. Returns final dataframe with number of pump and dumps.
# -- EXAMPLE INPUT --
# symbol_name : "XRP-BTC" - symbol name provided by the exchange.
# f_path : '../data' - output file from previously generated.
# volume_thresh : 5 (500%) - volume threshold
# price_thresh : 1.05 (5%) -  price threshold
# window_size : 24 - size of the window for the rolling average (in hours)
# candle_size = '12h' - candlesticks
def analyse_symbol(symbol_name, f_path, volume_thresh, price_thresh, window_size, candle_size):
    return 1
