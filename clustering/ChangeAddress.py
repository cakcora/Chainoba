import csv
from clustering.LoadDataBaha import TransactionsWithoutDuplications



def ChangeAddress(d, m, y, Offset):
    """
The change address Heuristic should  satisfie the following conditions:
    1- Transaction  has exactly two outputs.
    2- The number of  inputs is equal to one.
    3- One output of the transaction  did not exist before.

It takes the values that is required to generate COMPOSITE graph(day, month, year, and offset), to pass it to
TransactionsWithoutDuplications function which will also pass it to loadData function.

The function will create csv file (in clustering folder, called ChangeAddress)
 in each row it has the transaction hash and the input address and output address that belong to the same user.

Reference:
Ermilov D, Panov M, Yanovich Y. Automatic Bitcoin address clustering.
In2017 16th IEEE International Conference on Machine Learning and Applications (ICMLA) 2017 Dec 18 (pp. 461-466). IEEE.


    """


    arr, TransactionsTo, TransactionsFrom = TransactionsWithoutDuplications(d, m, y, Offset)
    NumberOfTxsFrom = len(TransactionsFrom)
    with open('changeAddress.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Transaction'] + ['First Address'] + ['Second Address'])

        #  for loop to check all the transactions in the COMPOSITE graph.
    for x in range(NumberOfTxsFrom):
        uniqueoutadd = []
        uniqueinadd = []
        position = []
        countrows = 0
        changeaddresssecondvalue = ''
        changeaddressfirstvalue = ''
        changeaddressone = ''
        changeaddresstwo = ''
        # find number of input addresses, for the transaction.
        for row in arr:
            if row[0] == TransactionsFrom[x] and row[1] not in uniqueoutadd:
                position.append(countrows)
                uniqueoutadd.append(row[1])
            countrows += 1

            ## find number of output addresses for the transaction.
            if row[1] == TransactionsFrom[x] and row[0] not in uniqueinadd:
                uniqueinadd.append(row[0])

        # Check the conditions of number of inputs and outputs.
        if len(uniqueoutadd) == 2 and len(uniqueinadd) == 1:
            changeaddressone = True
            changeaddresstwo = True

            # Check if one of the addresses output addresses is new.
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