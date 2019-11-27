
'''
Returns the edge connectivity of the graph or digraph G.

The edge connectivity is equal to the minimum number of edges that must be removed to disconnect G or render it trivial. If source and target nodes are provided, this function returns the local edge connectivity: the minimum number of edges that must be removed to break all paths from source to target in G.

'''

import networkx as nx


def calculate(network):
    try:
        n = nx.edge_connectivity(network)
    except:
        n = 0
    return n
