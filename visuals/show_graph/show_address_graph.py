"""
Generating Address Graph based on method proposed by Akcora, C. G. et al.
Resource:
    Article: Blockchain: A Graph Primer
    Authors: Akcora, C. G., Gel, Y. R., & Kantarcioglu, M.
    source: https://arxiv.org/abs/1708.08749
"""
from visuals.show_graph._show_graph import ShowGraphABC


class ShowAddressGraph(ShowGraphABC):
    """
    This class generates an Address Graph.
    """
    def __init__(self):
        """
        Initializing the visualizations based on superclass constructor.
        Creating a canvas and initializing overall layout of the visualization.
        """
        super().__init__(ShowGraphABC._UNDIRECTED, "address")

    def add_node(self, inputs, outputs, amounts):
        """
        Adds information of an address graph.
        :param inputs: Input addresses that send bitcoin. Should be in form of a list data type.
        :param outputs: Output addresses that send bitcoin. Should be in form of a list data type.
        :param amounts: Amount each input address sends to its corresponding output address in the list of input
        and output. Should be in form of a list.
        :return:
        """
        # Creating the corresponding tuples: (input[i],output[i],amount[i])
        input_edge = zip(inputs, outputs, amounts)
        for i in input_edge:
            inputs = i[0]
            outputs = i[1]
            weight = i[2]
            self.graph.add_node(inputs)
            self.graph.add_node(outputs)
            self.graph.add_edge(inputs, outputs, value=weight, title=weight)
        self.graph.options = self.options
