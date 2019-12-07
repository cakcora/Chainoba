import csv
from clustering.LoadDataBaha import TransactionsWithoutDuplications


def CommonSpending(d, m, y, Offset):


    """
This function  is for implementing CommonSpending Heuristic: If two or more addresses are inputs of the same transaction
with one output, then all these addresses are controlled by the same user.
the function will create csv file in each row it has the transaction hash and the input addresses of the transaction.

    """


    arr, TransactionsTo, TransactionsFrom = TransactionsWithoutDuplications(d, m, y, Offset)
    NumberOfTxsTo = len(TransactionsTo)
    with open('CommonSpending.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Transaction'] + ['First Input Address'] + ['Second Input Address'] + ['Third Input Address'])


    for x in range(NumberOfTxsTo):
        num_input_addresses = 0.
        num_out_addresses = 0
        InputAddresses = []
        OutAddresses = []

        for row in arr:

            if row[1] == TransactionsTo[x] and row[0] not in InputAddresses:
                num_input_addresses = num_input_addresses + 1
                InputAddresses.append(row[0])

        for row in arr:

            if row[0] == TransactionsTo[x] and row[1] not in OutAddresses:
                num_out_addresses = num_out_addresses + 1
                OutAddresses.append(row[1])

        if len(InputAddresses) >= 2 and len(OutAddresses) == 1:
            with open('CommonSpending.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([TransactionsTo[x]] + [InputAddresses[0]] + [InputAddresses[1]])



