from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, BitcoinCirculation


def serialize_bitcoin_circulation(bitcoin_circulation: BitcoinCirculation):
    return {"Id": bitcoin_circulation.id,
            "Date": bitcoin_circulation.date.strftime('%Y-%m-%d'),
            "TotBTC": bitcoin_circulation.tot_btc,
            "CircPercent": bitcoin_circulation.circ_percent,
            "NotCircuPercent": bitcoin_circulation.not_circu_percent
            }


class BitcoinCirculationByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "TotBTC": fields.Float(),
        "CircPercent": fields.Float(),
        "NotCircuPercent": fields.Float(),
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             TotBTC=None,
             CircPercent=None,
             NotCircuPercent=None):

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
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
