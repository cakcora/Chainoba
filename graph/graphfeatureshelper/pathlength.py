def pathlen(nxobj)->list:
    '''

    :param nxobj:
    :return: List of all_paris_shortest_path between every nodes
    '''
    try:
        if (nx.is_directed(nxobj))==True:
            return  'Success',list(nx.all_pairs_shortest_path_length(G))
    except Exception as e:
        return 'Fail',e
