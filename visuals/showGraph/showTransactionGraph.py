import json
from pyvis.network import Network
import os

class ShowTransactionGraph:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open('layouts/transaction_graph_layout.json') as f:
            self.options = json.load(f)

    def show_graph(self):
        dir_output = "output"
        if not os.path.exists(dir_output):
            os.makedirs("output")
        self.graph.show("output/transaction_graph.html")

    def add_transaction(self,input, output, in_time, out_time, amount):
        input_edge = zip(input, in_time, output, out_time, amount)
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


def main():

    graph2 = ShowTransactionGraph()
    graph2.add_transaction(["T1","T2","T4","T3"],["T3","T6","T2","T2"], [1,3,2,2], [2,5,4,4], [2,2,5,2])
    graph2.add_transaction(["T5", "T7", "T9", "T10"], ["T6", "T6", "T11", "T12"], [1, 1, 2, 2], [2, 2, 4, 4], [3, 2, 5, 2])
    graph2.show_graph()

if __name__== "__main__":
    main()
