# INDIVIDUAL PROJECT PROPOSAL – BLOCKCHAIN ANALYSIS (COMP 7570)
### BY: KARAN GOVIL (7888564)
### GROUP: ANOMALY DETECTION

##### 1.	What is your group, what are your considered articles?
GROUP: Anomaly Detection  
Articles:  
•	Extortion graph exploration techniques in the bitcoin network  
•	BitcoinHeist: Topological data analysis for ransomware detection on the Bitcoin blockchain  
•	Tracking Ransomware End-to-end  
•	Exploiting Blockchain Data to Detect Smart Ponzi Schemes on Ethereum  
•	The Anatomy of a Cryptocurrency Pump-and-Dump  
•	To the moon: defining and detecting cryptocurrency pump-and-dumps  
•	The Fifth Labor - The Concept  


##### 2.	What is the aim in your project? What algorithms will you implement?
The aim of the project is to detect anomalies in the Ethereum network. The specific aim is to explore and detect the Smart Ponzi scheme in Ethereum (Ponzi Schemes implemented as Smart Contracts on blockchain). This is done in 3 steps:  
1.	Obtaining the source codes of open source smart contracts and checking if it is a Ponzi scheme  
2.	After that, 2 features from the data are to be extracted: account and code features  
3.	A classification model is built and applied.  
The algorithm used is a bagging-based algorithm, named Random Forest (combination of Decision Trees).  


##### 3.  What type of data do you require from the database, on which blockchain?
1.	Source codes of open smart contracts  
2.	External and internal transactions to extract features like Balance, Investment, Known Rate etc.  
It is required for Ethereum.


##### 4.  What will be your results about? Addresses, transactions, blocks, clusters, etc.?
The results will be about transactions and the smart contracts in Ethereum.


##### 5. Are your results time dependent? A time dependent result is valid for a specific time period. For example, degree centrality of an address can be computed daily.
The results are not time dependent.


##### 6. What do we need to store from your results? (for example, the fact that “address a appears in the same cluster with address b” can be stored).
We need to store the trending data in order to estimate the number of smart Ponzi schemes on Ethereum. We also need to store data corresponding to numerous features including Balance, Max number of payments to all participants, number of investments to the contract, number of payments from the contract, proportion of investors who received at least 1 payment.


##### 7. What are your findings that can be visualized by the visualization group?
The visualization group need to visualize the number of detected Smart Ponzi Schemes with corresponding probability range and the schemes created each month.


##### 8. Can your results be used as input in algorithms of other groups? (this estimate will be updated after you see algorithms that are being implemented by others)
The results will be used by the visualization team.
