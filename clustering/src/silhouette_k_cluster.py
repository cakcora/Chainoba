"""
This file implements k means clustering on bitcoin data from 2009. For visualization, silhouette analysis is used
"""
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import graph.getGraph.addressFeatures

# terminal can only output certain number of columns
pd.set_option('display.max_columns', 10)

# TODO: Graph team has yet to turn this into one function call
# The workaround for the team being is to merge the different dataframes
res, df0 = graph.getGraph.addressFeatures.getFeatures(9, 1, 2009, 'LEVEL_OF_ACTIVITY')
res, df = graph.getGraph.addressFeatures.getFeatures(9, 1, 2009, 'TOTAL_BTC_RECEIVED')
res, df1 = graph.getGraph.addressFeatures.getFeatures(9, 1, 2009, 'TOTAL_BTC_SENT')
res, df2 = graph.getGraph.addressFeatures.getFeatures(9, 1, 2009, 'CURRENT_BALANCE')


def load_data():
    """
    Call the graph's team function to get the dataframe
    Merge the different dataframes
    :return: dataframe with the first column dropped
    """
    data_frame = pd.concat([df0, df, df1, df2], ignore_index=True, sort=True).fillna(0)
    cols = ['Node', 'Bitcoin Sent', 'Amount', 'Current Balance', 'total_degree']
    data_frame = data_frame[cols]

    # print(data_frame)
    cleaned_df = data_frame.drop('Node', 1)
    # print(cleaned_df)
    return cleaned_df


def cluster(cleaned_df, num_cluster=8):
    """
    :param cleaned_df: the dataframe
    :param num_cluster: optimal number of clusters
    :return: a cluster fit of the data
    """
    kmeans = KMeans(num_cluster)
    cl = kmeans.fit(cleaned_df)
    centroids = kmeans.predict(cleaned_df)
    plt.scatter(cleaned_df[:, 0], cleaned_df[:, 1], c=centroids, s=50, cmap='viridis')

    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    return cl


def data_pipeline(dataframe):
    """
    Builds a pipeline and standardizes data
    :param dataframe:
    :return: pipe and the standardized data
    """
    log = FunctionTransformer(func=np.log1p, inverse_func=np.expm1, validate=True)
    scale = StandardScaler()
    pca = PCA(n_components=dataframe.shape[1])

    # build pipeline
    pipe = Pipeline([('log', log),
                     ('scale', scale),
                     ('PCA', pca)])

    results = pipe.fit_transform(dataframe)
    return pipe, results


def find_optimal_num_cluster(cleaned_df):
    """
    :param cleaned_df:
    :return: optimal cluster number
    """
    sil = []
    kmax = list(range(2, 10))
    for k in kmax:
        kmeans = KMeans(n_clusters=kmax[0]).fit(cleaned_df)
        labels = kmeans.fit_predict(cleaned_df)
        # labels = kmeans.labels_
        score = silhouette_score(cleaned_df, labels, metric='euclidean')
        sil.append(score)
        print('For k = {}, silhouette score is {}'.format(k, score))
    plt.plot(kmax, sil)
    plt.title('Silhouette score values vs Numbers of Clusters')
    plt.show()
    return max(sil)


def calc_tsne(results, n_components=2, perplexity=20, n_iter=300, verbose=1):
    """
    :param results: the dataframe
    :return: t-sne result
    """
    data_pipeline(results)
    time_start = time.time()
    tsne = TSNE(n_components=n_components, perplexity=perplexity, n_iter=n_iter, verbose=verbose, learning_rate=100)
    tsne_results = tsne.fit_transform(results)
    print('T-SNE done! Time elapsed: {} seconds'.format(time.time() - time_start))
    return tsne_results


def plot_tsne(cl, tsne_results):
    """
    :param cl: the clustered fit
    :param tsne_results
    plots t-sne
    """
    NUM_COLORS = cl.n_clusters
    cm = plt.get_cmap('nipy_spectral')

    fig = plt.figure(figsize=(15, 12))
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1. * i / NUM_COLORS) for i in range(NUM_COLORS)])

    for c in np.unique(cl.labels_):
        mask = cl.labels_ == c
        if np.sum(mask) == c:
            lbl = '_nolegend_'
        else:
            lbl = c

        plt.scatter(tsne_results[mask][:, 0], tsne_results[mask][:, 1], s=20, alpha=.4, label=lbl)

    legend = plt.legend(bbox_to_anchor=(1, 1))
    for lh in legend.legendHandles:
        lh.set_alpha(1)

    plt.title('T-SNE', fontsize=20)
    plt.xlabel('first principal component')
    plt.ylabel('second principal component')
    plt.show()
