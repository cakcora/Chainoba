from flask_restful import Resource
from foundations.api.models.models import Transaction
from foundations.api.models.models import db_session
from webargs import fields, validate
from webargs.flaskparser import use_kwargs


def serialize_transaction(transaction):
    return {'id': transaction.id, 'hash': transaction.hash, 'version': transaction.version,
            'locktime': transaction.locktime, 'version': transaction.block_id}


class TransactionEndpoint(Resource):
    args_block = {
        'block_id': fields.Integer(
            required=True,
            validate=lambda blk_id: blk_id > 0,
            location='query'
        )
    }

    @use_kwargs(args_block)
    def get(self, block_id):
        block_transactions = db_session.query(Transaction).filter(Transaction.block_id == block_id).order_by(
            Transaction.id.asc())
        trans_counter = 0

        trans_list = dict()  # the list of transactions returned by the API
        for transaction in block_transactions:
            trans_as_dict = serialize_transaction(transaction)
            trans_list[trans_as_dict['hash']] = trans_as_dict
            trans_counter += 1

        return {'block id': block_id, 'num_trans': trans_counter, 'transactions': trans_list}
