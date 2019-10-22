# Individual Project Proposal – Blockchain Analysis (COMP 7570)
### By: Bryan Wodi
### Group: Clustering

##### 1.	What is your group, what are your considered articles?
Group: Clustering  
Articles:
* Clustering in weighted networks
* Clustering Blockchain Data 
* Clustering and community detection in directed networks
* A Fistful of Bitcoins: Characterizing Payments Among Men with No Names
* Tracing Transactions Across Cryptocurrency Ledgers

##### 2.	What is the aim in your project? What algorithms will you implement?
My project will focus on clustering behavioral patterns between addresses in the blockchain. I will first use the Levenshtein distance algorithm to measure similarities between addresses to merge them. Then, by using the Wagner-Fischer’s algorithm, I will generate a matrix of distances between the addresses. Subsequently, I will use the  Ward’s method to cluster the addresses.


##### 3.  What type of data do you require from the database, on which blockchain?
A network of bitcoin addresses showing their transactions with each other.


##### 4.  What will be your results about? Addresses, transactions, blocks, clusters, etc.?
Ideally, the results of this technique can be used to cluster transactions and addresses with similar patterns. 

##### 5. Are your results time dependent? A time dependent result is valid for a specific time period. For example, degree centrality of an address can be computed daily.
Yes.

##### 6. What do we need to store from your results? (for example, the fact that “address a appears in the same cluster with address b” can be stored).
Lists of clusters and their members. The members being addresses or transaction identifiers.


##### 7. What are your findings that can be visualized by the visualization group?
The different clusters formed from the network, showing their members, as well as outliers (if any).


##### 8. Can your results be used as input in algorithms of other groups? (this estimate will be updated after you see algorithms that are being implemented by others)
It can be used by the anomaly detection and visualization teams.