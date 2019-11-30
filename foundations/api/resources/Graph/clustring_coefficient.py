from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, ClusteringCoefficient


def serialize_clustering_coefficient(clustering_coefficient: ClusteringCoefficient):
    return {"Id": clustering_coefficient.id,
            "Date": clustering_coefficient.date.strftime('%Y-%m-%d'),
            "ClustCoeff": clustering_coefficient.clustcoeff

            }


class ClusteringCoefficientByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "ClustCoeff": fields.Float()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             ClustCoeff=None):

        clustering_coefficient = ClusteringCoefficient(date=Date,
                                                     clustcoeff=ClustCoeff)
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
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
