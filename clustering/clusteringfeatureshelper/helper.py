import networkx as nx


def calculate(network):
    '''

    Betweenness centrality of a node v is the sum of the fraction of all-pairs shortest paths that pass through v.

    '''
    try:
        n = nx.betweenness_centrality(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7) 



def calculateclosenesscentrality(network):
    '''
    Closeness centrality at a node is 1/average distance to all other nodes.

    The closeness centrality is normalized to to n-1 / size(G)-1 where n is the number of nodes in the connected part of graph containing the node. If the graph is not completely connected, this algorithm computes the closeness centrality for each connected part separately.

    It measures how fast information spreads from a given node to other reachable nodes in the graphs. For a node $u$, it represents the reciprocal of the average shortest path length between $u$ and every other reachable node in the graph:

    '''
    try:
        n = nx.closeness_centrality(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7)



def calculateclusteringcoefficient(network):

    '''
    Compute the average clustering coefficient for the graph G.
    '''
    try:
        n = nx.average_clustering(network)
    except:
        n = 0
    return round(n, 7)




def calculatecommunicabilitycentrality(network):
    '''
    Communicability centrality, also called subgraph centrality, of a node n is the sum of closed walks of all lengths starting and ending at node n.


    '''
    try:
        n = nx.communicability_centrality(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  Q
    else:
        return round(sum(n.values())/len(n.values()), 7)



def calculatekcore(net):
    '''
    Return the core number for each vertex.

    A k-core is a maximal subgraph that contains nodes of degree k or more.

    The core number of a node is the largest value k of a k-core containing that node.
    '''
    if net.number_of_selfloops() > 0: 
        try:
            net.remove_edges_from(net.selfloop_edges())
        except: 
            return 0
    try:
        c = nx.core_number(net).values()
    except:
        return 0

    if len(c) == 0:
        return 0
    else:
        return round(sum(c)/len(c),7)



def calculatedensity(network):
    '''
    Return the density of a graph.
    '''

    try:
        n = nx.density(network)
    except:
        return 0
 
    return round(n, 7) 



def calculateeccentricity(network):
    '''

    The eccentricity of a node v is the maximum distance from v to all other nodes in G.
    '''
    try:
        n = nx.eccentricity(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7)



def calculatecliques(network):
    '''
    Returns the number of maximal cliques in G.
    '''
    try:
        n = nx.graph_number_of_cliques(network)
    except:
        n = 0
    return n



def calculatetrianglenumber(network):
    '''
    Finds the number of triangles that include a node as one vertex.
    '''
    try:
        n = nx.triangles(network)
    except:
        return 0
 
    if len(n) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7) 
    



def calculatepagerank(network):
    '''

    Return the PageRank of the nodes in the graph.

    PageRank computes a ranking of the nodes in the graph G based on the structure of the incoming links. It was originally designed as an algorithm to rank web pages.

    '''
    try:
        n = nx.pagerank_numpy(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7)


def calculatesquareclustering(network):
    '''
    Compute the squares clustering coefficient for nodes: the fraction of possible squares that exist at the node.

    '''
    try:
        n = nx.square_clustering(network)
    except:
        return 0
 
    if len(n.values()) == 0: 
        return 0  
    else:
        return round(sum(n.values())/len(n.values()), 7)


def calculategraphtransitivity(network):
    '''
    Compute graph transitivity, the fraction of all possible triangles present in G.

    '''
    try:
        n = nx.transitivity(network)
    except:
        n = 0
    return round(n, 5)



