"""  Author: Saumya Omanakuttan
Reference Papers are listed below:
1. Akcora, Cuneyt Gurcan, Yulia R. Gel, and Murat Kantarcioglu. "Blockchain: A graph primer." arXiv preprint arXiv:1708.08749 (2017).
2. Akcora, C. G., Dey, A. K., Gel, Y. R., & Kantarcioglu, M. (2018, June). Forecasting bitcoin price with graph chainlets. In Pacific-Asia Conference on Knowledge
Discovery and Data Mining (pp. 765-776). Springer, Cham.
3. Chen, Ting, Yuxiao Zhu, Zihao Li, Jiachi Chen, Xiaoqi Li, Xiapu Luo, Xiaodong Lin, and Xiaosong Zhange. "Understanding ethereum via graph analysis.
In IEEE INFOCOM 2018-IEEE Conference on Computer Communications, pp.1484-1492. IEEE, 2018.
4. Ron, Dorit, and Adi Shamir. "Quantitative analysis of the full bitcoin transaction graph." In International Conference on Financial Cryptography and Data
Security, pp. 6-24. Springer, Berlin, Heidelberg, 2013.

"""

import pandas as pd
import networkx as nx
from collections import defaultdict
import requests

BTC_CIRC_URL="http://159.203.28.234:5000/bitcoin/bitcoin_circulation"
BTC_CC_URL = "http://159.203.28.234:5000/bitcoin/clustering_coefficient"
BTC_MAE = "http://159.203.28.234:5000/bitcoin/most_active_entity"
BTC_PC = "http://159.203.28.234:5000/bitcoin/pearson_coefficient"


def BTCirculation(date, ntObj, dbobj):

    ''' Analyse the Total Bitcoin In Circulation on Daily Basis'''

    try:
        count = 0
        count1 = 0
        BitcoinCircle = 0.0
        outdegree = dict(ntObj.out_degree(weight='weight'))
        indegree = dict(ntObj.in_degree(weight='weight'))
        for key, inval in indegree.items():
            if len(key) != 64:
                count = count + inval
        for key, outval in outdegree.items():
            if len(key) != 64:
                count1 = count1 + outval
        NtBitcoinCircle = ((count - count1)/count)*100
        Total = count+count1
        bitcoinCirculated = 100 -NtBitcoinCircle

        data = {
            'Date': date,
            'TotBTC': Total,
            'CircPercent': bitcoinCirculated,
            'NotCircuPercent': NtBitcoinCircle
        }
        r = requests.post(url=BTC_CIRC_URL, data=data)


        dbobj = dbobj.append({"Date": date, "Total Bitcoin": Total, "Circulating Bitcoins %" :bitcoinCirculated, "Not Circulating Bitcoins %" : NtBitcoinCircle }, ignore_index=True)


        return "Success", dbobj

    except Exception as e:
        return 'Fail', e


def MostActiveEntity(Date, ntObj,dfObj):

    ''' Analyse the Most Active Entity on Daily Basis'''

    df = pd.DataFrame(columns=["Date", "Node", "Total Number of Transaction"])
    try:
        outdegree = dict(ntObj.out_degree)
        indegree = dict(ntObj.in_degree)
        tot = defaultdict(list)
        for key, inval in indegree.items():
            if len(key) != 64:
                total = inval + outdegree[key]
                tot[key].append(total)

                dfObj = dfObj.append({"Date": Date,"Node": key,"Total Number of Transaction": total}, ignore_index=True)
        dfObj.sort_values(by=['Total Number of Transaction'], inplace=True, ascending=False)

        df = dfObj.head()

        for ind in df.index:
            data = {
                'Date': df['Date'][ind],
                'Addr': df['Node'][ind],
                'NoOfTrans': df['Total Number of Transaction'][ind]
            }

            r = requests.post(url= BTC_MAE, data=data)


        return "Success", df
    except Exception as e:
        return 'Fail', e



def clusteringCoefficientNode(ntObj):

    ''' Analyse the Clustering Co-efficient on Address on Daily Basis'''

    try:
        df = pd.DataFrame(columns=["Node", "ClusteringCoefficient"])
        G = nx.Graph()
        for u, v, data in ntObj.edges(data=True):
            w = data['weight'] if 'weight' in data else 1.0
            if G.has_edge(u, v):
                G[u][v]['weight'] += w
            else:
                G.add_edge(u, v, weight=w)

        Clustercoef = dict(nx.clustering(G,weight= 'weight'))
        for key, val in Clustercoef.items():
            if len(key) != 64:
                df = df.append({"Node": key, "ClusteringCoefficient": val}, ignore_index=True)
    except Exception as e:
        return 'Fail', e
    return "Success", df



def clusteringCoefficientonGraph(date,ntObj,dfObj ):

    ''' Analyse the Clustering Co-efficient on Daily Basis'''

    try:
        G = nx.Graph()
        for u, v, data in ntObj.edges(data=True):
            w = data['weight'] if 'weight' in data else 1.0
            if G.has_edge(u, v):
                G[u][v]['weight'] += w
            else:
                G.add_edge(u, v, weight=w)

        Clustercoef = nx.average_clustering(G)

        dfObj = dfObj.append({"Date": date, "Clustering coefficient":  Clustercoef}, ignore_index=True)

        data = {
            'Date': date,
            'ClustCoeff': Clustercoef
        }
        r = requests.post(url=BTC_CC_URL, data=data)

        return "Success", dfObj
    except Exception as e:
        return 'Fail', e


def PearsonCoefficient(date,ntObj,dfObj):

    ''' Analyse the Pearson Co-efficient on Daily Basis'''

    try:
        Pearcoef = 0.0
        G = nx.Graph()
        for u, v, data in ntObj.edges(data=True):
            w = data['weight'] if 'weight' in data else 1.0
            if G.has_edge(u, v):
                G[u][v]['weight'] += w
            else:
                G.add_edge(u, v, weight=w)

        Pearcoef = float(nx.degree_pearson_correlation_coefficient(G))

        dfObj = dfObj.append({"Date": date, "Pearson coefficient":  Pearcoef}, ignore_index=True)

        data = {
            'Date': date,
            'PearCoeff': Pearcoef
        }
        r = requests.post(url=BTC_PC, data=data)

        return "Success", dfObj
    except Exception as e:
        return 'Fail', e