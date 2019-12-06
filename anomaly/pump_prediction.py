"""
This program uses the Random Forest machine learning model to predict whether a coin is going to be pumped or not, given
information about all the necessary features.
Implemented from the paper: The Anatomy of a Cryptocurrency Pump and Dump Scheme by Xu, Livshits.
"""

import sys
import pyreadr
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


pd.set_option("display.max_columns", 100000)
pd.set_option("display.max_rows", 100000)
np.set_printoptions(threshold=sys.maxsize)


# get the pump activities from telegram channels
# return all the pumps and all the (unique) coins that have been pumped
def get_pump_activities():
    pumps = pd.read_csv("./pump_data/telegrampumps.csv", encoding="ISO-8859-1")
    pumps_unique = pumps.drop_duplicates(subset=["Symbol", "datetime", "dex"])
    return pumps, pumps_unique


# get information about the involved exchanges in the known pumps
# return the information about those exchanges
def get_coin_list(pumps):
    pump_exchanges = np.sort(pumps["dex"].unique())  # get the names of the exchanges
    dexs = np.append(pump_exchanges, ['CCCAGG'])  # and CCCAGG
    return pump_exchanges, dexs


# get the price of the pumped coins on different exchanges.
# get all coin status on those exchanges
# return the pump events on the 4 main exchanges
def get_listing_status(pumps, pumps_unique, dexs):
    hour_price = []
    cryptopia_coins = pd.read_csv("./pump_data/cryptopia_coins_regression.csv")
    # list of all coins (symbols), collected from different dataset.
    symbols = np.unique(np.append(pumps["Symbol"], cryptopia_coins["Symbol"]))

    #  listing status in terms of total number on different exchanges
    listing_status = pd.DataFrame(index=["Active", "Delisted", "Total"], columns=dexs[0:4])
    pumps_cryptopia = pumps_unique.loc[pumps_unique['dex'] == dexs[2]]  # dexs[2] = Cryptopia

    # list of active coins that have been pumped on Cryptopia
    listed_cryptopia = cryptopia_coins.loc[(cryptopia_coins["ListingStatus"] == "Active") & (cryptopia_coins["pumped"] == True)]

    listing_status.iloc[0]["Cryptopia"] = len(listed_cryptopia)
    listing_status.iloc[1]["Cryptopia"] = len(np.unique(pumps_cryptopia["Symbol"])) - len(listed_cryptopia)
    listing_status.iloc[2]["Cryptopia"] = len(np.unique(pumps_cryptopia["Symbol"]))

    # list of active coins that have been pumped on Binance
    binance_coins = pd.read_csv("./pump_data/binance_coins.csv")
    bittrex_coins = pd.read_csv("./pump_data/bittrex_coins.csv")

    # list of active coins that have been pumped on Yobit
    yobit_coins = pd.read_csv("./pump_data/yobit_coins.csv")

    pumps_binance = pumps_unique.loc[pumps_unique['dex'] == dexs[0]]  # dexs[0] = Binance
    pumps_bittrex = pumps_unique.loc[pumps_unique['dex'] == dexs[1]]  # dexs[1] = Bittrex
    pumps_yobit = pumps_unique.loc[pumps_unique['dex'] == dexs[3]]  # dexs[3] = Binance

    listed_binance = pd.DataFrame()
    listed_bittrex = pd.DataFrame()
    listed_yobit = pd.DataFrame()
    unique_coins = np.unique(pumps_binance["Symbol"])

    # get unique coins listed on Binance
    for i in range(len(binance_coins)):
        sym = binance_coins.iloc[i]["symbol"]
        sym = sym[0:-3]  # remove the last 3 characters (paired coin)
        if sym in unique_coins:
            listed_binance.append(binance_coins.iloc[i])

    # get unique coins listed on Bitrrex
    unique_coins = np.unique(pumps_bittrex["Symbol"])
    for i in range(len(bittrex_coins)):
        sym = bittrex_coins.iloc[i]["Currency"]
        sym = sym[0:-3]
        if sym in unique_coins:
            listed_bittrex.append(bittrex_coins.iloc[i])

    # get the final listed status table, to see active and delisted numbers of coins
    # for binance
    listing_status.iloc[0]["Binance"] = len(listed_binance)
    listing_status.iloc[1]["Binance"] = len(np.unique(pumps_binance["Symbol"])) - len(listed_binance)
    listing_status.iloc[2]["Binance"] = len(np.unique(pumps_binance["Symbol"]))

    # for bittrex
    listing_status.iloc[0]["Bittrex"] = len(listed_bittrex)
    listing_status.iloc[1]["Bittrex"] = len(np.unique(pumps_bittrex["Symbol"])) - len(listed_bittrex)
    listing_status.iloc[2]["Bittrex"] = len(np.unique(pumps_bittrex["Symbol"]))

    # for yobit
    listing_status.iloc[0]["Yobit"] = len(listed_yobit)
    listing_status.iloc[1]["Yobit"] = len(np.unique(pumps_yobit["Symbol"])) - len(listed_yobit)
    listing_status.iloc[2]["Yobit"] = len(np.unique(pumps_yobit["Symbol"]))

    print("Listing status: ")
    print(listing_status)
    return pumps_binance, pumps_bittrex, pumps_cryptopia, pumps_yobit


