import random
import networkx as nx

# Import the ethereum graph from 'graph' team.
def generate_undirected_graph():
    """
    This is a randomly generated graph we can use for quick tests.
    """

    G = nx.Graph()
    G.add_nodes_from([i+1 for i in range(100)])

    for i in range(500):
        first_vertex = random.choice(list(G.nodes()))
        sec_vertex = random.choice(list(G.nodes()))
        if (first_vertex != sec_vertex):
            if (not G.has_edge(first_vertex, sec_vertex)):
                G.add_edge(first_vertex, sec_vertex)
    return G

def generate_undirected_graph_from_citeseer():
    """
    The graph data is collected from citeseer, and modified to meet the expected format of NetworkX library.
    """
    G = nx.read_edgelist("../dataset/citeseer/citeseer.edges.nx_edgelist")
    return G

def generate_bitcoin_graph_from_edgelist():
    """
    The graph data is collected from our server to show that the functions in this module are compatible with Bitcoin Data.
    """
    G = nx.Graph()
    G = nx.read_edgelist("../dataset/bitcoin.edgelist")
    return G

