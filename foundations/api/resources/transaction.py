import json
import requests
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.models import Transaction, db_session
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions


def serialize_transaction(transaction_data, input_response, output_response, transaction_id):
    return {'TransactionId': transaction_id,
            'Hash': transaction_data.hash.strip(), 'Version': transaction_data.version,
            'LockTime': transaction_data.locktime, 'BlockId': transaction_data.block_id,
            'NumberOfInputs': (input_response["TransactionInputData"][str(transaction_id)])['NumberOfInputs'],
            'TransactionInputs': (input_response["TransactionInputData"][str(transaction_id)])['TransactionInputs'],
            'NumberOfOutputs': (output_response["TransactionOutputData"][str(transaction_id)])['NumberOfOutputs'],
            'TransactionOutputs': (output_response["TransactionOutputData"][str(transaction_id)])['TransactionOutputs']
            }


# Validate Transaction Ids Input of TransactionEndpoint endpoint
def ValidateTransactionIds(self, transaction_ids):
    validationErrorList = []
    if len(transaction_ids) == 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.TransactionIdsInputMissing.value})
    if len(transaction_ids) > 10:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.NumberOfTransactionIdsLimitExceeded.value})
    if len(transaction_ids) > 0:
        for transaction_id in transaction_ids:
            if transaction_id <= 0:
                validationErrorList.append(
                    {"ErrorMessage": ResponseDescriptions.InvalidTransactionIdsInputValues.value})
                break
    return validationErrorList


class TransactionByHashEndpoint(Resource):
    args_transaction_by_hash = {
        'transaction_hash': fields.String()
    }

    @use_kwargs(args_transaction_by_hash)
    def get(self, transaction_hash):
        transaction = db_session.query(Transaction).filter(Transaction.hash == transaction_hash).one_or_none()
        if transaction is None:
            return {"ResponseCode": ResponseCodes.NoDataFound.value,
                    "ResponseDesc": ResponseCodes.NoDataFound.name,
                    "ErrorMessage": ResponseDescriptions.NoDataFound.value}

        input_response = json.loads(requests.get('http://localhost:5000/bitcoin/transactions/inputs',
                                                 json={'transaction_ids': [transaction.id]}).text)

        output_response = json.loads(requests.get('http://localhost:5000/bitcoin/transactions/outputs',
                                                  json={'transaction_ids': [transaction.id]}).text)
        transaction_json = serialize_transaction(transaction, input_response, output_response, transaction.id)
        return {
            'ResponseCode': ResponseCodes.Success.value,
            'ResponseDesc': ResponseCodes.Success.name,
            'TransactionData': transaction_json
        }


class TransactionEndpoint(Resource):
    args_transaction = {
        'transaction_ids': fields.List(fields.Integer())
    }

    @use_kwargs(args_transaction)
    def get(self, transaction_ids):
        # Validate User Input
        validations_result = ValidateTransactionIds(self, transaction_ids)
        if validations_result is not None and len(validations_result) > 0:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ValidationErrors": validations_result}
        try:
            block_transactions_dict = {}
            num_of_empty_transactions = 0
            for transaction_id in sorted(transaction_ids):
                trans_as_dict = {}
                transaction_data = db_session.query(Transaction).filter(Transaction.id == transaction_id).order_by(
                    Transaction.id.asc())
                input_response = json.loads(requests.get('http://localhost:5000/bitcoin/transactions/inputs',
                                                         json={'transaction_ids': [transaction_id]}).text)

                output_response = json.loads(requests.get('http://localhost:5000/bitcoin/transactions/outputs',
                                                          json={'transaction_ids': [transaction_id]}).text)

                if input_response["ResponseCode"] == ResponseCodes.Success.value and \
                        output_response["ResponseCode"] == ResponseCodes.Success.value:
                    block_transactions_dict[transaction_id] = serialize_transaction(transaction_data[0], input_response,
                                                                                    output_response, transaction_id)
                    if trans_as_dict is None or (
                            trans_as_dict is not None and
                            (input_response["TransactionInputData"][str(transaction_id)])['NumberOfInputs'] == 0 and
                            (output_response["TransactionOutputData"][str(transaction_id)])['NumberOfOutputs'] == 0):
                        num_of_empty_transactions = num_of_empty_transactions + 1

                elif input_response["ResponseCode"] != ResponseCodes.Success.value:
                    return {"ResponseCode": input_response["ResponseCode"],
                            "ResponseDesc": input_response["ResponseDesc"],
                            "ErrorMessage": "Internal Error in Transaction Input Service : "
                                            + input_response["ErrorMessage"]
                            }
                elif output_response["ResponseCode"] != ResponseCodes.Success.value:
                    return {"ResponseCode": output_response["ResponseCode"],
                            "ResponseDesc": output_response["ResponseDesc"],
                            "ErrorMessage": "Internal Error in Transaction Output Service : "
                                            + output_response["ErrorMessage"]
                            }

            if num_of_empty_transactions != len(transaction_ids):
                return {
                    'ResponseCode': ResponseCodes.Success.value,
                    'ResponseDesc': ResponseCodes.Success.name,
                    'TransactionData': block_transactions_dict
                }
            else:
                return {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        except Exception as ex:
            return {"ResponseCode": ResponseCodes.InternalError.value,
                    "ResponseDesc": ResponseCodes.InternalError.name,
                    "ErrorMessage": str(ex)}
