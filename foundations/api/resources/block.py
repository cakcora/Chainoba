#!/usr/bin/env python3
# Name: block.py
# Usecase: Bitcoin block API
# Functionality: GET

import time
from datetime import datetime, timedelta

from common.utils import serialize_block, serialize_transaction
from flask_restful import Resource
from models.models import Block, Transaction
from models.models import db_session
from models.response_codes import ResponseCodes
from models.response_codes import ResponseDescriptions
from sqlalchemy import and_
from webargs import fields
from webargs.flaskparser import use_kwargs


def ValidateBlockInput(year, month, day, date_offset):
    """
    Method to validate block input parameters
    :param year:
    :param month:
    :param day:
    :param date_offset:
    """
    validationErrorList = []
    if day > 31 or day <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidDayInput.value})
    if year > int(datetime.now().year) or year < 2009:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidYearInput.value})
    if month > 12 or month <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidMonthInput.value})
    if date_offset <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidDateOffsetInput.value})
    return validationErrorList


def ValidateBlockIds(block_ids):
    """
    Method to validate block ids sent as input parameters
    :param block_ids:
    """
    validationErrorList = []
    if len(block_ids) == 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.BlockIdsInputMissing.value})
    if len(block_ids) > 5:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.NumberOfBlockIdsLimitExceeded.value})
    if len(block_ids) > 0:
        for block_id in block_ids:
            if block_id <= 0:
                validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidBlockIdsInputValues.value})
                break
    return validationErrorList


class GetBlockDataByDateEndpoint(Resource):
    """
    Class implementing get block by date API
    """
    args = {"day": fields.Integer(),
            "month": fields.Integer(),
            "year": fields.Integer(),
            "date_offset": fields.Integer()
            }

    @use_kwargs(args)
    def get(self, year, month, day, date_offset):
        """
        Method for GET request
        :param year:
        :param month:
        :param day:
        :param date_offset:
        """
        # Validate User Input
        try:
            request = {"day": day, "month": month, "year": year, "date_offset": date_offset}
            validations_result = ValidateBlockInput(year, month, day, date_offset)
            response = {}
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:  # all valid

                from_time = datetime(int(year), int(month), int(day))
                to_time = from_time + timedelta(days=int(date_offset))

                from_unixtime = time.mktime(from_time.timetuple())  # get the unix time to form the query
                to_unixtime = time.mktime(to_time.timetuple())

                # perform the query
                block_data = db_session.query(Block).filter(
                    and_(Block.ntime >= from_unixtime, Block.ntime <= to_unixtime)).order_by(Block.ntime.asc())
                if block_data is not None and len(list(block_data)) != 0:
                    block_list = []
                    for block in block_data:
                        block_list.append(serialize_block(block))
                    response = {
                        "ResponseCode": ResponseCodes.Success.value,
                        "ResponseDesc": ResponseCodes.Success.name,
                        "FromDate": from_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "ToDate": to_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "NumberOfBlocks": len(block_list),
                        "Blocks": block_list}
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


class GetTransactionDataByBlockID(Resource):
    """
    Class implementing get transaction data by block ID API
    """
    args_block = {
        "block_ids": fields.List(fields.Integer())
    }

    @use_kwargs(args_block)
    def get(self, block_ids):
        """
        Method for GET request
        :param block_ids: 
        """
        try:
            # Validate User Input
            request = {"block_ids": block_ids}
            response = {}
            validations_result = ValidateBlockIds(block_ids)
            if validations_result is not None and len(validations_result) > 0:
                response = {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                            "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                            "ValidationErrors": validations_result}
            else:
                block_transactions_dict = {}
                num_of_empty_blocks = 0

                for blk_id in sorted(block_ids):
                    transactions = db_session.query(Transaction).filter(Transaction.block_id == blk_id).order_by(
                        Transaction.id.asc())
                    trans_list = []
                    for transaction in transactions:
                        trans_list.append(serialize_transaction(transaction))
                    if len(trans_list) == 0:
                        num_of_empty_blocks = num_of_empty_blocks + 1
                    block_transactions_dict[blk_id] = {"NumberOfTransactions": len(trans_list),
                                                       "Transactions": trans_list}

                if block_transactions_dict is not None and num_of_empty_blocks != len(block_ids):
                    response = {"ResponseCode": ResponseCodes.Success.value,
                                "ResponseDesc": ResponseCodes.Success.name,
                                "BlockTransactionData": block_transactions_dict}
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
