from datetime import datetime
import os

import psycopg2 as psycopg2
from psycopg2 import IntegrityError
from blockchain_parser.blockchain import Blockchain

# https://github.com/alecalve/python-bitcoin-blockchain-parser
# https://libraries.io/pypi/blockchain-parser
# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
blockchain = Blockchain(os.path.expanduser('fewBlocks'))

con = psycopg2.connect(database="blockchain", user="postgres", password="1", host="127.0.0.1", port="5432")
con.autocommit = False
cur = con.cursor()
i = 1


def insert_block(block):
        cur.execute(
            '''INSERT INTO bitcoin.block (hash,version,hashPrev,hashMerkleRoot,nBits,nNonce,ntime) 
                   values (%s , %s , %s , %s , %s , %s , %s) returning id''',
            (block.hash, block.header.version, block.header.previous_block_hash, block.header.merkle_root,
             block.header.bits, block.header.nonce, datetime.timestamp(block.header.timestamp)))
        return cur.fetchone()[0]



def insert_transaction(transaction, block_id):
    cur.execute('''INSERT INTO bitcoin.transaction (hash,version,locktime,block_id) 
                      values (%s , %s , %s , %s) returning id''',
                (transaction.hash, transaction.version, transaction.locktime, block_id))
    return cur.fetchone()[0]


def insert_input(input, transaction_id):
    cur.execute('''INSERT INTO bitcoin.input (prevout_hash, prevout_n, sequence, transaction_id, scriptsig) 
                    values (%s , %s , %s , %s, %s)''',
                (input.transaction_hash,
                 input.transaction_index,
                 input.sequence_number,
                 transaction_id,
                 input.script.hex.hex()))


def insert_output(output, transaction_id, output_index):
    cur.execute('''INSERT INTO bitcoin.output (value, transaction_id, scriptpubkey,script_type, index) 
                               values ( %s , %s , %s, %s, %s) returning id''',
                (output.value, transaction_id, output.script.hex.hex(), output.type, output_index))
    output_id = cur.fetchone()[0]
    insert_addresses(output.addresses, output_id)


def insert_addresses(addresses, output_id):
    for address in addresses:
        public_key = None
        if address.public_key is not None:
            public_key = address.public_key.hex()
        address_id = get_address(address.address)
        if address_id is None:
            cur.execute("INSERT INTO bitcoin.address (hash, public_key, address) values ('%s', '%s' , '%s')  returning id" %(address.hash.hex(), public_key, address.address))
            address_id = cur.fetchone()[0]
        cur.execute("INSERT INTO bitcoin.output_address (output_id, address_id) values (%s , %s)",
                    (output_id, address_id))


def get_address(address):
    cur.execute("SELECT address.id from bitcoin.address where address = '%s' " % address)
    try:
        return cur.fetchone()[0]
    except TypeError:
        return None


for blck in blockchain.get_unordered_blocks():
    try:
        try:
            blck_id = insert_block(blck)
        except IntegrityError:
            #print("already saved!")
            con.rollback()
            continue

        for tx in blck.transactions:
            tran_id = insert_transaction(tx, blck_id)
            out_index = 0
            for txout in tx.outputs:
                insert_output(txout, tran_id, out_index)
                out_index = out_index + 1
            for txin in tx.inputs:
                insert_input(txin, tran_id)

            i = i + 1
            print("%d blocks saved. last block id = %d" % (i, blck_id))

        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error in transaction Reverting all other operations of a transaction ", error)
        con.rollback()
        #break

con.close()
