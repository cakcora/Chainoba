import time
from datetime import datetime, timedelta
from flask_restful import Resource
from models.models import Block, Transaction
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from models.models import db_session
from sqlalchemy import and_
from webargs import fields, validate
from webargs.flaskparser import use_kwargs


def serialize_block(block):
    return {'id': block.id, 'hash_prev': block.hashprev, 'hash': block.hash,
            'n_time': datetime.utcfromtimestamp(block.ntime).strftime('%Y-%m-%d %H:%M:%S'),
            'nnonce': block.nnonce, 'version': block.version, 'hash_merkle_root': block.hashmerkleroot,
            'nbits': block.nbits}


def serialize_transaction(transaction):
    return {'transaction_id': transaction.id, 'hash': transaction.hash, 'version': transaction.version,
            'locktime': transaction.locktime, 'version': transaction.block_id}


def CreateErrorResponse(self, code, desc, message):
    json_data = {}
    json_data["ResponseCode"] = code
    json_data["ResponseDesc"] = desc
    json_data["ErrorMessage"] = message
    return json_data


def ValidateBlockInput(self, year, month, day, date_offset):
    validationErrorList = []
    if not (str(year) and str(year).strip()):
        validationErrorList.append(
            CreateErrorResponse(self, ResponseCodes.YearInputMissing.name, str(ResponseCodes.YearInputMissing.value),
                                ResponseDescriptions.YearInputMissing.value))
    if str(year) and str(year).strip() and (
            not str.isdigit(year) or (
            str.isdigit(year) and (int(year) > int(datetime.now().year) or int(year) < 2009))):
        validationErrorList.append(
            CreateErrorResponse(self, ResponseCodes.InvalidYearInput.name, str(ResponseCodes.InvalidYearInput.value),
                                ResponseDescriptions.InvalidYearInput.value))
    if not (str(month) and str(month).strip()):
        validationErrorList.append(
            CreateErrorResponse(self, ResponseCodes.MonthInputMissing.name, str(ResponseCodes.MonthInputMissing.value),
                                ResponseDescriptions.MonthInputMissing.value))
    if str(month) and str(month).strip() and (
            not str.isdigit(month) or (str.isdigit(month) and (int(month) > 12 or int(month) <= 0))):
        validationErrorList.append(
            CreateErrorResponse(self, ResponseCodes.InvalidMonthInput.name, str(ResponseCodes.InvalidMonthInput.value),
                                ResponseDescriptions.InvalidMonthInput.value))
    if not (str(day) and str(day).strip()):
        validationErrorList.append(
            CreateErrorResponse(self, ResponseCodes.DayInputMissing.name, str(ResponseCodes.DayInputMissing.value),
                                ResponseDescriptions.DayInputMissing.value))
    if str(day) and str(day).strip() and (
            not str.isdigit(day) or (str.isdigit(day) and (int(day) > 31 or int(day) <= 0))):
        validationErrorList.append(
            CreateErrorResponse(self, ResponseCodes.InvalidDayInput.name, str(ResponseCodes.InvalidDayInput.value),
                                ResponseDescriptions.InvalidDayInput.value))
    if not (str(date_offset) and str(date_offset).strip()):
        validationErrorList.append(
            CreateErrorResponse(self, ResponseCodes.DateOffsetInputMissing.name,
                                str(ResponseCodes.DateOffsetInputMissing.value),
                                ResponseDescriptions.DateOffsetInputMissing.value))
    if str(date_offset) and str(date_offset).strip() and (
            not str.isdigit(date_offset) or (
            str.isdigit(date_offset) and (int(date_offset) > 31 or int(date_offset) <= 0))):
        validationErrorList.append(
            CreateErrorResponse(self, ResponseCodes.InvalidDateOffsetInput.name,
                                str(ResponseCodes.InvalidDateOffsetInput.value),
                                ResponseDescriptions.InvalidDateOffsetInput.value))
    return validationErrorList


