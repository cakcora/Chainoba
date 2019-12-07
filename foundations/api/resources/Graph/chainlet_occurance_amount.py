from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, ChainletsOccuranceAmount


def serialize_chainlets_occurance_amount(chainlets_occurance_amount: ChainletsOccuranceAmount):
    return {"Id": chainlets_occurance_amount.id,
            "Date": chainlets_occurance_amount.date.strftime('%Y-%m-%d'),
            "SplitChltAmt": chainlets_occurance_amount.split_chlt_amt,
            "MergeChltAmt": chainlets_occurance_amount.merge_chlt_amt,
            "TransitionChltAmt": chainlets_occurance_amount.transition_chlt_amt
            }


class ChainletsOccuranceAmountByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "SplitChltAmt": fields.Float(),
        "MergeChltAmt": fields.Float(),
        "TransitionChltAmt": fields.Float()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             SplitChltAmt=None,
             MergeChltAmt=None,
             TransitionChltAmt=None):

        chainlets_occurance_amount = ChainletsOccuranceAmount(date=Date,
                                                              split_chlt_amt=SplitChltAmt,
                                                              merge_chlt_amt=MergeChltAmt,
                                                              transition_chlt_amt=TransitionChltAmt
                                                              )
        db_session.add(chainlets_occurance_amount)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "ChainletsOccuranceAmount": serialize_chainlets_occurance_amount(chainlets_occurance_amount)}
        except SQLAlchemyError as e:
            print(str(e))
            db_session.rollback()
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": ResponseDescriptions.ErrorFromDataBase.value}

        return response

    @use_kwargs(get_args)
    def get(self, Date=None):

        error = self.validateChainletsOccuranceAmountInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        chainlets_occurance_amount = db_session.query(ChainletsOccuranceAmount).filter(
            and_(ChainletsOccuranceAmount.date == Date)).one_or_none()

        if chainlets_occurance_amount is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "ChainletsOccuranceAmount": serialize_chainlets_occurance_amount(chainlets_occurance_amount)}

        return response

    def validateChainletsOccuranceAmountInput(self, date):
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
