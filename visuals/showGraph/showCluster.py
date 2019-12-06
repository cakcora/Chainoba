import json
from pyvis.network import Network
import os
import random


class ShowCluster:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open('layouts/undirected_layout.json') as f:
            self.options = json.load(f)

    def show_graph(self):
        dir_output = "output"
        if not os.path.exists(dir_output):
            os.makedirs("output")
        self.graph.show("output/cluster_graph.html")

    def add_address_graph(self, inputs, outputs, amounts):
        input_edge = zip(inputs, outputs, amounts)
        for i in input_edge:
            inputs = i[0]
            outputs = i[1]
            weight = i[2]
            self.graph.add_node(inputs)
            self.graph.add_node(outputs)
            self.graph.add_edge(inputs, outputs, value=weight, title=weight)
        self.graph.options = self.options

    @staticmethod
    def rand_colors(n):
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
        num_clusters = max(cluster)
        colors = self.rand_colors(num_clusters)
        for i in self.graph.nodes:
            try:
                value = cluster[address.index(i["id"])]
                i["color"] = "rgb" + str(colors[value - 1])
            except Exception:
                pass

def main():

    graph2 = ShowCluster()
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
