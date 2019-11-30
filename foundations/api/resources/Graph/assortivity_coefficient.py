from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, AssortivityCoefficient


def serialize_assortativity_coefficient(assortativity_coefficient: AssortivityCoefficient):
    return {"Id": assortativity_coefficient.id,
            "Date": assortativity_coefficient.date.strftime('%Y-%m-%d'),
            "AssortCoeff": assortativity_coefficient.assortcoeff

            }


class AssortativityCoefficientByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "AssortCoeff": fields.Float()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             AssortCoeff=None):

        assortativity_coefficient = AssortivityCoefficient(date=Date,
                                                                  assortcoeff=AssortCoeff)
        db_session.add(assortativity_coefficient)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "AssortivityCoefficient": serialize_assortativity_coefficient(
                            assortativity_coefficient)}
        except SQLAlchemyError as e:
            print(str(e))
            db_session.rollback()
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": ResponseDescriptions.ErrorFromDataBase.value}

        return response

    @use_kwargs(get_args)
    def get(self, Date=None):

        error = self.validateAssortivityCoefficientInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        assortativity_coefficient = db_session.query(AssortivityCoefficient).filter(
            and_(AssortivityCoefficient.date == Date)).one_or_none()

        if assortativity_coefficient is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "AssortivityCoefficient": serialize_assortativity_coefficient(
                            assortativity_coefficient)}

        return response

    def validateAssortivityCoefficientInput(self, date):
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
