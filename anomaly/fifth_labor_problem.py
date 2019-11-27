import requests
import time
import pandas as pd


# fifth_labor_problem1 method returns additional suspicious addresses regarding following problem:
# If an address receives multiple payments from suspicious Ransomware addresses
# ( i.e. merge address), then it is regarded as suspicious
def fifth_labor_problem1():
    url = 'https://blockchain.info/rawaddr/'
    with open('chainletElimination.txt', 'r') as file:
        data = file.readlines()

    suspicious_dictionary = dict()

    start = time.time()

    for line in range(1000):  # len(data) is more than 20K

        suspicious_address = data[line].split("\t")[1].split("\n")[0]
        # in case bad connection, skip one transaction.
        try:
            request = requests.get(url + suspicious_address)
            json_text = request.json()
        except BaseException as error:
            print("invalid request or invalid json:{}" + format(error) + "in line" + str(line))
            line += 1
            continue

        # store all the transactions containing initial suspicious addresses
        transaction_list = json_text["txs"]

        # TODO: len(transaction_list) only can get 50 transactions at most.
        #  However, transaction counts are more.
        # print(len(transaction_list))

        output_address_set = set()

        # using initial suspicious addresses as inputs return all the output addresses within one transaction
        print("executing line number:", line)  # line number 83, transaction list 37 +, it is coin based trans
        for i in range(len(transaction_list)):
            # print("transaction_list", i)
            # It is a coinBase transaction without "prev_out" in input address.
            if "prev_out" not in transaction_list[i]["inputs"][0]:
                break
            else:
                for j in range(len(transaction_list[i]["inputs"])):
                    # suspicious_address as an input, find out all output addresses.
                    if transaction_list[i]["inputs"][j]["prev_out"]["addr"] == suspicious_address:
                        for x in range(len(transaction_list[i]["out"])):
                            output_address_set.add(transaction_list[i]["out"][x]["addr"])

        suspicious_dictionary[suspicious_address] = output_address_set

    # TEST: SHOW whole suspicious dictionary information
    # print(str(suspicious_dictionary).replace(", ", "\n"))
    # print("--------------------------------------------")

    # set of all output addresses
    output_addresses_set = set()
    merging_addresses_set = set()

    # iterate suspicious_dictionary to find merging addresses in one transaction.
    for key, value in suspicious_dictionary.items():
        address_list = list(value)
        for i in range(len(address_list)):
            if address_list[i] not in output_addresses_set:
                output_addresses_set.add(address_list[i])
            else:
                # duplicate output addresses, then add into merging addresses est
                merging_addresses_set.add(address_list[i])

    end = time.time()

    merging_addresses_file = open("merging_addresses.txt", "a")

    # write to merging_addresses.txt file
    for addr in merging_addresses_set:
        merging_addresses_file.write(addr + "\n")

    merging_addresses_file.close()

    # Testing 1000 lines from input require 636 secs, found 1217 merging addresses
    #                                                   with 4 exchange addresses
    # TODO: some merging addresses seem to be exchange addresses
    print("Time elapsed: ", end - start)
    print(len(output_addresses_set))
    print("--------------------------------------------")
    print(len(merging_addresses_set))
    print(merging_addresses_set)


# preprocessing transaction_details_26_10_2019.csv file - generate exchange_addresses.txt
def generate_exchange_address():

    data_frame = pd.read_csv('transaction_details_26_10_2019.csv', usecols=['Inputs'])
    file = open("exchange_addresses.txt", "w+")
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
# eliminated exchange addresses from merging address list
def check_exchange_address():
    with open('merging_addresses.txt', 'r') as file:
        merging_list = file.readlines()
    with open('exchange_addresses.txt', 'r') as file:
        exchange_list = file.readlines()

    # check if duplicates
    if len(merging_list) == len(set(merging_list)):
        print("no duplicates")
    else:
        print("duplicates")

    for addr in merging_list:
        if addr in exchange_list:
            print(addr)

    # TODO: will eliminate addr from merging_address after all the computation is done.


# generate_exchange_addresses()
# fifth_labor_problem1()
# check_exchange_address()


# TODO: If multiple suspicious addresses merge after N block, then the merging address is suspicious.
def fifth_labor_problem2():
    return 0
