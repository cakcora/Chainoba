import numpy as np

"""
This file will have all the functions related to clustering
- clustering
- clustering-classes
  - driver.py
"""


def load_data():
    """
    This function is going to load the data - eventually it is going to hit an api endpoint
    and get the data from there but for the time being we will be using a hardcoded file
    :return:
    """
    return ""



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



def cluster():
    """
    This function is going to apply k means clustering on the data set
    :return:
    """
    return ""


def assign_cluster_to_data():
    """
    This function will loop through the data provided from the cluster function and assign it to
    different clusters
    :return:
    """
    return ""


def find_category_of_cluster():
    """
    This function returns the category of the cluster that is being passed to it
    :return:
    """
    return ""


def re_cluster():
    """
    This function is going to apply a second round of clustering if there is a mix of addresses in a cluster from the
    first round of clustering
    :return:
    """
    return ""


def ward_method_clustering(G):
    """
    Performs agglomerative hierarchical clustering  of user or transaction addresses with similar behavior patterns.

    :param G: Networkx MultiDiGraph object
    :return: dict: A dictionary of addresses where keys are the cluster labels and values are members of the same
    cluster
    """

    if G[0] == 'Fail':
        return None

    return ward_method_clustering(G[1].nodes)
