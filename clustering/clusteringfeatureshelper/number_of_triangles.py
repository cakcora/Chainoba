'''

Finds the number of triangles that include a node as one vertex.
'''

import networkx as nx


def calculate(network):
    try:
        n = nx.triangles(network)
    except:
        return 0
 
    if len(n) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7) 

