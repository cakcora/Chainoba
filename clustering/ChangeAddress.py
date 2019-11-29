import csv
from clustering.LoadDataBaha import TransactionsWithoutDuplications



def ChangeAddress(d, m, y, Offset):
    """
    The change address Heuristic should  satisfie the following conditions:
    1- Transaction  has exactly two outputs.
    2- The number of  inputs is equal to one.
    3- One output of the transaction  did not exist before

    """


    arr, TransactionsTo, TransactionsFrom = TransactionsWithoutDuplications(d, m, y, Offset)
    NumberOfTxsFrom = len(TransactionsFrom)
    with open('changeAddress.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Transaction'] + ['First Address'] + ['Second Address'])

    for x in range(NumberOfTxsFrom):
        uniqueoutadd = []
        uniqueinadd = []
        position = []
        countrows = 0
        changeaddresssecondvalue = ''
        changeaddressfirstvalue = ''
        changeaddressone = ''
        changeaddresstwo = ''

        for row in arr:
            if row[0] == TransactionsFrom[x] and row[1] not in uniqueoutadd:
                position.append(countrows)
                uniqueoutadd.append(row[1])
            countrows += 1

            if row[1] == TransactionsFrom[x] and row[0] not in uniqueinadd:
                uniqueinadd.append(row[0])


        if len(uniqueoutadd) == 2 and len(uniqueinadd) == 1:
            changeaddressone = True
            changeaddresstwo = True
            for z in range(position[0]):
                if arr[z, 0] == uniqueoutadd[0] or arr[z, 1] == uniqueoutadd[0]:
                    changeaddressone = False
                    break
            if changeaddressone == True:
                changeaddressfirstvalue = uniqueoutadd[0]


            for w in range(position[1]):
                if arr[w, 0] == uniqueoutadd[1] or arr[w, 1] == uniqueoutadd[1]:
                    changeaddresstwo = False
                    break
            if changeaddresstwo == True:
                changeaddresssecondvalue = uniqueoutadd[1]

        if changeaddressone == True:
            with open('changeAddress.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([TransactionsFrom[x]] + [uniqueinadd[0]] + [changeaddressfirstvalue])

        elif changeaddresstwo == True:
            with open('changeAddress.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([TransactionsFrom[x]] + [uniqueinadd[0]] + [changeaddresssecondvalue])