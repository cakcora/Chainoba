import requests
import time

CONSTANTS = {
    'DATA_FILE': 'chainletElimination.txt',
    'TAB': '\t',
    'ADD_DETAIL_API': 'https://blockchain.info/rawaddr/',
    'TX_DETAIL_API': 'https://blockchain.info/rawtx/',
    'ADDRESS_COUNT': 10
}


def check_loop(transaction_map=None, suspicious_address=None):
    transactions = list(transaction_map.keys())
    assert len(transactions) == len(set(transactions))
    number_of_loop = 0
    loop_nodes = list()
    for i in range(len(transactions)):
        assert len(transaction_map.get(transactions[i])) == len(set(transaction_map.get(transactions[i])))
        sibling_transactions = transactions[i + 1:len(transactions)]
        assert transactions[i] not in sibling_transactions
        for j in range(len(sibling_transactions)):
            # No transaction should have same output address multiple times; check if creating set cause any loss of address
            assert len(transaction_map.get(sibling_transactions[j])) == len(
                set(transaction_map.get(sibling_transactions[j])))
            # find common address between 2 transactions
            if set(transaction_map.get(sibling_transactions[j])) & set(transaction_map.get(transactions[i])):
                # print('{} and {} has common address'.format(transactions[i], sibling_transactions[j]))
                common_addresses = set(transaction_map.get(transactions[i])) & set(
                    transaction_map.get(sibling_transactions[j]))
                # print(common_addresses)
                loop_nodes.append((transactions[i], sibling_transactions[j],common_addresses))
                number_of_loop = number_of_loop + 1

    # for current_transaction in transactions:
    #     other_transactions = [tx for tx in transactions if tx != current_transaction]
    #     assert current_transaction not in other_transactions
    #
    #     for otx in other_transactions:
    #         # No transaction should have same output address multiple times; check if creating set cause any loss of address
    #         assert len(transaction_map.get(current_transaction)) == len(set(transaction_map.get(current_transaction)))
    #         assert len(transaction_map.get(otx)) == len(set(transaction_map.get(otx)))
    #         # find common address between 2 transactions
    #         if set(transaction_map.get(current_transaction)) & set(transaction_map.get(otx)):
    #             # print('{} and {} has common address'.format(current_transaction, otx))
    #             # print(set(transaction_map.get(current_transaction)) & set(transaction_map.get(otx)))
    #             number_of_loop = number_of_loop + 1
    assert len(loop_nodes) == number_of_loop
    print('Number of Loop detected {}'.format(number_of_loop))
    print('----------------------------------------------------')
    return loop_nodes


# 027c2aeefd3e2cbb4316d7bb85314e86b4c6cb9e950f7f110be4677279f46f59
def get_suspicious_address():
    data_file = open(CONSTANTS['DATA_FILE'], 'r')
    addr_count = 1
    map_address_loop = dict()
    start_time = time.time()
    for line in data_file:
        _, address = line.split(CONSTANTS['TAB'])
        address = address.strip()
        # print(address)
        print('Processing suspicious address {} {}'.format(address, addr_count),end=' ')
        # print('===================================================')
        request = requests.get(CONSTANTS['ADD_DETAIL_API'] + address)
        json_text = request.json()
        transactions = json_text['txs']

        transaction_map = dict()
        for i in range(len(transactions)):
            # print('Transaction {} {}'.format(transactions[i]['hash'], i))
            print('.', end='')
            output_list = transactions[i]['out']
            output_adresses = list()
            for output in output_list:
                # address not found for the output object
                if 'addr' in output:
                    # TODO use set instead of checking for same output address for single transaction
                    if output['addr'] in output_adresses:
                        print('Same output address for transaction: output: {} transaction: {}'.format(output['addr'],
                                                                                                       transactions[i][
                                                                                                           'hash']))
                        break
                    output_adresses.append(output['addr'])
            # create transaction output map for further processing
            transaction_map[transactions[i]['hash']] = output_adresses
        print()

        detected_loops = check_loop(transaction_map, address)
        assert map_address_loop.get(address) is None
        map_address_loop[address] = detected_loops

        addr_count = addr_count + 1
        if addr_count > CONSTANTS['ADDRESS_COUNT']:
            break
    data_file.close()
    elapsed_time = time.time() - start_time
    print('===============######==================')
    print('Elapsed time: {} sec.'.format(elapsed_time))
    print('Processed Address {} .'.format(CONSTANTS['ADDRESS_COUNT']))



# TODO detect loop when multiple level (N number of hops) loop detection
if __name__ == '__main__':
    get_suspicious_address()
