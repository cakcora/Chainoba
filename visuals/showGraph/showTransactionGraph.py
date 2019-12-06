from visuals.showGraph._show_graph import ShowGraphABC


class ShowTransactionGraph(ShowGraphABC):
    def __init__(self):
        super().__init__(ShowGraphABC.DIRECTED, "transaction")

    def add_node(self, inputs, outputs, in_time, out_time, amounts):
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
