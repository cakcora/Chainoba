from flask_restful import Resource
from foundations.api.models.models import Input as  TransactionInput
from foundations.api.models.models import db_session, Output, OutputAddress, Address
from webargs import fields
from webargs.flaskparser import use_kwargs
from foundations.api.models.ResponseCodes import ResponseCodes
from foundations.api.models.ResponseCodes import ResponseDescriptions


def serialize_transaction_input(trans_input):
    return {'input_id': trans_input.id, 'prevout_hash': trans_input.prevout_hash, 'prevout_n': trans_input.prevout_n,
            'scriptsig': str(trans_input.scriptsig), 'sequence': trans_input.sequence,
            'prev_output_id': trans_input.prev_output_id
            }


# TODO
# 1. Verify for the NULL in the prev_output_id for the inputs in the transactions

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


class TransactionInputEndpoint(Resource):
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
            total_inputs = 0
            transaction_inputs_dict = {}
            for trans_id in sorted(transaction_ids):
                transaction_inputs = db_session.query(TransactionInput).filter(
                    TransactionInput.transaction_id == int(trans_id)).all()

                previous_output_ids = []
                total_inputs = 0
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
                    total_inputs = total_inputs + 1
                transaction_inputs_dict[trans_id] = {"num_of_inputs": total_inputs,
                                                     "inputs": trans_input_list}

            if total_inputs > 0:
                return {
                    'ResponseCode': "0" + str(ResponseCodes.Success.value),
                    'ResponseDesc': ResponseCodes.Success.name,
                    'transaction_inputs': transaction_inputs_dict
                }
            else:
                return CreateErrorResponse(self, ResponseCodes.NoDataFound.name,
                                           str(ResponseCodes.NoDataFound.value),
                                           ResponseDescriptions.NoDataFound.value)

        except Exception as ex:
            return CreateErrorResponse(self, ResponseCodes.InternalError.name,
                                       str(ResponseCodes.InternalError.value),
                                       str(ex))
