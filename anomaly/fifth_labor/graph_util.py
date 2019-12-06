import pandas as pd
import requests

import anomaly.fifth_labor.util as helper

CONSTANTS = {
    'ADDR_DETAIL_API': 'https://blockchain.info/rawaddr/',
}
RESPONSE = {
    'success': 200,
    'invalid': 422
}


def get_transaction_list(address):
    """
    GET the transactions related to the ransomware addresses
    :param address:
    :return: RESPONSE_CODE, Transaction JSON
    """
    try:
        request = requests.get(CONSTANTS['ADDR_DETAIL_API'] + address)
        json_text = request.json()
        return RESPONSE['success'], json_text["txs"]
    except BaseException as error:
        return RESPONSE['invalid'], None


def get_input_address(transaction_json):
    """
    Extract the input addresses from a transaction
    :param transaction_json:
    :return: list() of input addresses
    """
    input_list = transaction_json['inputs']
    transaction_input_list = list()
    for input in input_list:
        # check for coin_base transaction
        if 'prev_out' not in input:
            continue
        transaction_input_list.append((input['prev_out']['addr'], input['prev_out']['value']))
    return transaction_input_list


def get_output_address(transaction_json):
    """
    GET the output addresses from a transaction
    :param transaction_json:
    :return: list() of output address
    """
    output_list = transaction_json['out']
    transaction_output_address = list()
    for output in output_list:
        # address not found for the output object
        if 'addr' in output:
            transaction_output_address.append((output['addr'], output['value']))
    return transaction_output_address


def get_edge_list(ransomware_df):
    """
    - GET address details with related transactions and amount
    - create the edge list in dataframe data structure
    :param ransomware_df:
    :return: DataFrame edge_list
    """
    progress_bar = helper.progress_bar(max_value=ransomware_df.shape[0], title='Requesting Ransomware address detail..')
    edge_list_df = pd.DataFrame(columns=['source', 'target', 'weight', 'length'])

    error_response_count = 0
    for index, ransomware in ransomware_df.iterrows():
        response, transaction_list = get_transaction_list(ransomware['address'])

        # check for successful API request
        # happens when the connection is lost with the server or response taking too long
        if response != RESPONSE['success']:
            error_response_count = error_response_count + 1
            continue

        # the server fives at most 50 transaction for each address request
        assert len(transaction_list) <= 50

        for i in range(len(transaction_list)):
            input_address_list = get_input_address(transaction_list[i])
            output_address_list = get_output_address(transaction_list[i])
            for input in input_address_list:
                edge_list_df = edge_list_df.append(
                    {'source': input[0], 'target': transaction_list[i]['hash'], 'weight': input[1], 'length': input[1]},
                    ignore_index=True)
            for output in output_address_list:
                edge_list_df = edge_list_df.append(
                    {'source': transaction_list[i]['hash'], 'target': output[0], 'weight': output[1],
                     'length': output[1]},
                    ignore_index=True)

        progress_bar.update()
    print("\nRequested address :{}".format(ransomware_df.shape[0]))
    print("Unsuccessful Requests :{}".format(error_response_count))
    print()
    return edge_list_df
