from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource
from models.models import Address
from models.models import Output as TransactionOutput
from models.models import OutputAddress as TransactionOutputAddress
from models.models import db_session
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions


def serialize_address(address):
    return {"AddressId": address.id,
            "Hash": address.hash.strip(),
            "PublicKey": address.public_key.strip(),
            "Address": address.address.strip()
            }


def serialize_transaction_output_address(address_id):
    address_list = db_session.query(Address).filter(
        Address.id == address_id).order_by(Address.id.asc())
    for address in address_list:
        address_as_dict = serialize_address(address)
        return address_as_dict


# Validate Transaction Ids Input of GetTransactionOutputAddressByTransactionOutputId endpoint
def ValidateTransactionIdAndTransactionOutputId(self, transaction_id, transaction_output_id):
    validationErrorList = []
    if transaction_id <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidTransactionIdInputValue.value})
    if transaction_output_id <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidTransactionOutputIdInputValue.value})
    return validationErrorList


class GetTransactionOutputAddressByTransactionOutputId(Resource):
    args_transactionoutput = {"transaction_id": fields.Integer(),
                              "transaction_output_id": fields.Integer()
                              }

    @use_kwargs(args_transactionoutput)
    def get(self, transaction_id, transaction_output_id):
        try:
            request = {"transaction_id": transaction_id, "transaction_output_id": transaction_output_id}
            response = {}
            # Validate User Input
            validations_result = ValidateTransactionIdAndTransactionOutputId(self, transaction_id,
                                                                             transaction_output_id)
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:
                transaction_output_id_list = db_session.query(TransactionOutput).filter(
                    TransactionOutput.transaction_id == transaction_id).order_by(
                    TransactionOutput.id.asc()).with_entities(
                    TransactionOutput.id).all()
                trans_output_ids = [output.id for output in transaction_output_id_list]
                if transaction_output_id in trans_output_ids:
                    output_address_list = db_session.query(TransactionOutputAddress).filter(
                        TransactionOutputAddress.output_id == transaction_output_id).order_by(
                        TransactionOutputAddress.id.asc()).all()
                    total_num_of_output_addresses = 0
                    output_addresses = []
                    for output_address in output_address_list:
                        output_addresses.append(serialize_transaction_output_address(output_address.address_id))
                        total_num_of_output_addresses = total_num_of_output_addresses + 1

                    if total_num_of_output_addresses > 0:
                        response = {
                            "ResponseCode": ResponseCodes.Success.value,
                            "ResponseDesc": ResponseCodes.Success.name,
                            "TransactionId": transaction_id,
                            "TransactionOutputId": transaction_output_id,
                            "NumberOfOutputAddresses": len(output_addresses),
                            "OutputAddresses": output_addresses
                        }
                    else:
                        response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                                    "ResponseDesc": ResponseCodes.NoDataFound.name,
                                    "ErrorMessage": ResponseDescriptions.NoDataFound.value}
                else:
                    response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                                "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                                "ErrorMessage": ResponseDescriptions.OutputDoesNotBelongToTransaction.value}
        except Exception as ex:
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": str(ex)}
        finally:
            # file = open('/Logs/GetTransactionOutputAddressByTransactionOutputIdLog.txt', 'w')
            # file.write("Time:" + str(datetime.now()) + "\r\n")
            # file.write("Request : " + request + "\r\n")
            # file.write("Response : " + response + "\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.close()
            return response
