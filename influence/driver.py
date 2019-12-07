from graph.getGraph.getAPIData import getGraph

import matplotlib.pyplot as plt
import random
import networkx as nx
from influence.generator import generate_undirected_graph
import influence.centralities as centralities

# ======= Dilawer's Functions =============

# Get k-core subgraph for a given graph 'G' and of specified coreness 'k'
def get_k_cores(G, k):
    """
    Gets y
    """
    return ""

# Maximum k-core subgraph for a given graph 'G'
def max_k_core_graph(G):
    """
    """
    return ""

# Get the maximum degree of a graph
def max_deg(G):
    max_degree = 0
    for node in G.nodes():
        deg = G.degree[node]
        if(deg>max_degree):
            max_degree = deg
    return max_degree

# Get the maximum K value for a given vertex
def get_max_k_value(G, vertex):
    return G.number_of_edges(vertex)

# Import the ethereum graph from 'graph' team.
def generate_undirected_graph():
    """
    Using networkx, put together a undirected graph.
    :return:
    """

def generate_edges(graph):

    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges

# ======= End of Dilawer's Functions =============

# ======= Matthias's Functions =============

def calculate_degree_centrality_for_nodes():
    G = generate_undirected_graph()
    print(G)
    C = centralities.calculate_degree_centrality_for_nodes(G)
    print(C)

def calculate_degree_centrality_for_graph():
    G = generate_undirected_graph()
    C = centralities.calculate_degree_centrality_for_graph(G)
    print(C)

def calculate_betweenness_centrality_for_nodes():
    G = generate_undirected_graph()
    C = centralities.calculate_betweenness_centrality_for_nodes(G)
    print(C)

def calculate_betweenness_centrality_for_graph():
    G = generate_undirected_graph()
    C = centralities.calculate_betweenness_centrality_for_graph(G)
    print(C)

def calculate_closeness_centrality_for_graph():
    G = generate_undirected_graph()
    C = centralities.calculate_closeness_centrality_for_graph(G)
    print(C)

def calculate_generalized_hoede_bakker_index():
    """
    We will assert the functionality of this implementation by a simplied & hypothetical B and gd.
    """

    # Sample Influence Function
    # Everyone will follow Node 0's decision
    def B(I):
        return [I[0]] * len(I)

    # Sample Group Decision Function
    # If Node 0 and Node 1 has the same opinion, they follow Node 0. Otherwise, they follow Node 1.
    def gd(I):
        if I[0] == I[1]:
            return I[0]
        else:
            return I[1]
        
    # Let's assume we have 10 people in the group
    n = 10

    # The influential power of Node 0 is 1.0. Everyone will listen to her!
    print("calculate_generalized_hoede_bakker_index(): asserting index == 1 Node 0")
    assert (1 == centralities.calculate_generalised_hoede_bakker_index(n, 0, B, gd))

    # The influential power of Node 1 (or all the other nodes in this case) will be 0, because they'll always listen to Node 0.
    print("calculate_generalized_hoede_bakker_index(): asserting index == 0 Node 1")
    assert (0 == centralities.calculate_generalised_hoede_bakker_index(n, 1, B, gd))

# ======= End of Matthias's Functions =============

if __name__ == '__main__':
    
    print ("calculate_degree_centrality_for_nodes()")
    calculate_degree_centrality_for_nodes()
    print ("calculate_degree_centrality_for_graph()")
    calculate_degree_centrality_for_graph()
    print ("calculate_betweenness_centrality_for_graph()")
    calculate_betweenness_centrality_for_graph()
    print ("calculate_betweenness_centrality_for_nodes()")
    calculate_betweenness_centrality_for_nodes()
    print ("calculate_closeness_centrality_for_graph()")
    calculate_closeness_centrality_for_graph()
    print ("calculate_generalized_hoede_bakker_index()")
    calculate_generalized_hoede_bakker_index()
