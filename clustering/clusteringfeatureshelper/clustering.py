'''
Compute the average clustering coefficient for the graph G.
'''

import networkx as nx

def calculate(network):
    try:
        n = nx.average_clustering(network)
    except:
        n = 0
    return round(n, 7)
