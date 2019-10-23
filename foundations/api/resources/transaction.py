import json

import requests
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_transaction(transaction):
    return {'id': transaction.id, 'hash': transaction.hash, 'version': transaction.version,
            'locktime': transaction.locktime, 'version': transaction.block_id}


args_transaction = {
    'transaction_ids': fields.List(fields.Integer(validate=lambda trans_id: trans_id > 0))
}


class TransactionEndpoint(Resource):

    @use_kwargs(args_transaction)
    def get(self, transaction_ids):
        block_transactions_dict = {}
        if len(transaction_ids) > 10:
            return {'message': 'Transaction IDs limit is 10'}, 400

        for transaction in transaction_ids:
            trans_as_dict = {}
            input_response = json.loads(requests.get('http://localhost:5000/bitcoin/transactions/inputs',
                                                     json={'transaction_ids': [transaction]}).text)

            trans_as_dict["inputs"] = input_response["transaction_inputs"][str(transaction)]

            output_response = json.loads(requests.get('http://localhost:5000/bitcoin/transactions/outputs',
                                                      json={'transaction_ids': [transaction]}).text)
            trans_as_dict["outputs"] = output_response["transaction_outputs"][str(transaction)]

            block_transactions_dict[transaction] = trans_as_dict

        return {'blocks': block_transactions_dict}
