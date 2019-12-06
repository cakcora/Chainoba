#!/usr/bin/env python3
# Name: total_size.py
# Usecase: Graph APIs: Total Size
# Functionality: GET & POST

from flask_restful import Resource
from models.models import db_session, TransactionSize
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_transaction_size(transaction_size: TransactionSize):
    """
    Method to serialize transaction size data
    :param transaction_size:
    """
    return {"Id": transaction_size.id,
            "Date": transaction_size.date.strftime('%Y-%m-%d'),
            "TransSizeLT1": transaction_size.trans_size_lt1,
            "TransSizeLT10": transaction_size.trans_size_lt10,
            "TransSizeLT100": transaction_size.trans_size_lt100,
            "TransSizeLT5000": transaction_size.trans_size_lt5000,
            "TransSizeLT20000": transaction_size.trans_size_lt20000,
            "TransSizeLT50000": transaction_size.trans_size_lt50000,
            "TransSizeGT50000": transaction_size.trans_size_gt50000
            }


class TransactionSizeByDateEndpoint(Resource):
    """
    Class implementing transaction size by date
    """
    get_args = {"Date": fields.Date()}
    insert_args = {
        "Date": fields.Date(),
        "TransSizeLT1": fields.Integer(),
        "TransSizeLT10": fields.Integer(),
        "TransSizeLT100": fields.Integer(),
        "TransSizeLT5000": fields.Integer(),
        "TransSizeLT20000": fields.Integer(),
        "TransSizeLT50000": fields.Integer(),
        "TransSizeGT50000": fields.Integer()
    }

    @use_kwargs(insert_args)
    def post(self, Date, TransSizeLT1=None, TransSizeLT10=None, TransSizeLT100=None, TransSizeLT5000=None,
             TransSizeLT20000=None, TransSizeLT50000=None, TransSizeGT50000=None):
        """
        Method for POST request
        :param Date:
        :param TransSizeLT1:
        :param TransSizeLT10:
        :param TransSizeLT100:
        :param TransSizeLT5000:
        :param TransSizeLT20000:
        :param TransSizeLT50000:
        :param TransSizeGT50000:
        """

        transaction_size = TransactionSize(date=Date, trans_size_lt1=TransSizeLT1, trans_size_lt10=TransSizeLT10,
                                           trans_size_lt100=TransSizeLT100, trans_size_lt5000=TransSizeLT5000,
                                           trans_size_lt20000=TransSizeLT20000, trans_size_lt50000=TransSizeLT50000,
                                           trans_size_gt50000=TransSizeGT50000)
        db_session.add(transaction_size)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "TransactionSize": serialize_transaction_size(transaction_size)}
        except SQLAlchemyError as e:
            print(str(e))
            db_session.rollback()
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": ResponseDescriptions.ErrorFromDataBase.value}

        return response

    @use_kwargs(get_args)
    def get(self, Date=None):
        """
        Method for GET request
        :param Date:
        """
        error = self.validateTransactionSizeInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        transaction_size = db_session.query(TransactionSize).filter(
            and_(TransactionSize.date == Date)).one_or_none()

        if transaction_size is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "TransactionSize": serialize_transaction_size(transaction_size)}

        return response

    def validateTransactionSizeInput(self, date):
        """
        Method to validate transaction size input date
        :param date:
        """
        error = None
        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
