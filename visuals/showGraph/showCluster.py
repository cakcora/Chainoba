import json
from pyvis.network import Network
import os
import random

class ShowCluster:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open('layouts\\cluster_layout.json') as f:
            self.composite_options = json.load(f)

    def show_graph(self):
        dirOutput = "output"
        if not os.path.exists(dirOutput):
            os.makedirs("output")
        self.graph.show("output\\cluster_gragh.html")

    def add_address_graph(self, input, output, amount):
        input_edge = zip(input, output, amount)
        for i in input_edge:
            input = i[0]
            output = i[1]
            weight = i[2]
            self.graph.add_node(input)
            self.graph.add_node(output)
            self.graph.add_edge(input, output, value=weight,title = weight)
        self.graph.options = self.composite_options

    def colors(self, n):
        ret = []
        r = int(random.random() * 256)
        g = int(random.random() * 256)
        b = int(random.random() * 256)
        step = 256 / n
        for i in range(n):
            r += step
            g += step
            b += step
            r = int(r) % 256
            g = int(g) % 256
            b = int(b) % 256
            ret.append((r, g, b))
        return ret

    def cluster_addresses(self, address, cluster):
        colors = self.colors(4)
        for i in self.graph.nodes:
            try:
                value = cluster[address.index(i["id"])]
                i["color"] = "rgb" + str(colors[value - 1])
            except Exception:
                pass

def main():

    graph2 = showCluster()
    input =["a1", "a2", "a3", "a4","a21", "a22", "a23", "a24","a11", "a12", "a13", "a14"]
    cluster_input = [1,2,3,1,2,3,1,2,3,1,2,3]
    output = [ "a220", "a23", "a240", "a110", "a120", "a13", "a140", "a1", "a20", "a30", "a4", "a210"]
    amount = [1,2,3,1,2,3,1,3,1,2,1]
    graph2.add_address_graph(input,output,amount)
    graph2.cluster_addresses(["a1","a2","a3","a4","a13"],[2,2,1,1,1])
    graph2.cluster_addresses(input,cluster_input)

    graph2.show_graph()

if __name__== "__main__":
    main()