# plot the pumps on different exchanges on different periods of time
# to get an idea of how active these exchanges were on pump and dump schemes
def plot_pumps(pumps_binance, pumps_bittrex, pumps_cryptopia, pumps_yobit):
    # get market caps of all the coins, add to features
    caps = pd.read_csv("./pump_data/coin_caps.csv")

    # For Binance
    time_line_binance = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime("%d %b") for date in pumps_binance["datetime"]]
    time_line_binance.reverse()
    num_pumps_binance = np.arange(0., len(pumps_binance), 1)

    plt.xticks(rotation=45)
    plt.plot(time_line_binance, num_pumps_binance)
    plt.gca().set(xlabel="Time", ylabel="Number of pumps", title="Number of pumps on Binance")
    plt.show()

    # For Bittrex
    time_line_bittrex = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime("%d %b") for date in pumps_bittrex["datetime"]]
    time_line_bittrex.reverse()
    num_pumps_bittrex = np.arange(0., len(pumps_bittrex), 1)

    plt.xticks(rotation=45)
    plt.plot(time_line_bittrex, num_pumps_bittrex, 'g-')
    plt.gca().set(xlabel="Time", ylabel="Number of pumps", title="Number of pumps on Bittrex")
    plt.show()

    # For Yobit
    time_line_yobit = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime("%d %b") for date in pumps_yobit["datetime"]]
    time_line_yobit.reverse()
    num_pumps_yobit = np.arange(0., len(pumps_yobit), 1)

    plt.xticks(rotation=45)
    # Set the locator
    locator = mdates.MonthLocator()  # every month
    # Specify the format - %b gives us Jan, Feb...
    fmt = mdates.DateFormatter('%b')
    plt.plot(time_line_yobit, num_pumps_yobit, 'p-')
    plt.gca().xaxis.set_major_locator(locator)
    plt.gca().xaxis.set_major_formatter(fmt)
    plt.gca().set(xlabel="Time: From 21 July to 27 Oct 2018", ylabel="Number of pumps", title="Number of pumps on Yobit")
    plt.show()

    # For Cryptopia
    fig, ax = plt.subplots()
    num_pumps_cryptopia = np.arange(0., len(pumps_cryptopia), 1)
    time_line_cryptopia = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime("%d %b") for date in pumps_cryptopia["datetime"]]
    time_line_cryptopia.reverse()
    # print(time_line_cryptopia)

    # Set the locator
    locator = mdates.MonthLocator()  # every month
    # Specify the format - %b gives us Jan, Feb...
    fmt = mdates.DateFormatter('%b')
    plt.plot(time_line_cryptopia, num_pumps_cryptopia, 'r-')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)
    fig.autofmt_xdate()
    ax.set(xlabel="Time: from July to Oct 2018", ylabel="Number of pumps",
           title="Number of pumps on Cryptopia")
    plt.xticks(rotation=45)
    plt.show()


# create the regression table with feature data, combined with previously extracted data,
# get it ready to be loaded.
# Only for Cryptopia as this is the most active exchange with pump and dump schemes as
# well as we were able to get the all necessary data from it.
def create_regression_table():
    pumps_cryptopia = pd.read_csv("./pump_data/pumps_cryptopia.csv", encoding="ISO-8859-1")
    num_pumps = np.arange(0., len(pumps_cryptopia), 1)
    reprate = pumps_cryptopia["reprate"]
    reprate = reprate.iloc[::-1]
    plt.plot(num_pumps, reprate)
    plt.gca().set(xlabel="pumps", ylabel="Index")
    plt.show()

    # create regression table for cryptopia
    # this data will be used to train the models
    reg_cryptopia = pd.read_csv("./pump_data/reg_cryptopia.csv")
    reg_cryptopia_new = reg_cryptopia.drop(reg_cryptopia.columns[[1, 2]], axis=1)


# get the data for all coins listed on Cryptopia.
# return the data so we can train the random forest models with it.
def load_data():
    reg_cryptopia = pd.read_csv("./pump_data/reg_cryptopia_new.csv")
    print("Features: ")
    print(reg_cryptopia.columns)
    reg_cryptopia = reg_cryptopia.drop(reg_cryptopia.index[[45000, 70300]])
    reg_cryptopia = shuffle(reg_cryptopia)
    reg_cryptopia.reset_index(inplace=True, drop=True)
    return reg_cryptopia


