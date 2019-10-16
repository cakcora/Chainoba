

# Foundation Team

In the **foundation group**, we are going to **parse the bitcoin data** and save the result in the structured SQL database. 
We will start with the blocks for 2009 until we get a proper server. We will also provide an API on top of the stored database to provide necessary data to other groups.

# My Contribution

I used the [blockchain parser](https://libraries.io/pypi/blockchain-parser) python library to parse the bitcoin blockchain. 
I tried to understand all fields in a bitcoin block<sup>1</sup> to create required tables using *PostgreSQL*.
Using aforementioned library, I wrote a code to parse raw *`.dat`* datafiles of [Bitcoin Core wallet](https://bitcoin.org/en/wallets/desktop/windows/bitcoincore/?platform=windows&step=5) and save the corresponding 
blocks, transactions and addresses. I am also going to parallelize the parser to make the parsing process faster.
# Data structure 
The below diagram show Block, Transaction, Transaction input, Transaction output, and Address tables and their relationship.
  <p align="center">
  <img src="/images/ERM.png" alt="ERM Diagram" height="700"/>
  </p>



1) I have found *[Learn me a bitcoin ](https://learnmeabitcoin.com/guide/)*
very useful for understanding every single field in a bitcoin block, which could be helpful for other students.
