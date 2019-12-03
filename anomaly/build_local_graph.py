import requests

CONSTANTS = {
    'DATA_FILE': 'chainletElimination.txt',
    'TAB': '\t',
    'ADD_DETAIL_API': 'https://blockchain.info/rawaddr/',
    'TX_DETAIL_API': 'https://blockchain.info/rawtx/',
    'ADDRESS_COUNT': 1000,
    'HOP_LEVEL': 1,
    'suspicious_input_address': 'fifth_labor/input_address_list',
    'suspicious_output_address': 'fifth_labor/output_address_lis',
    'transaction_output_address': 'fifth_labor/transaction_output_address',
    'split_transactions': 'fifth_labor/split_transactions',
    'split_address_threshold': 2,
    'loop_addresses':'fifth_labor/loop_addresses'
}


# get transaction list by bitCoin address
def get_transaction_list(address):
    try:
        request = requests.get(CONSTANTS['ADD_DETAIL_API'] + address)
        json_text = request.json()
        return json_text["txs"]
    except BaseException as error:
        print("invalid request or invalid json:{}" + format(error) + "in line" + str(address))
        return None


def get_input_address(transaction_json):
    input_list = transaction_json['inputs']
    transaction_input_list = list()
    for input in input_list:
        if 'prev_out' not in input:
            continue
        transaction_input_list.append(input['prev_out']['addr'])
    return transaction_input_list


def get_output_address(transaction_json, level):
    # add the OUTPUT addresses to the transaction node
    output_list = transaction_json['out']
    transaction_output_address = list()
    # transaction_output_address_file = open(CONSTANTS['transaction_output_address'] + '_' + str(level) + '.txt', 'a+')
    for output in output_list:
        # address not found for the output object
        if 'addr' in output:
            # transaction_output_address_file.write('{}\t{}\n'.format(transaction_json['hash'], output['addr']))
            transaction_output_address.append(output['addr'])
    # transaction_output_address_file.close()
    return transaction_output_address


def find_all_the_input_address():
    data_file = open(CONSTANTS['DATA_FILE'], 'r')
    input_address_file = open(CONSTANTS['suspicious_input_address'] + '_' + str(0) + '.txt', 'w+')
    # output_address_file = open(CONSTANTS['suspicious_output_address'] + '_' + str(0) + '.txt', 'w+')

    address_count = 1
    for line in data_file:
        _, addr_hash = line.split(CONSTANTS['TAB'])
        addr_hash = addr_hash.strip()
        print('Processing address {}'.format(addr_hash), end=' ')
        transactions_list = get_transaction_list(addr_hash)
        if transactions_list is None:
            continue
        assert len(transactions_list) <= 50
        # num_transaction = len(transaction_json) if len(transaction_json) <= 2 else 2
        num_transaction = len(transactions_list)
        transaction_output_address_file = open(CONSTANTS['transaction_output_address'] + '_' + str(0) + '.txt', 'a+')
        for i in range(num_transaction):
            print('.', end='')
            input_list = get_input_address(transactions_list[i])
            output_list = get_output_address(transactions_list[i], 0)
            assert addr_hash in input_list or addr_hash in output_list
            if addr_hash in input_list:
                input_address_file.write('{}\t{}\n'.format(addr_hash, transactions_list[i]['hash']))
                for output in output_list:
                    transaction_output_address_file.write('{}\t{}\n'.format(transactions_list[i]['hash'], output))
            # if addr_hash in output_list:
            # output_address_file.write('{}\t{}\n'.format(addr_hash, transactions_list[i]['hash']))

        if address_count > CONSTANTS['ADDRESS_COUNT']: break
        address_count = address_count + 1
        print()
    input_address_file.close()
    transaction_output_address_file.close()
    # output_address_file.close()


def find_all_the_input_address_from_transaction_output():
    data_file = open(CONSTANTS['transaction_output_address'] + '_' + str(0) + '.txt', 'r')
    input_address_file = open(CONSTANTS['suspicious_input_address'] + '_' + str(1) + '.txt', 'w+')
    output_address_file = open(CONSTANTS['suspicious_output_address'] + '_' + str(1) + '.txt', 'w+')

    address_count = 1
    for line in data_file:
        _, addr_hash = line.split(CONSTANTS['TAB'])
        addr_hash = addr_hash.strip()
        print('Processing address {}'.format(addr_hash), end=' ')
        transactions_list = get_transaction_list(addr_hash)
        if transactions_list is None:
            continue
        assert len(transactions_list) <= 50
        # num_transaction = len(transaction_json) if len(transaction_json) <= 2 else 2
        num_transaction = len(transactions_list)
        transaction_output_address_file = open(CONSTANTS['transaction_output_address'] + '_' + str(1) + '.txt', 'a+')
        for i in range(num_transaction):
            print('.', end='')
            input_list = get_input_address(transactions_list[i])
            output_list = get_output_address(transactions_list[i], 1)
            assert addr_hash in input_list or addr_hash in output_list
            if addr_hash in input_list:
                input_address_file.write('{}\t{}\n'.format(addr_hash, transactions_list[i]['hash']))
                for output in output_list:
                    transaction_output_address_file.write('{}\t{}\n'.format(transactions_list[i]['hash'], output))
            # if addr_hash in output_list:
            #     output_address_file.write('{}\t{}\n'.format(addr_hash, transactions_list[i]['hash']))

        if address_count > CONSTANTS['ADDRESS_COUNT']: break
        address_count = address_count + 1
        print()
        transaction_output_address_file.close()
    input_address_file.close()
    output_address_file.close()
    data_file.close()


