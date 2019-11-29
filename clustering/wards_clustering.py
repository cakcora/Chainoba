from clustering.levenshtein_distance import levenshtein_distance
from sklearn.cluster import AffinityPropagation

import numpy as np


def ward_method_clustering(nodes):
    """
    Performs agglomerative hierarchical clustering  of user or transaction addresses with similar behavior patterns.

    :param nodes: The nodes of the network graph
    :return: dict: A dictionary of addresses where keys are the cluster labels and values are members of the same
    cluster
    """

    result = []
    levenshtein_distances = -1 * np.array([[levenshtein_distance(w1, w2) for w1 in nodes] for w2 in nodes])
    affinity_propagation = AffinityPropagation(affinity="precomputed", damping=0.5)
    affinity_propagation.fit(levenshtein_distances)

    cluster_center_indices = affinity_propagation.cluster_centers_indices_
    unique_labels = np.unique(affinity_propagation.labels_)

    for cluster_id in unique_labels:
        cluster_list = []
        for index, node in enumerate(nodes):
            if index == cluster_center_indices[cluster_id]:
                exemplar = node
                list_of_names = np.nonzero(affinity_propagation.labels_ == cluster_id)
                for i in list_of_names[0]:
                    if index == i:
                        cluster_list.append(node)
                cluster = np.unique(cluster_list)
                # cluster_str = ", ".join(cluster)
        result[exemplar] = cluster

    return result
