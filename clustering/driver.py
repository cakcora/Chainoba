
from clustering.behaviour_pattern_clustering import bpc

"""
This file will have all the functions related to clustering
- clustering
- clustering-classes
  - driver.py
"""
import clustering.src.silhouette_k_cluster


def load_data():
    """
    This function is going to load the data into a dataframe by calling the functions provided
    by the graph time
    :return: dataframe - please see src/silhouette_k_clustering for more detail
    """
    return clustering.src.silhouette_k_cluster.load_data()


def cluster():
    """
    Applies K means clustering algorithm and builds a scatter plot for visualization
    """
    df = clustering.src.silhouette_k_cluster.load_data()
    num_cluster = clustering.src.silhouette_k_cluster.find_optimal_num_cluster(df)
    data_frame = clustering.src.silhouette_k_cluster.data_pipeline(df)
    cl = clustering.src.silhouette_k_cluster.cluster(data_frame, num_cluster)
    tsne_plotter(cl, data_frame)


def tsne_plotter(cl, data_frame):
    """
    Plots a 3D t-SNE for the data
    :param cl: cluster fit data
    :param data_frame: the actual dataframe
    :return: plots a t-sne graph
    """
    tsne_results = clustering.src.silhouette_k_cluster.calc_tsne(data_frame)
    clustering.src.silhouette_k_cluster.plot_tsne(cl, tsne_results)


def handle_missing_values():
 
    """
    This function  is for implementing CommonSpending Heuristic: If two or more addresses are inputs of the same transaction
    with one output, then all these addresses are controlled by the same user. this function return CSV file that store all
    addresses that belong to a certain user in one row.
     :return:
    """
    return ""



def feature_engineering():

    """
    This function  is for implementing ChangeAddress Heuristic: If a transaction has one input and two or more  output
    of the same transaction with one output, then all these addresses are controlled by the same user.

     :return:
    """
    return ""

def TransitiveClosure():
    """
    Transitive closure is for over all the transactions. For example, if there is one transaction in which 1 and 2 are
    used as sending addresses, and another transaction in which 2 and 3 are used as sending addresses, we conclude that
    all three addresses are jointly owned.
    """




def data_encoding():
    """
    Convert non-numeric data into numeric ones, In order to ease the computation
    :return:
    """
    return ""


def data_preprocessing():
    """
    scale the values of the features, Principal component analysis (PCA)
    in order to enhance the performance of the model .
    """
    return ""


def behaviour_pattern_clustering(G, k):
    """
        Performs Behavior pattern clustering (BPC) of users with similar behavior patterns based on their spending
        patterns.
        The algorithm is based on the paper:
            Behavior pattern clustering in blockchain networks by Huang et. al (2017)
            DOI 10.1007/s11042-017-4396-4

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
    return bpc(G, k)
