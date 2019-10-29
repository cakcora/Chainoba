## Project
The Fifth Labor: How to launder the coins gained from a BitcoinHeist

## Team & Articles

I am in the *Anomaly Detection Team*. **Fifth Labor** is an open problem. So we have to consider multiple articles. Here is the list of articles we will consider as a starting point for this project.
>- "Tracking ransomware end-to-end", in *2018 IEEE Symposium on Security and Privacy (SP)* by D. Y. Huang, M. M. Aliapoulios, V. G. Li, L. Invernizzi, E. Bursztein, K. McRoberts, J. Levin, K. Levchenko, A. C. Snoeren, and D. McCoy
>- "Bitcoinheist: Topological data analysis for ransomware detection on the bitcoin blockchain", *arXiv preprint arXiv:1906.07852, 2019*
>- "Tracing transactions across cryptocurrency ledgers", *28th USENIX Security Symposium (USENIX Security 19), 2019, pp. 837–850*

## Project Goals
The final goal of this project is to find ways to obfuscate the withdrawal of the ransomware payment. However, the final goal may not be achievable within the time-frame of this course. Therefore, for this course project, I will try to implement the methods (models, heuristics, etc. ) to detect the suspicious addresses based on the last two (no. 3 & 4 )linking behaviors listed below:
>1. If an address receives multiple payments from suspicious ransomware addresses ( i.e. *merge address*), then it is regarded as suspicious.
>2. If multiple suspicious addresses merge after N block, then the merging address is suspicious.
>3. If a *Loop* is found in the graph, then both the source and the destination address is considered suspicious.
>4. If a transaction splits one input address to multiple addresses, then the addresses will be considered suspicious.

## Dataset
Here is a list of data type we will need for this project:
>- We will need the known ransomware family and addresses in these ransomware families, which we took from the following sources:
	- https://github.com/cakcora/CoinWorks#raw-data-files
	- https://github.com/cakcora/TheCircus/blob/master/data/allAddresses.txt
>- Cryptocurrencies are converted to fiat money only through *exchanges*. So, we will need the addresses and transactions related to known exchanges. The data will be parsed from *WalletExplorer*, which has a list of 87 exchanges, and all the transactions and addresses related to these exchanges.
>-  The updated transactions in the Bitcoin blockchain will be required to validate the methods. Later, we may need data from other blockchains (e.g. Monero, Ethereum) for tracing cross-ledger transactions. 

## Results

The results will be a list of suspicious addresses and transactions in a blockchain detected by the model. 

## Dependency on time

There will be a dependency on the time as an address not detected as suspicious can become suspicious by future transactions.

## Data Storing
Each suspicious address and transaction should be stored as addresses linked (by merging or splitting) to the suspicious address will be detected as suspicious. 

## Visualization

The visualization team will receive the list of suspicious addresses and transactions along with the time so that these could be marked to show the difference from other addresses.


## Dependency with other Projects

We are going to work on addresses detected as ransomware addresses by the BitcoinHeist approach.