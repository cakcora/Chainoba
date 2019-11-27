'''

Return the PageRank of the nodes in the graph.

PageRank computes a ranking of the nodes in the graph G based on the structure of the incoming links. It was originally designed as an algorithm to rank web pages.


'''
import networkx as nx


def calculate(network):
    try:
        n = nx.pagerank_numpy(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7) 
