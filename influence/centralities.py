"""
This source file provides methods to calculate the following measures:
- Degree Centrality (Nodes, Graph),
- Closeness Centrality (Nodes, graph),
- Betweenness Centrality (Nodes, graph),
- Generalized Hoede-Bakker Index (Node).

Note:
- Clustering Group's function to calculating closeness centrality is not used because it returned "None" Type for a valid graph.

Resource:
    Article: Social networks: Prestige, centrality, and influence
    Authors: Agnieszka Rusinowska, Rudolf Berghammer, Harrie de Swart, Michel Grabisch
    Source: https://link.springer.com/chapter/10.1007/978-3-642-21070-9_2
"""

import networkx as nx
import clustering.clusteringfeatureshelper.helper as clustering_helper
import itertools
import math

def calculate_degree_centrality_for_nodes(G):
    """
    Calculates and returns the degree centralities for each node in the graph.

    :param G: NetworkX.Graph
    :return: Dictionary where key is the index of each node, and value is the degree centrality of the i_th node
    """

    return nx.degree_centrality(G)

def calculate_degree_centrality_for_graph(G):
    """
    Calculates and returns the degree centrality of the graph.

    :param G: NetworkX.Graph
    :return: A single float value that represents the degree centrality of the graph.
    """

    centrality_for_nodes = calculate_degree_centrality_for_nodes(G)

    max_key = max(centrality_for_nodes, key=centrality_for_nodes.get)
    max_value = centrality_for_nodes[max_key]

    up = 0

    for k, v in centrality_for_nodes.items():
        up += abs(max_value - v)

    n = len(centrality_for_nodes.items())
    down = n - 2

    if down >= 0:
        return 0

    centrality_for_graph = up / down

    # print(centrality_for_nodes)
    # print (max_key)
    # print (centrality_for_nodes[max_key])
    # print(centrality_for_graph)

    return centrality_for_graph

def calculate_closeness_centrality_for_nodes(G):
    """
    Calculates and returns the closeness centrality of the nodes.

    :param G: NetworkX.Graph
    :return: Dictionary where key is the index of each node, and value is the degree centrality of the i_th node
    """

    return nx.closeness_centrality(G)

def calculate_closeness_centrality_for_graph(G):
    """
    Calculates and returns the closeness centrality of the graph.

    :param G: NetworkX.Graph
    :return: A single float value that represents the closeness centrality of the graph.
    """

    # centrality_for_nodes = clustering_helper.calculateclosenesscentrality(G)
    centrality_for_nodes = calculate_closeness_centrality_for_nodes(G)

    max_key = max(centrality_for_nodes, key=centrality_for_nodes.get)
    max_value = centrality_for_nodes[max_key]

    up = 0

    for k, v in centrality_for_nodes.items():
        up += abs(max_value - v)

    n = len(centrality_for_nodes.items())
    down = ((n - 1) * (n - 2)) / (2 * n - 3)

    centrality_for_graph = up / down

    # print(centrality_for_nodes)
    # print (max_key)
    # print (centrality_for_nodes[max_key])
    # print(centrality_for_graph)

    return centrality_for_graph

def calculate_betweenness_centrality_for_nodes(G):
    """
    Calculates and returns the betweenness centralities for each node in the graph.

    :param G: NetworkX.Graph
    :return: Dictionary where key is the index of each node, and value is the betweenness centrality of the i_th node
    """

    return nx.betweenness_centrality(G)

def calculate_betweenness_centrality_for_graph(G):
    """
    Calculates and returns the betweenness centrality of the graph.

    :param G: NetworkX.Graph
    :return: A single float value that represents the betweenness centrality of the graph.
    """

    centrality_for_nodes = calculate_betweenness_centrality_for_nodes(G)

    max_key = max(centrality_for_nodes, key=centrality_for_nodes.get)
    max_value = centrality_for_nodes[max_key]

    up = 0

    for k, v in centrality_for_nodes.items():
        up += abs(max_value - v)

    n = len(centrality_for_nodes.items())
    down = (n - 1)

    centrality_for_graph = up / down

    # print(centrality_for_nodes)
    # print (max_key)
    # print (centrality_for_nodes[max_key])
    # print(centrality_for_graph)

    return centrality_for_graph

def calculate_hoede_bakker_index_get_group_decision(I, B, gd):
    """
    Calculates and returns the group decision of I.
    This is meant to be a private helper function.

    Example:
    inclination_vector = [0, 1, 1, 1]
    influence_function = "function" # B
    decision_vector = [0, 0, 0, 0]
    group_decision_function = "function -> return 1 or 0" # GD


    :param G: An array of [+1, -1]. Inclination Vector.
    :param B: Influnece Function.
    :param gd: Group Decision Function.
    :return: A single value of +1 or -1 that represents the group decision value.
    """

    return gd(B(I))

def calculate_generalised_hoede_bakker_index(n, k, B, gd):
    """
    Calculates and returns the Generalized Hoede-Bakker Index of a group of size N for Node k.

    :param n: The size of the group.
    :param k: The index of the node to get the hoede-bakker index for.
    :param B: Influence Function.
    :param gd: Group Decision Function.
    :return: A single value of +1 or -1 that represents the group decision value.
    """

    # If the size of group is lower than 1, always return 1.
    if n <= 1:
        return 1

    up = 0
    down = math.pow(2, n)

    for I in list(itertools.product([-1, 1], repeat=n)):
        gd_Bi = calculate_hoede_bakker_index_get_group_decision(I, B, gd)
        up += I[k] * gd_Bi

    return up/down
