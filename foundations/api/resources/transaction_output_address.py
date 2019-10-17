from flask_restful import Resource
from foundations.api.models.models import OutputAddress as TransactionOutputAddress
from foundations.api.models.models import Output as TransactionOutput
from foundations.api.models.models import Address
from foundations.api.models.models import db_session
from webargs import fields, validate
from webargs.flaskparser import use_kwargs


def serialize_address(address, output_id):
    return {'address_id': address.id, 'output_id': output_id, 'hash': address.hash.strip(),
            'public_key': address.public_key.strip(),
            'address': address.address.strip()
            }


def serialize_transaction_output_address(address_id, output_id):
    address_list = db_session.query(Address).filter(
        Address.id == address_id).order_by(Address.id.asc())
    for address in address_list:
        address_as_dict = serialize_address(address, output_id)
        return address_as_dict


class TransactionOutputAddressEndpoint(Resource):
    args = {
        'transaction_id': fields.Integer(
            required=True,
            validate=lambda blk_id: blk_id > 0,
            location='query'
        )
    }

    @use_kwargs(args)
    def get(self, transaction_id):
        transaction_output_id_list = db_session.query(TransactionOutput).filter(
            TransactionOutput.transaction_id == transaction_id).order_by(TransactionOutput.id.asc()).with_entities(
            TransactionOutput.id).all()
        output_addresses = []
        transaction_output_address_list = {'addresses': []}
        for output_id in transaction_output_id_list:
            output_address_list = db_session.query(TransactionOutputAddress).filter(
                TransactionOutputAddress.output_id == output_id.id).order_by(TransactionOutputAddress.id.asc()).all()
            for output_address in output_address_list:
                trans_output_address_as_dict = serialize_transaction_output_address(output_address.address_id,
                                                                                    output_id.id)
                output_addresses.append(trans_output_address_as_dict)

        transaction_output_address_list['addresses'] = output_addresses

        return {'transaction_id': transaction_id,
                'transaction-output_addresses': transaction_output_address_list['addresses']}
