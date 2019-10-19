import requests
from flask_restful import Resource
from models.models import Transaction
from models.models import db_session
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_transaction(transaction):
    return {'id': transaction.id, 'hash': transaction.hash, 'version': transaction.version,
            'locktime': transaction.locktime, 'version': transaction.block_id}


args_block = {
    'block_id': fields.List(fields.Integer(validate=lambda blk_id: blk_id > 0))
}


class TransactionEndpoint(Resource):

    @use_kwargs(args_block)
    def get(self, block_id):

        block_transactions_dict = {}
        for blk_id in block_id:
            transaction_ids = []
            block_transactions = db_session.query(Transaction).filter(Transaction.block_id == blk_id).order_by(
                Transaction.id.asc())

            trans_list = []  # the list of transactions returned by the API
            for transaction in block_transactions:
                trans_as_dict = serialize_transaction(transaction)
                trans_list.append(trans_as_dict)
                transaction_ids.append(trans_as_dict['id'])

            print("Transaction ids: {}".format(transaction_ids))
            input_response = requests.post('http://localhost:5000/bitcoin/inputs',
                                           json={'transaction_ids': transaction_ids}).text
            print(input_response)

            # Visit this after completing transaction input endpoint

            block_transactions_dict[blk_id] = trans_list

        return {'block_transactions': block_transactions_dict}
