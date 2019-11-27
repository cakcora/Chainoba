'''
Compute the squares clustering coefficient for nodes: the fraction of possible squares that exist at the node.

'''


import networkx as nx




def calculate(network):
    try:
        n = nx.square_clustering(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7) 
