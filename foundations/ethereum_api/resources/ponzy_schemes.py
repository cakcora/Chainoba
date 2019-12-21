#!/usr/bin/env python3
# Name: ponzi_scheme.py
# Usecase: Ethereum Ponzi Scheme API
# Functionality: GET

from flask_restful import Resource
from models.models import PonziAnomaly, db_session
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from utils.serialize import serialize_ponzi_data


class GetPonziAnomalyDataEndpoint(Resource):
    """
    Class implementing get ponzi anomaly data API
    """

    def get(self):
        """
        Method for GET request
        """
        # Validate User Input
        try:
            # perform the query
            ponzi_anomaly_data = db_session.query(PonziAnomaly).order_by(PonziAnomaly.id.asc()).all()
            if ponzi_anomaly_data is not None and len(list(ponzi_anomaly_data)) != 0:
                ponzi_Anomaly_list = []
                for ponzi_Anomaly in ponzi_anomaly_data:
                    ponzi_Anomaly_list.append(serialize_ponzi_data(ponzi_Anomaly))
                response = {
                    "ResponseCode": ResponseCodes.Success.value,
                    "ResponseDesc": ResponseCodes.Success.name,
                    "NumberOfRecords": len(ponzi_Anomaly_list),
                    "Data": ponzi_Anomaly_list}
            else:
                response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                            "ResponseDesc": ResponseCodes.NoDataFound.name,
                            "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        except Exception as ex:
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": str(ex)}
        finally:
            return response
