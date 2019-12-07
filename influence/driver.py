from graph.getGraph.getAPIData import getGraph

import numpy as np
import matplotlib.pyplot as plt
import os
import math
import random
import pandas as pd
import networkx as nx

# The functions written below will provide any external team access to influence teams implementation.

"""
 k-core decomposition | Dilawer | Requires Etherium Data  ---
 Implementation of graph insertion is built on top of the subcore algorithm. These funcitons work together
 to generate a graph from Etherium data, The insertion of nodes is done incrementally, while maintaining
 k-core decomposition.
"""

# Get k-core subgraph for a given graph 'G' and of specified coreness 'k'
def get_k_cores(G, k):
    return nx.k_core(G, k)

# Maximum k-core subgraph for a given graph 'G'
def max_k_core_graph(G):
    return nx.k_core(G)

# Get the maximum K value for a given vertex
def get_max_k_value(G, vertex):
    return G.number_of_edges(vertex)

# Import the ethereum graph from 'graph' team.
def generate_undirected_graph():

    G = nx.Graph()

    G.add_nodes_from([i+1 for i in range(100)])

    for i in range(500):
        first_vertex = random.choice(list(G.nodes()))
        sec_vertex = random.choice(list(G.nodes()))
        if (first_vertex != sec_vertex):
            if (not G.has_edge(first_vertex, sec_vertex)):
                G.add_edge(first_vertex, sec_vertex)
    return G