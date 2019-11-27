
'''
Node connectivity is equal to the minimum number of nodes that must be removed to disconnect G or render it trivial. If source and target nodes are provided, this function returns the local node connectivity.

Returns the average connectivity of a graph G.
'''

import networkx as nx


def calculate(network):
    try:
        n = nx.average_node_connectivity(network)
    except:
        return 0
 
    return round(n, 7) 
