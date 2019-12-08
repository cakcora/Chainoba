import networkx as nx
from visuals.show_graph.show_address_graph import address_graph


class KCore:

    def __init__(self, graph):
        self.graph = graph

    # Get k-core sub-graph for a given graph 'G' and of specified coreness 'k'
    def get_k_cores(self, k, core):
        return nx.k_core(self.graph, k)

    def get_core_number(self):
        return nx.core_number(self.graph)

    # Maximum k-core sub-graph for a given graph 'G'
    def max_k_core_graph(self):
        return nx.k_core(self.graph)

    def get_graph(self):
        return self.graph

    def make_graph(self):

        graph2 = address_graph()

        # the fist list, represents input addresses the second is output addresses and the last list represents the corresponding bitcoin amount
        # transferred. address a1 has sent 1 bitcoin to a1. a2 has sent 1 bitcoin to a1

        graph2.add_address_node(["a1", "a2", "a3", "a4"], ["a1", "a1", "a5", "a3"], [1, 1, 1, 2])
        graph2.add_address_node(["a4", "a5", "a3", "a6"], ["a4", "a1", "a5", "a3"], [1, 3, 1, 2])
        graph2.add_address_node(["a1"], ["a3"], [1, 1, 1, 2])
        graph2.add_address_node(["a9"], ["a19"], [1, 1, 1, 2])
        graph2.add_address_node(["a1", "a5", "a3", "a6"], ["a2", "a6", "a4", "a7"], [1, 3, 1, 2])

        inputs = ["a7", "a8", "a9", "a10"]
        output = ["a11", "a12", "a13", "a14"]
        amount = [1, 3, 1, 2]

        graph2.add_address_node(inputs, output, amount)

        graph2.show_graph()

        # g = address_graph()
        # # Populate using loop?
        # g.add_address_node(1, 2, 3)
        # graph.show_graph()

