#!/usr/bin/env python3
# Name: transaction_output_address.py
# Usecase: Bitcoin transaction output address API
# Functionality: GET

from flask_restful import Resource
from models.models import Output as TransactionOutput
from models.models import OutputAddress as TransactionOutputAddress
from models.models import db_session
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from utils.serialize import serialize_transaction_output_address
from utils.validate import validate_transaction_id_and_transaction_output_id
from webargs import fields
from webargs.flaskparser import use_kwargs


class GetTransactionOutputAddressByTransactionOutputId(Resource):
    """
    Class implementing get transaction output address by transaction output id
    """
    args_transactionoutput = {"transaction_id": fields.Integer(),
                              "transaction_output_id": fields.Integer()
                              }

    @use_kwargs(args_transactionoutput)
    def get(self, transaction_id, transaction_output_id):
        """
        Method for GET request
        :param transaction_id:
        :param transaction_output_id:
        """
        try:
            request = {"transaction_id": transaction_id, "transaction_output_id": transaction_output_id}
            response = {}
            # Validate User Input
            validations_result = validate_transaction_id_and_transaction_output_id(transaction_id,
                                                                                   transaction_output_id)
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:
                transaction_output_id_list = db_session.query(TransactionOutput).filter(
                    TransactionOutput.transaction_id == transaction_id).order_by(
                    TransactionOutput.id.asc()).with_entities(
                    TransactionOutput.id).all()
                trans_output_ids = [output.id for output in transaction_output_id_list]
                if transaction_output_id in trans_output_ids:
                    output_address_list = db_session.query(TransactionOutputAddress).filter(
                        TransactionOutputAddress.output_id == transaction_output_id).order_by(
                        TransactionOutputAddress.id.asc()).all()
                    total_num_of_output_addresses = 0
                    output_addresses = []
                    for output_address in output_address_list:
                        output_addresses.append(serialize_transaction_output_address(output_address.address_id))
                        total_num_of_output_addresses = total_num_of_output_addresses + 1

                    if total_num_of_output_addresses > 0:
                        response = {
                            "ResponseCode": ResponseCodes.Success.value,
                            "ResponseDesc": ResponseCodes.Success.name,
                            "TransactionId": transaction_id,
                            "TransactionOutputId": transaction_output_id,
                            "NumberOfOutputAddresses": len(output_addresses),
                            "OutputAddresses": output_addresses
                        }
                    else:
                        response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                                    "ResponseDesc": ResponseCodes.NoDataFound.name,
                                    "ErrorMessage": ResponseDescriptions.NoDataFound.value}
                else:
                    response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                                "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                                "ErrorMessage": ResponseDescriptions.OutputDoesNotBelongToTransaction.value}
        except Exception as ex:
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": str(ex)}
        finally:
            return response
