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


pd.set_option("display.max_columns", 100000)
pd.set_option("display.max_rows", 100000)
np.set_printoptions(threshold=sys.maxsize)


""" GET PUMP ACTIVITIES """
pumps = pd.read_csv("./pump_data/telegrampumps.csv", encoding="ISO-8859-1")
pumps_unique = pumps.drop_duplicates(subset=["Symbol", "datetime", "dex"])


""" GET COIN LIST """
pump_exchanges = np.sort(pumps["dex"].unique())  # get the names of the exchanges
dexs = np.append(pump_exchanges, ['CCCAGG'])  # and CCCAGG


""" GET HOURLY PRICE """
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
# print(unique_coins)
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
        # print("**")
        # pd.merge(listed_binance, binance_coins[i])
        listed_bittrex.append(bittrex_coins.iloc[i])


# get the final listed status table, to see active and delisted numbers of coins
listing_status.iloc[0]["Binance"] = len(listed_binance)
listing_status.iloc[1]["Binance"] = len(np.unique(pumps_binance["Symbol"])) - len(listed_binance)
listing_status.iloc[2]["Binance"] = len(np.unique(pumps_binance["Symbol"]))


listing_status.iloc[0]["Bittrex"] = len(listed_bittrex)
listing_status.iloc[1]["Bittrex"] = len(np.unique(pumps_bittrex["Symbol"])) - len(listed_bittrex)
listing_status.iloc[2]["Bittrex"] = len(np.unique(pumps_bittrex["Symbol"]))


listing_status.iloc[0]["Yobit"] = len(listed_yobit)
listing_status.iloc[1]["Yobit"] = len(np.unique(pumps_yobit["Symbol"])) - len(listed_yobit)
listing_status.iloc[2]["Yobit"] = len(np.unique(pumps_yobit["Symbol"]))
print("Listing status: ")
print(listing_status)
# time1 = as.numeric(max(pumps$datetime)+3600*18)


# get market caps of all the coins, add to features
caps = pd.read_csv("./pump_data/coin_caps.csv")


""" NUMBER OF PUMPS THROUGH TIME GRAPHS """
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

""" REGRESSION TABLE """
pumps_cryptopia = pd.read_csv("./pump_data/pumps_cryptopia.csv", encoding="ISO-8859-1")
num_pumps = np.arange(0., len(pumps_cryptopia), 1)
reprate = pumps_cryptopia["reprate"]
reprate = reprate.iloc[::-1]
plt.plot(num_pumps, reprate)
plt.gca().set(xlabel="pumps", ylabel="Index")
plt.show()


""" CREATE REG_CRYPTOPIA_NEW """
# this data will be used to train the models
reg_cryptopia = pd.read_csv("./pump_data/reg_cryptopia.csv")
reg_cryptopia_new = reg_cryptopia.drop(reg_cryptopia.columns[[1, 2]], axis=1)


# TODO: could try to add more columns to reg_cryptopia_new manually, right now temporarily read data from csv file
""" APPLY RANDOM FOREST MODEL"""
reg_cryptopia_new = pd.read_csv("./pump_data/reg_cryptopia_new.csv")
reg_cryptopia_new = reg_cryptopia_new.drop(reg_cryptopia_new.index[[45000, 70300]])
reg_cryptopia_new = shuffle(reg_cryptopia_new)
reg_cryptopia_new.reset_index(inplace=True, drop=True)


X_reg = reg_cryptopia_new.drop(["pumped"], axis=1)  # or X
Y_reg = reg_cryptopia_new[["pumped"]]  # or Y
X_1 = X_reg[:3000]  # training data for classifier model 1
Y_1 = Y_reg[:3000]  # training data for classifier 1
X_2 = X_reg[:50000]  # training data for classifier 2
Y_2 = Y_reg[:50000]  # training data for classifier 2

X_1.fillna(0, inplace=True)  # replace NA values with 0
Y_1.fillna(0, inplace=True)
X_2.fillna(0, inplace=True)
Y_2.fillna(0, inplace=True)
# print("&&&&&&&" + str(type(X_1)))
# print(np.where(np.isnan(X)))
# np.nan_to_num(Y)
# pd.DataFrame(Y).fillna(0)


