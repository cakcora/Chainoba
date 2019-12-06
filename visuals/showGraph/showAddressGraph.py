import json
from pyvis.network import Network
import os


class ShowAddressGraph:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open(os.path.join(os.path.dirname(__file__), 'layouts', 'undirected_layout.json')) as f:
            self.options = json.load(f)

    def show_graph(self):
        dir_output = "output"
        if not os.path.exists(dir_output):
            os.makedirs("output")
        self.graph.show("output/address_graph.html")

    def add_address_node(self, inputs, outputs, amounts):
        input_edge = zip(inputs, outputs, amounts)
        for i in input_edge:
            inputs = i[0]
            outputs = i[1]
            weight = i[2]
            self.graph.add_node(inputs)
            self.graph.add_node(outputs)
            self.graph.add_edge(inputs, outputs, value=weight, title=weight)
        self.graph.options = self.options
