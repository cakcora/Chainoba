'''
Total number of edges n the graph (graph size):
m = |E|
'''
import networkx as nx


def calculate(network):
    try:
        n = network.size()
    except:
        n = 0
    return n
