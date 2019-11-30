from datetime import datetime
from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, ChainletsOccurance


def serialize_chainlets_occurance(chainlets_occurance: ChainletsOccurance):
    return {"Id": chainlets_occurance.id,
            "Date": chainlets_occurance.date.strftime('%Y-%m-%d'),
            "SplitChlt": chainlets_occurance.split_chlt,
            "MergeChlt": chainlets_occurance.merge_chlt,
            "TransitionChlt": chainlets_occurance.transition_chlt
            }


class ChainletsOccuranceByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "SplitChlt": fields.Integer(),
        "MergeChlt": fields.Integer(),
        "TransitionChlt": fields.Integer()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             SplitChlt=None,
             MergeChlt=None,
             TransitionChlt=None):

        chainlets_occurance = ChainletsOccurance(date=Date,
                                                 split_chlt=SplitChlt,
                                                 merge_chlt=MergeChlt,
                                                 transition_chlt=TransitionChlt
                                                 )
        db_session.add(chainlets_occurance)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "ChainletsOccurance": serialize_chainlets_occurance(chainlets_occurance)}
        except SQLAlchemyError as e:
            print(str(e))
            db_session.rollback()
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": ResponseDescriptions.ErrorFromDataBase.value}

        return response

    @use_kwargs(get_args)
    def get(self, Date=None):

        error = self.validateChainletsOccuranceInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        chainlets_occurance = db_session.query(ChainletsOccurance).filter(
            and_(ChainletsOccurance.date == Date)).one_or_none()

        if chainlets_occurance is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "ChainletsOccurance": serialize_chainlets_occurance(chainlets_occurance)}

        return response

    def validateChainletsOccuranceInput(self, date):
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
