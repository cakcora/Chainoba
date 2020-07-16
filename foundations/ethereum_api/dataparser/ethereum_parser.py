import os
from datetime import datetime
import psycopg2 as psycopg2
from psycopg2 import sql
import requests
assert requests.get('https://github.com/blockchain-etl/ethereum-etl').status_code == 200

def main():
    # input entries
    start_block = input("Enter the start block: ")
    end_block = input("Enter the end block: ")
    batch_size = input("Enter the batch size: ")
    date_entry = input("Enter a date in YYYY-MM-DD format: ")

    # sql connection
    con = psycopg2.connect(database="ethereum", user="lipsa", password="postgres", host="localhost", port="5432")
    con.autocommit = False
    cur = con.cursor()
    schema = 'ethereum'
    table_blocks = 'blocks'
    table_transactions = 'transactions'
    table_logs = 'logs'
    table_receipts = 'receipts'
    table_traces='traces'
    table_contracts='contracts'
    table_tokentransfers = 'token_transfers'
    table_tokens = 'tokens'
 
    blocks_csvfile = '$HOME/Documents/BLOCKCHAIN/Chainoba-master/foundations/ethereum-api/dataparser/blocks-0-500000.csv'
    blocks_query = sql.SQL(f"COPY {schema}.{table_blocks} (number,hash,parent_hash,nonce,sha3_uncles,logs_bloom,transactions_root,state_root,receipts_root,miner, \
    difficulty,total_difficulty,size,extra_data,gas_limit,gas_used,time_stamp,transaction_count) \
        FROM '/Users/lipsa/Documents/BLOCKCHAIN/Chainoba-master/foundations/ethereum_api/dataparser/blocks-0-500000.csv' DELIMITER ',' CSV HEADER;")
    cur.execute(blocks_query)

    transactions_query = sql.SQL(f"COPY {schema}.{table_transactions} (hash,nonce,block_hash,block_number,transaction_index,from_address, \
        to_address,value,gas,gas_price,input,block_timestamp) \
        FROM '/Users/lipsa/Documents/BLOCKCHAIN/Chainoba-master/foundations/ethereum_api/dataparser/transactions-0-500000.csv' DELIMITER ',' CSV HEADER;")
    cur.execute(transactions_query)
    
    logs_query = sql.SQL(f"COPY {schema}.{table_logs} (log_index,transaction_hash,transaction_index, \
    block_hash,block_number,address,data,topics) \
        FROM '/Users/lipsa/Documents/BLOCKCHAIN/Chainoba-master/foundations/ethereum_api/dataparser/logs-0-500000.csv' DELIMITER ',' CSV HEADER;")
    cur.execute(logs_query)

    receipts_query = sql.SQL(f"COPY {schema}.{table_receipts} (transaction_hash,transaction_index, block_hash,block_number,cumulative_gas_used, \
        gas_used,contract_address,root,status) \
        FROM '/Users/lipsa/Documents/BLOCKCHAIN/Chainoba-master/foundations/ethereum_api/dataparser/receipts-0-500000.csv' DELIMITER ',' CSV HEADER;")
    cur.execute(receipts_query)

    traces_query = sql.SQL(f"COPY {schema}.{table_traces} (transaction_hash, transaction_index,from_address,to_address, value, \
    input ,output ,trace_type, call_type ,reward_type,gas ,gas_used ,subtraces ,trace_address,error ,status ,block_number ,trace_id ) \
        FROM '/Users/lipsa/Documents/BLOCKCHAIN/Chainoba-master/foundations/ethereum_api/dataparser/traces-0-500000.csv' DELIMITER ',' CSV HEADER;")
    cur.execute(traces_query)

    contracts_query = sql.SQL(f"COPY {schema}.{table_contracts} ( address,bytecode,function_sighashes,is_erc20,is_erc721,block_number) \
        FROM '/Users/lipsa/Documents/BLOCKCHAIN/Chainoba-master/foundations/ethereum_api/dataparser/contracts-0-500000.csv' DELIMITER ',' CSV HEADER;")
    cur.execute(contracts_query)

    token_transfers_query = sql.SQL(f"COPY {schema}.{table_tokentransfers} ( token_address,from_address,to_address,value,transaction_hash, \
        log_index,block_number) \
        FROM '/Users/lipsa/Documents/BLOCKCHAIN/Chainoba-master/foundations/ethereum_api/dataparser/token_transfers-0-500000.csv' DELIMITER ',' CSV HEADER;")
    cur.execute(token_transfers_query)

    tokens_query = sql.SQL(f"COPY {schema}.{table_tokens} (address,symbol,name, \
    decimals,total_supply, block_number) \
        FROM '/Users/lipsa/Documents/BLOCKCHAIN/Chainoba-master/foundations/ethereum_api/dataparser/tokens-0-500000.csv' DELIMITER ',' CSV HEADER;")
    cur.execute(tokens_query)


    # batch commands
    export_blocks_and_transactions()
    export_token_transfers()
    export_receipts_and_logs()
    extract_token_transfers()
    export_contracts()
    export_tokens() 
    # export_traces()
    # export_geth_traces()
    get_block_range_for_date()

