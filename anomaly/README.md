# Anomaly

Please put your function signatures in the driver.py file. The actual implementation of the functions are not included 
in this file.

## Fifth labor problem - Merging behavior
fifth_labor_problem.py aims to  find out all the suspicious nodes starting from a dataset that contains a set of known suspicious nodes.
We have called the original API(https://blockchain.info/) to illustrate the result from real data. Data file contains ~20K initial suspicious addresses, range(1000) is used instead of range(len(date)) for demonstration.
- Problem1: If an address receives multiple payments (i.e. merge address) then it is regarded suspicious.\
    Simply run fifth_labor_problem1()\
    Demonstration: \
    Computation takes ~21mins(1252secs), found 1202 merging addresses including
    {'1DxZGpmCwRUTeb5g1za1CJ2mcFK5w6f69M', '1JzvWfkKhmDzVweYLkpiaZi7D8zG6XBg5E', '1BrqDeueryM4b4mpzrxvf7Txs15eiqYRRk'...}
    and also 4 exchange addresses.
    This method will generate merging_addresses.txt and to see if these merging addresses contain
    any exchange addresses(which is not malicious) run check_exchange_address().

- Problem2: If multiple addresses merge after N block, then the merging address is suspicious.\
    We simplified problem into 1 to 1 and 1 to 2 transaction only and within 3 hops
    Run fifth_labor_problem2()\
    Demonstration: \

    | Hops  | Time(seconds) | Merging address count  |
    | ------|:-------------:| ----------------------:|
    |      1|            677|                       0|
    |      2|           1843|                       3|
    |      3|           4677|                      26|
    
    Run check_exchange_address()\
    We did not see any exchange addresses in the result.\
    Considering 2 hops, we found {'14mhJHmj25kAiBDpUd3hord9Wm694CxEDn', '1dice97ECuByXAvqXpaYzSaQuPVvrtmz6', '1diceDCd27Cc22HV3qPNZKwGnZ8QwhLTc'}
    and last two addresses are known to be the address of gambling company. Moreover, in 3 hops, there are some bank addresses.\
    It is hard to test more than 3 hops as the computation time grows exponentially(find it in the table).\
    Note: generate_exchange_addresses() is preprossing method to generate exchange_addresses.txt
    