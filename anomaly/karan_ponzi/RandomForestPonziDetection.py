from sklearn.metrics import precision_score, recall_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from etherscan.accounts import Account
from etherscan.etherscan import Client
import json, requests
import argparse
import sys
import csv
import datetime, dateutil.parser
import string

with open('api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

ponzi = []
ponzi_file = "PonziData.csv"
non_ponzi = []
non_ponzi_file = "NonPonzi.csv"
features = pd.DataFrame(columns=['Address', 'Bal', 'N_maxpay', 'N_investment', 'N_payment', 'Paid_rate', 'Ponzi'])

with open(ponzi_file, encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    for row in reader:
        addr_ponzi = ''.join(e for e in row[0] if e.isalnum())
        ponzi.append(addr_ponzi)

with open(non_ponzi_file, encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    for row in reader:
        addr_non_ponzi = ''.join(e for e in row[0] if e.isalnum())
        non_ponzi.append(addr_non_ponzi)


def Paid_rate_division(n, d):
    return n / d if d else 0


for addr_ponzi in ponzi:
    addr_ponzi = ''.join(e for e in addr_ponzi if e.isalnum()).lower()
    print("Retrieving transactions and balance of contract ", addr_ponzi, "...", end=" \n")
    sys.stdout.flush()
    api = Client(api_key=key, cache_expire_after=5)
    text = api.get_transactions_by_address(addr_ponzi, tx_type='normal')
    tint = api.get_transactions_by_address(addr_ponzi, tx_type='internal')
    Bal = api.get_eth_balance(addr_ponzi)

    count_text = 0
    users_tint = 0
    N_investment = 0
    N_maxpay = 0
    N_payment = 0
    Paid_rate = 0
    ponzi_flag = 1

    for t in text:
        if (t['is_error'] is False):
            if t['to']:
                N_investment += 1
                if (t['value'] >= N_maxpay): N_maxpay = t['value']

    for t2 in tint:
        if (t2['is_error'] is False):
            if (t2['from'] == addr_ponzi):
                N_payment += 1
            elif (t2['to'] == addr_ponzi):
                N_investment += 1
                if (t2['value'] >= N_maxpay): N_maxpay = t2['value']

    Paid_rate = Paid_rate_division(N_payment, N_investment)

    print(addr_ponzi, round(Bal * 10 ** -18, 4), round(N_maxpay * 10 ** -18, 4), N_investment, N_payment,
          round(Paid_rate, 2), ponzi_flag)
    if (Bal > 0.0 and N_payment > 0.0 and N_investment > 0.0):
        features = features.append({'Address': addr_ponzi, 'Bal': Bal * 10 ** -18, 'N_maxpay': N_maxpay * 10 ** -18,
                                    'N_investment': N_investment, 'N_payment': N_payment, 'Paid_rate': Paid_rate,
                                    'Ponzi': ponzi_flag}, ignore_index=True)

for addr_non_ponzi in non_ponzi:
    addr_non_ponzi = ''.join(e for e in addr_non_ponzi if e.isalnum()).lower()
    print("Retrieving transactions and balance of contract ", addr_non_ponzi, "...", end=" \n")
    sys.stdout.flush()
    api = Client(api_key=key, cache_expire_after=5)
    text = api.get_transactions_by_address(addr_non_ponzi, tx_type='normal')
    tint = api.get_transactions_by_address(addr_non_ponzi, tx_type='internal')
    Bal = api.get_eth_balance(addr_non_ponzi)

    count_text = 0
    users_tint = 0
    N_investment = 0
    N_maxpay = 0
    N_payment = 0
    Paid_rate = 0
    ponzi_flag = 0

    for t in text:
        if (t['is_error'] is False):
            if t['to']:
                N_investment += 1
                if (t['value'] >= N_maxpay): N_maxpay = t['value']

    for t2 in tint:
        if (t2['is_error'] is False):
            if (t2['from'] == addr_non_ponzi):
                N_payment += 1
            elif (t2['to'] == addr_non_ponzi):
                N_investment += 1
                if (t2['value'] >= N_maxpay): N_maxpay = t2['value']

    Paid_rate = Paid_rate_division(N_payment, N_investment)
    print(addr_non_ponzi, round(Bal * 10 ** -18, 4), round(N_maxpay * 10 ** -18, 4), N_investment, N_payment,
          round(Paid_rate, 2), ponzi_flag)
    if (Bal > 0.0 and N_payment > 0.0 and N_investment > 0.0):
        features = features.append({'Address': addr_non_ponzi, 'Bal': Bal * 10 ** -18, 'N_maxpay': N_maxpay * 10 ** -18,
                                    'N_investment': N_investment, 'N_payment': N_payment, 'Paid_rate': Paid_rate,
                                    'Ponzi': ponzi_flag}, ignore_index=True)

'''
w,h = 150, 7
Matrix = [[0 for x in range(w)] for y in range(h)]

numpy [0][0] = 'Address'
Matrix [0][1] = 'Bal'
Matrix [0][2] = 'N_maxpay'
Matrix [0][3] = 'N_investment'
Matrix [0][4] = 'N_payment'
Matrix [0][5] = 'Paid_rate'
Matrix [0][6] = 'Ponzi'

print(Matrix)

'''

print(features)
# Labels are the values we want to predict
labels = np.array(features['Ponzi'])
# Remove the labels from the features
# axis 1 refers to the columns
features = features.drop('Ponzi', axis=1)
features = features.drop('Address', axis=1)
# Saving feature names for later use
feature_list = list(features.columns)
# Convert to numpy array
features = np.array(features)

# Using Skicit-learn to split data into training and testing sets
from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25,
                                                                            random_state=42)

print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)
print(test_labels)

# Import the model we are using
from sklearn.ensemble import RandomForestRegressor

# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators=1000, random_state=42)
# Train the model on training data
rf.fit(train_features, train_labels)

# Use the forest's predict method on the test data
predictions = rf.predict(test_features)
# Calculate the absolute errors
errors = abs(predictions - test_labels)
# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')

# Calculate mean absolute percentage error (MAPE)
mape = 100 * Paid_rate_division(errors, test_labels)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')
