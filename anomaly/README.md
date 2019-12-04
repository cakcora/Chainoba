# Anomaly

Please put your function signatures in the driver.py file. The actual implementation of the functions are not included 
in this file.

## Fifth labor problem - Merging behavior
fifth_labor_problem.py aims to  find out all the suspicious nodes starting from a dataset that contains a set of known suspicious nodes.
We have called the original API(https://blockchain.info/) to illustrate the result from real data.
- Problem1: If an address receives multiple payments (i.e. merge address) then it is regarded suspicious.
    Simply run fifth_labor_problem1()\
    Data file contains ~20K initial suspicious addresses.
    Range(1000) is used instead of range(len(date)) for demonstration. \
    Result: \
    Computation takes ~20mins(1252secs), found 1202 merging addresses including
    {'1DxZGpmCwRUTeb5g1za1CJ2mcFK5w6f69M', '1JzvWfkKhmDzVweYLkpiaZi7D8zG6XBg5E', '1BrqDeueryM4b4mpzrxvf7Txs15eiqYRRk'...}
    and 4 exchange addresses.
    This method will generate merging_addresses.txt and to see if these merging addresses contain
    any exchange addresses(which is not malicious) run check_exchange_address().

- Problem2: If multiple addresses merge after N block, then the merging address is suspicious.
