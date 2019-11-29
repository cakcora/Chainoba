import json
from pyvis.network import Network
import os

class show_path:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)

        with open('layouts\path_layout.json') as f:
            self.composite_options = json.load(f)


    def show_graph(self):
        dirOutput = "output"
        if not os.path.exists(dirOutput):
            os.makedirs("output")
        self.graph.show("output\path_graph.html")

    def add_path(self, input, amount):

        input_edge = zip(input[0:len(input)-1], input[1:len(input)],amount)

        for i in input_edge:
            input = i[0]
            output = i[1]
            weight = i[2]
            self.graph.add_node(input)
            self.graph.add_node(output)
            self.graph.add_edge(input, output, value = weight, title = weight)

        self.graph.options = self.composite_options


    def show(self):
        self.show_graph()

'''
def main():
    graph2 = show_path()
    path = ["a2","a3","a4","a5","a6","a7", "a8","a9","a10"]
    amount = [19,18,18,18,17,16,16,19,20]
    graph2.add_path(path, amount)
    graph2.show_graph()

if __name__== "__main__":
    main()
'''