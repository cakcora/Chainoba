#!/usr/bin/env python3
# Name: transactions.py
# Usecase: Transaction API
# Functionality: GET

import time
from datetime import datetime, timedelta

from flask_restful import Resource
from models.models import Transaction, EthereumToken, db_session
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_, or_
from utils.serialize import *
from utils.validate import *
from webargs import fields
from webargs.flaskparser import use_kwargs


class GetTransactionDataByDateAndTokenNameEndpoint(Resource):
    """
    Class implementing get transaction data by date and token name API
    """
    args = {"day": fields.Integer(),
            "month": fields.Integer(),
            "year": fields.Integer(),
            "date_offset": fields.Integer(),
            "token_name": fields.String()
            }

    @use_kwargs(args)
    def get(self, year, month, day, date_offset, token_name):
        """
        Method for GET request
        :param year:
        :param month:
        :param day:
        :param date_offset:
        :param token_name:
        """
        # Validate User Input
        try:
            request = {"day": day, "month": month, "year": year, "date_offset": date_offset, "token_name": token_name}
            validations_result = validate_input(year, month, day, date_offset)
            response = {}
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:  # all valid

                from_time = datetime(int(year), int(month), int(day))
                to_time = from_time + timedelta(days=int(date_offset))

                from_unixtime = time.mktime(from_time.timetuple())  # get the unix time to form the query
                to_unixtime = time.mktime(to_time.timetuple())

                token_data = db_session.query(EthereumToken).filter(
                    EthereumToken.token_name == token_name).first()

                # perform the query
                transaction_data = db_session.query(Transaction).filter(
                    and_(Transaction.ntime >= from_unixtime, Transaction.ntime
                         <= to_unixtime)).order_by(Transaction.ntime.asc())

                if transaction_data is not None and len(list(transaction_data)) != 0:
                    transaction_list = []
                    for transaction in transaction_data:
                        transaction_list.append(serialize_transaction(transaction))
                        response = {
                            "ResponseCode": ResponseCodes.Success.value,
                            "ResponseDesc": ResponseCodes.Success.name,
                            "FromDate": from_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "ToDate": to_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "TokenId": token_data.token_id,
                            "TokenName": token_data.token_name,
                            "NumberOfTransactions": len(transaction_list),
                            "Transactions": transaction_list}
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


class GetTransactionDataByNodeEndpoint(Resource):
    """
    Class implementing get transaction data by node API
    """
    args = {"node_address": fields.Integer()}

    @use_kwargs(args)
    def get(self, node_address):
        """
        Method for GET request
        :param node_address:
        """
        # Validate User Input
        try:
            request = {"node_address": node_address}
            validations_result = validate_node_input(node_address)
            response = {}
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:  # all valid
                # perform the query
                transaction_data = db_session.query(Transaction).filter(
                    or_(Transaction.from_node == node_address, Transaction.to_node
                        == node_address)).order_by(Transaction.from_node.asc())

                if transaction_data is not None and len(list(transaction_data)) != 0:
                    transaction_list = []
                    for transaction in transaction_data:
                        token_data = db_session.query(EthereumToken).filter(
                            EthereumToken.token_id == transaction.token_id).first()
                        transaction_list.append(serialize_transaction_with_token_data(transaction, token_data))
                    response = {
                        "ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "NumberOfTransactions": len(transaction_list),
                        "Transactions": transaction_list}
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
