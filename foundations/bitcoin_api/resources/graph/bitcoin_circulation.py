#!/usr/bin/env python3
# Name: bitcoin_circulation.py
# Usecase: Graph APIs: Bitcoin Circulation
# Functionality: GET & POST

from flask_restful import Resource
from models.models import db_session, BitcoinCirculation
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_bitcoin_circulation(bitcoin_circulation: BitcoinCirculation):
    """
    Method to seralize bitcoin circulation data
    :param bitcoin_circulation:
    """
    return {"Id": bitcoin_circulation.id,
            "Date": bitcoin_circulation.date.strftime('%Y-%m-%d'),
            "TotBTC": bitcoin_circulation.tot_btc,
            "CircPercent": bitcoin_circulation.circ_percent,
            "NotCircuPercent": bitcoin_circulation.not_circu_percent
            }


class BitcoinCirculationByDateEndpoint(Resource):
    """
    Class implementing bitcoin circulation by date
    """
    get_args = {"Date": fields.Date()}
    insert_args = {
        "Date": fields.Date(),
        "TotBTC": fields.Float(),
        "CircPercent": fields.Float(),
        "NotCircuPercent": fields.Float(),
    }

    @use_kwargs(insert_args)
    def post(self, Date, TotBTC=None, CircPercent=None, NotCircuPercent=None):
        """
        Method for POST request
        :param Date:
        :param TotBTC:
        :param CircPercent:
        :param NotCircuPercent:
        """

        bitcoin_circulation = BitcoinCirculation(date=Date,
                                                 tot_btc=TotBTC,
                                                 circ_percent=CircPercent,
                                                 not_circu_percent=NotCircuPercent)
        db_session.add(bitcoin_circulation)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "BitcoinCirculation": serialize_bitcoin_circulation(
                            bitcoin_circulation)}
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

        error = self.validateBitcoinCirculationInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        bitcoin_circulation = db_session.query(BitcoinCirculation).filter(
            and_(BitcoinCirculation.date == Date)).one_or_none()

        if bitcoin_circulation is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "BitcoinCirculation": serialize_bitcoin_circulation(
                            bitcoin_circulation)}

        return response

    def validateBitcoinCirculationInput(self, date):
        """
        Method to validate bitcoin circulation input date
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
