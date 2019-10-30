from flask_restful import Resource
from models.models import Output as TransactionOutput
from models.models import db_session
from webargs import fields
import json
import requests
from webargs.flaskparser import use_kwargs
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions


def serialize_address(address, output_id):
    return {'address_id': int(address.id), 'hash': address.hash.strip(),
            'public_key': address.public_key.strip(),
            'address': address.address.strip()
            }


def serialize_transaction_output(trans_output, num_of_output_addresses, output_address_as_dict):
    return {'output_id': int(trans_output.id), 'value': trans_output.value,
            'scriptpubkey': str(trans_output.scriptpubkey),
            'index': trans_output.index,
            'script_type': str(trans_output.script_type).strip(),
            'num_of_output_addresses': num_of_output_addresses,
            'output-addresses': output_address_as_dict
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


class TransactionOutputEndpoint(Resource):
    args = {'transaction_ids': fields.List(fields.String())}

    @use_kwargs(args)
    def get(self, transaction_ids):
        transaction_ids = list(set(list(transaction_ids)))
        transaction_ids = [transaction_id.strip() for transaction_id in transaction_ids if transaction_id.strip()]
        validation_errors = {"Errors": []}
        validations_result = ValidateTransactionIds(self, transaction_ids)
        if validations_result is not None and len(validations_result) > 0:
            validation_errors["Errors"] = validations_result
            return validation_errors
        try:
            transaction_outputs_dict = {}
            for transaction_id in sorted(transaction_ids):
                transaction_outputs = db_session.query(TransactionOutput).filter(
                    TransactionOutput.transaction_id == int(transaction_id)).order_by(TransactionOutput.id.asc()).all()

                trans_output_as_list = []
                total_num_of_transaction_outputs = 0
                for trans_output in transaction_outputs:
                    output_address_response = json.loads(
                        requests.get('http://localhost:5000/bitcoin/transactions/outputs/addresses',
                                     {'transaction_id': transaction_id,
                                      'transaction_output_id': str(trans_output.id)}).text)
                    if output_address_response["ResponseCode"] == "0" + str(ResponseCodes.Success.value):
                        trans_output_as_list.append(serialize_transaction_output(trans_output,
                                                                                 int(
                                                                                                 output_address_response[
                                                                                                     "num_of_output_addresses"]),
                                                                                 output_address_response[
                                                                                     "output-addresses"]))
                    total_num_of_transaction_outputs = total_num_of_transaction_outputs + 1
                transaction_outputs_dict[transaction_id] = {
                    "num_of_outputs": total_num_of_transaction_outputs,
                    "outputs": trans_output_as_list
                }

            total_outputs = 0
            for key, value in transaction_outputs_dict.items():
                total_outputs += len(value)

            if total_outputs > 0:
                return {
                    'ResponseCode': "0" + str(ResponseCodes.Success.value),
                    'ResponseDesc': ResponseCodes.Success.name,
                    'transaction_outputs': transaction_outputs_dict
                }
            else:
                return CreateErrorResponse(self, ResponseCodes.NoDataFound.name,
                                           str(ResponseCodes.NoDataFound.value),
                                           ResponseDescriptions.NoDataFound.value)

        except Exception as ex:
            return CreateErrorResponse(self, ResponseCodes.InternalError.name,
                                       str(ResponseCodes.InternalError.value),
                                       str(ex))
