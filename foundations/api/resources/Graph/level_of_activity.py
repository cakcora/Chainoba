from flask_restful import Resource
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from models.models import db_session, ActivityLevel
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_activity_level(activity_level: ActivityLevel):
    return {"Id": activity_level.id,
            "Date": activity_level.date.strftime('%Y-%m-%d'),
            "LOALT2": activity_level.loalt2,
            "LOALT5": activity_level.loalt5,
            "LOALT10": activity_level.loalt10,
            "LOALT100": activity_level.loalt100,
            "LOALT1000": activity_level.loalt1000,
            "LOALT5000": activity_level.loalt5000,
            "LOAGT5000": activity_level.loagt5000
            }


class ActivityLevelByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "LOALT2": fields.Integer(),
        "LOALT5": fields.Integer(),
        "LOALT10": fields.Integer(),
        "LOALT100": fields.Integer(),
        "LOALT1000": fields.Integer(),
        "LOALT5000": fields.Integer(),
        "LOAGT5000": fields.Integer()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             LOALT2=None,
             LOALT5=None,
             LOALT10=None,
             LOALT100=None,
             LOALT1000=None,
             LOALT5000=None,
             LOAGT5000=None):

        activity_level = ActivityLevel(date=Date,
                                       loalt2=LOALT2,
                                       loalt5=LOALT5,
                                       loalt10=LOALT10,
                                       loalt100=LOALT100,
                                       loalt1000=LOALT1000,
                                       loalt5000=LOALT5000,
                                       loagt5000=LOAGT5000
                                       )
        db_session.add(activity_level)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "ActivityLevel": serialize_activity_level(activity_level)}
        except SQLAlchemyError as e:
            print(str(e))
            db_session.rollback()
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": ResponseDescriptions.ErrorFromDataBase.value}

        return response

    @use_kwargs(get_args)
    def get(self, Date=None):

        error = self.validateActivityLevelInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        activity_level = db_session.query(ActivityLevel).filter(
            and_(ActivityLevel.date == Date)).one_or_none()

        if activity_level is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "ActivityLevel": serialize_activity_level(activity_level)}

        return response

    def validateActivityLevelInput(self, date):
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
