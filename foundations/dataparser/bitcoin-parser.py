import multiprocessing as mp
from config import cfg as CONFIG
import time
import os
from datetime import datetime
import psycopg2 as psycopg2
from blockchain_parser.blockchain import Blockchain
from psycopg2 import IntegrityError

# https://github.com/alecalve/python-bitcoin-blockchain-parser
# https://libraries.io/pypi/blockchain-parser
# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
blockchain = Blockchain(os.path.expanduser('fewBlocks'))


def create_db_connection():
    con = psycopg2.connect(database=CONFIG.POSTGRES_DB,
                           user=CONFIG.POSTGRES_USER,
                           password=CONFIG.POSTGRES_PW,
                           host=CONFIG.POSTGRES_HOST,
                           port=CONFIG.POSTGRES_PORT)
    return con


i = 1


def insert_block(cur, block):
    cur.execute(
        '''INSERT INTO bitcoin.block (hash,version,hashPrev,hashMerkleRoot,nBits,nNonce,ntime) 
               values (%s , %s , %s , %s , %s , %s , %s) returning id''',
        (block.hash, block.header.version, block.header.previous_block_hash, block.header.merkle_root,
         block.header.bits, block.header.nonce, datetime.timestamp(block.header.timestamp)))
    return cur.fetchone()[0]


def insert_transaction(cur, transaction, block_id):
    cur.execute('''INSERT INTO bitcoin.transaction (hash,version,locktime,block_id) 
                      values (%s , %s , %s , %s) returning id''',
                (transaction.hash, transaction.version, transaction.locktime, block_id))
    return cur.fetchone()[0]


def insert_input(cur, input, transaction_id):
    cur.execute('''INSERT INTO bitcoin.input (prevout_hash, prevout_n, sequence, transaction_id, scriptsig) 
                    values (%s , %s , %s , %s, %s)''',
                (input.transaction_hash,
                 input.transaction_index,
                 input.sequence_number,
                 transaction_id,
                 input.script.hex.hex()))


def insert_output(cur, output, transaction_id, output_index):
    cur.execute('''INSERT INTO bitcoin.output (value, transaction_id, scriptpubkey,script_type, index) 
                               values ( %s , %s , %s, %s, %s) returning id''',
                (output.value, transaction_id, output.script.hex.hex(), output.type, output_index))
    output_id = cur.fetchone()[0]
    insert_addresses(cur,output.addresses, output_id)


def insert_addresses(cur, addresses, output_id):
    for address in addresses:
        public_key = None
        if address.public_key is not None:
            public_key = address.public_key.hex()
        address_id = get_address(cur,address.address)
        if address_id is None:
            cur.execute(
                "INSERT INTO bitcoin.address (hash, public_key, address) values ('%s', '%s' , '%s')  "
                "on conflict (hash) do update set hash = '%s'  returning id" % (
                    address.hash.hex(), public_key, address.address, address.hash.hex()))
            address_id = cur.fetchone()[0]
        cur.execute("INSERT INTO bitcoin.output_address (output_id, address_id) values (%s , %s)",
                    (output_id, address_id))


def get_address(cur, address):
    cur.execute("SELECT address.id from bitcoin.address where address = '%s' " % address)
    try:
        return cur.fetchone()[0]
    except TypeError:
        return None


def process_blocks(blck):
    start_time = time.time()
    global i
    con = create_db_connection()
    cur = con.cursor()
    print("--- open connection %s  ---" % (time.time() - start_time))

    try:
        try:
            start_time = time.time()
            blck_id = insert_block(cur, blck)
            print("--- insert block %s  ---" % (time.time() - start_time))
        except IntegrityError:
            print("already saved!")
            con.rollback()
            return 0

        for tx in blck.transactions:
            start_time = time.time()
            tran_id = insert_transaction(cur, tx, blck_id)
            print("--- insert transaction %s  ---" % (time.time() - start_time))
            out_index = 0
            for txout in tx.outputs:
                insert_output(cur, txout, tran_id, out_index)
                out_index = out_index + 1
            for txin in tx.inputs:
                insert_input(cur, txin, tran_id)

        print("last block id = %d" %blck_id)
        cur.close()
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error in transaction Reverting all other operations of a transaction ", error)
        con.rollback()
        # break


if __name__ == '__main__':
    pool = mp.Pool()
    pool.map(process_blocks, blockchain.get_unordered_blocks())
