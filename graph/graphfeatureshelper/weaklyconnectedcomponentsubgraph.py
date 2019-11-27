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
