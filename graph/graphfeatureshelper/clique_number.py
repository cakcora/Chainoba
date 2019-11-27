import networkx as nx
'''
Return the clique number (size of the largest clique) for G.
'''

def calculate(network):
    try:
        n = nx.graph_clique_number(network)
    except:
        n = 0
    return n
