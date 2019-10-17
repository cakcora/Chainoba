from flask_restful import Resource
from foundations.api.models.models import OutputAddress as TransactionOutputAddress
from foundations.api.models.models import Output as TransactionOutput
from foundations.api.models.models import Address
from foundations.api.models.models import db_session
from webargs import fields, validate
from webargs.flaskparser import use_kwargs


def serialize_address(address, output_id):
    return {'address_id': address.id, 'hash': address.hash.strip(),
            'public_key': address.public_key.strip(),
            'address': address.address.strip()
            }


def serialize_transaction_output(trans_output, output_address_as_dict):
    return {'id': trans_output.id, 'value': trans_output.value, 'scriptpubkey': str(trans_output.scriptpubkey),
            'transaction_id': trans_output.transaction_id, 'index': trans_output.index,
            'script_type': str(trans_output.script_type).strip(), 'addresses': output_address_as_dict
            }


def serialize_transaction_output_address(trans_output_id):
    output_address_list = db_session.query(TransactionOutputAddress).filter(
        TransactionOutputAddress.output_id == trans_output_id).order_by(TransactionOutputAddress.id.asc()).all()
    out_addr = {'addresses': []}
    addr_list = []
    for output in output_address_list:
        address_list = db_session.query(Address).filter(
            Address.id == output.address_id).order_by(Address.id.asc()).all()
        for address in address_list:
            address_as_dict = serialize_address(address, trans_output_id)
            addr_list.append(address_as_dict)
    out_addr['addresses'] = addr_list
    return out_addr


class TransactionOutputEndpoint(Resource):
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
            TransactionOutput.transaction_id == transaction_id).order_by(TransactionOutput.id.asc()).all()

        trans_output_counter = 0
        trans_output_list = []
        trans_output_dict = {'trans_output': []}
        for trans_output in transaction_outputs:
            trans_output_address_as_dict = serialize_transaction_output_address(trans_output.id)
            trans_output_as_dict = serialize_transaction_output(trans_output, trans_output_address_as_dict['addresses'])
            trans_output_list.append(trans_output_as_dict)
            trans_output_counter += 1
        trans_output_dict['trans_output'] = trans_output_list

        return {'transaction_id': transaction_id, 'num_trans_outputs': trans_output_counter,
                'transaction-outputs': trans_output_dict['trans_output']}
