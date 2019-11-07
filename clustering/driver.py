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
     get the  number of missing values in the datasets to handle those missing values.
     :return:
    """
    return ""

def feature_engineering():
    """
     drop features that have not any impact on our goal
     :return:
    """

    return ""
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

    :return:
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
