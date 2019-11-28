import queue
import time

import requests

CONSTANTS = {
    'DATA_FILE': 'chainletElimination.txt',
    'TAB': '\t',
    'ADD_DETAIL_API': 'https://blockchain.info/rawaddr/',
    'TX_DETAIL_API': 'https://blockchain.info/rawtx/',
    'ADDRESS_COUNT': 10000,
    'HOP_LEVEL': 2
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
                loop_nodes.append((transactions[i], sibling_transactions[j], common_addresses))
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
        print('Processing suspicious address {} {}'.format(address, addr_count), end=' ')
        # print('===================================================')
        request = requests.get(CONSTANTS['ADD_DETAIL_API'] + address)
        json_text = request.json()
        transactions = json_text['txs']
        assert len(transactions) <= 50
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

class Path:
    def __init__(self, source, length):
        self.source = source
        self.length = length

    def get_source(self):
        return self.source

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length

    def set_source(self, source):
        self.source = source


class AddressNode:
    def __init__(self, addr_hash, level):
        self.level = level
        self.addr_hash = addr_hash
        self.paths = list()
        self.transactions = list()

    def add_paths(self, path):
        self.paths.append(path)

    def add_transaction(self, trx):
        self.transactions.append(trx)

    def get_path(self):
        return self.paths

    def get_transactions(self):
        return self.transactions

    def get_hash(self):
        return self.addr_hash

    def check_match(self, path_list):
        matched_paths = list()
        for path in self.paths:
            for other_path in path_list:
                if (path.source == other_path.source) and (path.length == other_path.length):
                    matched_paths.append(path)

        return matched_paths


class TransactionNode:
    def __init__(self, trx_hash, level):
        self.trx_hash = trx_hash
        self.input_address_list = list()
        self.output_address_list = list()
        self.level = level

    def add_input_address(self, address_hash):
        self.input_address_list.append(address_hash)

    def add_output_address(self, address_hash):
        self.output_address_list.append(address_hash)

    def get_trx_hash(self):
        return self.trx_hash

    def get_input_address(self):
        return self.input_address_list

    def get_output_address(self):
        return self.output_address_list


# detect loop for maximum 3 hops
def travarse_network(address_hash, level):
    addr_hash = address_hash
    address = AddressNode(addr_hash=addr_hash, level=level)
    request = requests.get(CONSTANTS['ADD_DETAIL_API'] + addr_hash)
    json_text = request.json()
    transaction_json = json_text['txs']
    assert len(transaction_json) <= 50
    transaction_node_list = list()
    for i in range(len(transaction_json)):
        print('.', end='')
        address.add_transaction(transaction_json[i]['hash'])
        # print('Transaction {} {}'.format(transactions[i]['hash'], i))
        transaction = TransactionNode(trx_hash=transaction_json[i]['hash'], level=level)

        input_list = transaction_json[i]['inputs']

        for input in input_list:
            if 'prev_out' not in input:
                continue
            transaction.add_input_address(input['prev_out']['addr'])

        output_list = transaction_json[i]['out']

        for output in output_list:
            # address not found for the output object
            if 'addr' in output:
                # TODO use set instead of checking for same output address for single transaction
                # if output['addr'] in transaction.get_output_address():
                #     print('Same output address for transaction: output: {} transaction: {}'.format(output['addr'],
                #                                                                                    transaction_json[
                #                                                                                        i][
                #                                                                                        'hash']))
                #     break
                transaction.add_output_address(output['addr'])
        # create transaction output map for further processing
        transaction_node_list.append(transaction)
    return address, transaction_node_list


def build_graph():
    level = 1
    data_file = open(CONSTANTS['DATA_FILE'], 'r')
    transaction_map = dict()
    address_map = dict()

    address_list = list()
    addr_count = 1
    while level <= CONSTANTS['HOP_LEVEL']:

        address_hash = set()
        if level == 1:
            addr_count = 1
            for line in data_file:
                _, addr_hash = line.split(CONSTANTS['TAB'])
                addr_hash = addr_hash.strip()
                address_hash.add(addr_hash)
                addr_count = addr_count + 1
                if addr_count > CONSTANTS['ADDRESS_COUNT']: break

        else:

            for key in transaction_map.keys():
                transaction = transaction_map.get(key)
                if transaction.level == level - 1:
                    address_hash = address_hash | set(transaction.get_output_address())

        print('Travarsing network for level {}'.format(level))
        addr_count = 1
        for addr_hash in address_hash:
            print('Processing suspicious address {} {}'.format(addr_hash, addr_count), end=' ')
            address_node, transaction_list = travarse_network(addr_hash, level)
            address_list.append(address_node)
            address_map[address_node.get_hash()] = address_node
            for trx in transaction_list:
                transaction_map[trx.get_trx_hash()] = trx
            addr_count = addr_count + 1
            # if addr_count > CONSTANTS['ADDRESS_COUNT']: break
            print()
        level = level + 1

    # start bfs
    for key in address_map.keys():
        address = address_map.get(key)
        root_nodes = list()
        if address.level == 1:
            root_nodes.append(address)
        address_queue = queue.Queue()
        for root_node in root_nodes:
            address_queue.put(root_node)
            while address_queue.empty() is not True:
                current_node = address_queue.get()
                for trx in current_node.get_transactions():
                    output_address = transaction_map.get(trx).get_output_address()
                    for ah in output_address:
                        addr_node = address_map.get(ah)
                        new_paths = list()
                        for path in current_node.get_path():
                            new_paths.append(Path(length=path.length + 1, source=path.source))
                            addr_node.add_paths(Path(length=path.length + 1, source=path.source))
                        matched_path = addr_node.check_match(path_list=new_paths)
                        if len(matched_path) > 0:
                            print("Loop detected...Source :{} Destination:{}".format(current_node.get_hash(),
                                                                                     addr_node.get_hash()))
                        address_map[addr_node.get_hash()] = addr_node


# assert addr_count == CONSTANTS['ADDRESS_COUNT']


if __name__ == '__main__':
    build_graph()
# get_suspicious_address()
