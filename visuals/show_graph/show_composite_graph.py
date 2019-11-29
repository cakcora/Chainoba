import json
from pyvis.network import Network
import os


class composite_graph:

    def __init__(self):
        self.graph = Network(height="750px", width="100%", directed=True)

        with open('layouts\composite_graph_layout.json') as f:
            self.composite_options = json.load(f)


    def show_graph(self):
        dirOutput = "output"
        if not os.path.exists(dirOutput):
            os.makedirs("output")
        self.graph.show("output\composite_graph.html")

    def add_composite_nodes(self, input,amount_in, output,amount_out,time):

        level_input =time + time - 1
        level_trans = level_input + 1
        level_output = level_input + 2
        T = "T"+str(level_trans)
        self.graph.add_node(T, level=level_trans, shape="square", color ="rgb(28,163,236)")
        input_edge = zip(input, amount_in)

        for i in input_edge:
            input = i[0] + str(level_input)
            label = i[0]
            weight = i[1]
            self.graph.add_node(input, level=level_input, label =label)
            self.graph.add_edge(input, T, value = weight)

        output_edge = zip(output, amount_out)
        for j in output_edge:
            label = j[0]
            output = j[0] + str(level_output)
            weight = j[1]
            self.graph.add_node(output, level=level_output, label = label)
            self.graph.add_edge(T, output, value=weight, title = weight)

        self.graph.options = self.composite_options


    def show(self):
        self.show_graph()



'''
def main():

    graph2 = composite_graph()

    
    #call add_composite_node(nodes that are sending transactions ,amount of bitcoin corresponding nodes, output addresses, 
    #the amount each node recieve, time )
    #for time you dont necessarily need to add the exact time just add natural numbers. the graph is represented based on 
    #the order of numbers from left to right
 
    # address a2 and a3 have send 200 and 400 bitcoins to address a5 a6 a6 each one has received 300,100,100 bitcoins
    graph2.add_composite_nodes(["a2","a3"],[200,400],["a5","a6","a7"],[300,100,100],1)
    graph2.add_composite_nodes(["a6","a7"],[10,400],["a12","a13"],[400,10],2)
    graph2.add_composite_nodes(["a12","a15"],[10,400],["a16"],[410],3)
    graph2.add_composite_nodes(["a2","a15"],[10,400],["a2"],[410],3)
    graph2.add_composite_nodes(["a2","a12"],[10,400],["a2"],[410],4)
    graph2.add_composite_nodes(["a2","a1"],[10,400],["a2"],[410],5)
    graph2.add_composite_nodes(["a2","a15"],[10,400],["a2"],[410],6)

    graph2.show_graph()

if __name__== "__main__":
    main()
    '''