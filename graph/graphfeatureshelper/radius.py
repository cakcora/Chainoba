'''

The radius is the minimum eccentricity.
'''

import networkx as nx



def calculate(network):
    try:
        n = nx.radius(network)
    except:
        return 0
 
    return round(n, 7) 