# fifth labor problem 5
def find_all_spliting_nodes():
    data_file = open(CONSTANTS['suspicious_input_address'] + '_' + str(0) + '.txt', 'r')

    address_set = set()
    for line in data_file:
        addr_hash, _ = line.split(CONSTANTS['TAB'])
        addr_hash = addr_hash.strip()
        address_set.add(addr_hash)

    data_file.close()
    split_transactions_file = open(CONSTANTS['split_transactions'] + '.txt', 'w+')
    for addr_hash in address_set:
        print('Processing address {}'.format(addr_hash), end=' ')
        transactions_list = get_transaction_list(addr_hash)
        if transactions_list is None:
            continue
        assert len(transactions_list) <= 50
        # num_transaction = len(transaction_json) if len(transaction_json) <= 2 else 2
        num_transaction = len(transactions_list)
        for i in range(num_transaction):
            print('.', end='')
            input_list = get_input_address(transactions_list[i])
            output_list = get_output_address(transactions_list[i], 1)
            assert addr_hash in input_list or addr_hash in output_list
            if len(input_list) == 1 and len(output_list) > CONSTANTS['split_address_threshold']:
                split_transactions_file.write(
                    '{}\t{}\t{}\t{}\n'.format(addr_hash, transactions_list[i]['hash'],
                                              str(len(output_list)), str(len(input_list))))
        print()
    split_transactions_file.close()

    return


def get_address_map(file_name):
    # data_file = open(CONSTANTS['suspicious_input_address'] + '_' + str(0) + '.txt', 'r')
    data_file = open(file_name, 'r')
    address_map = dict()
    for line in data_file:
        addr_hash, transaction_hash = line.split(CONSTANTS['TAB'])
        addr_hash = addr_hash.strip()
        transaction_hash = transaction_hash.strip()
        if address_map.get(addr_hash) is None:
            transaction_list = list()
            transaction_list.append(transaction_hash)
            address_map[addr_hash] = transaction_list
        else:
            transaction_list = address_map.get(addr_hash)
            transaction_list.append(transaction_hash)
            address_map[addr_hash] = transaction_list
    data_file.close()
    return address_map


def get_transaction_map(file_name):
    # transaction_file = open(CONSTANTS['transaction_output_address'] + '_' + str(0) + '.txt', 'r')
    transaction_file = open(file_name, 'r')
    transaction_map = dict()
    for line in transaction_file:
        transaction_hash, addr_hash = line.split(CONSTANTS['TAB'])
        addr_hash = addr_hash.strip()
        transaction_hash = transaction_hash.strip()
        if transaction_map.get(transaction_hash) is None:
            address_list = list()
            address_list.append(addr_hash)
            transaction_map[transaction_hash] = address_list
        else:
            address_list = transaction_map.get(transaction_hash)
            address_list.append(addr_hash)
            transaction_map[transaction_hash] = address_list
    transaction_file.close()
    return transaction_map


def find_all_the_loops():
    address_map_starter = get_address_map(CONSTANTS['suspicious_input_address'] + '_' + str(0) + '.txt')
    transaction_map_starter = get_transaction_map(CONSTANTS['transaction_output_address'] + '_' + str(0) + '.txt')

    address_map_second_level = get_address_map(CONSTANTS['suspicious_input_address'] + '_' + str(1) + '.txt')
    transaction_map_second_level = get_transaction_map(CONSTANTS['transaction_output_address'] + '_' + str(1) + '.txt')

    loop_addresses = open(CONSTANTS['loop_addresses']+'.txt','w+')
    for starter_address in address_map_starter.keys():
        transaction_list = address_map_starter.get(starter_address)
        for starter_trx in transaction_list:
            assert transaction_map_starter.get(starter_trx) is not None
            address_list = transaction_map_starter.get(starter_trx)
            if len(address_list) > 1:
                for i in range(len(address_list)):
                    for j in range((i + 1), len(address_list)):
                        if address_map_second_level.get(address_list[i]) is not None and address_map_second_level.get(
                                address_list[j]) is not None:
                            trx_list_i = address_map_second_level.get(address_list[i])
                            trx_list_j = address_map_second_level.get(address_list[j])
                            for trx_i_k in range(len(trx_list_i)):
                                for trx_j_l in range(len(trx_list_j)):
                                    if transaction_map_second_level.get(
                                            trx_i_k) is not None and transaction_map_second_level.get(
                                        trx_j_l) is not None:
                                        common_addresses = set(transaction_map_second_level.get(
                                            trx_i_k)) & set(transaction_map_second_level.get(
                                            trx_j_l))
                                        if len(common_addresses) > 0:
                                            loop_addresses.write('Src:{}; Detected Loop Count {}'.format(starter_address,str(len(common_addresses))))
    loop_addresses.close()


    return


if __name__ == '__main__':
    # find_all_the_input_address()
    # find_all_the_input_address_from_transaction_output()
    # find_all_spliting_nodes()
    # find_all_the_loops()
    print('Loop detection')
