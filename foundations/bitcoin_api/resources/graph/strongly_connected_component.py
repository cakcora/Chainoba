#!/usr/bin/env python3
# Name: strongly_connected_component.py
# Usecase: Graph APIs: Strongly Connected Component
# Functionality: GET & POST

from flask_restful import Resource
from models.models import db_session, StronglyConnectedComponent
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_strongly_connected_component(strongly_connected_component: StronglyConnectedComponent):
    """
    Method to serialize strongly connected component
    :param strongly_connected_component:
    """
    return {"Id": strongly_connected_component.id,
            "Date": strongly_connected_component.date.strftime('%Y-%m-%d'),
            "SCC": strongly_connected_component.scc
            }


class StronglyConnectedComponentByDateEndpoint(Resource):
    """
    Class implementing strongly connected component by date
    """
    get_args = {"Date": fields.Date()}
    insert_args = {
        "Date": fields.Date(),
        "SCC": fields.Integer()
    }

    @use_kwargs(insert_args)
    def post(self, Date, SCC=None):
        """
        Method for POST request
        :param Date:
        :param SCC:
        """

        strongly_connected_component = StronglyConnectedComponent(date=Date,
                                                                  scc=SCC)
        db_session.add(strongly_connected_component)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "StronglyConnectedComponent": serialize_strongly_connected_component(
                            strongly_connected_component)}
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

        error = self.validateStronglyConnectedComponentInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        strongly_connected_component = db_session.query(StronglyConnectedComponent).filter(
            and_(StronglyConnectedComponent.date == Date)).one_or_none()

        if strongly_connected_component is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "StronglyConnectedComponent": serialize_strongly_connected_component(
                            strongly_connected_component)}

        return response

    def validateStronglyConnectedComponentInput(self, date):
        """
        Method to validate strongly connected component input date
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
