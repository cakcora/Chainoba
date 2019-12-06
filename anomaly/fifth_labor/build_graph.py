# networkx version 2.4

import networkx as nx


def get_loop(graph):
    """
    Find loops in a graph
    :param graph:
    :return: list() with nodes in the loop
    """
    try:
        if nx.is_directed(graph):
            # if the graph is directed acyclic graph then orientation of the edges should be ignored to find the cycle
            if nx.is_directed_acyclic_graph(graph) == True:
                return list(nx.find_cycle(graph, orientation='ignore'))
            else:
                return list(nx.find_cycle(graph, orientation='original'))
    # if no cycle is found the function throws an Exception
    # So, return a list with zero nodes
    except Exception as e:
        return list()


def get_split_nodes(graph, output_address_threshold):
    """
    Find the transaction nodes with one input edge and output edges more than the threshold
    :param graph:
    :param output_address_threshold:
    :return: list() with transaction split nodes
    """
    split_node_list = list()
    for n in graph.nodes():
        if len(n) > 34:  # if the node is a transaction
            n_in_degree = graph.in_degree(n)
            n_out_degree = graph.out_degree(n)
            n_degree = graph.degree(n)
            assert n_in_degree + n_out_degree == n_degree
            if n_out_degree > output_address_threshold:
                split_node_list.append((n, n_in_degree, n_out_degree, n_degree))

    return split_node_list


def build_graph(edge_list_df):
    """
    Build the graph using networkx library from a given edge_list dataframe object
    :param edge_list_df:
    :return: the Graph object
    """
    graph = nx.from_pandas_edgelist(edge_list_df, edge_attr=True, create_using=nx.MultiDiGraph())

    return graph
