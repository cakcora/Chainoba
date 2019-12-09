from etherscan.etherscan import *
from foundations.EthereumAPI.resources.ponzy_schemes import GetPonziAnomalyDataEndpoint
import json, requests
import argparse
import pandas as pd
import sys

# Reading Ethereum API key
with open('api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']


# handling paid rate 0 division errors
def Paid_rate_division(n, d):
    return n / d if d else 0


'''
class account_data has the function get_account_data which fetches the addresses from the database using EthereumAPI. Then using the addresses,  feature data like Balance and transaction information is fetched from Etherscan API and returned in a pandas Dataframe
'''


class account_data:
    def get_account_data(self):
        # Variable decalaration, where ponzi and non_ponzi are arrays that will contain the addresses of ponzi and non ponzi schemes respectively
        ponzi = []
        non_ponzi = []
        features = pd.DataFrame(
            columns=['Address', 'Bal', 'N_maxpay', 'N_investment', 'N_payment', 'Paid_rate', 'Ponzi'])
        mean_ponzi_data = pd.DataFrame(columns=['Address', 'Bal', 'N_maxpay', 'N_investment', 'N_payment', 'Paid_rate'])
        mean_nonponzi_data = pd.DataFrame(
            columns=['Address', 'Bal', 'N_maxpay', 'N_investment', 'N_payment', 'Paid_rate'])

        # number of payments to the account
        N_investment = 0
        # Maximum payment from the account to another account
        N_maxpay = 0
        # Total payments from the account
        N_payment = 0
        # Number of payments from the account/number of payments to the account
        Paid_rate = 0
        # Ponzi flag to signify if the scheme is ponzi
        ponzi_flag = True

        gpa = GetPonziAnomalyDataEndpoint()
        reader_db = gpa.get()

        ponzi_data_latest = reader_db['Data']

        # print(ponzi_data_latest)

        for item in ponzi_data_latest:
            if item["Label"] == "Ponzi":
                ponzi.append(item["Address"])
            elif item["Label"] == "Nonponzi":
                non_ponzi.append(item["Address"])

        '''
        #this was added in case data was in a csv file
        ponzi_file = "PonziData.csv"
        non_ponzi_file = "NonPonziData.csv"
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

        '''

        # Hitting Etherscan API to fetch balance and details
        for addr_ponzi in ponzi:
            addr_ponzi = ''.join(e for e in addr_ponzi if e.isalnum()).lower()
            print("Retrieving transactions and balance of contract ", addr_ponzi, "...", end=" \n")
            sys.stdout.flush()
            api = Client(api_key=key, cache_expire_after=5)
            text = api.get_transactions_by_address(addr_ponzi, tx_type='normal')
            tint = api.get_transactions_by_address(addr_ponzi, tx_type='internal')
            Bal = api.get_eth_balance(addr_ponzi)

            N_investment = 0
            N_maxpay = 0
            N_payment = 0
            Paid_rate = 0
            ponzi_flag = True

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
            #    if (Bal > 0.0 and N_payment > 0.0 and N_investment > 0.0):
            features = features.append({'Address': addr_ponzi, 'Bal': Bal * 10 ** -18, 'N_maxpay': N_maxpay * 10 ** -18,
                                        'N_investment': N_investment, 'N_payment': N_payment, 'Paid_rate': Paid_rate,
                                        'Ponzi': ponzi_flag}, ignore_index=True)
            mean_ponzi_data = mean_ponzi_data.append(
                {'Address': addr_ponzi, 'Bal': Bal * 10 ** -18, 'N_maxpay': N_maxpay * 10 ** -18,
                 'N_investment': N_investment, 'N_payment': N_payment, 'Paid_rate': Paid_rate}, ignore_index=True)

        for addr_non_ponzi in non_ponzi:
            addr_non_ponzi = ''.join(e for e in addr_non_ponzi if e.isalnum()).lower()
            print("Retrieving transactions and balance of contract ", addr_non_ponzi, "...", end=" \n")
            sys.stdout.flush()
            api = Client(api_key=key, cache_expire_after=5)
            text = api.get_transactions_by_address(addr_non_ponzi, tx_type='normal')
            tint = api.get_transactions_by_address(addr_non_ponzi, tx_type='internal')
            Bal = api.get_eth_balance(addr_non_ponzi)

            N_investment = 0
            N_maxpay = 0
            N_payment = 0
            Paid_rate = 0
            ponzi_flag = False

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
            #    if (Bal > 0.0 and N_payment > 0.0 and N_investment > 0.0):
            features = features.append(
                {'Address': addr_non_ponzi, 'Bal': Bal * 10 ** -18, 'N_maxpay': N_maxpay * 10 ** -18,
                 'N_investment': N_investment, 'N_payment': N_payment, 'Paid_rate': Paid_rate,
                 'Ponzi': ponzi_flag}, ignore_index=True)
            mean_nonponzi_data = mean_nonponzi_data.append(
                {'Address': addr_non_ponzi, 'Bal': Bal * 10 ** -18, 'N_maxpay': N_maxpay * 10 ** -18,
                 'N_investment': N_investment, 'N_payment': N_payment, 'Paid_rate': Paid_rate}, ignore_index=True)

        return features, mean_nonponzi_data, mean_ponzi_data
