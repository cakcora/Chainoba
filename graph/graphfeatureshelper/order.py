'''
Total number of nodes in the graph (graph order):
n = |V|
'''
import networkx as nx


def calculate(network):
    try:
        n = network.order()
    except:
        n = 0
    return n
