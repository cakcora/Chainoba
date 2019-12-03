import requests

CONSTANTS = {
    'DATA_FILE': 'chainletElimination.txt',
    'TAB': '\t',
    'ADD_DETAIL_API': 'https://blockchain.info/rawaddr/',
    'TX_DETAIL_API': 'https://blockchain.info/rawtx/',
    'ADDRESS_COUNT': 10,
    'HOP_LEVEL': 1
}


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


# for amount < 0.3 bitcoins/shatosis
# TODO detect loop when multiple level (N number of hops) loop detection


# detect loop for maximum 3 hops
def travarse_network(address_hash, level):
    addr_hash = address_hash
    # create Address Node
    address = AddressNode(addr_hash=addr_hash, level=level)

    # send request for address detail
    request = requests.get(CONSTANTS['ADD_DETAIL_API'] + addr_hash)
    json_text = request.json()

    # get the transactios
    try:
        transaction_json = json_text['txs']
    except:
        print("Could not process the response for {}".format(address_hash))
        return
    assert len(transaction_json) <= 50
    transaction_node_list = list()
    starter_transaction_node_list = list()
    # num_transaction = len(transaction_json) if len(transaction_json) <= 2 else 2
    num_transaction = len(transaction_json)
    for i in range(num_transaction):
        print('.', end='')
        # add transaction to the address node
        address.add_transaction(transaction_json[i]['hash'])
        # print('Transaction {} {}'.format(transactions[i]['hash'], i))

        # Create a transaction node with each transaction hash
        transaction = TransactionNode(trx_hash=transaction_json[i]['hash'], level=level)

        # get the input addresses of the transaction
        # add the INPUT addresses to the transaction node
        input_list = transaction_json[i]['inputs']
        for input in input_list:
            if 'prev_out' not in input:
                continue

            transaction.add_input_address(input['prev_out']['addr'])

        # add the OUTPUT addresses to the transaction node
        output_list = transaction_json[i]['out']
        for output in output_list:
            # address not found for the output object
            if 'addr' in output:
                transaction.add_output_address(output['addr'])

        # the starting address hash should be in either the input address list or in the output address list
        assert address_hash in transaction.get_input_address() or address_hash in transaction.get_output_address()

        # if the starting address is in the input address list then the transaction is a starter address for this graph
        if address_hash in transaction.get_input_address() and level == 1:
            starter_transaction_node_list.append(transaction)
        # create transaction output map for further processing
        transaction_node_list.append(transaction)
    return address, transaction_node_list, starter_transaction_node_list


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
                addr_count = addr_count + 1
        else:
            for key in transaction_map.keys():
                transaction = transaction_map.get(key)
                if transaction.level == level - 1:
                    address_hash = address_hash | set(transaction.get_output_address())

        print('Travarsing network for level {}'.format(level))
        addr_count = 1
        starter_transactions_full_graph = list()
        for addr_hash in address_hash:
            print('Processing suspicious address {} {}'.format(addr_hash, addr_count), end=' ')

            address_node, transaction_list, starter_transactions = travarse_network(addr_hash, level)
            if address_node is None or transaction_list is None or starter_transactions is None:
                continue

            if level == 1:
                starter_transactions_full_graph = starter_transactions
            address_list.append(address_node)

            # create a map for faster access to a specific address and transaction
            address_map[address_node.get_hash()] = address_node
            for trx in transaction_list:
                transaction_map[trx.get_trx_hash()] = trx
            addr_count = addr_count + 1
            # if addr_count > CONSTANTS['ADDRESS_COUNT']: break
            print()
        level = level + 1

    assert len(starter_transactions_full_graph) > 0

    # the BFS for asigning values to each address node should start with the starter transaction nodes
    # start bfs

    # for key in address_map.keys():
    #     address = address_map.get(key)
    #     root_nodes = list()
    #     if address.level == 1:
    #         root_nodes.append(address)
    #     address_queue = queue.Queue()
    #     for root_node in root_nodes:
    #         address_queue.put(root_node)
    #         while address_queue.empty() is not True:
    #             current_node = address_queue.get()
    #             for trx in current_node.get_transactions():
    #                 output_address = transaction_map.get(trx).get_output_address()
    #                 for ah in output_address:
    #                     addr_node = address_map.get(ah)
    #                     new_paths = list()
    #                     for path in current_node.get_path():
    #                         new_paths.append(Path(length=path.length + 1, source=path.source))
    #                         addr_node.add_paths(Path(length=path.length + 1, source=path.source))
    #                     matched_path = addr_node.check_match(path_list=new_paths)
    #                     if len(matched_path) > 0:
    #                         print("Loop detected...Source :{} Destination:{}".format(current_node.get_hash(),
    #                                                                                  addr_node.get_hash()))
    #                     address_map[addr_node.get_hash()] = addr_node


# assert addr_count == CONSTANTS['ADDRESS_COUNT']
# TODO Test for larger number of nodes and hops 3
# check for spent addresses and unspent addresses




def detect_spent_unspent_addresses():
    data_file = open(CONSTANTS['DATA_FILE'], 'r')
    addr_count = 1
    spent_addresses = list()
    unspent_address = list()
    for line in data_file:
        _, addr_hash = line.split(CONSTANTS['TAB'])
        addr_hash = addr_hash.strip()
        print('Processing address {} {}'.format(addr_hash, addr_count))
        request = requests.get(CONSTANTS['ADD_DETAIL_API'] + addr_hash)
        json_text = request.json()
        transaction_json = json_text['txs']
        assert len(transaction_json) <= 50
        input_address_list = list()
        output_address_list = list()
        for i in range(len(transaction_json)):
            input_list = transaction_json[i]['inputs']
            for input in input_list:
                if 'prev_out' not in input:
                    continue

                input_address_list.append(input['prev_out']['addr'])

            output_list = transaction_json[i]['out']

            for output in output_list:
                # address not found for the output object
                if 'addr' in output:
                    output_address_list.append(output['addr'])

            assert addr_hash in output_address_list or addr_hash in input_address_list
        if addr_count > 10: break
        addr_count = addr_count + 1

    if addr_hash in output_address_list and addr_hash not in input_address_list:
        unspent_address.append(addr_hash)
    else:
        spent_addresses.append(addr_hash)

    print('spent address : {}; unspent address: {}'.format(len(spent_addresses), len(unspent_address)))


# transactions having one input address and multiple addresses as output
def detect_split_transaction():
    return 'transaction'


if __name__ == '__main__':
    build_graph()
    # detect_loop()
    # detect_spent_unspent_addresses()

# get_suspicious_address()
