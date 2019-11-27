'''

Betweenness centrality of a node v is the sum of the fraction of all-pairs shortest paths that pass through v.

'''
import networkx as nx


def calculate(network):
    try:
        n = nx.betweenness_centrality(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7) 
