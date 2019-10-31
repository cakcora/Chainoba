import json
import requests
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource
from models.models import Output as TransactionOutput
from models.models import db_session
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions


def serialize_transaction_output(trans_output, num_of_output_addresses, output_address_as_dict):
    return {'OutputId': trans_output.id, 'Value': trans_output.value,
            'ScriptPublicKey': str(trans_output.scriptpubkey),
            'Index': trans_output.index,
            'ScriptType': str(trans_output.script_type).strip(),
            'NumberOfOutputAddresses': num_of_output_addresses,
            'OutputAddresses': output_address_as_dict
            }


# Validate Transaction Ids Input of TransactionOutputEndpoint endpoint
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


class TransactionOutputEndpoint(Resource):
    args_transaction = {'transaction_ids': fields.List(fields.Integer())}

    @use_kwargs(args_transaction)
    def get(self, transaction_ids):
        # Validate User Input
        validations_result = ValidateTransactionIds(self, transaction_ids)
        if validations_result is not None and len(validations_result) > 0:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ValidationErrors": validations_result}
        try:
            transaction_outputs_dict = {}
            for transaction_id in sorted(transaction_ids):
                transaction_outputs = db_session.query(TransactionOutput).filter(
                    TransactionOutput.transaction_id == transaction_id).order_by(
                    TransactionOutput.id.asc()).all()

                trans_output_as_list = []
                total_num_of_transaction_outputs = 0
                for transaction_output in transaction_outputs:
                    output_address_response = json.loads(
                        requests.get('http://localhost:5000/bitcoin/transactions/outputs/addresses',
                                     {'transaction_id': transaction_id,
                                      'transaction_output_id': transaction_output.id}).text)
                    if output_address_response["ResponseCode"] == ResponseCodes.Success.value:
                        trans_output_as_list.append(serialize_transaction_output(transaction_output,
                                                                                 output_address_response[
                                                                                     "NumberOfOutputAddresses"],
                                                                                 output_address_response[
                                                                                     "OutputAddresses"]))
                        total_num_of_transaction_outputs = total_num_of_transaction_outputs + 1
                    else:
                        return {"ResponseCode": output_address_response["ResponseCode"],
                                "ResponseDesc": output_address_response["ResponseDesc"],
                                "ErrorMessage": "Internal Error in Transaction Output Address Service : "
                                                + output_address_response["ErrorMessage"]
                                }
                transaction_outputs_dict[transaction_id] = {"NumberOfOutputs": total_num_of_transaction_outputs,
                                                            "TransactionOutputs": trans_output_as_list}

            if total_num_of_transaction_outputs > 0:
                return {'ResponseCode': ResponseCodes.Success.value,
                        'ResponseDesc': ResponseCodes.Success.name,
                        'TransactionOutputData': transaction_outputs_dict
                        }
            else:
                return {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        except Exception as ex:
            return {"ResponseCode": ResponseCodes.InternalError.value,
                    "ResponseDesc": ResponseCodes.InternalError.name,
                    "ErrorMessage": str(ex)}
