#!/usr/bin/env python3
# Name: assortativity_coefficient.py
# Usecase: Graph APIs: Assortativity Coefficient
# Functionality: GET & POST

from flask_restful import Resource
from models.models import db_session, AssortativityCoefficient
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_assortativity_coefficient(assortativity_coefficient: AssortativityCoefficient):
    """
    Method to seralize assortativity data
    :param assortativity_coefficient:
    :return:
    """
    return {"Id": assortativity_coefficient.id,
            "Date": assortativity_coefficient.date.strftime('%Y-%m-%d'),
            "AssortCoeff": assortativity_coefficient.assort_coeff
            }


class AssortativityCoefficientByDateEndpoint(Resource):
    """
    Class implementing assortativity coefficient endpoint
    """
    get_args = {"Date": fields.Date()}
    insert_args = {
        "Date": fields.Date(),
        "AssortCoeff": fields.Float()
    }

    @use_kwargs(insert_args)
    def post(self, Date, AssortCoeff=None):
        """
        Method for POST request
        :param Date:
        :param AssortCoeff:
        """

        assortativity_coefficient = AssortativityCoefficient(date=Date,
                                                             assort_coeff=AssortCoeff)
        db_session.add(assortativity_coefficient)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "AssortativityCoefficient": serialize_assortativity_coefficient(
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
        """
        Method for GET request
        :param Date:
        :return:
        """

        error = self.validateAssortativityCoefficientInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        assortativity_coefficient = db_session.query(AssortativityCoefficient).filter(
            and_(AssortativityCoefficient.date == Date)).one_or_none()

        if assortativity_coefficient is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "AssortativityCoefficient": serialize_assortativity_coefficient(
                            assortativity_coefficient)}

        return response

    def validateAssortativityCoefficientInput(self, date):
        """
        Method to validate assortativity coefficient input date
        :param date:
        :return:
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
