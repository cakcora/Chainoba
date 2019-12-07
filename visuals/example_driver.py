from visuals.show_graph import (ShowAddressGraph, ShowTransactionGraph, ShowPath, ShowCluster, ShowCompositeGraph)


def main():

    # An object of a cluster graph
    g4 = ShowCluster()
    # Input addresses
    inputs = ["a1", "a2", "a3", "a4", "a21", "a22", "a23", "a24", "a11", "a12", "a13", "a14"]
    # Clusters corresponding to each input addresses
    cluster_inputs = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
    # Output addresses
    outputs = ["a220", "a23", "a240", "a110", "a120", "a13", "a140", "a1", "a20", "a30", "a4", "a210"]
    # Amount each input address has sent to the corresponding output address
    amount = [1, 2, 3, 1, 2, 3, 1, 3, 1, 2, 1]
    # Creating nodes
    g4.add_node(inputs, outputs, amount)
    # Assigning addresses ["a1", "a2", "a3", "a4", "a13"] to clusters [2, 2, 1, 1, 1]
    g4.cluster_addresses(["a1", "a2", "a3", "a4", "a13"], [2, 2, 1, 1, 1])
    # Clustering input addresses
    g4.cluster_addresses(inputs, cluster_inputs)
    g4.show_graph()

    # An object of a composite graph
    g5 = ShowCompositeGraph()
    # At time t = 1 addresses a2 and a3 send 200 and 400 bitcoins to addresses a5,a6 and, a7
    # and they receiver300, 100 and, 100 bitcoins in that order
    g5.add_node(["a2", "a3"], [200, 400], ["a5", "a6", "a7"], [300, 100, 100], 1)
    # At time t=2 addresses a6 and a7 send 10 and 400 bitcoins to addresses a12 and a 13 and
    # each receive 400 and 10 bitcoins
    g5.add_node(["a6", "a7"], [10, 400], ["a12", "a13"], [400, 10], 2)
    # Showing the result in a browser
    g5.show_graph()

    # An object of address graph
    g1 = ShowAddressGraph()
    inputs = ["a7", "a8", "a9", "a10"]
    outputs = ["a11", "a12", "a13", "a14"]
    amount = [1, 3, 1, 2]
    g1.add_node(inputs, outputs, amount)
    g1.show_graph()

    # An object of Transaction Graph
    g2 = ShowTransactionGraph()
    g2.add_node(["T1", "T2", "T4", "T3"], ["T3", "T6", "T2", "T2"], [1, 3, 2, 2], [2, 5, 4, 4], [2, 2, 5, 2])
    g2.add_node(["T5", "T7", "T9", "T10"], ["T6", "T6", "T11", "T12"], [1, 1, 2, 2], [2, 2, 4, 4], [3, 2, 5, 2])
    g2.show_graph()

    # An object of a Path graph
    g3 = ShowPath()
    path = ["a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10"]
    amount = [19, 18, 18, 18, 17, 16, 16, 19, 20]
    g3.add_path(path, amount)
    g3.show_graph()


if __name__ == "__main__":
    main()
