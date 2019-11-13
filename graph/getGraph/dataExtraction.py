import json


def Extract_MainGraph(x, edgelist):
    """
    # Create an edgelist for Composite Graph where x is the transaction detail as an input

    """
    try:
        y = json.loads(x)
        csv = " "
        for k in y["TransactionData"]:
            el = y["TransactionData"][k]
            Hash = el["Hash"]
            PreviousTransactionOutputId = ""
            PreviousTransactionOutputId = el["TransactionInputs"][0]["PreviousTransactionOutputId"]

            if PreviousTransactionOutputId is not None:
                for l in el["TransactionInputs"]:
                    InputAddress = l["InputAddresses"][0]["Address"]
                    InputValue = l["Value"]
                    csv = csv+ "\n" + str(InputAddress) + "," + str(Hash) + "," + str(InputValue)
                for m in el["TransactionOutputs"]:
                    OutputAddress = m["OutputAddresses"][0]["Address"]
                    OutputValue = m["Value"]
                    csv = csv + "\n"+ str(Hash) + "," + str(OutputAddress) + "," + str(OutputValue)
            else:
                OutputAddress = el["TransactionOutputs"][0]["OutputAddresses"][0]["Address"]
                OutputValue = el["TransactionOutputs"][0]["Value"]
                csv = csv + "\n" + str(Hash) + "," + OutputAddress + "," + str(OutputValue)

        csvfile = open(edgelist, "a")
        csvfile.write(csv)
        csvfile.close()
    except Exception as e:
        return 'Fail', e

    return 'Success',"CSV UPDATED"

def Extract_AddressGraph(x,temp_path):
    """
        # Create an edgelist for Address Graph where x is the transaction detail as an input

    """
    try:
        y = json.loads(x)

        csv = " "

        for k in y["TransactionData"]:
            el = y["TransactionData"][k]
            PreviousTransactionOutputId = ""
            PreviousTransactionOutputId = el["TransactionInputs"][0]["PreviousTransactionOutputId"]

            if PreviousTransactionOutputId is not None:
                for l in el["TransactionInputs"]:
                    InputAddress = l["InputAddresses"][0]["Address"]
                    for m in el["TransactionOutputs"]:
                        OutputAddress = m["OutputAddresses"][0]["Address"]
                        csv = csv + "\n"+str(InputAddress) + "," + str(OutputAddress)
            else:
                OutputAddress = el["TransactionOutputs"][0]["OutputAddresses"][0]["Address"]
                csv = csv + "\n"+"," + str(OutputAddress)

        csvfile = open(temp_path, "a")
        csvfile.write(csv)
        csvfile.close()
    except Exception as e:
        return 'Fail', e

    return 'Success', "yes"

def Extract_TransactionGraph(x,temp_path):
    """
            # Create an edgelist for Transaction Graph where x is the transaction detail as an input

    """
    try:
        y = json.loads(x)
        csv = " "
        for k in y["TransactionData"]:
            el = y["TransactionData"][k]
            Hash = el["Hash"]
            PreviousTransactionOutputId = ""
            PreviousTransactionOutputId = el["TransactionInputs"][0]["PreviousTransactionOutputId"]

            if PreviousTransactionOutputId is not None:
                for l in el["TransactionInputs"]:
                    HashOfPreviousTransaction = l["HashOfPreviousTransaction"]
                    csv = csv+ "\n" + str(HashOfPreviousTransaction) + "," + str(Hash)

            else:
                csv = csv + "\n"+ "," + str(Hash)
        # append csv data to file
        csvfile = open(temp_path, "a")
        csvfile.write(csv)
        csvfile.close()


    except Exception as e:
        return 'Fail', e

    return 'Success', "yes"
