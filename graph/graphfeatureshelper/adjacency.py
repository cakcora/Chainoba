def _build_adjacency_dict(nxobj) :#-> Dict[Node, Set[Node]]:
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
