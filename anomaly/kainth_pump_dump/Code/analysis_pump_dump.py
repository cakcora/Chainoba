import ccxt
import pandas as pd
import os


# gets symbol name from the csv file
def get_symbol(f_path):
    df = pd.read_csv(f_path, index_col=0, parse_dates=["Timestamp"])
    filename = os.path.basename(f_path)
    symbol_name = filename.split("_")[1].replace("-", "/")
    print("Loading:", symbol_name)

    return symbol_name


# extracts the symbol pairs and stores them in a df per exchange
def extract_symbol_df_from_csvs(folder):
    for subdir, dirs, files in os.walk(folder):
        symbols = []

        exchange_n = subdir.split("/")[-1]

        if 'data' not in exchange_n:
            for file in files:
                if ".csv" in file:
                    symbols.append(get_symbol('../data/' + subdir + '/' + file))
            header = ['Symbol']
            df = pd.DataFrame(symbols, columns=header)
            filename = '{}_symbols.csv'.format(exchange_n)
            df.to_csv(filename)


# analyses all the symbol pairs in subfolders of a given folder
# returns a df indexed by exchange with the number price and volume spikes, and number of pumps
def analyse_folder(folder, vol_thresh, price_thresh, window_size=24, candle_size='1h'):
    row_list = []  # list for each row of the result df

    # -- loop through folders --
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if ".csv" in file:
                f_path = subdir + '/' + file
                result_row = analyse_symbol(f_path, vol_thresh, price_thresh, window_size, candle_size)
                row_list.append(result_row)

    # -- create result df --
    df = pd.DataFrame(row_list)
    df.set_index('Exchange', inplace=True)
    df.sort_index(inplace=True)

    return df


# Main analysis method for pump and dump detection. Returns final dataframe with number of pump and dumps.
# -- EXAMPLE INPUT --
# symbol_name : "XRP-BTC" - symbol name provided by the exchange.
# f_path : '../data' - output file from previously generated.
# volume_thresh : 5 (500%) - volume threshold
# price_thresh : 1.05 (5%) -  price threshold
# window_size : 24 - size of the window for the rolling average (in hours)
# candle_size = '12h' - candlesticks
# returns final dataframe
def analyse_symbol(f_path, volume_thresh, price_thresh, window_size=24, candle_size='1h'):
    # -- load the data --
    exchange_name, symbol_name, df = load_csv(f_path)

    # -- find spikes --
    vol_mask, vol_df = find_vol_spikes(df, volume_thresh, window_size)
    num_v_spikes = get_num_rows(vol_df)  # the number of volume spikes found for this symbol pair

    price_mask, price_df = find_price_spikes(df, price_thresh, window_size)
    num_p_spikes = get_num_rows(price_df)

    pd_mask, pd_df = find_price_dumps(df, window_size)

    vd_mask, vd_df = find_volume_dumps(df, window_size)

    # find coinciding price and volume spikes
    vp_combined_mask = (vol_mask) & (price_mask)
    vp_combined_df = df[vp_combined_mask]
    num_vp_combined_rows = get_num_rows(vp_combined_df)

    # coinciding price and volume spikes for alleged P&D (more than 1x per given time removed)
    vp_combined_rm = rm_same_day_pumps(vp_combined_df)
    num_alleged = get_num_rows(vp_combined_rm)

    # find coniciding price and volume spikes with dumps
    final_combined_mask = (vol_mask) & (price_mask) & (pd_mask)
    final_combined = df[final_combined_mask]
    final_combined_rm = rm_same_day_pumps(final_combined)  # remove indicators which occur on the same day
    num_final_combined = get_num_rows(final_combined_rm)

    row_entry = {'Exchange': exchange_name,
                 'Symbol': symbol_name,
                 'Price Spikes': num_p_spikes,
                 'Volume Spikes': num_v_spikes,
                 'Alleged Pump and Dumps': num_alleged,
                 'Pump and Dumps': num_final_combined}

    print(row_entry)

    return row_entry


