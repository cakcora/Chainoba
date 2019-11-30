from datetime import datetime
from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, AddressDistribution


def serialize_address_distribution(address_distribution: AddressDistribution):
    return {"id": address_distribution.id,
            "date": address_distribution.date.strftime('%Y-%m-%d'),
            "ReceiveOnlyPer": address_distribution.receiveonlyper,
            "SendReceivePer": address_distribution.sendreceiveper
            }


class AddressDistributionByDateEndpoint(Resource):
    get_args = {"Date": fields.Date()
                }
    insert_args = {
        "Date": fields.Date(),
        "ReceiveOnlyPer": fields.Float(),
        "SendReceivePer": fields.Float()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             ReceiveOnlyPer=None,
             SendReceivePer=None):
        address_distribution = AddressDistribution(date=Date,
                                              receiveonlyper=ReceiveOnlyPer,
                                              sendreceiveper=SendReceivePer
                                              )
        db_session.add(address_distribution)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "AddressDistribution": serialize_address_distribution(address_distribution)}
        except SQLAlchemyError as e:
            print(str(e))
            db_session.rollback()
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": ResponseDescriptions.ErrorFromDataBase.value}

        return response

    @use_kwargs(get_args)
    def get(self, Date=None):

        error = self.validateAddressDistributionInput(Date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        address_distribution = db_session.query(AddressDistribution).filter(
            and_(AddressDistribution.date == Date)).one_or_none()

        if address_distribution is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "AddressDistribution": serialize_address_distribution(address_distribution)}

        return response

    def validateAddressDistributionInput(self, date):
        error = None

        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
