import requests
import os
from dataExtraction import Extract_MainGraph,Extract_AddressGraph,Extract_TransactionGraph
from dataProcessing import EdgeListCreation, VertexListCreation
BLOCK_URL = "http://localhost:5000/bitcoin/blocks"
TRANSBLOCK_URL = "http://localhost:5000/bitcoin/blocks/transactions"
TRANSACTION_URL = "http://localhost:5000/bitcoin/transactions"
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


def getGraph(dd=9, mm=1, yy=2009, dOffset=1,graphType = 'COMPOSITE',dirPath=""):
    try:
        """Get block ids"""
        result, blkID = getBlockIds(dd, mm, yy, dOffset)
        transId = []
        bCount = 0

        if result == 'Success':
            """Get transactions by block ids (block_ids maximum size 5)"""
            while bCount < len(blkID):
                if (len(blkID) - bCount) > BLOCK_SIZE:
                    counter = bCount+BLOCK_SIZE
                else:
                    counter = len(blkID)
                result2, transacId = getTransactionIds(blkID[bCount : counter])
                if result2 == 'Success':
                    transId = transId + transacId
                    bCount = counter
                else:
                    return 'Fail', transacId
            graphfilepath = ""
            """Check if path exists, if not then create it"""
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            edgelist_file_name = graphType + "_Graph_edgelist" + str(dd) + "_" + str(mm) + "_" + str(yy) + "_" + str(dOffset) + ".csv"
            edgelist_full_path = os.path.join(dirPath, edgelist_file_name)
            temp = graphType + "_temp_" + str(dd) + "_" + str(mm) + "_" + str(yy) + "_" + str(dOffset) + ".csv"
            temp_path = os.path.join(dirPath, temp)
            if os.path.isfile(edgelist_full_path):
                os.remove(edgelist_full_path)
            if graphType != 'COMPOSITE':
                if os.path.isfile(temp_path):
                    os.remove(temp_path)
                f = open(temp_path, "a")
                f.write("From,To")
                f.close()
            if graphType == 'COMPOSITE':
                f = open(edgelist_full_path, "a")
                f.write("From,To,Amount")
                f.close()
            else:
                vertexlist_file_name = graphType + "_Graph_vertexlist" + str(dd) + "_" + str(mm) + "_" + str(yy) + "_" + str(dOffset) + ".csv"
                vertexlist_full_path = os.path.join(dirPath, vertexlist_file_name)
                if os.path.isfile(vertexlist_full_path):
                    os.remove(vertexlist_full_path)
            bCount = 0
            """Get transactions' details by transaction id (transaction_ids maximum size 10)"""
            while bCount < len(transId):
                if (len(transId) - bCount) > TRANSACTION_SIZE:
                    counter = bCount+TRANSACTION_SIZE
                else:
                    counter = len(transId)
                result3, transacDetail = getTransactionDetails(transId[bCount: counter])
                if result3 == 'Success':
                    if graphType == 'COMPOSITE':
                        result4, graphfilepath = Extract_MainGraph(transacDetail,edgelist_full_path)
                        if result4 != 'Success':
                            return 'Fail', graphfilepath
                    elif graphType == 'ADDRESS':
                        result4, graphfilepath = Extract_AddressGraph(transacDetail,temp_path)
                        if result4 != 'Success':
                            return 'Fail', graphfilepath
                    elif graphType == 'TRANSACTION':
                        result4, graphfilepath = Extract_TransactionGraph(transacDetail,temp_path)
                        if result4 != 'Success':
                            return 'Fail', graphfilepath
                    else:
                        os.remove(temp_path)
                        return 'Fail', 'Wrong graph type'
                    bCount = counter
                else:
                    return 'Fail', transacDetail
            if graphType !='COMPOSITE':
                """Calling functions to create edge list and vertex list"""
                result5 = EdgeListCreation(temp_path,edgelist_full_path)
                result6 = VertexListCreation(temp_path, vertexlist_full_path)
                if result5 != 'Success' and result6 != 'Success':
                    os.remove(temp_path)
                    return 'Fail', result5 + " " + result6
                os.remove(temp_path)
        else:
            return 'Fail', blkID
    except Exception as e:
        return 'Fail', e
    return 'Success', 'csv file at its given path'
