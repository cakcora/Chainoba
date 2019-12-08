from influence.generator import generate_undirected_graph
from influence.generator import generate_bitcoin_graph_from_edgelist
from visuals.show_graph.show_address_graph import address_graph

from influence.kcore import KCore

from graph.getGraph.ethereumGraph.getAPIData import getEthereumgraph
from graph.getGraph.getAPIData import getGraph

import matplotlib.pyplot as plt
import random
import networkx as nx

# G = getGraph(9, 2, 2009, 1, 'ADDRESS')[1]

G = generate_bitcoin_graph_from_edgelist()

g1 = KCore(G)

g1.make_graph()

# H = g1.max_k_core_graph()
# pos = nx.spring_layout(H)
# nx.draw(H, pos, node_size=300, weight=.1)
# plt.show()