# export_blocks_and_transactions
def export_blocks_and_transactions():
    os.system(f'ethereumetl export_blocks_and_transactions --start-block {start_block} --end-block {end_block} \
    --blocks-output blocks-{start_block}-{end_block}.csv --transactions-output transactions-{start_block}-{end_block}.csv \
    --provider-uri https://mainnet.infura.io/v3/239a1d18eba14f0f9dc1c882de0dc872')


# export_token_transfers
def export_token_transfers():
    os.system(f'ethereumetl export_token_transfers --start-block {start_block} --end-block {end_block} \
    --provider-uri file://$HOME/Library/Ethereum/geth.ipc --batch-size {batch_size} --output token_transfers-{start_block}-{end_block}.csv')


# export_receipts_and_logs
def export_receipts_and_logs():
    os.system(f'ethereumetl extract_csv_column --input transactions-{start_block}-{end_block}.csv --column hash --output transaction_hashes-{start_block}-{end_block}.txt')
    os.system(f'ethereumetl export_receipts_and_logs --transaction-hashes transaction_hashes-{start_block}-{end_block}.txt \
    --provider-uri file://$HOME/Library/Ethereum/geth.ipc --receipts-output receipts-{start_block}-{end_block}.csv --logs-output logs-{start_block}-{end_block}.csv')


# extract_token_transfers
def extract_token_transfers():
    os.system(f'ethereumetl extract_token_transfers --logs logs-{start_block}-{end_block}.csv --output token_transfers-{start_block}-{end_block}.csv')


# export_contracts
def export_contracts():
    os.system(f'ethereumetl extract_csv_column --input receipts-{start_block}-{end_block}.csv --column contract_address --output contract_addresses-{start_block}-{end_block}.txt')
    os.system(f'ethereumetl export_contracts --contract-addresses contract_addresses-{start_block}-{end_block}.txt \
    --provider-uri file://$HOME/Library/Ethereum/geth.ipc --output contracts-{start_block}-{end_block}.csv')


# export_tokens
def export_tokens():
    os.system(f'ethereumetl filter_items -i contracts-{start_block}-{end_block}.csv -p "item[\'is_erc20\'] or item[\'is_erc721\']" | \
    ethereumetl extract_field -f address -o token_addresses-{start_block}-{end_block}.txt')
    os.system(f'ethereumetl export_tokens --token-addresses token_addresses-{start_block}-{end_block}.txt \
    --provider-uri file://$HOME/Library/Ethereum/geth.ipc --output tokens-{start_block}-{end_block}.csv')

# export_traces
 def export_traces():
     os.system(f'ethereumetl export_traces --start-block {start_block} --end-block {end_block} \
     --provider-uri file://$HOME/Library/Ethereum/parity.ipc --batch-size {batch_size} --output traces-{start_block}-{end_block}.csv')
     os.system(f'ethereumetl export_geth_traces --start-block {start_block} --end-block {end_block} \
     --provider-uri file://$HOME/Library/Ethereum/geth.ipc --batch-size {batch_size} --output geth_traces-{start_block}-{end_block}.json')


# export_geth_traces
 def export_geth_traces():
     os.system(f'ethereumetl extract_geth_traces --input geth_traces-{start_block}-{end_block}.json --output traces-{start_block}-{end_block}.csv')


# get_block_range_for_date
def get_block_range_for_date():
    os.system(f'ethereumetl get_block_range_for_date --provider-uri=https://mainnet.infura.io/v3/239a1d18eba14f0f9dc1c882de0dc872 --date date_entry')


if __name__ == "__main__":
    main()

