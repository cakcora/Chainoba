import requests
import networkx as nx
ETHER_URL = "http://localhost:6000/ethereum/transactions"

def getdata(day,month,year,dOffset,tokename):
    query_params = {
        'day': day,
        'month': month,
        'year': year,
        'date_offset': dOffset,
        'token_name': tokename
    }
    try:
        response = requests.get(ETHER_URL, params=query_params)
        y= response.json()
        if y['ResponseCode'] != 200:
            return 'Fail', y['ResponseDesc']

    except Exception as e:
        return 'Fail', e
    return 'Success', response.json()


def getEthereumgraph(day,month,year,dOffset,tokename):
    #get ethereum data from API
    try:
        result, etherdata= getdata(day,month,year,dOffset,tokename)
        if result=='Success':
            G= nx.MultiDiGraph()

            for trans in etherdata['Transactions']:
                G.add_edge(trans['InputNodeAddress'], trans['OutputNodeAddress'], weight=int(trans['TokenAmount']))
        else:
            return 'Fail', etherdata
    except Exception as e:
        return 'Fail', e
    return 'Success', G

"""
if __name__=='__main__':
    result,graph = getEthereumgraph(24, 4, 2018, 1, "zrx")
    print(result)
    print(graph.in_degree(weight='weight'))
"""