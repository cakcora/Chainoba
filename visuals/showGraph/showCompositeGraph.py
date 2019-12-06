import json
from pyvis.network import Network
import os


class ShowCompositeGraph:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open('layouts/directed_layout.json') as f:
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


def main():
    graph2 = ShowCompositeGraph()

    # call add_composite_node(nodes that are sending transactions ,amount of bitcoin corresponding nodes, output addresses,
    # the amount each node recieve, time )
    # for time you dont necessarily need to add the exact time just add natural numbers. the graph is represented based on
    # the order of numbers from left to right

    # address a2 and a3 have send 200 and 400 bitcoins to address a5 a6 a6 each one has received 300,100,100 bitcoins
    graph2.add_composite_nodes(["a2", "a3"], [200, 400], ["a5", "a6", "a7"], [300, 100, 100], 1)
    graph2.add_composite_nodes(["a6", "a7"], [10, 400], ["a12", "a13"], [400, 10], 2)
    graph2.add_composite_nodes(["a12", "a15"], [10, 400], ["a16"], [410], 3)
    graph2.add_composite_nodes(["a2", "a15"], [10, 400], ["a2"], [410], 3)
    graph2.add_composite_nodes(["a2", "a12"], [10, 400], ["a2"], [410], 4)
    graph2.add_composite_nodes(["a2", "a1"], [10, 400], ["a2"], [410], 5)
    graph2.add_composite_nodes(["a2", "a15"], [10, 400], ["a2"], [410], 6)

    graph2.show_graph()


if __name__ == "__main__":
    main()
