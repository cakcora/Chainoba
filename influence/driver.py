from graph.getGraph.getAPIData import getGraph

import matplotlib.pyplot as plt
import random
import networkx as nx

# Get k-core subgraph for a given graph 'G' and of specified coreness 'k'
def get_k_cores(G, k):
    """
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

message, G = getGraph(9, 2, 2009, 2, 'ADDRESS')

nx.draw(G)
plt.show()

# H = max_k_core_graph(G)
# maxGdeg = max_deg(G)
# L = nx.k_core(G, maxGdeg)
#
# print("FOR H-----")
# max_degree = 0
# for node in H.nodes():
#     node_deg = H.degree[node]
#     if(node_deg > max_degree):
#         max_degree = node_deg
# print(max_degree)
#
# min_degree = max_degree
# for node in H.nodes():
#     node_deg = H.degree[node]
#     if(node_deg < min_degree):
#         min_degree = node_deg
# print(min_degree)
#
# print("For L----")
# max_degree = 0
# for node in L.nodes():
#     node_deg = L.degree[node]
#     if(node_deg > max_degree):
#         max_degree = node_deg
# print(max_degree)
#
# min_degree = max_degree
# for node in L.nodes():
#     node_deg = L.degree[node]
#     if(node_deg < min_degree):
#         min_degree = node_deg
# print(min_degree)
#
# nx.draw(H)
# plt.show()

# G = generate_undirected_graph()
# K = max_k_core_graph(G)

# nx.draw(H)

# nx.draw(K)
# plt.show()

# print(get_max_k_value(G), G.nodes[0][0])

# k1 = get_k_cores(G,1)