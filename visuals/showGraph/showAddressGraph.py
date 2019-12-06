import json
from pyvis.network import Network
import os

class ShowAddressGraph:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open('layouts/address_graph_layout.json') as f:
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


def main():
    graph2 = ShowAddressGraph()

    # the fist list, represents input addresses the second is output addresses and the last list represents the corresponding bitcoin amount
    # transferred. address a1 has sent 1 bitcoin to a1. a2 has sent 1 bitcoin to a1

    graph2.add_address_node(["a1", "a2", "a3", "a4"], ["a1", "a1", "a5", "a3"], [1, 1, 1, 2])
    graph2.add_address_node(["a4", "a5", "a3", "a6"], ["a4", "a1", "a5", "a3"], [1, 3, 1, 2])
    graph2.add_address_node(["a1"], ["a3"], [1, 1, 1, 2])
    graph2.add_address_node(["a9"], ["a19"], [1, 1, 1, 2])
    graph2.add_address_node(["a1", "a5", "a3", "a6"], ["a2", "a6", "a4", "a7"], [1, 3, 1, 2])
    input = ["a7", "a8", "a9", "a10"]
    output = ["a11", "a12", "a13", "a14"]
    amount = [1, 3, 1, 2]
    graph2.add_address_node(input, output, amount)
    graph2.show_graph()


if __name__ == "__main__":
    main()
