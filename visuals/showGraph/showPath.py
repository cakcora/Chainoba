import json
from pyvis.network import Network
import os


class ShowPath:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open('layouts/path_layout.json') as f:
            self.options = json.load(f)

    def show_graph(self):
        dir_output = "output"
        if not os.path.exists(dir_output):
            os.makedirs("output")
        self.graph.show("output/path_graph.html")

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


def main():
    graph2 = ShowPath()
    path = ["a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10"]
    amount = [19, 18, 18, 18, 17, 16, 16, 19, 20]
    graph2.add_path(path, amount)
    graph2.show_graph()


if __name__ == "__main__":
    main()
