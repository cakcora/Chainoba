
## COMP 7570/4060- Blockchain Analysis

### Individual Project Proposal

##### Sourav.
-   **What is your group, what are your considered articles?**
    
    -   Group name: Anomaly Detection 
    -   Articles:
        -   BitcoinHeist: Topological Data Analysis for Ransomware Detection on the Bitcoin Blockchain, Cuneyt Gurcan Akcora
        -   To the moon: defining and detecting cryptocurrency pump-and-dumps, Josh Kamps
        -   Tracking Ransomware End-to-end, DY Huang
        -   Bitcoin Transaction Graph Analysis-Micheal Fleder
        - The Anatomy of a Cryptocurrency Pump-and-Dump, J Xu
        - The Fifth Labor - The Concept
-   **What is the aim in your project? What algorithms will you implement?**
    
    -   The project aims is to check the anomalous behavior of Bitcoin data by exploring data set compromises of addresses and transaction data graph collectively using machine learning techniques.
        
    -   The following algorithms will be implemented:
        
        -   Clustering the data set so that it is explored easily.
        -   Find out anomalous behavior of ransomware or malicious services
-   **What type of data do you require from the database, on which blockchain?**
    
    -   The relational schema is required for the information on all transactions parsed from Bitcoin. Also,  information about ransomware family and their data set is required to train the data for prediction.
-   **What will be your results about? Addresses, transactions, blocks, clusters,etc.?**
    
    -   The result will be about addresses and transactions behavior i.e. either suspicious or non-suspicious inferred from the algorithm.
-   **Are your results time dependent? A time dependent result is valid for a specific time period. For example, degree centrality of an address can be computed daily.**
    
    -   The results are time-dependent because a given user exhibit different behavior in a particular time-frame and undergoes change its coin usage behavior in another time-frame.
   -   **What do we need to store from your results? (for example, the fact that “address a appears in the same cluster with address b” can be stored).**
    
        -   Results data that can be stored involves the details of various addresses and transactions that will be recognized as suspicious by the given model. 
-   **What are your findings that can be visualized by the visualization group?**
	- Clustering and visualization of suspicious behavior from non suspicious behavior.
    
-   **Can your results be used as input in algorithms of other groups? (this estimate will be updated after you see algorithms that are being implemented by others)**
    
    -   Yes, the results will be used by the Visualization team.
