'''
Return the density of a graph.
'''

import networkx as nx



def calculate(network):
    try:
        n = nx.density(network)
    except:
        return 0
 
    return round(n, 7) 
