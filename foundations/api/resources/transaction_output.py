#!/usr/bin/env python3
# Name: transaction_output.py
# Usecase: Bitcoin transaction output API
# Functionality: GET

import json

import requests
from flask_restful import Resource
from models.models import Output as TransactionOutput
from models.models import db_session
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from utils.serialize import serialize_transaction_output
from utils.validate import validate_transaction_ids
from webargs import fields
from webargs.flaskparser import use_kwargs


class TransactionOutputEndpoint(Resource):
    """
    Class implementing transaction output API
    """
    args_transaction = {"transaction_ids": fields.List(fields.Integer())}

    @use_kwargs(args_transaction)
    def get(self, transaction_ids):
        """
        Method for GET request
        :param transaction_ids:
        """
        try:
            transaction_ids = list(set(list(transaction_ids)))
            request = {"transaction_ids": transaction_ids}
            response = {}
            # Validate User Input
            validations_result = validate_transaction_ids(transaction_ids)
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:
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
                            response = {"ResponseCode": output_address_response["ResponseCode"],
                                        "ResponseDesc": output_address_response["ResponseDesc"],
                                        "ErrorMessage": "Internal Error in Transaction Output Address Service : "
                                                        + output_address_response["ErrorMessage"]
                                        }
                            break
                    transaction_outputs_dict[transaction_id] = {"NumberOfOutputs": total_num_of_transaction_outputs,
                                                                "TransactionOutputs": trans_output_as_list}

                if total_num_of_transaction_outputs > 0:
                    response = {"ResponseCode": ResponseCodes.Success.value,
                                "ResponseDesc": ResponseCodes.Success.name,
                                "TransactionOutputData": transaction_outputs_dict
                                }
                else:
                    response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                                "ResponseDesc": ResponseCodes.NoDataFound.name,
                                "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        except Exception as ex:
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": str(ex)}
        finally:
            return response
