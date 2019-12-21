#!/usr/bin/env python3
# Name: clustering_coefficient.py
# Usecase: Graph APIs: Clustering Coefficient
# Functionality: GET & POST

from flask_restful import Resource
from models.models import db_session, ClusteringCoefficient
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_clustering_coefficient(clustering_coefficient: ClusteringCoefficient):
    """
    Method to serialize clustering coefficient data
    :param clustering_coefficient:
    """
    return {"Id": clustering_coefficient.id,
            "Date": clustering_coefficient.date.strftime('%Y-%m-%d'),
            "ClustCoeff": clustering_coefficient.clust_coeff
            }


class ClusteringCoefficientByDateEndpoint(Resource):
    """
    Class implementing clustering coefficient by date
    """
    get_args = {"Date": fields.Date()}
    insert_args = {
        "Date": fields.Date(),
        "ClustCoeff": fields.Float()
    }

    @use_kwargs(insert_args)
    def post(self, Date, ClustCoeff=None):
        """
        Method for POST request
        :param Date:
        :param ClustCoeff:
        """

        clustering_coefficient = ClusteringCoefficient(date=Date,
                                                       clust_coeff=ClustCoeff)
        db_session.add(clustering_coefficient)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "ClusteringCoefficient": serialize_clustering_coefficient(
                            clustering_coefficient)}
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

        error = self.validateClusteringCoefficientInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        clustering_coefficient = db_session.query(ClusteringCoefficient).filter(
            and_(ClusteringCoefficient.date == Date)).one_or_none()

        if clustering_coefficient is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "ClusteringCoefficient": serialize_clustering_coefficient(
                            clustering_coefficient)}

        return response

    def validateClusteringCoefficientInput(self, date):
        """
        Method to validate clustering coefficient input date
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
