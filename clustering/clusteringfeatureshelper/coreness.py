'''
Return the core number for each vertex.

A k-core is a maximal subgraph that contains nodes of degree k or more.

The core number of a node is the largest value k of a k-core containing that node.
'''

import networkx as nx


def calculate(net):
    if net.number_of_selfloops() > 0: 
        try:
            net.remove_edges_from(net.selfloop_edges())
        except: 
            return 0
    try:
        c = nx.core_number(net).values()
    except:
        return 0

    if len(c) == 0:
        return 0
    else:
        return round(sum(c)/len(c),7)




