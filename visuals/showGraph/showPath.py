"""
Generating Path Graph based on method proposed by Akcora, C. G. et al.
Resource:
    Article: Blockchain: A Graph Primer
    Authors: Akcora, C. G., Gel, Y. R., & Kantarcioglu, M.
source: https://arxiv.org/abs/1708.08749
"""
from visuals.showGraph._show_graph import ShowGraphABC


class ShowPath(ShowGraphABC):
    """
    This class generates a Path Graph.
    """
    def __init__(self):
        """
        Initializing the visualizations based on superclass constructor.
        Creating a canvas and initializing overall layout of the visualization.
        """
        super().__init__(ShowGraphABC._UNDIRECTED, "path")

    def add_path(self, addresses, amount):
        """
        Call this function to pass address nodes of a path.
        :param addresses: Address nodes that form a path. Should be in form of a list.
        :param amount: Amount of bitcoin that one address has sent to the second address in addresses list. Should be in form of a list.
        :return:
        """
        # creating the corresponding tuples: (inputs[i], amount[i])
        input_edge = zip(addresses[0:len(addresses) - 1], addresses[1:len(addresses)], amount)
        for i in input_edge:
            addresses = i[0]
            outputs = i[1]
            weights = i[2]
            self.graph.add_node(addresses)
            self.graph.add_node(outputs)
            self.graph.add_edge(addresses, outputs, value=weights, title=weights)
        self.graph.options = self.options
