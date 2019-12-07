"""
Generating Composite Graph based on method proposed by Akcora, C. G. et al.
Resource:
    Article: Blockchain: A Graph Primer
    Authors: Akcora, C. G., Gel, Y. R., & Kantarcioglu, M.
    source: https://arxiv.org/abs/1708.08749
"""
from visuals.showGraph._show_graph import ShowGraphABC


class ShowCompositeGraph(ShowGraphABC):
    """
    This class generates a Composite Graph.
    """
    def __init__(self):
        """
        Initializing the visualizations based on superclass constructor.
        Creating a canvas and initializing overall layout of the visualization.
        """
        super().__init__(ShowGraphABC._DIRECTED, "composite")

    def add_node(self, inputs, amount_in, outputs, amount_out, time):
        """
        Adding information of a composite graph.
        :param inputs: Input addresses that send bitcoin. Should be in form of a list data type.
        :param amount_in: Amount of bitcoin which each input address had spent.
        :param outputs: Output addresses that receive bitcoin. Should be in form of a list data type.
        :param amount_out: Amount of bitcoin which each output address had received.
        :param time: Time when a transactions had happened. Should be in form of a list data type.
        :return:
        """
        level_input = time + time - 1
        level_trans = level_input + 1
        level_output = level_input + 2
        transaction_node = "T" + str(level_trans)
        self.graph.add_node(transaction_node, level=level_trans, shape="square", color="rgb(28,163,236)")

        # Creating the corresponding tuples: (inputs[i], amount_in[i])
        input_edge = zip(inputs, amount_in)
        for i in input_edge:
            inputs = i[0] + str(level_input)
            label = i[0]
            weight = i[1]
            self.graph.add_node(inputs, level=level_input, label=label)
            self.graph.add_edge(inputs, transaction_node, value=weight)

        # Creating the corresponding tuples: (outputs[i], amounts_out[i])
        output_edge = zip(outputs, amount_out)
        for j in output_edge:
            label = j[0]
            outputs = j[0] + str(level_output)
            weight = j[1]
            self.graph.add_node(outputs, level=level_output, label=label)
            self.graph.add_edge(transaction_node, outputs, value=weight, title=weight)
        self.graph.options = self.options
