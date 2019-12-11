"""
        This class implements Behavior pattern clustering (BPC) of users with similar behavior patterns based on their spending
        patterns.
        The algorithm is based on the paper:
            Behavior pattern clustering in blockchain networks by Huang et. al (2017)
            DOI 10.1007/s11042-017-4396-4
"""
from copy import deepcopy
from itertools import combinations
from tslearn.metrics import dtw
import numpy as np

# The basis for choosing this value was not discussed in the paper.
# I chose 10 because of available compute power
MAX_ITER_NUM = 10


class Sequence:
    """
    A class used to represent a sequence of transaction amounts for a Blockchain user.
    A sequence is defined in the paper as the transaction amount change over time for a given node.

    Node-level representation:
        {
            user_address: "12higDjoCCNXSA95xZMWUdPvXNmkAduhWv"
            transaction_amounts: [54, 21, 69, 74]
        }

    Attributes
    ----------
    user_address: str
        a node in the address graph network
    transaction_amounts: list
        the extracted sequence of the user's transaction amount change over time

    Methods
    -------
    add_transaction_amount(amount)
        Appends amount to the list of transactions called transaction_amounts

    get_transactions()
        Getter. Returns transaction_amounts
    """

    def __init__(self, user_address):
        self.user_address = user_address
        self.transaction_amounts = []

    def add_transaction_amount(self, amount):
        num_trans = len(self.transaction_amounts)
        if num_trans == 0 or self.transaction_amounts[num_trans - 1] != amount:
            self.transaction_amounts.append(amount)

    def get_transactions(self):
        return self.transaction_amounts


########################### End of Class Sequence #################################

def generate_cluster_centers(k, sequences):
    """Utility function that uniformly generates a list of k centroids from a sorted list
    of sequences.

    Parameters
    ----------
    k: int
        Number of clusters (hence centroids) to generate
    sequences: list
        A list of sequences. Note: Assumes sequences is sorted. (e.g. [[0], [0, 1], [0, 3]] )

    Returns
    -------
    cluster_centroids: list
        list of centroids of length k. (e.g) [[0], [0, 3]] where k = 2
    """
    cluster_centroids = np.random.choice(sequences, k, replace=False).tolist()
    return cluster_centroids


def unique_items_count(list_):
    """Utility function that computes and returns the number of unique items in a list as well as
    those unite items

    Parameters
    ----------
    list_: list
        A given list of items

    Returns
    -------
    (len_unique_items, unique_items) : tuple
        len_unique_items: int
            count of unique items
        unique_items: list
            list of unique items
    """
    unique_items = []
    for item in list_:
        if item not in unique_items:
            unique_items.append(item)
    return len(unique_items), unique_items


def assign_cluster(list_centroids, seq):
    """Returns the label of a given sequence.

    Using the Dynamic Time Warping (DTW) similarity measure, it compares sequence similarities
    between  each centroid and the given sequence. The centroid with the least DTW distance is
    returned as the cluster label.

    Parameters
    ----------
    list_centroids: list of lists (e.g. [[0], [0, 1]] )
        sequences which have been selected as centroids of the dataset
    seq: list (e.g. [0, 1] )
        The given sequence
    """
    dtw_distances = np.zeros(len(list_centroids))
    for i, centroid in enumerate(list_centroids):
        dtw_distances[i] = dtw(centroid, seq)

    ordered_labels_by_dtw_distances = [x for _, x in sorted(zip(dtw_distances, list_centroids))]

    return ordered_labels_by_dtw_distances[0]



def subset_check(a, b):
    """Utility function that checks that all contents of a are in b.

        Parameters
        ----------
        a: list
            list of items
        b: list
            list of items

        Returns
        -------
        True/False: boolean
            true if all a is a subset of b, false otherwise
        """
    for item in a:
        if item not in b:
            return False
    return True


def bpc(G, k):
    """Performs Behavior pattern clustering (BPC) of users with similar behavior patterns based on their spending
        patterns.

        Parameters
        ----------
        :param G: Networkx MultiDiGraph object
            A transaction network where each edge represents: {fromUserAddress, toUserAddress, amountOfTransaction}
        :param k: int
            The number of clusters the user wants
        :return: (message, resultList): tuple
            * message: string
                "Success" - if successfully performed clustering
                "Fail: with error in the same message string" - if unsuccessful
            * resultList: list
                [[0], [0, 1], [0, 1, 2, 3, 0, 1, 0, 1, 2]] - cluster labels if successful (i.e.) message == "Success"
                None - if unsuccessful
                The cluster labels represent the transaction behaviour pattern of each node in the transaction graph (G)

        """
    edges = G.edges
    nodes = G.nodes

    # Extract transaction sequences for each node
    node_sequences = dict.fromkeys(nodes)  # {node0: S0, node1: S1, ..., nodeN, SN }

    for edge in edges:
        (source, target, amt) = edge

        if node_sequences[source] is None:
            node_sequences[source] = Sequence(source)
        if node_sequences[target] is None:
            node_sequences[target] = Sequence(target)

        node_sequences[source].add_transaction_amount(amt)
        node_sequences[target].add_transaction_amount(amt)

    sequences = []
    for s in node_sequences.values():
        sequences.append(s.get_transactions())
    # Sort the sequences with respect to their distances to their nearest neighbors
    sequences.sort()

    # Before clustering, ensure there are at least k distinct features in the dataset
    num_features, unique_items = unique_items_count(sequences)

    if num_features < k:
        return str("Fail: Number of unique features: {} < k: {}".format(num_features, k)), None

    # Clusterize!
    # Pick k centroids from uniform distribution
    cluster_centroids = generate_cluster_centers(k, unique_items)

    # Cluster labels look like this: ( [[0], [0, 1], [0, 1, 2, 3, 0, 1, 0, 1, 2]] ) for 3 labels
    cluster_labels = []
    clusters = []
    iter_count = 0
    while iter_count < MAX_ITER_NUM:
        for i in range(len(sequences)):
            cluster_labels.append(assign_cluster(cluster_centroids, sequences[i]))

        # For keeping track of previous cluster centroid values after update
        cluster_centroids_prev = deepcopy(cluster_centroids)

        # For each new cluster, select a centroid that minimizes the distances
        # TODO: was unable to implement this due to time constraint. Used random combination instead.
        centroid_combinations = list(combinations(unique_items, k))
        cluster_centroids.clear()

        index = int(np.random.uniform(high=len(centroid_combinations)))
        cluster_centroids = centroid_combinations[index]
        cluster_centroids = [x for x in cluster_centroids]
        cluster_labels.clear()
        for i in range(len(sequences)):
            cluster_labels.append(assign_cluster(cluster_centroids, sequences[i]))

        if subset_check(cluster_centroids, cluster_centroids_prev) and \
                subset_check(cluster_centroids_prev, cluster_centroids) and \
                len(cluster_centroids) == len(cluster_centroids_prev):
            break

        iter_count += 1
    print(cluster_labels)
    return "Success", cluster_labels
