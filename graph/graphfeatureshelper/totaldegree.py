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
