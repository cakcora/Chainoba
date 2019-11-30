from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, PearsonCoefficient


def serialize_pearson_coefficient(pearson_coefficient: PearsonCoefficient):
    return {"Id": pearson_coefficient.id,
            "Date": pearson_coefficient.date.strftime('%Y-%m-%d'),
            "PearCoeff": pearson_coefficient.pear_coeff

            }


class PearsonCoefficientByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "PearCoeff": fields.Float()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             PearCoeff=None):

        pearson_coefficient = PearsonCoefficient(date=Date,
                                                 pearcoeff=PearCoeff)
        db_session.add(pearson_coefficient)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "PearsonCoefficient": serialize_pearson_coefficient(
                            pearson_coefficient)}
        except SQLAlchemyError as e:
            print(str(e))
            db_session.rollback()
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": ResponseDescriptions.ErrorFromDataBase.value}

        return response

    @use_kwargs(get_args)
    def get(self, Date=None):

        error = self.validatePearsonCoefficientInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        pearson_coefficient = db_session.query(PearsonCoefficient).filter(
            and_(PearsonCoefficient.date == Date)).one_or_none()

        if pearson_coefficient is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "PearsonCoefficient": serialize_pearson_coefficient(
                            pearson_coefficient)}

        return response

    def validatePearsonCoefficientInput(self, date):
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
