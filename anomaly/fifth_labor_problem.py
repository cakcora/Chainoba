# fifth_labor_problem1 method returns additional suspicious addresses regarding following problem:
# If an address receives multiple payments from suspicious Ransomware addresses
# ( i.e. merge address), then it is regarded as suspicious

import requests
import time


def fifth_labor_problem1():
    url = 'https://blockchain.info/rawaddr/'
    with open('chainletElimination.txt', 'r') as file:
        data = file.readlines()

    suspicious_dictionary = dict()

    start = time.time()

    for line in range(1000):  # len(data) is more than 20K

        suspicious_address = data[line].split("\t")[1].split("\n")[0]
        request = requests.get(url + suspicious_address)
        json_text = request.json()

        # store all the transactions containing initial suspicious addresses
        transaction_list = json_text["txs"]

        # TODO: len(transaction_list) only can get 50 transactions at most.
        #  However, transaction counts are more.
        # print(len(transaction_list))

        output_address_set = set()

        # using initial suspicious addresses as inputs return all the output addresses within one transaction
        print("executing line number:", line)  # line number 83, transaction list 37 +
        for i in range(len(transaction_list)):
            # print("transaction_list", i)
            # check if it is a COINBASE transaction, if there is "prev_out" in input address.
            if "prev_out" not in transaction_list[i]["inputs"][0]:
                break
            else:
                for j in range(len(transaction_list[i]["inputs"])):
                    if transaction_list[i]["inputs"][j]["prev_out"]["addr"] == suspicious_address:
                        for x in range(len(transaction_list[i]["out"])):
                            output_address_set.add(transaction_list[i]["out"][x]["addr"])

        suspicious_dictionary[suspicious_address] = output_address_set

    # TEST: SHOW whole suspicious dictionary information
    # print(str(suspicious_dictionary).replace(", ", "\n"))
    # print("--------------------------------------------")

    non_merging_addresses_set = set()
    merging_addresses_set = set()

    # iterate suspicious_dictionary to find merging addresses in one transaction.
    for key, value in suspicious_dictionary.items():
        address_list = list(value)
        for i in range(len(address_list)):
            if address_list[i] not in non_merging_addresses_set:
                non_merging_addresses_set.add(address_list[i])
            else:
                merging_addresses_set.add(address_list[i])

    end = time.time()

    # Testing 1000 lines from input require 636 secs, found 1217 merging addresses
    # TODO: some merging addresses seem to be exchange addresses
    print("Time elapsed: ", end - start)
    print(len(non_merging_addresses_set))
    print("--------------------------------------------")
    print(len(merging_addresses_set))
    print(merging_addresses_set)


fifth_labor_problem1()

# TODO: If multiple suspicious addresses merge after N block, then the merging address is suspicious.
def fifth_labor_problem2():
    return 0