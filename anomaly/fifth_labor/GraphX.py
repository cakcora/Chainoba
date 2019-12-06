# networkx version 2.4

import networkx as nx


class GraphX:
    """
        This class build a Multigraph using the networkx library from the edge list provided
        Find split nodes
        Find loop in the built graph

        Attributes:

            __edge_list: ransomware address type and address hash,
            __graph: the graph object


        Methods:
            get_loop() : GET loop nodes from the graph
            get_split_nodes() : Find the transaction nodes with one input edge and output edges more than the threshold
            build_graph() : Build the graph using networkx library from the given edge_list dataframe object

    """

    def __init__(self, edge_list):
        """
        GraphX class Constructor
        :param edge_list:
        :type  edge_list DataFrame
        """
        self.__edge_list = edge_list
        self.__graph = None

    def get_loop(self):
        """
        GET loop nodes from the graph

        :return: list() with nodes in the loop
        """
        if self.__graph is None:
            print('You have to build the graph first')
            return
        try:
            if nx.is_directed(self.__graph):
                # if the graph is directed acyclic graph then orientation of the edges should be ignored to find the cycle
                if nx.is_directed_acyclic_graph(self.__graph) == True:
                    return list(nx.find_cycle(self.__graph, orientation='ignore'))
                else:
                    return list(nx.find_cycle(self.__graph, orientation='original'))
        # if no cycle is found the function throws an Exception
        # So, return a list with zero nodes
        except Exception as e:
            return list()

    def get_split_nodes(self, output_address_threshold):
        """
        Find the transaction nodes with one input edge and output edges more than the threshold

        :param output_address_threshold:
        :type output_address_threshold int
        :return: list() with transaction split nodes
        """
        if self.__graph is None:
            print('You have to build the graph first')
            return
        split_node_list = list()
        for n in self.__graph.nodes():
            if len(n) > 34:  # if the node is a transaction
                n_in_degree = self.__graph.in_degree(n)
                n_out_degree = self.__graph.out_degree(n)
                n_degree = self.__graph.degree(n)
                assert n_in_degree + n_out_degree == n_degree
                if n_out_degree > output_address_threshold:
                    split_node_list.append((n, n_in_degree, n_out_degree, n_degree))

        return split_node_list

    def build_graph(self):
        """
        Build the graph using networkx library from the given edge_list dataframe object

        :return: the Graph object
        """
        self.__graph = nx.from_pandas_edgelist(self.__edge_list, edge_attr=True, create_using=nx.MultiDiGraph())

        return self.__graph
