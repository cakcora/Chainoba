## Influence Team

---
## k-core decomposition
In order to get the k-core subgraph of ethereum/bitcoin network, use the function we can make use of the given implemented functions. 

### Install required packages.
**please run `pip install -r requirements.txt`**

> ## Naming Conventions
- **G** is used to denote the graph.
- **k** is used to denote the k-core value of the subgraph
- **K** is used to denote the maximum k value of a vertex
- **u** is used to denote the vertex

> ## Functions

- `get_k-core(G,k)` - Provide G and k, this function will return to you the k-core subgraph of G.

- `max_k_core_graph(G)` - Maximum k-core subgraph for a given graph 'G'. This will give you the most densely connected subgraph with the maximum k values.

- `get_max_k_value(G, vertex)` - Get the maximum K value for a given vertex.

> ## Functions to be implemented

- `subcore(G, K, u)` - Maintains the K values of vertices when
a single edge is inserted or removed. _this function will be used for comparative results_

- `insert_edge` - Maintains the K values of vertices when
a single edge is inserted or removed. _this function will be used for comparative results_

- `remove_edge` - Maintains the K values of vertices when
a single edge is inserted or removed. _this function will be used for comparative results_