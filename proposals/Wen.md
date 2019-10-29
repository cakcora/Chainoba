# COMP 7570 - Blockchain Analysis - Project Proposal
## Qi Wen 
#### Anomaly Detection group.

***
###### Articles 
EGRET: Extortion Graph Exploration Techniques in the Bitcoin Network

Tracking Ransomware End-to-end

BitcoinHeist: Topological Data Analysis for Ransomware Detection on the Bitcoin Blockchain

Tracing transactions across cryptocurrency ledgers

***
###### What is the aim in your project? What algorithms will you implement?
Aim to find out all the suspicious nodes starting from a dataset that contains a set of known suspicious nodes.
- If an address receives multiple payments (i.e. merge address) then it is regarded suspicious.
- If multiple addresses merge after N block, then the merging address is suspicious.

###### What type of data do you require from the database, on which blockchain?
The bitcoin public addresses and transactions related to known exchanges. The data will be parsed from WalletExplorer.

###### What will be your results about? Addresses, transactions, blocks, clusters, etc.?
A list of suspicious addresses and transactions beside original suspicious addresses.

###### Are your results time dependent? A time dependent result is valid for a specific time period. For example, degree centrality of an address can be computed daily.
No, because unsuspected addresses could become suspicious in the future.

###### What do we need to store from your results? (for example, the fact that “address a appears in the same cluster with address b” can be stored). 
A list which contains suspicious addresses and transactions

###### What are your findings that can be visualized by the visualization group? 
The visualization team will receive the list of suspicious addresses and transactions along with the time so that these could be marked to show the difference from other addresses.

###### Can your results be used as input in algorithms of other groups? (this estimate will be updated after you see algorithms that are being implemented by others)
Can be used in visualization group



