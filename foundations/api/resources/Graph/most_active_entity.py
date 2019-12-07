from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, MostActiveEntity


def serialize_most_active_entity(most_active_entity: MostActiveEntity):
    return {"Id": most_active_entity.id,
            "Date": most_active_entity.date.strftime('%Y-%m-%d'),
            "Addr": most_active_entity.addr,
            "NoOfTrans": most_active_entity.no_of_trans
            }


class MostActiveEntityByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "Addr": fields.String(),
        "NoOfTrans": fields.Integer()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             Addr=None,
             NoOfTrans=None):

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
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
