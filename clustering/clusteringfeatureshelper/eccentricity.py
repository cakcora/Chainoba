'''

The eccentricity of a node v is the maximum distance from v to all other nodes in G.
'''

import networkx as nx

def calculate(network):
    try:
        n = nx.eccentricity(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7) 
