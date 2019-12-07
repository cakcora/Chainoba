"""
Generating an Address Graph and grouping the address nodes which belong to the same class.
Resource:
    Article: Blockchain: A Graph Primer
    Authors: Akcora, C. G., Gel, Y. R., & Kantarcioglu, M.
    source: https://arxiv.org/abs/1708.08749
"""
from visuals.show_graph._show_graph import ShowGraphABC
import random


class ShowCluster(ShowGraphABC):
    """
    This class generates an Address Graphs and groups the addresses.
    """
    def __init__(self):
        """
        Initializing the visualizations based on superclass constructor.
        Creating a canvas and initializing overall layout of the visualization.
        """
        super().__init__(ShowGraphABC._UNDIRECTED, "cluster")

    def add_node(self, inputs, outputs, amounts):
        """
        Adds information of an address graph
        :param inputs: Input addresses that send bitcoin
        :param outputs: Output addresses that receive bitcoin.
        :param amounts: Amount of bitcoin each input address sends to corresponding
         output address in the input and output list.
        :return:
        """
        # creating the corresponding tuples: (input[i],output[i],amount[i])
        input_edge = zip(inputs, outputs, amounts)
        for i in input_edge:
            inputs = i[0]
            outputs = i[1]
            weight = i[2]
            self.graph.add_node(inputs)
            self.graph.add_node(outputs)
            self.graph.add_edge(inputs, outputs, value=weight, title=weight)
        self.graph.options = self.options

    def cluster_addresses(self, address, cluster):
        """
        Gets addresses and clusters which each address belongs to it.
        :param address: Addresses in the address graph.
        :param cluster: The cluster that each corresponding address belongs to it.
        :return:
        """
        # The number of colors that needs to be generated
        num_clusters = max(cluster)
        colors = rand_colors(num_clusters)
        # Search in all nodes and assign a color to each node in each cluster
        for i in self.graph.nodes:
            try:
                value = cluster[address.index(i["id"])]
                i["color"] = "rgb" + str(colors[value - 1])
            except Exception:
                pass


def rand_colors(n):
    """
    Generating random colors.
    :param n: Number of colors that needs to be generated.
    :return: A list of size n with n different colors generated randomly.
    """
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
