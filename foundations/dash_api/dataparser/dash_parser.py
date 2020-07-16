import os
from datetime import datetime
import requests
assert requests.get('https://github.com/blockchain-etl/bitcoin-etl').status_code == 200

#----------start_block & end_block are used for export_blocks_and_transactions----------
#start_block = input("Enter the start block: ")
#end_block = input("Enter the end block: ")
#batch_size = input("Enter the batch size: ")

#----------date_entry is used for get_block_range_for_date----------
#date_entry = input("Enter a date in YYYY-MM-DD format: ")

#----------start_date & end_date are used for export_all------------------ 
start_date = input("Enter a start date in YYYY-MM-DD format: ")
end_date = input("Enter an end date in YYYY-MM-DD format: ")

#----------export_blocks_and_transactions for given start_block and end_block-------------
def export_blocks_and_transactions():
    os.system(f'bitcoinetl export_blocks_and_transactions --start-block {start_block} --end-block {end_block} \
--provider-uri http://cai:password@localhost:8328 --chain dash \
 --blocks-output blocks-{start_block}-{end_block}.json --transactions-output transactions-{start_block}-{end_block}.json')

#def enrich_transactions():
#    os.system(f'bitcoinetl enrich_transactions  \
#  --provider-uri http://cai:password@localhost:8328 \
#  --transactions-input transactions-{start_block}-{end_block}.json --transactions-output enriched_transactions-{start_block}-{end_block}.json')

#def get_block_range_for_date():
    #os.system(f'bitcoinetl get_block_range_for_date --provider-uri http://cai:password@localhost:8328 --date={date_entry}')

def export_all():
    os.system(f'bitcoinetl export_all --provider-uri http://cai:password@localhost:8328 --start {start_date} --end {end_date}')

#---------export_all is the main function to get blocks and transactions for a date range --------------------
if __name__ == "__main__":
    #export_blocks_and_transactions()
    #enrich_transactions()
    #get_block_range_for_date()
    export_all()
    


    