# prepare the data for training and testing
# the data is split with different ratios for different random forest models
# return all these set of X and Y in training data so we can use them to train the models
def split_data(data):
    X_reg = data.drop(["pumped"], axis=1)  # or X
    Y_reg = data[["pumped"]]  # or Y
    X_1 = X_reg[:3000]  # training data for classifier model 1
    Y_1 = Y_reg[:3000]  # training data for classifier model 1
    X_2 = X_reg[:50000]  # training data for classifier model 2
    Y_2 = Y_reg[:50000]  # training data for classifier model 2

    X_1.fillna(0, inplace=True)  # replace NA values in the data with 0
    Y_1.fillna(0, inplace=True)
    X_2.fillna(0, inplace=True)
    Y_2.fillna(0, inplace=True)
    return X_reg, Y_reg, X_1, Y_1, X_2, Y_2


# train a given random forest model with given training data and cross validation
# return the predictions and the scores of the model, using built in sklearn random
# forest library
def run_random_forest(X_data, Y_data, rf_classifier, cross_validation):
    scores = []
    predictions = []

    for train_index, test_index in cross_validation.split(X_data, Y_data):
        print("*****")
        # Split the data into training data and test data
        x_train, x_test = X_data.iloc[train_index], X_data.iloc[test_index]
        y_train, y_test = Y_data.iloc[train_index], Y_data.iloc[test_index]
        # print out some general information about the data in this split
        print("X_train: ", x_train.shape)
        print("Y_train: " + str(y_train.shape) + " - Number of True values: " +
              str(len(y_train) - y_train["pumped"].value_counts()[False]))
        print("X_test: ", x_test.shape)
        print("Y_test: " + str(y_test.shape) + " - Number of True values: " +
              str(len(y_test) - y_test["pumped"].value_counts()[False]))

        # train the model
        rf_classifier.fit(x_train, y_train.values.ravel())
        # test with cross validation
        prediction = rf_classifier.predict(x_test)
        prediction = prediction.reshape((prediction.shape[0], 1))
        predictions.append(prediction)
        score = rf_classifier.score(x_test, y_test.values.ravel())
        print("Are predictions the same as actual values? " + str(np.array_equiv(prediction, y_test.values)))
        scores.append(score)

    return predictions, scores


# run the random forest model with the test data, and print out the result
# need to pass in the split point as parameter as which part of the data is
# considered the test data, that the model has not seen yet.
def test_model(scores, X_reg, Y_reg, split_point, rf_classifier, model_num):
    print(scores)
    print("Shape of test data: For X: " + str(X_reg[split_point:].shape) + " - For Y: " + str(Y_reg[split_point:].shape))
    X_t = X_reg[split_point:]
    X_t.fillna(0, inplace=True)
    Y_t = Y_reg[split_point:]
    Y_t.fillna(0, inplace=True)
    rf_classifier.predict(X_t)
    s = rf_classifier.score(X_t, Y_t)
    print("Number of True values in Y_test: ", len(Y_t) - Y_t["pumped"].value_counts()[False])
    print("Accuracy of model " + str(model_num) + " :" + str(s))
    print("==================")


# given the training data, we need to stratify it first with cross validation because of
# the nature of the data, where it is extremely imbalanced.
# create two different random forest models, train them with given training data.
# then test the models with the actual test data.
def predict_results(X_reg, Y_reg, X_1, Y_1, X_2, Y_2):
    # Apply cross validation and stratify the data with both models
    cross_validation = StratifiedKFold(n_splits=5, shuffle=True, random_state=None)

    # create and train the first random forest model
    print("Running the 1st model...")
    rf_classifier_1 = RandomForestClassifier(n_estimators=30, criterion='gini', max_depth=5, min_samples_split=2,
                                             min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto',
                                             max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None,
                                             bootstrap=True, oob_score=False, n_jobs=-1, random_state=0, verbose=0,
                                             warm_start=False, class_weight='balanced')
    predictions_1, scores_1 = run_random_forest(X_1, Y_1, rf_classifier_1, cross_validation)
    print("Done!\n")

    print("************************\n")

    # create and train the second random forest model
    print("Running the 2nd model...")
    rf_classifier_2 = RandomForestClassifier(n_estimators=200, criterion='gini', max_depth=5, min_samples_split=2,
                                             min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto',
                                             max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None,
                                             bootstrap=True, oob_score=False, n_jobs=-1, random_state=0, verbose=0,
                                             warm_start=False, class_weight='balanced')
    predictions_2, scores_2 = run_random_forest(X_2, Y_2, rf_classifier_2, cross_validation)
    print("Done!\n")

    # TEST THE MODELS WITH TEST DATA
    # for model 1
    test_model(scores_1, X_reg, Y_reg, 3001, rf_classifier_1, 1)

    # for model 2
    test_model(scores_2, X_reg, Y_reg, 50001, rf_classifier_2, 2)
