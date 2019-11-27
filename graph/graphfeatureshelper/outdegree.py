def indegree(NxObj)->list:
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
