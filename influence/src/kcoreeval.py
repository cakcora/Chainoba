from influence.generator import generate_bitcoin_graph_from_edgelist
from influence.kcore import KCore

# from graph.getGraph.ethereumGraph.getAPIData import getEthereumgraph
from graph.getGraph.getAPIData import getGraph
import networkx as nx

graph1 = KCore(generate_bitcoin_graph_from_edgelist())

inputs = ["a2", "a3"]
outputs = ["a4", "a2"]
amount = [5, 1]

graph1.generate_graph(inputs, outputs, amount)