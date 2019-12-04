from influence.generator import generate_undirected_graph
from influence.generator import  generate_bitcoin_graph_from_edgelist
from influence.kcore import get_k_cores
from influence.kcore import max_k_core_graph
from graph.getGraph.getAPIData import getGraph

import matplotlib.pyplot as plt
import random
import networkx as nx


# G = getGraph(9, 2, 2009, 10, 'ADDRESS')[1]

G = generate_bitcoin_graph_from_edgelist()



H = max_k_core_graph(G)


pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=3, weight=.1)
plt.show()

pos = nx.spring_layout(H,k=0.15,iterations=20)
nx.draw(H, pos)
plt.show()


print(nx.core_number(H))

