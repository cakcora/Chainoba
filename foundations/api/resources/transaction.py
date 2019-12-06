#!/usr/bin/env python3
# Name: transaction.py
# Usecase: Bitcoin transaction API
# Functionality: GET

import json

import requests
from common.utils import serialize_transactions
from flask_restful import Resource
from models.models import Transaction, db_session
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from webargs import fields
from webargs.flaskparser import use_kwargs


def ValidateTransactionHash(transaction_hash):
    """
    Validate transaction hash data
    :param self:
    :param transaction_hash:
    """
    validationErrorList = []
    if not transaction_hash or len(transaction_hash) == 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.TransactionHashInputMissing.value})
    return validationErrorList


def ValidateTransactionIds(transaction_ids):
    """
    Method to validate transaction ids
    :param transaction_ids:
    """
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
    """
    Class implementing transaction by hash API
    """
    args_transaction_by_hash = {
        "transaction_hash": fields.String()
    }

    @use_kwargs(args_transaction_by_hash)
    def get(self, transaction_hash):
        """
        Method for GET request
        :param transaction_hash:
        :return:
        """
        try:
            transaction_hash = transaction_hash.strip()
            request = {"transaction_hash": transaction_hash}
            response = {}
            # Validate User Input
            validations_result = ValidateTransactionHash(transaction_hash)
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:
                transaction = db_session.query(Transaction).filter(Transaction.hash == transaction_hash).one_or_none()
                if transaction is None:
                    response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                                "ResponseDesc": ResponseCodes.NoDataFound.name,
                                "ErrorMessage": ResponseDescriptions.NoDataFound.value}
                else:
                    input_response = json.loads(requests.get('http://localhost:5000/bitcoin/transactions/inputs',
                                                             json={'transaction_ids': [transaction.id]}).text)

                    output_response = json.loads(requests.get('http://localhost:5000/bitcoin/transactions/outputs',
                                                              json={'transaction_ids': [transaction.id]}).text)

                    if input_response["ResponseCode"] == ResponseCodes.Success.value and \
                            output_response["ResponseCode"] == ResponseCodes.Success.value:
                        transaction_json = serialize_transactions(transaction, input_response, output_response,
                                                                  transaction.id)
                        response = {
                            "ResponseCode": ResponseCodes.Success.value,
                            "ResponseDesc": ResponseCodes.Success.name,
                            "TransactionData": transaction_json
                        }
                        if transaction_json is None or (
                                transaction_json is not None and
                                (input_response["TransactionInputData"][str(transaction.id)])["NumberOfInputs"] == 0 and
                                (output_response["TransactionOutputData"][str(transaction.id)])[
                                    "NumberOfOutputs"] == 0):
                            response = {
                                "ResponseCode": ResponseCodes.NoDataFound.value,
                                "ResponseDesc": ResponseCodes.NoDataFound.name,
                                "ErrorMessage": ResponseDescriptions.NoDataFound.value
                            }
                    elif input_response["ResponseCode"] != ResponseCodes.Success.value:
                        response = {"ResponseCode": input_response["ResponseCode"],
                                    "ResponseDesc": input_response["ResponseDesc"],
                                    "ErrorMessage": "Internal Error in Transaction Input Service : "
                                                    + input_response["ErrorMessage"]
                                    }
                    elif output_response["ResponseCode"] != ResponseCodes.Success.value:
                        response = {"ResponseCode": output_response["ResponseCode"],
                                    "ResponseDesc": output_response["ResponseDesc"],
                                    "ErrorMessage": "Internal Error in Transaction Output Service : "
                                                    + output_response["ErrorMessage"]
                                    }

        except Exception as ex:
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": str(ex)}
        finally:
            return response


class TransactionEndpoint(Resource):
    """
    Class implementing transactions API
    """
    args_transaction = {
        'transaction_ids': fields.List(fields.Integer())
    }

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
            validations_result = ValidateTransactionIds(transaction_ids)
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:
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
                        block_transactions_dict[transaction_id] = serialize_transactions(transaction_data[0],
                                                                                         input_response,
                                                                                         output_response,
                                                                                         transaction_id)
                        if trans_as_dict is None or (
                                trans_as_dict is not None and
                                (input_response["TransactionInputData"][str(transaction_id)])["NumberOfInputs"] == 0 and
                                (output_response["TransactionOutputData"][str(transaction_id)])[
                                    "NumberOfOutputs"] == 0):
                            num_of_empty_transactions = num_of_empty_transactions + 1

                    elif input_response["ResponseCode"] != ResponseCodes.Success.value:
                        response = {"ResponseCode": input_response["ResponseCode"],
                                    "ResponseDesc": input_response["ResponseDesc"],
                                    "ErrorMessage": "Internal Error in Transaction Input Service : "
                                                    + input_response["ErrorMessage"]
                                    }
                        break
                    elif output_response["ResponseCode"] != ResponseCodes.Success.value:
                        response = {"ResponseCode": output_response["ResponseCode"],
                                    "ResponseDesc": output_response["ResponseDesc"],
                                    "ErrorMessage": "Internal Error in Transaction Output Service : "
                                                    + output_response["ErrorMessage"]
                                    }
                        break

                if num_of_empty_transactions != len(transaction_ids):
                    response = {
                        "ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "TransactionData": block_transactions_dict
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
