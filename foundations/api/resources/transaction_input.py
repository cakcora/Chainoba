from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource
from models.models import Input as  TransactionInput
from models.models import db_session, Output, OutputAddress, Address
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions


def serialize_transaction_input(trans_input):
    return {'InputId': trans_input.id,
            'HashOfPreviousTransaction': trans_input.prevout_hash.strip(),
            'PreviousOutputNumber': trans_input.prevout_n,
            'ScriptSignature': str(trans_input.scriptsig).strip(),
            'SequenceNumber': trans_input.sequence,
            'PreviousTransactionOutputId': trans_input.prev_output_id
            }


def serialize_address(address):
    return {'AddressId': address.id,
            'Hash': address.hash.strip(),
            'PublicKey': address.public_key.strip(),
            'Address': address.address.strip()
            }


# Validate Transaction Ids Input of TransactionInputEndpoint endpoint
def ValidateTransactionIds(self, transaction_ids):
    validationErrorList = []
    if len(transaction_ids) == 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.TransactionIdsInputMissing.value})
    if len(transaction_ids) > 10:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.NumberOfTransactionIdsLimitExceeded.value})
    if len(transaction_ids) > 0:
        for transaction_id in transaction_ids:
            if transaction_id <= 0:
                validationErrorList.append(
                    {"ErrorMessage": ResponseDescriptions.InvalidTransactionIdsInputValues.value})
                break
    return validationErrorList


class TransactionInputEndpoint(Resource):
    args_transaction = {'transaction_ids': fields.List(fields.Integer())}

    @use_kwargs(args_transaction)
    def get(self, transaction_ids):
        try:
            transaction_ids = list(set(list(transaction_ids)))
            request = {"transaction_ids": transaction_ids}
            response = {}
            # Validate User Input
            validations_result = ValidateTransactionIds(self, transaction_ids)
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:
                transaction_inputs_dict = {}
                for transaction_id in sorted(transaction_ids):
                    transaction_inputs = db_session.query(TransactionInput).filter(
                        TransactionInput.transaction_id == transaction_id).all()
                    previous_output_ids = []
                    trans_input_list = []
                    total_num_of_inputs = 0

                    for transaction_input in transaction_inputs:
                        trans_input_as_dict = serialize_transaction_input(transaction_input)
                        prev_output_id = trans_input_as_dict["PreviousTransactionOutputId"]

                        if prev_output_id is not None:
                            prev_out = db_session.query(Output).filter(Output.id == prev_output_id).one()
                            trans_input_as_dict["Value"] = prev_out.value

                            previous_output_ids.append(prev_output_id)
                            prev_addresses = []
                            prev_address = db_session.query(OutputAddress, Address).filter(
                                OutputAddress.output_id == prev_output_id).filter(
                                Address.id == OutputAddress.address_id).all()
                            for address in prev_address:
                                address_as_dict = serialize_address(address.Address)
                                prev_addresses.append(address_as_dict)
                            trans_input_as_dict["InputAddresses"] = prev_addresses

                        trans_input_list.append(trans_input_as_dict)
                        total_num_of_inputs = total_num_of_inputs + 1
                    transaction_inputs_dict[transaction_id] = {"NumberOfInputs": total_num_of_inputs,
                                                               "TransactionInputs": trans_input_list}

                if total_num_of_inputs > 0:
                    response = {'ResponseCode': ResponseCodes.Success.value,
                                'ResponseDesc': ResponseCodes.Success.name,
                                'TransactionInputData': transaction_inputs_dict
                                }
                else:
                    response = {"ResponseCode": ResponseCodes.NoDataFound.value,
                                "ResponseDesc": ResponseCodes.NoDataFound.name,
                                "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        except Exception as ex:
            response = {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": str(ex)}
        finally:
            # file = open('/Logs/TransactionInputLog.txt', 'w')
            # file.write("Time:" + str(datetime.now()) + "\r\n")
            # file.write("Request : " + request + "\r\n")
            # file.write("Response : " + response + "\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.write("\r\n")
            # file.close()
            return response
