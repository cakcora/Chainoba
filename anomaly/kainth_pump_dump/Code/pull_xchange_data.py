import ccxt
import pandas as pd
import time
import os


def create_ohlcv_df(data):
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(data, columns=header)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms', origin='unix')  # convert timestamp to datetime
    return df


# Pulls the raw data from exchanges. Returns list of fetched symbols.
# -- EXAMPLE INPUT --
# exchange = 'binance'
# from_date = '2019-11-20 00:00:00'
# number_candles = 240 - number of candles
# candle_size = '12h' - candlesticks
# f_path = '../data' - CSV OHLCV file path for output

def pull_data(exchange, from_date, n_candles, c_size, f_path, skip=False):
    count = 1
    msec = 1000
    hold = 5

    missing_symbols = []

    # -- create a folder --
    newpath = f_path + '/' + exchange + '/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # -- load exchange --
    exc_instance = getattr(ccxt, exchange)()
    exc_instance.load_markets()
    from_timestamp = exc_instance.parse8601(from_date)

    # -- pull ohlcv --
    for symbol in exc_instance.symbols:
        for attempt in range(3):  # 3 attempts max
            try:
                print('Pulling:', exchange, ':', symbol, '[{}/{}]'.format(count, len(exc_instance.symbols)))
                data = exc_instance.fetch_ohlcv(symbol, c_size, from_timestamp, n_candles)

                # if < n_candles returned, skip this pair
                if len(data) < n_candles and skip is True:
                    continue

                # -- create DF --
                df = create_ohlcv_df(data)

                # -- save CSV --
                symbol = symbol.replace("/", "-")

                filename = newpath + '{}_{}_[{}]-TO-[{}].csv'.format(exchange, symbol, df['Timestamp'].iloc[0],
                                                                     df['Timestamp'].iloc[-1])
                filename = filename.replace(":", ".")
                df.to_csv(filename)

            except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout,
                    IndexError) as error:
                print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
                time.sleep(hold)
            else:  # if no error, proceed to next iteration
                break
        else:  # we failed all attempts
            print('All attempts failed, skipping:', symbol)
            missing_symbols.append(symbol)
            continue

        count += 1

        time.sleep((exc_instance.rateLimit / msec) + 5)  # add 5 seconds to rate limit just to be safe

    # print out any symbols we could not obtain
    if len(missing_symbols) is not 0:
        print('Unable to obtain:', missing_symbols)

    return missing_symbols


from_date = '2019-11-20 00:00:00'
# exchanges = ['binance', 'kraken', 'kucoin', 'lbank']
exchanges = ['lbank']


for e in exchanges:
    pull_data(e, from_date, 480, '1h', '../data')
