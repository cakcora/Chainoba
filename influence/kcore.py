import networkx as nx
from visuals.show_graph.show_address_graph import address_graph

class KCore:

    def __init__(self, graph):
        self.graph = graph

    # Return the k-core of this graph
    #   k - [int, optional] The order of the core. If not specified return the main core.
    #   core_number : [dictionary, optional] Precomputed core numbers for the graph G.
    def get_k_cores(self, k, core):
        return nx.k_core(self.graph, k)

    # This function will return a dictionary keyed by node to the core number.
    def get_core_number(self):
        return nx.core_number(self.graph)

    # Maximum k-core sub-graph for this graph
    def max_k_core_graph(self):
        return nx.k_core(self.graph)

    # Get the graph associated with the object instance
    def get_graph(self):
        return self.graph

    # Generate view for a given graph
    #     - Provide list of all input addresses
    #     - Provide list of all output addresses
    #     - Provide list of all amounts between input and output addresses
    def generate_graph(self, inputs, outputs, amount):
        graph = address_graph()
        graph.add_address_node(inputs, outputs, amount)
        graph.show_graph()