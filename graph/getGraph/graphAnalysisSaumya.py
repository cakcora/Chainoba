import pandas as pd
import networkx as nx
from collections import defaultdict


def BTCirculation(date, ntObj, dbobj):

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



        dbobj = dbobj.append({"Date": date, "Total Bitcoin": Total, "Circulating Bitcoins %" :bitcoinCirculated, "Not Circulating Bitcoins %" : NtBitcoinCircle }, ignore_index=True)
        return "Success", dbobj

    except Exception as e:
        return 'Fail', e


def MostActiveEntity(Date, ntObj,dfObj):

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

        return "Success", df
    except Exception as e:
        return 'Fail', e



def clusteringCoefficientNode(ntObj):
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

        return "Success", dfObj
    except Exception as e:
        return 'Fail', e


def PearsonCoefficient(date,ntObj,dfObj):
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

        return "Success", dfObj
    except Exception as e:
        return 'Fail', e





