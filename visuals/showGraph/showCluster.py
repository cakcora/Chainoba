from visuals.showGraph._show_graph import ShowGraphABC
import random


class ShowCluster(ShowGraphABC):
    def __init__(self):
        super().__init__(ShowGraphABC.UNDIRECTED, "cluster")

    def add_node(self, inputs, outputs, amounts):
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
        num_clusters = max(cluster)
        colors = rand_colors(num_clusters)
        for i in self.graph.nodes:
            try:
                value = cluster[address.index(i["id"])]
                i["color"] = "rgb" + str(colors[value - 1])
            except Exception:
                pass


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
