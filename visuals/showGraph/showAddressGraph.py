from visuals.showGraph._show_graph import ShowGraphABC


class ShowAddressGraph(ShowGraphABC):
    def __init__(self):
        super().__init__(ShowGraphABC.UNDIRECTED, "address")

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
