import networkx as nx

# Get k-core subgraph for a given graph 'G' and of specified coreness 'k'
def get_k_cores(G, k):
    return nx.k_core(G, k)

# Maximum k-core subgraph for a given graph 'G'
def max_k_core_graph(G):
    return nx.k_core(G)