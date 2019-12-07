import networkx as nx


def _build_adjacency_dict(network) :#-> Dict[Node, Set[Node]]:
    """
    Construct adjacency dict mapping node to a set of its neighbor nodes
    :param Nxobj:
    :return: dict
    """
    adj = defaultdict(set)
    for (node1, node2) in nxobj.edges():
        adj[node1].add(node2)
        adj[node2].add(node1)
    return dict(adj)



def calculateclique(network)->int:
    '''
    Return the clique number (size of the largest clique) for G.
    '''
    try:
        n = nx.graph_clique_number(network)
    except:
        n = 0
    return n


def calculatediameter(network):
    '''
    Return the diameter of the graph G.
    '''
    try:
        n = nx.diameter(network)
    except:
        return 0

    return round(n, 7)


def calculateedgeconnectivity(network):
    '''
    Returns the edge connectivity of the graph or digraph G.

    The edge connectivity is equal to the minimum number of edges that must be removed to disconnect G or render it trivial. If source and target nodes are provided, this function returns the local edge connectivity: the minimum number of edges that must be removed to break all paths from source to target in G.

    '''
    try:
        n = nx.edge_connectivity(network)
    except:
        n = 0
    return n


def cyclelist(network)->list:
    '''
    list(nx.find_cycle(nxgraph, orientation='ignore'))
    :param nxgraph:
    :return:list generator of subgraph objects
    '''
    try:
        if nx.is_directed(nxgraph):
            if nx.is_directed_acyclic_graph(nxgraph)==True:
                return "Success",list(nx.find_cycle(nxgraph,orientation='ignore'))
            else:
                return "Success",list(nx.find_cycle(nxgraph, orientation='original'))
    except Exception as e:
        return "Fail",e


def indegree(network)->list:
    '''
    returns list showing nodes with indegree
    :param NxObj:
    :return: list
    '''
    data = []
    for address in G.nodes:
        if len(address) != 64:
            degree = (address, G.in_degree(address))
            data.append(degree)
    return data


def calculatenodeconnectivity(network):
    '''
    Node connectivity is equal to the minimum number of nodes that must be removed to disconnect G or render it trivial. If source and target nodes are provided, this function returns the local node connectivity.

    Returns the average connectivity of a graph G.
    '''
    try:
        n = nx.average_node_connectivity(network)
    except:
        return 0
 
    return round(n, 7)


def calculateorder(network):
    '''
    Total number of nodes in the graph (graph order):
    n = |V|
    '''
    try:
        n = network.order()
    except:
        n = 0
    return n


def indegree(network)->list:
    '''
    returns list showing nodes with indegree
    :param NxObj:
    :return: list
    '''
    data = []
    for address in G.nodes:
        if len(address) != 64:
            degree = (address, G.in_degree(address))
            data.append(degree)
    return data


def pathlen(network)->list:
    '''

    :param nxobj:
    :return: List of all_paris_shortest_path between every nodes
    '''
    try:
        if (nx.is_directed(nxobj))==True:
            return  'Success',list(nx.all_pairs_shortest_path_length(G))
    except Exception as e:
        return 'Fail',e



def calculateradius(network):
    '''

    The radius is the minimum eccentricity.
    '''

    try:
        n = nx.radius(network)
    except:
        return 0
 
    return round(n, 7)



def calculatesize(network):
    '''
    Total number of edges n the graph (graph size):
    m = |E|
    '''
    try:
        n = network.size()
    except:
        n = 0
    return n


def totaldegree(Nxobj)->list:
    '''
    :param Nxobj:
    :return: list
    '''
    data=[]
    for address in G.nodes():
        if len(address)!=64:
            degree=(address,G.in_degree(address)+G.out_degree(address))
            data.append(degree)
    return data



def weakly_connected_component_subgraphs(G, copy=True)->nx.MultiDiGraph():
    """DEPRECATED: Use ``(G.subgraph(c) for c in weakly_connected_components(G))``

           Or ``(G.subgraph(c).copy() for c in weakly_connected_components(G))``
    """
    msg = "weakly_connected_component_subgraphs is deprecated and will be removed in 2.2" \
        "use (G.subgraph(c).copy() for c in weakly_connected_components(G))"
    if nx.is_directed(G):
        for c in nx.weakly_connected_components(G):
            if copy:
                yield G.subgraph(c).copy()
            else:
                yield G.subgraph(c)
    else:
        return 'Fail'
