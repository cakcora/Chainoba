# Clustering

## Behavior Pattern Clustering (BPC)
This is a similarity measure in blockchain networks that clusters behavior patterns of users into different categories 
based on behaviour templates. In this implementation, we cluster users' spending patterns on the Blockchain to identify
*k* unique spending behaviours throughout a given network.

The interface:
```behaviour_pattern_clustering(G, k)```  in ```driver.py``` explains how to use this module. 

## K-means clustering with silhouette analysis

K-means algorithm identifies k number of centroids, 
and then allocates every data point to the nearest 
cluster, while keeping the centroids as small as possible

Currently, bitcoin 2009 dataset is used for clustering but the code
can be extended to ethereum dataset as well. 

Clustering is done based on four node features
- `Level of activity `

- `Total bitcoins received`

- `Total bitcoins sent`

- `Current balance`


# 3-tier architecture for K means clustering:

`src` directory has the implementation for k-means clustering
and t-sne plot. The data for clustering comes from `graph` 
directory in the root folder. The below functions in the `driver` file of `cluserting` directory
can be called to get the results.

- `load_data()` - loads data from the 2009 bitcoin dataset

- `cluster()` - gets a cluster fit for the data

- `tsne_plotter` - processes the data and plots the t-sne plot



Here is a visual representation of the architecture for more clarity:

- `graph` - a pseudo layer that gets the data from the database

- `src/silhouette_k_cluster` - business layer with the logical implementation
    
- `driver` a pseudo UI layer that abstracts away the implementation, all interactions start from this layer
