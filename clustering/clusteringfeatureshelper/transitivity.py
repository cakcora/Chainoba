'''
Compute graph transitivity, the fraction of all possible triangles present in G.

'''

import networkx as nx


def calculate(network):
    try:
        n = nx.transitivity(network)
    except:
        n = 0
    return round(n, 5)
