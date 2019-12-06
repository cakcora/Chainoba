import json
from pyvis.network import Network
import os


class ShowTransactionGraph:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open(os.path.join(os.path.dirname(__file__), 'layouts', 'directed_layout.json')) as f:
            self.options = json.load(f)

    def show_graph(self):
        dir_output = "output"
        if not os.path.exists(dir_output):
            os.makedirs("output")
        self.graph.show("output/transaction_graph.html")

    def add_transaction(self, inputs, outputs, in_time, out_time, amounts):
        input_edge = zip(inputs, in_time, outputs, out_time, amounts)
        for i in input_edge:
            input_node = i[0]
            time_in = i[1]
            output_node = i[2]
            time_out = i[3]
            weights = i[4]
            self.graph.add_node(input_node, level=time_in, shape="square")
            self.graph.add_node(output_node, level=time_out, shape="square")
            self.graph.add_edge(input_node, output_node, value=weights, title=weights)
        self.graph.options = self.options
