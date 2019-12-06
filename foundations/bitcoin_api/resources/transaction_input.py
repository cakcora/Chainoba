#!/usr/bin/env python3
# Name: transaction_input.py
# Usecase: Bitcoin transaction input API
# Functionality: GET

from flask_restful import Resource
from models.models import Input as  TransactionInput
from models.models import db_session, Output, OutputAddress, Address
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from utils.serialize import serialize_transaction_input, serialize_address
from utils.validate import validate_transaction_ids
from webargs import fields
from webargs.flaskparser import use_kwargs


class TransactionInputEndpoint(Resource):
    """
    Class implementing transaction input API
    """
    args_transaction = {'transaction_ids': fields.List(fields.Integer())}

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
                transaction_inputs_dict = {}
                for transaction_id in sorted(transaction_ids):
                    transaction_inputs = db_session.query(TransactionInput).filter(
                        TransactionInput.transaction_id == transaction_id).all()
                    previous_output_ids = []
                    trans_input_list = []
                    total_num_of_inputs = 0

                    for transaction_input in transaction_inputs:
                        trans_input_as_dict = serialize_transaction_input(transaction_input)
                        prev_output_id = trans_input_as_dict["PreviousTransactionOutputId"]

                        if prev_output_id is not None:
                            prev_out = db_session.query(Output).filter(Output.id == prev_output_id).one()
                            trans_input_as_dict["Value"] = prev_out.value

                            previous_output_ids.append(prev_output_id)
                            prev_addresses = []
                            prev_address = db_session.query(OutputAddress, Address).filter(
                                OutputAddress.output_id == prev_output_id).filter(
                                Address.id == OutputAddress.address_id).all()
                            for address in prev_address:
                                address_as_dict = serialize_address(address.Address)
                                prev_addresses.append(address_as_dict)
                            trans_input_as_dict["InputAddresses"] = prev_addresses

                        trans_input_list.append(trans_input_as_dict)
                        total_num_of_inputs = total_num_of_inputs + 1
                    transaction_inputs_dict[transaction_id] = {"NumberOfInputs": total_num_of_inputs,
                                                               "TransactionInputs": trans_input_list}

                if total_num_of_inputs > 0:
                    response = {'ResponseCode': ResponseCodes.Success.value,
                                'ResponseDesc': ResponseCodes.Success.name,
                                'TransactionInputData': transaction_inputs_dict
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
