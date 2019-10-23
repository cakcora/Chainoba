from flask_restful import Resource
from models.models import Input as  TransactionInput
from models.models import db_session, Output, OutputAddress, Address
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_transaction_input(trans_input):
    return {'id': trans_input.id, 'prevout_hash': trans_input.prevout_hash, 'prevout_n': trans_input.prevout_n,
            'scriptsig': str(trans_input.scriptsig), 'sequence': trans_input.sequence,
            'prev_output_id': trans_input.prev_output_id, 'transaction_id': trans_input.transaction_id
            }

# TODO
# 1. Verify for the NULL in the prev_output_id for the inputs in the transactions


class TransactionInputEndpoint(Resource):
    args_transaction = {
        'transaction_ids': fields.List(fields.Integer(validate=lambda trans_id: trans_id > 0))
    }

    @use_kwargs(args_transaction)
    def get(self, transaction_ids):

        transaction_inputs_dict = {}
        for trans_id in transaction_ids:
            transaction_inputs = db_session.query(TransactionInput).filter(
                TransactionInput.transaction_id == trans_id).all()

            previous_output_ids = []
            trans_input_list = []  # the list of transactions returned by the API
            for trans_input in transaction_inputs:
                trans_input_as_dict = serialize_transaction_input(trans_input)

                prev_output_id = trans_input_as_dict["prev_output_id"]
                if prev_output_id is not None:
                    previous_output_ids.append(prev_output_id)
                    prev_address = db_session.query(TransactionInput, Output, OutputAddress, Address).filter(
                        Output.id == int(prev_output_id)).filter(OutputAddress.output_id == Output.id).filter(
                        Address.id == OutputAddress.address_id).all()

                    previous_output_address = prev_address["address"]
                    trans_input_as_dict["prev_output_id"] = previous_output_address

                trans_input_list.append(trans_input_as_dict)

            transaction_inputs_dict[trans_id] = trans_input_list

        total_inputs = 0
        for key, value in transaction_inputs_dict.items():
            total_inputs += len(value)

        return {'num_of_transaction_inputs': total_inputs, 'transaction_inputs': transaction_inputs_dict}
