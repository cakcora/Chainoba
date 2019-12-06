#!/usr/bin/env python3
# Name: total_btc_received.py
# Usecase: Graph APIs: Total Bitcoin Received
# Functionality: GET & POST

from flask_restful import Resource
from models.models import db_session, TotalBtcReceived
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_total_btc_received(total_btc_received: TotalBtcReceived):
    """
    Method to serialize total btc received
    :param total_btc_received:
    """
    return {"Id": total_btc_received.id,
            "Date": total_btc_received.date.strftime('%Y-%m-%d'),
            "BTCrecLT1": total_btc_received.btcreclt1,
            "BTCrecLT10": total_btc_received.btcreclt10,
            "BTCrecLT100": total_btc_received.btcreclt100,
            "BTCrecLT1000": total_btc_received.btcreclt1000,
            "BTCrecLT10000": total_btc_received.btcreclt10000,
            "BTCrecLT50000": total_btc_received.btcreclt50000,
            "BTCrecGT50000": total_btc_received.btcrecgt50000
            }


class TotalBtcReceivedByDateEndpoint(Resource):
    """
    Class implementing total btc received by date
    """
    get_args = {"Date": fields.Date()}
    insert_args = {
        "Date": fields.Date(),
        "BTCrecLT1": fields.Integer(),
        "BTCrecLT10": fields.Integer(),
        "BTCrecLT100": fields.Integer(),
        "BTCrecLT1000": fields.Integer(),
        "BTCrecLT10000": fields.Integer(),
        "BTCrecLT50000": fields.Integer(),
        "BTCrecGT50000": fields.Integer()
    }

    @use_kwargs(insert_args)
    def post(self, Date, BTCrecLT1=None, BTCrecLT10=None, BTCrecLT100=None, BTCrecLT1000=None, BTCrecLT10000=None,
             BTCrecLT50000=None, BTCrecGT50000=None):
        """
        Method for POST request
        :param Date:
        :param BTCrecLT1:
        :param BTCrecLT10:
        :param BTCrecLT100:
        :param BTCrecLT1000:
        :param BTCrecLT10000:
        :param BTCrecLT50000:
        :param BTCrecGT50000:
        """

        total_btc_received = TotalBtcReceived(date=Date, btcreclt1=BTCrecLT1, btcreclt10=BTCrecLT10,
                                              btcreclt100=BTCrecLT100, btcreclt1000=BTCrecLT1000,
                                              btcreclt10000=BTCrecLT10000, btcreclt50000=BTCrecLT50000,
                                              btcrecgt50000=BTCrecGT50000)
        db_session.add(total_btc_received)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "TotalBtcReceived": serialize_total_btc_received(total_btc_received)}
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
        error = self.validateTotalBtcReceivedInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        total_btc_received = db_session.query(TotalBtcReceived).filter(
            and_(TotalBtcReceived.date == Date)).one_or_none()

        if total_btc_received is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "TotalBtcReceived": serialize_total_btc_received(total_btc_received)}

        return response

    def validateTotalBtcReceivedInput(self, date):
        """
        Method to validate total btc received input date
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
