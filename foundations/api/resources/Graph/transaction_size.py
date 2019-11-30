
from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, TransactionSize


def serialize_transaction_size(transaction_size: TransactionSize):
    return {"Id": transaction_size.id,
            "Date": transaction_size.date.strftime('%Y-%m-%d'),
            "TransSizeLT1": transaction_size.transsizelt1,
            "TransSizeLT10": transaction_size.transsizelt10,
            "TransSizeLT100": transaction_size.transsizelt100,
            "TransSizeLT5000": transaction_size.transsizelt5000,
            "TransSizeLT20000": transaction_size.transsizelt20000,
            "TransSizeLT50000": transaction_size.transsizelt50000,
            "TransSizeGT50000": transaction_size.transsizegt50000
            }


class TransactionSizeByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
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
    def post(self, Date,
             TransSizeLT1=None,
             TransSizeLT10=None,
             TransSizeLT100=None,
             TransSizeLT5000=None,
             TransSizeLT20000=None,
             TransSizeLT50000=None,
             TransSizeGT50000=None):

        transaction_size = TransactionSize(date=Date,
                                              transsizelt1=TransSizeLT1,
                                              transsizelt10=TransSizeLT10,
                                              transsizelt100=TransSizeLT100,
                                              transsizelt5000=TransSizeLT5000,
                                              transsizelt20000=TransSizeLT20000,
                                              transsizelt50000=TransSizeLT50000,
                                              transsizegt50000=TransSizeGT50000
                                              )
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
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
