import random
import networkx as nx

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