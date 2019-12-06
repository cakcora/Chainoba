import visuals.showGraph.showAddressGraph as AG
import visuals.showGraph.showTransactionGraph as TG
import visuals.showGraph.showPath as P
import visuals.showGraph.showCluster as SC
import visuals.showGraph.showCompositeGraph as CG

def main():
    g1 = AG.ShowAddressGraph()
    # the fist list, represents input addresses the second is output addresses and the last list represents the corresponding bitcoin amount
    # transferred. address a1 has sent 1 bitcoin to a1. a2 has sent 1 bitcoin to a1
    g1.add_address_node(["a1", "a2", "a3", "a4"], ["a1", "a1", "a5", "a3"], [1, 1, 1, 2])
    g1.add_address_node(["a4", "a5", "a3", "a6"], ["a4", "a1", "a5", "a3"], [1, 3, 1, 2])
    g1.add_address_node(["a1"], ["a3"], [1, 1, 1, 2])
    g1.add_address_node(["a9"], ["a19"], [1, 1, 1, 2])
    g1.add_address_node(["a1", "a5", "a3", "a6"], ["a2", "a6", "a4", "a7"], [1, 3, 1, 2])
    inputs = ["a7", "a8", "a9", "a10"]
    output = ["a11", "a12", "a13", "a14"]
    amount = [1, 3, 1, 2]
    g1.add_address_node(inputs, output, amount)
    g1.show_graph()

    g2 = TG.ShowTransactionGraph()
    g2.add_transaction(["T1", "T2", "T4", "T3"], ["T3", "T6", "T2", "T2"], [1, 3, 2, 2], [2, 5, 4, 4], [2, 2, 5, 2])
    g2.add_transaction(["T5", "T7", "T9", "T10"], ["T6", "T6", "T11", "T12"], [1, 1, 2, 2], [2, 2, 4, 4], [3, 2, 5, 2])
    g2.show_graph()

    g3 = P.ShowPath()
    path = ["a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10"]
    amount = [19, 18, 18, 18, 17, 16, 16, 19, 20]
    g3.add_path(path, amount)
    g3.show_graph()

    g4 = SC.ShowCluster()
    input = ["a1", "a2", "a3", "a4", "a21", "a22", "a23", "a24", "a11", "a12", "a13", "a14"]
    cluster_input = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
    output = ["a220", "a23", "a240", "a110", "a120", "a13", "a140", "a1", "a20", "a30", "a4", "a210"]
    amount = [1, 2, 3, 1, 2, 3, 1, 3, 1, 2, 1]
    g4.add_address_graph(input, output, amount)
    g4.cluster_addresses(["a1", "a2", "a3", "a4", "a13"], [2, 2, 1, 1, 1])
    g4.cluster_addresses(input, cluster_input)
    g4.show_graph()

    g5 = CG.ShowCompositeGraph()

    # call add_composite_node(nodes that are sending transactions ,amount of bitcoin corresponding nodes, output addresses,
    # the amount each node recieve, time )
    # for time you dont necessarily need to add the exact time just add natural numbers. the graph is represented based on
    # the order of numbers from left to right

    # address a2 and a3 have send 200 and 400 bitcoins to address a5 a6 a6 each one has received 300,100,100 bitcoins
    g5.add_composite_nodes(["a2", "a3"], [200, 400], ["a5", "a6", "a7"], [300, 100, 100], 1)
    g5.add_composite_nodes(["a6", "a7"], [10, 400], ["a12", "a13"], [400, 10], 2)
    g5.add_composite_nodes(["a12", "a15"], [10, 400], ["a16"], [410], 3)
    g5.add_composite_nodes(["a2", "a15"], [10, 400], ["a2"], [410], 3)
    g5.add_composite_nodes(["a2", "a12"], [10, 400], ["a2"], [410], 4)
    g5.add_composite_nodes(["a2", "a1"], [10, 400], ["a2"], [410], 5)
    g5.add_composite_nodes(["a2", "a15"], [10, 400], ["a2"], [410], 6)

    g5.show_graph()

if __name__ == "__main__":
    main()





