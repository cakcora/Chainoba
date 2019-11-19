from sqlalchemy import or_
from sqlalchemy import and_
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs
import time
from datetime import datetime, timedelta
from foundations.EthereumAPI.models.models import Transaction, db_session
from foundations.EthereumAPI.models.ResponseCodes import ResponseCodes
from foundations.EthereumAPI.models.ResponseCodes import ResponseDescriptions


def serialize_transaction(transaction_data):
    return {"TransactionId": transaction_data.id,
            "InputNodeAddress": transaction_data.input_address,
            "OutputNodeAddress": transaction_data.output_address,
            "Timestamp": datetime.utcfromtimestamp(transaction_data.ntime).strftime('%Y-%m-%d %H:%M:%S'),
            "TokenAmount": transaction_data.token_amount
            }


def ValidateNodeInput(self, node_address):
    validationErrorList = []
    if node_address <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidNodeAddress.value})
    return validationErrorList


def ValidateInput(self, year, month, day, date_offset):
    validationErrorList = []
    if day > 31 or day <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidDayInput.value})
    if year > int(datetime.now().year) or year < 2016:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidYearInput.value})
    if month > 12 or month <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidMonthInput.value})
    if date_offset > 31 or date_offset <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidDateOffsetInput.value})
    return validationErrorList


class GetTransactionDataByDateEndpoint(Resource):
    args = {"day": fields.Integer(),
            "month": fields.Integer(),
            "year": fields.Integer(),
            "date_offset": fields.Integer()
            }

    @use_kwargs(args)
    def get(self, year, month, day, date_offset):
        # Validate User Input
        try:
            request = {"day": day, "month": month, "year": year, "date_offset": date_offset}
            validations_result = ValidateInput(self, year, month, day, date_offset)
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
            # file = open('/EthereumAPI/Logs/GetTransactionDataByDateLog.txt', 'w')
            # file.write("Time:" + str(datetime.now()) + "\r\n")
            # file.write("Request : " + request + "\r\n")
            # file.write("Response : " + response + "\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.close()
            return response


class GetTransactionDataByNodeEndpoint(Resource):
    args = {"node_address": fields.Integer()
            }

    @use_kwargs(args)
    def get(self, node_address):
        # Validate User Input
        try:
            request = {"node_address": node_address}
            validations_result = ValidateNodeInput(self, node_address)
            response = {}
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:  # all valid

                # perform the query
                transaction_data = db_session.query(Transaction).filter(
                    or_(Transaction.input_address == node_address, Transaction.output_address
                         == node_address)).order_by(Transaction.input_address.asc())
                if transaction_data is not None and len(list(transaction_data)) != 0:
                    transaction_list = []
                    for transaction in transaction_data:
                        transaction_list.append(serialize_transaction(transaction))
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
            # file = open('/EthereumAPI/Logs/GetTransactionDataByNodeLog.txt', 'w')
            # file.write("Time:" + str(datetime.now()) + "\r\n")
            # file.write("Request : " + request + "\r\n")
            # file.write("Response : " + response + "\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.close()
            return response