def get_num_rows(df):
    return df.shape[0]


def rm_same_day_pumps(df):
    # Removes spikes that occur on the same day
    df = df.copy()
    df['Timestamp_DAYS'] = df['Timestamp'].apply(lambda x: x.replace(hour=0, minute=0, second=0))
    df = df.drop_duplicates(subset='Timestamp_DAYS', keep='last')

    return df


# finds volume spikes with a certain threshold and window size
# returns a boolean_mask, dataframe
def find_vol_spikes(df, v_thresh, win_size):
    # -- add rolling average column to df --
    vRA = str(win_size) + 'h Volume RA'
    add_RA(df, win_size, 'Volume', vRA)

    # -- find spikes --
    vol_threshold = v_thresh * df[vRA]  # v_thresh increase in volume
    vol_spike_mask = df["Volume"] > vol_threshold  # where the volume is at least v_thresh greater than the x-hr RA
    df_vol_spike = df[vol_spike_mask]

    return vol_spike_mask, df_vol_spike


# finds price spikes with a certain threshold and window size
# returns a boolean_mask, dataframe
def find_price_spikes(df, p_thresh, win_size):
    # -- add rolling average column to df --
    pRA = str(win_size) + 'h Close Price RA'
    add_RA(df, win_size, 'Close', pRA)

    # -- find spikes --
    p_threshold = p_thresh * df[pRA]  # p_thresh increase in price
    p_spike_mask = df["High"] > p_threshold  # where the high is at least p_thresh greater than the x-hr RA
    df_price_spike = df[p_spike_mask]
    return p_spike_mask, df_price_spike


# finds price dumps with a certain threshold and window size
# returns a boolean_mask, dataframe
def find_price_dumps(df, win_size):
    pRA = str(win_size) + "h Close Price RA"
    pRA_plus = pRA + "+" + str(win_size)

    df[pRA_plus] = df[pRA].shift(-win_size)
    price_dump_mask = df[pRA_plus] <= (df[pRA] + df[pRA].std())
    # if the xhour RA from after the pump was detected is <= the xhour RA (+std dev) from before the pump was detected
    # if the price goes from the high to within a range of what it was before

    df_p_dumps = df[price_dump_mask]
    return price_dump_mask, df_p_dumps


def find_volume_dumps(df, win_size):
    vRA = str(win_size) + "h Volume RA"
    vRA_plus = vRA + "+" + str(win_size)

    df[vRA_plus] = df[vRA].shift(-win_size)
    price_dump_mask = df[vRA_plus] <= (df[vRA] + df[vRA].std())
    # if the xhour RA from after the pump was detected is <= the xhour RA (+std dev) from before the pump was detected
    # if the volume goes from the high to within a range of what it was before

    df_p_dumps = df[price_dump_mask]
    return price_dump_mask, df_p_dumps


# adds a rolling average column with specified window size to a given df and col
def add_RA(df, win_size, col, name):
    df[name] = pd.Series.rolling(df[col], window=win_size, center=False).mean()


# returns a (exchange_name ,symbol_name, dataframe) tuple
def load_csv(f_path, suppress=True):

    df = pd.read_csv(f_path, index_col=0, parse_dates=["Timestamp"])
    filename = os.path.basename(f_path)
    exchange_name = filename.split("_")[0]
    symbol_name = filename.split("_")[1].replace("-", "/")

    if not suppress:
        print("Exchange:", exchange_name, "\nSymbol:", symbol_name)

    return exchange_name, symbol_name, df


# Any of the data collected from pull_xchange_data.py will work if plugged into the file path,
# the basic parameters can also be changed here
analyse_symbol(f_path='../data/binance/binance_ADA-BNB_[2019-11-20 00.00.00]-TO-[2019-11-29 01.00.00].csv',
               volume_thresh=4,
               price_thresh=1.05,
               window_size=12,
               candle_size='1h')
