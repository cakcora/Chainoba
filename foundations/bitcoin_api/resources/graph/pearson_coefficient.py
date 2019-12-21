#!/usr/bin/env python3
# Name: pearson_coefficient.py
# Usecase: Graph APIs: Pearson Coefficient
# Functionality: GET & POST

from flask_restful import Resource
from models.models import db_session, PearsonCoefficient
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_pearson_coefficient(pearson_coefficient: PearsonCoefficient):
    """
    Method to serialize pearson coefficient
    :param pearson_coefficient:
    """
    return {"Id": pearson_coefficient.id,
            "Date": pearson_coefficient.date.strftime('%Y-%m-%d'),
            "PearCoeff": pearson_coefficient.pear_coeff
            }


class PearsonCoefficientByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()}
    insert_args = {
        "Date": fields.Date(),
        "PearCoeff": fields.Float()
    }

    @use_kwargs(insert_args)
    def post(self, Date, PearCoeff=None):
        """
        Method for POST request
        :param Date:
        :param PearCoeff:
        """

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
        """
        Method for GET request
        :param Date:
        """
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
        """
        Method to validate pearson coefficient input date
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
