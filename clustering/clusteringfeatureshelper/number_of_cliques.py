'''
Returns the number of maximal cliques in G.
'''

import networkx as nx


def calculate(network):
    try:
        n = nx.graph_number_of_cliques(network)
    except:
        n = 0
    return n
