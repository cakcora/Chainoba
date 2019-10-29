import json

import requests
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs
from foundations.api.models.models import Transaction, db_session
from foundations.api.models.ResponseCodes import ResponseCodes
from foundations.api.models.ResponseCodes import ResponseDescriptions


def serialize_transaction(transaction_data, input_response, output_response, transaction_id):
    return {'transaction_id': int(transaction_id),
            'hash': transaction_data.hash, 'version': transaction_data.version,
            'locktime': transaction_data.locktime, 'version': transaction_data.block_id,
            'num_of_inputs': (input_response["transaction_inputs"][str(transaction_id)])['num_of_inputs'],
            'inputs': (input_response["transaction_inputs"][str(transaction_id)])['inputs'],
            'num_of_outputs': (output_response["transaction_outputs"][str(transaction_id)])['num_of_outputs'],
            'outputs': (output_response["transaction_outputs"][str(transaction_id)])['outputs']
            }


args_transaction = {
    'transaction_ids': fields.List(fields.Integer(validate=lambda trans_id: trans_id > 0))
}


def CreateErrorResponse(self, code, desc, message):
    json_data = {}
    json_data["ResponseCode"] = code
    json_data["ResponseDesc"] = desc
    json_data["ErrorMessage"] = message
    return json_data


def ValidateTransactionIds(self, transaction_ids):
    validationErrorList = []

    if len(transaction_ids) == 0:
        validationErrorList.append(CreateErrorResponse(self, ResponseCodes.TransactionIdsInputMissing.name,
                                                       str(ResponseCodes.TransactionIdsInputMissing.value),
                                                       str(ResponseDescriptions.TransactionIdsInputMissing.value)))
    if len(transaction_ids) > 10:
        validationErrorList.append(CreateErrorResponse(self, ResponseCodes.NumberOfTransactionIdsLimitExceeded.name,
                                                       str(ResponseCodes.NumberOfTransactionIdsLimitExceeded.value),
                                                       str(
                                                           ResponseDescriptions.NumberOfTransactionIdsLimitExceeded.value)))
    if len(transaction_ids) > 0:
        for transaction_id in transaction_ids:
            if not str.isdigit(transaction_id) or (str.isdigit(str(transaction_id)) and int(transaction_id) <= 0):
                validationErrorList.append(
                    CreateErrorResponse(self, ResponseCodes.InvalidTransactionIdsInputValues.name,
                                        str(ResponseCodes.InvalidTransactionIdsInputValues.value),
                                        str(
                                            ResponseDescriptions.InvalidTransactionIdsInputValues.value)))
                break
    return validationErrorList


class TransactionEndpoint(Resource):
    args_transaction = {
        'transaction_ids': fields.List(fields.String())
    }

    @use_kwargs(args_transaction)
    def get(self, transaction_ids):
        transaction_ids = list(set(list(transaction_ids)))
        transaction_ids = [transaction_id.strip() for transaction_id in transaction_ids if transaction_id.strip()]
        validation_errors = {"Errors": []}
        validations_result = ValidateTransactionIds(self, transaction_ids)
        if validations_result is not None and len(validations_result) > 0:
            validation_errors["Errors"] = validations_result
            return validation_errors
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
                                                          json={'transaction_ids': [str(transaction_id)]}).text)

                if (input_response["ResponseCode"] == "0" + str(ResponseCodes.Success.value) and output_response[
                    "ResponseCode"] == "0" + str(ResponseCodes.Success.value)):
                    block_transactions_dict[transaction_id] = serialize_transaction(transaction_data[0], input_response,
                                                                                    output_response, transaction_id)
                    if trans_as_dict is None or (
                            trans_as_dict is not None and (input_response["transaction_inputs"][str(transaction_id)])[
                        'num_of_inputs'] == 0 and (output_response["transaction_outputs"][str(transaction_id)])[
                                'num_of_outputs'] == 0):
                        num_of_empty_transactions = num_of_empty_transactions + 1
                else:
                    if input_response["ResponseCode"] != "0" + str(ResponseCodes.Success.value):
                        return CreateErrorResponse(self, str(input_response["ResponseCode"]),
                                                   str(input_response["ResponseDesc"]),
                                                   "Error in Transaction Input Service : " + str(
                                                       input_response["ErrorMessage"]))
                    if output_response["ResponseCode"] != "0" + str(ResponseCodes.Success.value):
                        return CreateErrorResponse(self, str(output_response["ResponseCode"]),
                                                   str(output_response["ResponseDesc"]),
                                                   "Error in Transaction Output Service : " + str(
                                                       output_response["ErrorMessage"]))

            if num_of_empty_transactions != len(transaction_ids):
                return {
                    'ResponseCode': "0" + str(ResponseCodes.Success.value),
                    'ResponseDesc': ResponseCodes.Success.name,
                    'transaction_data': block_transactions_dict
                }
            else:
                return CreateErrorResponse(self, ResponseCodes.NoDataFound.name,
                                           str(ResponseCodes.NoDataFound.value),
                                           ResponseDescriptions.NoDataFound.value)
        except Exception as ex:
            return CreateErrorResponse(self, ResponseCodes.InternalError.name,
                                       str(ResponseCodes.InternalError.value),
                                       str(ex))
