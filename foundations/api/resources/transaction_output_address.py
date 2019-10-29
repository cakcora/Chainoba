from flask_restful import Resource
from foundations.api.models.models import Address
from foundations.api.models.models import Output as TransactionOutput
from foundations.api.models.models import OutputAddress as TransactionOutputAddress
from foundations.api.models.models import db_session
from webargs import fields
from webargs.flaskparser import use_kwargs
from foundations.api.models.ResponseCodes import ResponseCodes
from foundations.api.models.ResponseCodes import ResponseDescriptions


def serialize_address(address, output_id):
    return {'address_id': int(address.id), 'hash': address.hash.strip(),
            'public_key': address.public_key.strip(),
            'address': address.address.strip()
            }


def serialize_transaction_output_address(address_id, output_id):
    address_list = db_session.query(Address).filter(
        Address.id == address_id).order_by(Address.id.asc())
    for address in address_list:
        address_as_dict = serialize_address(address, output_id)
        return address_as_dict


def CreateErrorResponse(self, code, desc, message):
    json_data = {}
    json_data["ResponseCode"] = code
    json_data["ResponseDesc"] = desc
    json_data["ErrorMessage"] = message
    return json_data


def ValidateTransactionIdAndTransactionOutputId(self, transaction_id, transaction_output_id):
    validationErrorList = []
    if not str(transaction_id):
        validationErrorList.append(CreateErrorResponse(self, ResponseCodes.TransactionIdInputMissing.name,
                                                       str(ResponseCodes.TransactionIdInputMissing.value),
                                                       str(ResponseDescriptions.TransactionIdInputMissing.value)))
    if not str(transaction_output_id):
        validationErrorList.append(CreateErrorResponse(self, ResponseCodes.TransactionOutputIdInputMissing.name,
                                                       str(ResponseCodes.TransactionOutputIdInputMissing.value),
                                                       str(ResponseDescriptions.TransactionOutputIdInputMissing.value)))
    if not str.isdigit(transaction_id) or (str.isdigit(transaction_id) and int(transaction_id) <= 0):
        validationErrorList.append(CreateErrorResponse(self, ResponseCodes.InvalidTransactionIdInputValue.name,
                                                       str(ResponseCodes.InvalidTransactionIdInputValue.value),
                                                       str(ResponseDescriptions.InvalidTransactionIdInputValue.value)))
    if not str.isdigit(transaction_output_id) or (
            str.isdigit(transaction_output_id) and int(transaction_output_id) <= 0):
        validationErrorList.append(CreateErrorResponse(self, ResponseCodes.InvalidTransactionOutputIdInputValue.name,
                                                       str(ResponseCodes.InvalidTransactionOutputIdInputValue.value),
                                                       str(
                                                           ResponseDescriptions.InvalidTransactionOutputIdInputValue.value)))
    return validationErrorList


class GetTransactionOutputAddressByTransactionOutputId(Resource):
    args = {'transaction_id': fields.String(
        required=False,
        location='query'
    ), 'transaction_output_id': fields.String(
        required=False,
        location='query'
    )}

    @use_kwargs(args)
    def get(self, transaction_id, transaction_output_id):
        transaction_id = transaction_id.strip()
        transaction_output_id = transaction_output_id.strip()
        validation_errors = {"Errors": []}
        validations_result = ValidateTransactionIdAndTransactionOutputId(self, transaction_id, transaction_output_id)
        if validations_result is not None and len(validations_result) > 0:
            validation_errors["Errors"] = validations_result
            return validation_errors
        try:
            transaction_output_id_list = db_session.query(TransactionOutput).filter(
                TransactionOutput.transaction_id == int(transaction_id)).order_by(
                TransactionOutput.id.asc()).with_entities(
                TransactionOutput.id).all()
            trans_output_ids = []

            for output in transaction_output_id_list:
                trans_output_ids.append(output.id)
            if int(transaction_output_id) in trans_output_ids:
                output_address_list = db_session.query(TransactionOutputAddress).filter(
                    TransactionOutputAddress.output_id == transaction_output_id).order_by(
                    TransactionOutputAddress.id.asc()).all()
                total_output_addresses = 0
                output_addresses = []
                for output_address in output_address_list:
                    trans_output_address_as_dict = serialize_transaction_output_address(output_address.address_id,
                                                                                        transaction_output_id)
                    output_addresses.append(trans_output_address_as_dict)
                    total_output_addresses = total_output_addresses + 1
                if total_output_addresses > 0:
                    return {
                        'ResponseCode': "0" + str(ResponseCodes.Success.value),
                        'ResponseDesc': ResponseCodes.Success.name,
                        'transaction_id': int(transaction_id),
                        'transaction_output_id': int(transaction_output_id),
                        'num_of_output_addresses': len(output_addresses),
                        'output-addresses': output_addresses
                    }
                else:
                    return CreateErrorResponse(self, ResponseCodes.NoDataFound.name,
                                               str(ResponseCodes.NoDataFound.value),
                                               ResponseDescriptions.NoDataFound.value)
            else:
                return CreateErrorResponse(self, ResponseCodes.OutputDoesNotBelongToTransaction.name,
                                           str(ResponseCodes.OutputDoesNotBelongToTransaction.value),
                                           ResponseDescriptions.OutputDoesNotBelongToTransaction.value)
        except Exception as ex:
            return CreateErrorResponse(self, ResponseCodes.InternalError.name,
                                       str(ResponseCodes.InternalError.value),
                                       str(ex))
