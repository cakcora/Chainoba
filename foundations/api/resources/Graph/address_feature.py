from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_kwargs
from webargs import fields
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from api.models.models import db_session, AddressFeature


def serialize_feature_address(address_feature: AddressFeature):
    return {"id": address_feature.id,
            "date": address_feature.date.strftime('%Y-%m-%d'),
            "Address": address_feature.address.strip(),
            "No_of_SCC": address_feature.no_of_scc,
            "No_of_WCC": address_feature.no_of_wcc,
            "BTC_Received": address_feature.btc_received,
            "BTC_Sent": address_feature.btc_sent,
            "Activity_Level": address_feature.activity_level,
            "Clustering_Coeff": address_feature.clustering_coeff,
            "PearsonCC": address_feature.pearsoncc,
            "Maximal_Balance": address_feature.maximal_balance,
            "Current_Balance": address_feature.current_balance
            }


class AddressFeatureByDateEndpoint(Resource):
    get_args = {"date": fields.Date(),
                "address": fields.String()
                }
    insert_args = {
        "Address": fields.String(),
        "Date": fields.Date(),
        "No_of_SCC": fields.Integer(),
        "No_of_WCC": fields.Integer(),
        "BTC_Received": fields.Integer(),
        "BTC_Sent": fields.Integer(),
        "Activity_Level": fields.Integer(),
        "Clustering_Coeff": fields.Float(),
        "PearsonCC": fields.Float(),
        "Maximal_Balance": fields.Integer(),
        "Current_Balance": fields.Integer()
    }

    @use_kwargs(insert_args)
    def post(self, Date,
             Address,
             No_of_SCC=None,
             No_of_WCC=None,
             BTC_Received=None,
             BTC_Sent=None,
             Activity_Level=None,
             Clustering_Coeff=None,
             PearsonCC=None,
             Maximal_Balance=None,
             Current_Balance=None):
        address_feature = AddressFeature(date=Date,
                                         address=Address,
                                         no_of_scc=No_of_SCC,
                                         no_of_wcc=No_of_WCC,
                                         btc_received=BTC_Received,
                                         btc_sent=BTC_Sent,
                                         activity_level=Activity_Level,
                                         clustering_coeff=Clustering_Coeff,
                                         pearsoncc=PearsonCC,
                                         maximal_balance=Maximal_Balance,
                                         current_balance=Current_Balance)
        db_session.add(address_feature)
        try:
            db_session.commit()
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "AddressFeature": serialize_feature_address(address_feature)}
        except SQLAlchemyError as e:
            print(str(e))
            db_session.rollback()
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": ResponseDescriptions.ErrorFromDataBase.value}

        return response

    @use_kwargs(get_args)
    def get(self, date=None, address=None):

        error = self.validateAddressFeatureInput(address, date)
        if error is not None:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ErrorMessage": error.value}

        address_feature = db_session.query(AddressFeature).filter(
            and_(AddressFeature.address == address, AddressFeature.date == date)).one_or_none()

        if address_feature is None:
            response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        else:
            response = {"ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "AddressFeature": serialize_feature_address(address_feature)}

        return response

    def validateAddressFeatureInput(self, address, date):
        error = None
        if address is None:
            error = ResponseDescriptions.AddressInputMissing
        if date is None:
            error = ResponseDescriptions.DateInputMissing
        else:
            try:
                date.strftime('%Y-%m-%d')
            except ValueError:
                error = ResponseDescriptions.DateInputMissing
        return error
