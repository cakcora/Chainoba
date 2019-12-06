from flask_restful import Resource
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from models.models import db_session, WeaklyConnectedComponent
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_kwargs


def serialize_weakly_connected_component(weakly_connected_component: WeaklyConnectedComponent):
    return {"Id": weakly_connected_component.id,
            "Date": weakly_connected_component.date.strftime('%Y-%m-%d'),
            "WCC": weakly_connected_component.wcc
            }


class WeaklyConnectedComponentByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "WCC": fields.Integer()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             WCC=None):

        weakly_connected_component = WeaklyConnectedComponent(date=Date,
                                                              wcc=WCC)
        db_session.add(weakly_connected_component)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "WeaklyConnectedComponent": serialize_weakly_connected_component(
                            weakly_connected_component)}
        except SQLAlchemyError as e:
            print(str(e))
            db_session.rollback()
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": ResponseDescriptions.ErrorFromDataBase.value}

        return response

    @use_kwargs(get_args)
    def get(self, Date=None):

        error = self.validateWeaklyConnectedComponentInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        weakly_connected_component = db_session.query(WeaklyConnectedComponent).filter(
            and_(WeaklyConnectedComponent.date == Date)).one_or_none()

        if weakly_connected_component is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "WeaklyConnectedComponent": serialize_weakly_connected_component(
                            weakly_connected_component)}

        return response

    def validateWeaklyConnectedComponentInput(self, date):
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