def run_random_forest(X_data, Y_data, rf_classifier, cross_validation):
    scores = []
    predictions = []

    for train_index, test_index in cross_validation.split(X_data, Y_data):
        print("*****")
        x_train, x_test = X_data.iloc[train_index], X_data.iloc[test_index]
        y_train, y_test = Y_data.iloc[train_index], Y_data.iloc[test_index]
        print("X_train: ", x_train.shape)
        print("Y_train: " + str(y_train.shape) + " - Number of True values: " +
              str(len(y_train) - y_train["pumped"].value_counts()[False]))
        print("X_test: ", x_test.shape)
        print("Y_test: " + str(y_test.shape) + " - Number of True values: " +
              str(len(y_test) - y_test["pumped"].value_counts()[False]))

        # train the model
        rf_classifier.fit(x_train, y_train.values.ravel())
        prediction = rf_classifier.predict(x_test)
        prediction = prediction.reshape((prediction.shape[0], 1))
        # print("0000:" + str(prediction.shape))
        predictions.append(prediction)
        # print(predictions)
        score = rf_classifier.score(x_test, y_test.values.ravel())
        # print(prediction.shape)
        # diff = []
        print("Are preditions same as actual values? " + str(np.array_equiv(prediction, y_test.values)))
        # for i in range(prediction.shape[0]):
        #     # print("pred: " + str(prediction[i]) + "; " + str(y_test.values[i]))
        #     if prediction[i] != y_test.values[i]:
        #         diff.append(i)
        # print("diff: ", diff)
        scores.append(score)

    return predictions, scores


# Apply cross validation and stratify the data with both models
cross_validation = StratifiedKFold(n_splits=5, shuffle=True, random_state=None)

print("Running the 1st model...")
rf_classifier_1 = RandomForestClassifier(n_estimators=30, criterion='gini', max_depth=5, min_samples_split=2,
                                         min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto',
                                         max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None,
                                         bootstrap=True, oob_score=False, n_jobs=-1, random_state=0, verbose=0,
                                         warm_start=False, class_weight='balanced')
predictions_1, scores_1 = run_random_forest(X_1, Y_1, rf_classifier_1, cross_validation)
print("Done!\n")

print("************************\n")
print("Running the 2nd model...")
rf_classifier_2 = RandomForestClassifier(n_estimators=200, criterion='gini', max_depth=5, min_samples_split=2,
                                         min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto',
                                         max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None,
                                         bootstrap=True, oob_score=False, n_jobs=-1, random_state=0, verbose=0,
                                         warm_start=False, class_weight='balanced')
predictions_2, scores_2 = run_random_forest(X_2, Y_2, rf_classifier_2, cross_validation)
print("Done!")


# TEST THE MODELS WITH TEST DATA
print(scores_1)
print("Shape of test data: For X: " + str(X_reg[3001:].shape) + " - For Y: " + str(Y_reg[3001:].shape))
X_t = X_reg[3001:]
X_t.fillna(0, inplace=True)
Y_t = Y_reg[3001:]
Y_t.fillna(0, inplace=True)
rf_classifier_1.predict(X_t)
s = rf_classifier_1.score(X_t, Y_t)
print("Number of True values in Y_test: ", len(Y_t) - Y_t["pumped"].value_counts()[False])
print("Accuracy of model 1: " + str(s))
print("==================")

print(scores_2)
print("Shape of test data: For X: " + str(X_reg[50001:].shape) + " - For Y: " + str(Y_reg[50001:].shape))
X_t = X_reg[50001:]
X_t.fillna(0, inplace=True)
Y_t = Y_reg[50001:]
Y_t.fillna(0, inplace=True)
rf_classifier_2.predict(X_t)
s = rf_classifier_2.score(X_t, Y_t)
print("Number of True values in Y_test: ", len(Y_t) - Y_t["pumped"].value_counts()[False])
print("Accuracy of model 2: " + str(s))
print("==================")


# rf_regressor.fit(x_train, y_train)

# print(type(pumps["dex"]))
# for exchange in pumps["dex"]:
#     if exchange == "Cryptopia":
#         count += 1
# print("Count: " + str(count))
"""
hour_price_data = pd.read_csv("hour_price.csv")
# hour_price_data = hour_price_data.head(3)
cryptopia = pd.DataFrame()
for label in hour_price_data.columns:
    if "Cryptopia" in label:
        cryptopia[label] = hour_price_data[label]
for timestamp in cryptopia["GNO.Cryptopia.time"]:
    print(datetime.fromtimestamp(timestamp))
# print(cryptopia)"""

# data = result['cryptopiacoins']
# print(data)
# data = result[None]
"""count = 0
for i in pumped["pumped"]:
    if i:
        count += 1
print(count)
print(pumped["pumped"])"""
# print(hour_price_data['EXCL.Bittrex.time'][0])

# done! let's see what we got
# print(pyreadr.list_objects('/Users/ThanhTran/PycharmProjects/pumpdump/code_and_data/hourprice.RData')) # let's check what objects we got
# df1 = result["df1"] # extract the pandas data frame for object df1