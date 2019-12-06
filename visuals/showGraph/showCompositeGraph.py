import json
from pyvis.network import Network
import os


class ShowCompositeGraph:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open(os.path.join(os.path.dirname(__file__), 'layouts', 'directed_layout.json')) as f:
            self.options = json.load(f)

    def show_graph(self):
        dir_output = "output"
        if not os.path.exists(dir_output):
            os.makedirs("output")
        self.graph.show("output/composite_graph.html")

    def add_composite_nodes(self, inputs, amount_in, outputs, amount_out, time):
        level_input = time + time - 1
        level_trans = level_input + 1
        level_output = level_input + 2
        transaction_node = "T" + str(level_trans)
        self.graph.add_node(transaction_node, level=level_trans, shape="square", color="rgb(28,163,236)")
        input_edge = zip(inputs, amount_in)

        for i in input_edge:
            inputs = i[0] + str(level_input)
            label = i[0]
            weight = i[1]
            self.graph.add_node(inputs, level=level_input, label=label)
            self.graph.add_edge(inputs, transaction_node, value=weight)

        output_edge = zip(outputs, amount_out)
        for j in output_edge:
            label = j[0]
            outputs = j[0] + str(level_output)
            weight = j[1]
            self.graph.add_node(outputs, level=level_output, label=label)
            self.graph.add_edge(transaction_node, outputs, value=weight, title=weight)
        self.graph.options = self.options
