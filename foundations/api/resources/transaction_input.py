from flask_restful import Resource
from foundations.api.models.models import Input as  TransactionInput
from foundations.api.models.models import db_session
from webargs import fields, validate
from webargs.flaskparser import use_kwargs


def serialize_transaction_input(trans_input):
    return {'id': trans_input.id, 'prevout_hash': trans_input.prevout_hash, 'prevout_n': trans_input.prevout_n,
            'scriptsig': trans_input.scriptsig, 'sequence': trans_input.sequence,
            'prev_output_id': trans_input.prev_output_id, 'transaction_id': trans_input.transaction_id
            }


class TransactionInputEndpoint(Resource):
    args = {
        'transaction_id': fields.Integer(
            required=True,
            validate=lambda blk_id: blk_id > 0,
            location='query'
        )
    }

    @use_kwargs(args)
    def get(self, transaction_id):
        transaction_inputs = db_session.query(TransactionInput).filter(
            TransactionInput.transaction_id == transaction_id)

        trans_input_counter = 0
        trans_input_list = dict()  # the list of transactions returned by the API
        for trans_input in transaction_inputs:
            trans_input_as_dict = serialize_transaction_input(trans_input)
            trans_input_list[trans_input_as_dict['id']] = trans_input_as_dict
            trans_input_counter += 1

        return {'transaction_id': transaction_id, 'num_trans_inputs': trans_input_counter,
                'transactio_inputs': trans_input_list}
