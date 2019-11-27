def cyclelist(nxgraph)->list:
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
