from flask_restful import Resource
from foundations.api.models.models import Output as TransactionOutput
from foundations.api.models.models import db_session
from webargs import fields, validate
from webargs.flaskparser import use_kwargs


def serialize_transaction_output(trans_output):
    return {'id': trans_output.id, 'value': trans_output.value, 'scriptpubkey': trans_output.scriptpubkey,
            'transaction_id': trans_output.transaction_id, 'index': trans_output.index,
            'script_type': trans_output.script_type
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
        transaction_outputs = db_session.query(TransactionOutput).filter(
            TransactionOutput.transaction_id == transaction_id).order_by(TransactionOutput.id.asc())

        trans_output_counter = 0
        trans_output_list = dict()  # the list of transactions returned by the API
        for trans_output in transaction_outputs:
            trans_output_as_dict = serialize_transaction_output(trans_output)
            trans_output_list[trans_output_as_dict['id']] = trans_output_as_dict
            trans_output_counter += 1

        return {'transaction_id': transaction_id, 'num_trans_outputs': trans_output_counter,
                'transaction-outputs': trans_output_list}
