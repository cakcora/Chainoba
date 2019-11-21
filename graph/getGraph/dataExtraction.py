import json
import math


def Extract_MainGraph(x, dataFobj):
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
                    dataFobj=dataFobj.append({'source': str(InputAddress),'target': str(Hash),'weight':int(InputValue)}, ignore_index=True)
                for m in el["TransactionOutputs"]:
                    OutputAddress = m["OutputAddresses"][0]["Address"]
                    OutputValue = m["Value"]
                    dataFobj=dataFobj.append({'source': str(Hash), 'target': str(OutputAddress), 'weight': int(OutputValue)},
                                    ignore_index=True)
            else:
                OutputAddress = el["TransactionOutputs"][0]["OutputAddresses"][0]["Address"]
                OutputValue = el["TransactionOutputs"][0]["Value"]
                dataFobj=dataFobj.append({'source': str(Hash), 'target': str(OutputAddress), 'weight': int(OutputValue)},
                                ignore_index=True)

    except Exception as e:
        return 'Fail', e

    return 'Success',dataFobj

def Extract_AddressGraph(x,dataFobj):
    """
        # Create an edgelist for Address Graph where x is the transaction detail as an input
    """
    try:
        y = json.loads(x)

        for k in y["TransactionData"]:
            Input= 0
            el = y["TransactionData"][k]
            PreviousTransactionOutputId = ""
            PreviousTransactionOutputId = el["TransactionInputs"][0]["PreviousTransactionOutputId"]

            if PreviousTransactionOutputId is not None:
                for l in el["TransactionInputs"]:
                    NowInput = l["Value"]
                    Input = Input + NowInput
                for l in el["TransactionInputs"]:
                    InputAddress = l["InputAddresses"][0]["Address"]
                    NowInput = l["Value"]
                    for m in el["TransactionOutputs"]:
                        OutputAddress = m["OutputAddresses"][0]["Address"]
                        OutPutValue = m["Value"]
                        OutValue = math.ceil((NowInput / Input) * (OutPutValue))
                        dataFobj = dataFobj.append({'source': str(InputAddress), 'target': str(OutputAddress),'weight': int(OutValue)}, ignore_index = True)
            else:
                OutputAddress = el["TransactionOutputs"][0]["OutputAddresses"][0]["Address"]
                dataFobj = dataFobj.append({'source': None, 'target': str(OutputAddress)},
                                           ignore_index=True)
    except Exception as e:
        return 'Fail', e

    return 'Success', dataFobj

def Extract_TransactionGraph(x,dataFobj):
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
                    Value = l["Value"]
                    dataFobj = dataFobj.append({'source': str(HashOfPreviousTransaction), 'target': str(Hash),'weight': int(Value)},
                                               ignore_index=True)

            else:
                dataFobj = dataFobj.append({'source': None, 'target': str(Hash)},
                                           ignore_index=True)
    except Exception as e:
        return 'Fail', e

    return 'Success', dataFobj
