import requests
import networkx as nx

from graph.getGraph.dataExtraction import Extract_MainGraph, Extract_AddressGraph, Extract_TransactionGraph
from graph.getGraph.dataProcessing import EdgeListCreation, VertexListCreation
import pandas as pd
BLOCK_URL = "http://159.203.28.234:5000/bitcoin/blocks"
TRANSBLOCK_URL = "http://159.203.28.234:5000/bitcoin/blocks/transactions"
TRANSACTION_URL = "http://159.203.28.234:5000/bitcoin/transactions"

BLOCK_SIZE = 5
TRANSACTION_SIZE = 10


def getBlockIds(dd=9, mm=1, yy=2009, dateOff=1):
    """
    Method to get block ids (date_offset maximum value 31)
    """
    try:
        query_params = {
            'day': dd,
            'month': mm,
            'year': yy,
            'date_offset': dateOff
        }
        response = requests.get(BLOCK_URL, params=query_params)
        y = response.json()
        blockIds = []
        # check if it is a success
        if y['ResponseCode'] == 200:
            for readBlockId in y['Blocks']:
                blockIds.append(readBlockId['BlockId'])
        else:
            return 'Fail', y['ResponseDesc']
    except Exception as e:
        return 'Fail', e
    return 'Success', blockIds


def getTransactionIds(blockIds):
    """
    Method to get transactions by block ids (block_ids maximum size 5)
    """
    try:
        query_params = {
            'block_ids': [blockIds]
        }
        response = requests.get(TRANSBLOCK_URL, params=query_params)
        y = response.json()
        transIds = []
        if y['ResponseCode'] == 200:
            for readBlockData, value in y['BlockTransactionData'].items():
                for readTransId in value['Transactions']:
                    transIds.append(readTransId['TransactionId'])
        else:
            return 'Fail', y['ResponseDesc']
    except Exception as e:
        return 'Fail', e
    return 'Success', transIds


def getTransactionDetails(transId):
    """
    Method to get transactions' details by transaction id (transaction_ids maximum size 10)
    """
    try:
        query_param = {
            'transaction_ids': [transId]
        }
        response = requests.get(TRANSACTION_URL, params=query_param)
        y = response.json()
        if y['ResponseCode'] != 200:
            return 'Fail', y['ResponseDesc']
    except Exception as e:
        return 'Fail', e
    return 'Success', response.text


def getGraph(dd=9, mm=1, yy=2009, dOffset=1, graphType='COMPOSITE'):
    dfObj = pd.DataFrame()
    vertexlist = []

    try:
        """Get block ids"""
        result, blkID = getBlockIds(dd, mm, yy, dOffset)
        transId = []
        bCount = 0

        dfObj = pd.DataFrame(columns=['source', 'target', 'weight'])

        if result == 'Success':
            """Get transactions by block ids (block_ids maximum size 5)"""
            while bCount < len(blkID):
                if (len(blkID) - bCount) > BLOCK_SIZE:
                    counter = bCount + BLOCK_SIZE
                else:
                    counter = len(blkID)
                result2, transacId = getTransactionIds(blkID[bCount: counter])
                if result2 == 'Success':
                    transId = transId + transacId
                    bCount = counter
                else:
                    return 'Fail', transacId

            bCount = 0
            """Get transactions' details by transaction id (transaction_ids maximum size 10)"""
            while bCount < len(transId):
                if (len(transId) - bCount) > TRANSACTION_SIZE:
                    counter = bCount + TRANSACTION_SIZE
                else:
                    counter = len(transId)
                result3, transacDetail = getTransactionDetails(transId[bCount: counter])

                if result3 == 'Success':
                    if graphType == 'COMPOSITE':
                        result4, dfObj = Extract_MainGraph(transacDetail, dfObj)
                        if result4 != 'Success':
                            return 'Fail', dfObj
                    elif graphType == 'ADDRESS':
                        result4, dfObj = Extract_AddressGraph(transacDetail, dfObj)
                        if result4 != 'Success':
                            return 'Fail', dfObj
                    elif graphType == 'TRANSACTION':
                        result4, dfObj = Extract_TransactionGraph(transacDetail, dfObj)
                        if result4 != 'Success':
                            return 'Fail', dfObj
                    else:
                        return 'Fail', 'Wrong graph type'
                    bCount = counter
                else:
                    return 'Fail', transacDetail
            if graphType != 'COMPOSITE':
                """Calling functions to create edge list and vertex list"""
                result5, vertexlist = VertexListCreation(dfObj, vertexlist)
                result6, dfObj = EdgeListCreation(dfObj)
                if result5 != 'Success' and result6 != 'Success':
                    return 'Fail', result5 + " " + result6
        else:
            return 'Fail', blkID
        if graphType == 'COMPOSITE':
            netxObj = nx.from_pandas_edgelist(dfObj, edge_attr=True, create_using=nx.MultiDiGraph())
        else:
            netxObj = nx.from_pandas_edgelist(dfObj, edge_attr=True, create_using=nx.MultiDiGraph())
            netxObj.add_nodes_from(vertexlist)
    except Exception as e:
        return 'Fail', e
    return 'Success', netxObj
