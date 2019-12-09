## Influence Team

---
k-core decomposition

In order to get the k-core subgraph of ethereum/bitcoin network, use the function we can make use of the given implemented functions. 

### Install required packages.
**please run `pip install -r requirements.txt`**

> ## Naming Conventions
- **G** is used to denote the graph.
- **k** is used to denote the k-core value of the subgraph
- **K** is used to denote the maximum k value of a vertex
- **u** is used to denote the vertex

> ## KCore

>
    
- `def get_k_cores(k, core)` - Return the k-core of this graph
    -   k - [int, optional] The order of the core. If not specified return the main core.
    -   core_number : [dictionary, optional] Precomputed core numbers for the graph G.

- `def get_core_number()` - This function will return a dictionary keyed by node to the core number.

- `def max_k_core_graph()` - Maximum k-core sub-graph for this graph

- `def get_graph()` - Get the graph associated with the object instance

- `def generate_graph(input, output, amount)` - Provide 3 lists of inputs, outputs, and amounts **in-order**. This function will be updated to 
automatically extract this information once the graph functionality is better implemented.

---