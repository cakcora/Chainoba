from influence.generator import generate_undirected_graph
from influence.kcore import get_k_cores
from influence.kcore import max_k_core_graph
from graph.getGraph.getAPIData import getGraph

import matplotlib.pyplot as plt
import random
import networkx as nx

# message, G = getGraph(9, 2, 2009, 2, 'ADDRESS')

# Generate a random graph for testing functions
G = generate_undirected_graph()

print("hello world")

nx.write_edgelist(nx.path_graph(10), "test.edgelist")



nx.draw(G)
plt.show()