# Returns the blocks by day of the year
class GetBlockIDByDateEndpoint(Resource):
    args = {
        'year': fields.String(
            required=False,
            location='query'
        ),
        'month': fields.String(
            required=False,
            location='query'
        ),
        'day': fields.String(
            required=False,
            location='query'
        ),
        'date_offset': fields.String(
            required=False,
            location='query'
        )
    }

    @use_kwargs(args)
    def get(self, year, month, day, date_offset):
        year = year.strip()
        month = month.strip()
        day = day.strip()
        date_offset = date_offset.strip()
        validation_errors = {"Errors": []}
        validations_result = ValidateBlockInput(self, year, month, day, date_offset)
        if validations_result is not None and len(validations_result) > 0:
            validation_errors["Errors"] = validations_result
            return validation_errors
        else:
            try:
                from_time = datetime(int(year), int(month), int(day))
                to_time = from_time + timedelta(days=int(date_offset))

                from_unixtime = time.mktime(from_time.timetuple())  # get the unix time to form the query
                to_unixtime = time.mktime(to_time.timetuple())

                # perform the query
                block_data = db_session.query(Block).filter(
                    and_(Block.ntime >= from_unixtime, Block.ntime <= to_unixtime)).order_by(Block.ntime.asc())
                if block_data is not None and len(list(block_data)) != 0:
                    block_list = {}  # the list of blocks returned by the API
                    for block in block_data:
                        block_as_dict = serialize_block(block)
                        block_list[block_as_dict['hash']] = block_as_dict

                    return {
                        'ResponseCode': "0" + str(ResponseCodes.Success.value),
                        'ResponseDesc': ResponseCodes.Success.name,
                        'from_date': from_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'to_date': to_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'num_blocks': len(block_list),
                        'blocks': block_list}

                else:
                    return CreateErrorResponse(self, ResponseCodes.NoDataFound.name,
                                               str(ResponseCodes.NoDataFound.value),
                                               ResponseDescriptions.NoDataFound.value)
            except Exception as ex:
                return CreateErrorResponse(self, ResponseCodes.InternalError.name,
                                           str(ResponseCodes.InternalError.value),
                                           str(ex))


def ValidateBlockIds(self, block_ids):
    validationErrorList = []

    if len(block_ids) == 0:
        validationErrorList.append(CreateErrorResponse(self, ResponseCodes.BlockIdsInputMissing.name,
                                                       str(ResponseCodes.BlockIdsInputMissing.value),
                                                       str(ResponseDescriptions.BlockIdsInputMissing.value)))
    if len(block_ids) > 5:
        validationErrorList.append(CreateErrorResponse(self, ResponseCodes.NumberOfBlockIdsLimitExceeded.name,
                                                       str(ResponseCodes.NumberOfBlockIdsLimitExceeded.value),
                                                       str(ResponseDescriptions.NumberOfBlockIdsLimitExceeded.value)))
    if len(block_ids) > 0:
        for block_id in block_ids:
            if not str.isdigit(block_id) or (str.isdigit(str(block_id)) and int(block_id) <= 0):
                validationErrorList.append(CreateErrorResponse(self, ResponseCodes.InvalidBlockIdsInputValues.name,
                                                               str(ResponseCodes.InvalidBlockIdsInputValues.value),
                                                               str(
                                                                   ResponseDescriptions.InvalidBlockIdsInputValues.value)))
                break
    return validationErrorList


# Returns the blocks by day of the year
class GetTransactionIDByBlockID(Resource):
    args_block = {
        'block_ids': fields.List(fields.String())
    }

    @use_kwargs(args_block)
    def get(self, block_ids):
        block_ids = list(set(list(block_ids)))
        block_ids = [block_id.strip() for block_id in block_ids if block_id.strip()]
        validation_errors = {"Errors": []}
        validations_result = ValidateBlockIds(self, block_ids)
        if validations_result is not None and len(validations_result) > 0:
            validation_errors["Errors"] = validations_result
            return validation_errors
        try:
            block_transactions_dict = {}
            num_of_empty_blocks = 0
            for blk_id in sorted(block_ids):
                transactions = db_session.query(Transaction).filter(Transaction.block_id == blk_id).order_by(
                    Transaction.id.asc())

                trans_list = []  # the list of transactions returned by the API
                for transaction in transactions:
                    trans_as_dict = serialize_transaction(transaction)

                    trans_list.append(trans_as_dict)
                if len(trans_list) == 0:
                    num_of_empty_blocks = num_of_empty_blocks + 1
                block_transactions_dict[blk_id] = {"num_of_transactions": len(trans_list), 'transactions': trans_list}
            if block_transactions_dict is not None and num_of_empty_blocks != len(block_ids):
                return {
                    'ResponseCode': "0" + str(ResponseCodes.Success.value),
                    'ResponseDesc': ResponseCodes.Success.name,
                    'Block_Transaction_Data': block_transactions_dict
                }
            else:
                return CreateErrorResponse(self, ResponseCodes.NoDataFound.name,
                                           str(ResponseCodes.NoDataFound.value),
                                           ResponseDescriptions.NoDataFound.value)
        except Exception as ex:
            return CreateErrorResponse(self, ResponseCodes.InternalError.name,
                                       str(ResponseCodes.InternalError.value),
                                       str(ex))
