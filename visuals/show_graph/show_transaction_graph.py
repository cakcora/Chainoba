"""
Generating Transaction Graph based on method proposed by Akcora, C. G. et al.
Resource:
    Article: Blockchain: A Graph Primer
    Authors: Akcora, C. G., Gel, Y. R., & Kantarcioglu, M.
    source: https://arxiv.org/abs/1708.08749
"""
from visuals.show_graph._show_graph import ShowGraphABC


class ShowTransactionGraph(ShowGraphABC):
    """
    This class generates a Transaction Graph.
    """
    def __init__(self):
        """
        Initializing the visualizations based on superclass constructor.
        Creating a canvas and initializing overall layout of the visualization.
        """
        super().__init__(ShowGraphABC._DIRECTED, "transaction")

    def add_node(self, inputs, outputs, in_time, out_time, amounts):
        """
        Adds information of a transaction graph.
        :param inputs: Input transaction addresses that send bitcoin. Should be in form of a list data type.
        :param outputs: Output transaction addresses that receive bitcoin. Should be in form of a list data type.
        :param in_time: Time in which input transactions had happened. Should be in form of a list data type.
        :param out_time: Time in which output transactions had happened. Should be in form of a list data type.
        :param amounts: Amount of bitcoin which each input transaction had sent to an output transaction.
        :return:
        """
        # creating the corresponding tuples: (inputs[i], in_time[i], outputs[i], out_time[i], amounts[i])
        input_edge = zip(inputs, in_time, outputs, out_time, amounts)
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
