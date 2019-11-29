import csv
import pandas as pd
import numpy as np

def TransitiveClosure(d, m, y, Offset):
    """
              This finction is to implement Trasitive Closure Heuristic that concern about mutual addresses between
              transactions. for example (a and b are input addresses for T1) and (b and c  are input addresses for T2),
              so it is probably that a, b, and c belong to the same user. This function return a csv file where each row
               has the addresses belong to the same user.
            """

    arr, TransactionsTo, TransactionsFrom = TransactionsWithoutDuplications(d, m, y, Offset)
    NumberOfTxsTo = len(TransactionsTo)
    TxsWithTwoOrMoreInputs = []
    with open('TwoAddressesInput.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Transaction'] + ['First Address'] + ['Second Address'])

    with open('TransitiveClosure.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ['Transactions1'] + ['Transactions2'] + ['First Address'] + ['Second Address'] + ['Third Address'])


    for x in range(NumberOfTxsTo):
        TxInputAddresses = []

        for row in arr:
            if row[1] == TransactionsTo[x] and row[0] not in TxInputAddresses:
                TxInputAddresses.append(row[0])

        if len(TxInputAddresses) == 2:
            with open('TwoAddressesInput.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([TransactionsTo[x]] + [TxInputAddresses[0]] + [TxInputAddresses[1]])

    TwoAddressesInput = pd.read_csv('TwoAddressesInput.csv')
    arrTwoAddressesInput = np.array(TwoAddressesInput)

    count = len(arrTwoAddressesInput)
    for g in arrTwoAddressesInput:
        x = g
        arrTwoAddressesInput = np.delete(arrTwoAddressesInput, 0, axis=0)
        for f in arrTwoAddressesInput:
            pp = bool(set(g) & set(f))
            if pp == True:
                Transitive = sorted(list(set(x).union(set(f))))
                with open('TransitiveClosure.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([Transitive[0]] + [Transitive[1]] + [Transitive[2]] + [Transitive[3]] + [Transitive[4]])