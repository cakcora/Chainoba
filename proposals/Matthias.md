### What is your group, what are your considered articles?
- Influence.
- Social networks: Prestige, centrality, and influence

### What is the aim in your project? What algorithms will you implement?

The goal of my project is to implement a set of algorithms each of which will take the blockchain data, and output the centrality of each node as a float value.

Further, I will try to analyse what we could learn from the numbers. The paper provides several measures of centrality. But they are most commonly used in the normal social netowrk graphs, where the degree of each node is large and majority of nodes are connected over a few bridge nodes. On the other hand, the nodes in the block chain are often isolated.

To compare them, if time permits, it would be interesting to run the algorithm and compare how the values are different in the normal social networks like LinkedIn Network or Webpage networks, vs the blockchain network.

### What type of data do you require from the database, on which blockchain?

The bitcoin or Etherium blockchain data, with nodes' connections and their transfer amount.

### What will be your results about? Addresses, transactions, blocks, clusters, etc.?

The result would be a set of indicators for each node about how important they are in the network.

### Are your results time dependent? A time dependent result is valid for a specific time period. For example, degree centrality of an address can be computed daily.

No, it is not time dependent.

### What do we need to store from your results? (for example, the fact that “address a appears in the same cluster with address b” can be stored).

There will be outputs of different centrality measures per address or contract node.

### What are your findings that can be visualized by the visualization group?

The visualization group could emphasise the importance of nodes with the size of each node based on the measures. Since there are different measures of centrality, a node will have different centrality values based on the index used to calculate the centrality. So it'd be nice if we can switch between different index algorithms and see how the influences of the major nodes chnage.
Also, although it could be out of scope, we could attempt to visually emphasise how the major nodes in the graph are connected. But maybe they are already apparent from the graph itself?

### Can your results be used as input in algorithms of other groups? (this estimate will be updated after you see algorithms that are being implemented by others)

I'm not sure how this'd be used by others. It might be worth trying to measure the centrality of each cluster instead of nodes if clustera are loosely connected and not completely isolated
