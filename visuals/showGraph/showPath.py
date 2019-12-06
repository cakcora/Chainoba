import json
from pyvis.network import Network
import os


class ShowPath:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open(os.path.join(os.path.dirname(__file__), 'layouts', 'undirected_layout.json')) as f:
            self.options = json.load(f)

    def show_graph(self):
        self.graph.show("path_graph.html")

    def add_path(self, inputs, amount):
        input_edge = zip(inputs[0:len(inputs) - 1], inputs[1:len(inputs)], amount)
        for i in input_edge:
            inputs = i[0]
            outputs = i[1]
            weights = i[2]
            self.graph.add_node(inputs)
            self.graph.add_node(outputs)
            self.graph.add_edge(inputs, outputs, value=weights, title=weights)
        self.graph.options = self.options
