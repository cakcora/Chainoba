#!/usr/bin/env python3
# Name: most_active_entity.py
# Usecase: Graph APIs: Most Active Entity
# Functionality: GET & POST

from flask_restful import Resource
from models.models import db_session, MostActiveEntity
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_most_active_entity(most_active_entity: MostActiveEntity):
    """
    Method to serialize most active entity
    :param most_active_entity:
    """
    return {"Id": most_active_entity.id,
            "Date": most_active_entity.date.strftime('%Y-%m-%d'),
            "Addr": most_active_entity.addr,
            "NoOfTrans": most_active_entity.no_of_trans
            }


class MostActiveEntityByDateEndpoint(Resource):
    """
    Class implementing most active entity by date
    """
    get_args = {"Date": fields.Date()}
    insert_args = {
        "Date": fields.Date(),
        "Addr": fields.String(),
        "NoOfTrans": fields.Integer()
    }

    @use_kwargs(insert_args)
    def post(self, Date, Addr=None, NoOfTrans=None):
        """
        Method for POSt request
        :param Date:
        :param Addr:
        :param NoOfTrans:
        """

        most_active_entity = MostActiveEntity(date=Date,
                                              addr=Addr,
                                              no_of_trans=NoOfTrans)
        db_session.add(most_active_entity)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "MostActiveEntity": serialize_most_active_entity(
                            most_active_entity)}
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
        error = self.validateMostActiveEntityInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        most_active_entity = db_session.query(MostActiveEntity).filter(
            and_(MostActiveEntity.date == Date)).one_or_none()

        if most_active_entity is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "MostActiveEntity": serialize_most_active_entity(
                            most_active_entity)}

        return response

    def validateMostActiveEntityInput(self, date):
        """
        Method to validate active entity input
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
