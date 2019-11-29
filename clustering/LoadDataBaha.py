
import numpy as np
import time
from graph.getGraph.getAPIData import getGraph



def LoadData(d, m, y, Offset):
    """
    This function load the composit graph data by  calling getGraph function (built by the graph team) to build the COMPOSITE graph.
    It creates CSV file that represents the graph of transactions and addresses.

             """
    code = None
    dd = d
    mm = m
    yy = y
    dOffset = Offset
    graphType = 'COMPOSITE'
    code, x = getGraph(dd, mm, yy, dOffset, graphType)

    while code == None and x == None:
        time.sleep(30)


    data = x.edges()
    data = list(data)

    return data

def TransactionsWithoutDuplications(d, m, y, Offset):
    """
           This function aims to return the TransactionsFrom and TransactionsTo
            without duplication and the number of transactions.
           Those values will be passed to CommonSpending, ChangeAddress, and TransitiveClosure functions.
         """

    data = LoadData(d, m, y, Offset)
    arr = np.array(data)
    TransactionsTo = []
    TransactionsFrom = []


    for row in arr:
        if len(row[1]) == 34 and row[1] not in TransactionsTo:
            x = row[1]
            TransactionsTo.append(x)

    for row in arr:
        if len(row[0]) == 34 and row[0] not in TransactionsFrom:
            y = row[0]
            TransactionsFrom.append(y)


    return arr, TransactionsTo, TransactionsFrom