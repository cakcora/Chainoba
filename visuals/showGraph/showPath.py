from visuals.showGraph._show_graph import ShowGraphABC


class ShowPath(ShowGraphABC):
    def __init__(self):
        super().__init__(ShowGraphABC.UNDIRECTED, "path")

    def add_path(self, inputs, amount):
        input_edge = zip(inputs[0:len(inputs) - 1], inputs[1:len(inputs)], amount)
        for i in input_edge:
            inputs = i[0]
            outputs = i[1]
            weights = i[2]
            self.graph.add_node(inputs)
            self.graph.add_node(outputs)
            self.graph.add_edge(inputs, outputs, value=weights, title=weights)
        self.graph.options = self.options
