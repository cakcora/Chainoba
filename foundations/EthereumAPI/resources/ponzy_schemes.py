from flask_restful import Resource
from EthereumAPI.models.models import PonziAnomaly, db_session
from EthereumAPI.models.ResponseCodes import ResponseCodes
from EthereumAPI.models.ResponseCodes import ResponseDescriptions


def serialize_ponzi_data(ponzi_Anomaly_data):
    return {"Id": ponzi_Anomaly_data.id,
            "Address": ponzi_Anomaly_data.address,
            "Name": ponzi_Anomaly_data.name,
            "Label": ponzi_Anomaly_data.label
            }


class GetPonziAnomalyDataEndpoint(Resource):
    def get(self):
        # Validate User Input
        try:
            # perform the query
            ponzi_Anomaly_data = db_session.query(PonziAnomaly).order_by(PonziAnomaly.id.asc()).all()
            if ponzi_Anomaly_data is not None and len(list(ponzi_Anomaly_data)) != 0:
                ponzi_Anomaly_list = []
                for ponzi_Anomaly in ponzi_Anomaly_data:
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
            # file = open('/EthereumAPI/Logs/GetPonziAnomalyDataLog.txt', 'w')
            # file.write("Time:" + str(datetime.now()) + "\r\n")
            # file.write("Request : " + request + "\r\n")
            # file.write("Response : " + response + "\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.close()
            return response
