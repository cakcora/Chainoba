import requests
import time
import pandas as pd

CONSTANTS = {
    'DATA_FILE': 'chainletElimination.txt',
    'MERGING_FILE': 'merging_addresses.txt',
    'ADD_DETAIL_API': 'https://blockchain.info/rawaddr/',
    'EXCHANGE_FILE_CSV': 'transaction_details_26_10_2019.csv',
    'EXCHANGE_FILE_TXT': 'exchange_addresses.txt'
    # 'TX_DETAIL_API': 'https://blockchain.info/rawtx/',
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


# preprocessing transaction_details_26_10_2019.csv file - generate exchange_addresses.txt
def generate_exchange_address():
    data_frame = pd.read_csv(CONSTANTS['EXCHANGE_FILE_CSV'], usecols=['Inputs'])
    file = open(CONSTANTS['EXCHANGE_FILE_TXT'], "w+")
    address_set = set()

    for row in data_frame.iterrows():
        addresses = row[1]['Inputs']
        # some data is bad, pandas is not able to read.
        if type(addresses) is not float:
            address_list = str(addresses).split('#')
            for index in range(len(address_list)):
                if index % 2 == 1:
                    address_set.add(address_list[index])

    for addr in address_set:
        file.write(addr + "\n")


# testing, how many exchange addresses are generated in 1000 initial suspicious addresses.
# TODO: will eliminate addr from merging_address after all the computation is done.
def check_exchange_address():
    with open(CONSTANTS['MERGING_FILE'], 'r') as file:
        merging_list = file.readlines()
    with open(CONSTANTS['EXCHANGE_FILE_TXT'], 'r') as file:
        exchange_list = file.readlines()

    # suspicious address is an exchange address.
    for addr in merging_list:
        if addr in exchange_list:
            print(addr)


# suspicious_address as an input, find out all output addresses in transaction_list
def get_output_address(transaction_list, input_address):
    output_address_set = set()
    for i in range(len(transaction_list)):
        if "prev_out" not in transaction_list[i]["inputs"][0]:
            break
        else:
            for j in range(len(transaction_list[i]["inputs"])):
                if transaction_list[i]["inputs"][j]["prev_out"]["addr"] == input_address:
                    for x in range(len(transaction_list[i]["out"])):
                        output_address_set.add(transaction_list[i]["out"][x]["addr"])

    return output_address_set


# suspicious_address as an input, find out all output addresses in transaction_list
# with constrain of 1 to 1 and 1 to 2 transactions.
def get_output_address2(transaction_list, input_address):
    output_address_set = set()
    for i in range(len(transaction_list)):
        if "prev_out" not in transaction_list[i]["inputs"][0]:
            break
        else:
            if len(transaction_list[i]["inputs"]) == 1 and len(transaction_list[i]["out"]) <= 2 and \
                    transaction_list[i]["inputs"][0]["prev_out"]["addr"] == input_address:
                for j in range(len(transaction_list[i]["out"])):
                    output_address_set.add(transaction_list[i]["out"][j]["addr"])

    return output_address_set


# fifth_labor_problem1 method returns additional suspicious addresses regarding following problem:
# If an address receives multiple payments from suspicious Ransomware addresses
# ( i.e. merge address), then it is regarded as suspicious
def fifth_labor_problem1():
    with open(CONSTANTS['DATA_FILE'], 'r') as file:
        data = file.readlines()

    suspicious_dictionary = dict()
    start = time.time()

    for line in range(100):  # len(data) is more than 20K

        print("executing line number:", line)
        suspicious_address = data[line].split("\t")[1].split("\n")[0]
        transaction_list = get_transaction_list(suspicious_address)  # the size is 50 in maximum

        if transaction_list is None:
            line += 1
            continue

        output_address_set = set()

        # using initial suspicious addresses as inputs return all the output addresses within one transaction
        temp = get_output_address(transaction_list, suspicious_address)

        for items in temp:
            output_address_set.add(items)

        suspicious_dictionary[suspicious_address] = output_address_set

    # TEST: SHOW whole suspicious dictionary information
    # print("--------------------------------------------")
    # print(str(suspicious_dictionary).replace(", ", "\n"))

    address_set = set()
    merging_address_set = set()

    # iterate suspicious_dictionary to find merging addresses in one transaction.
    for key, value in suspicious_dictionary.items():
        address_list = list(value)
        for i in range(len(address_list)):
            if address_list[i] not in address_set:
                address_set.add(address_list[i])
            else:
                merging_address_set.add(address_list[i])

    end = time.time()

    # write to merging_addresses.txt file
    # merging_addresses_file = open(CONSTANTS['MERGING_FILE'], "a")
    # for addr in merging_addresses_set:
    #     merging_addresses_file.write(addr + "\n")
    #
    # merging_addresses_file.close()

    # Testing 1000 lines from input require 636 secs,
    # found 1217 merging addresses including 4 exchange addresses
    print("Time elapsed: ", end - start)
    print(len(address_set))
    print("--------------------------------------------")
    print(len(merging_address_set))
    print(merging_address_set)


# If multiple suspicious addresses merge after N block, then the merging address is suspicious.
# Only consider 1 to 1, 1 to 2 transactions for now and 3 hops max.
def fifth_labor_problem2():
    with open(CONSTANTS['DATA_FILE'], 'r') as file:
        data = file.readlines()

    suspicious_dictionary = dict()

    start = time.time()

    for line in range(1000):  # len(data) is more than 20K
        print("executing line number:", line)

        suspicious_address = data[line].split("\t")[1].split("\n")[0]
        transaction_list = get_transaction_list(suspicious_address)  # the size is 50 in maximum

        if transaction_list is None:
            line += 1
            continue

        output_address_set = set()

        hop1_address_list = list(get_output_address2(transaction_list, suspicious_address))

        for i in range(len(hop1_address_list)):
            output_address_set.add(hop1_address_list[i])
            hop2_transaction_list = get_transaction_list(hop1_address_list[i])
            if hop2_transaction_list is not None:
                hop2_address_list = list(get_output_address2(hop2_transaction_list, hop1_address_list[i]))
                for j in range(len(hop2_address_list)):
                    output_address_set.add(hop2_address_list[j])
                    hop3_transaction_list = get_transaction_list(hop2_address_list[j])
                    if hop3_transaction_list is not None:
                        hop3_address_list = list(get_output_address2(hop3_transaction_list, hop2_address_list[j]))
                        for x in range(len(hop3_address_list)):
                            output_address_set.add(hop3_address_list[x])

        suspicious_dictionary[suspicious_address] = output_address_set

    output_addresses_set = set()
    merging_addresses_set = set()

    # iterate suspicious_dictionary to find merging addresses in one transaction.
    for key, value in suspicious_dictionary.items():
        address_list = list(value)
        for i in range(len(address_list)):
            if address_list[i] not in output_addresses_set:
                output_addresses_set.add(address_list[i])
            else:
                merging_addresses_set.add(address_list[i])

    end = time.time()

    # write to merging_addresses.txt file
    merging_addresses_file = open(CONSTANTS['MERGING_FILE'], "a")
    for addr in merging_addresses_set:
        merging_addresses_file.write(addr + "\n")

    merging_addresses_file.close()

    print("Time elapsed: ", end - start)
    print(len(output_addresses_set))
    print("--------------------------------------------")
    print(len(merging_addresses_set))
    print(merging_addresses_set)


# generate_exchange_addresses()
# fifth_labor_problem1()
# fifth_labor_problem2()
# check_exchange_address()
