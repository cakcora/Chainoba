from flask_restful import Resource
from sqlalchemy import and_
from webargs import fields
from webargs.flaskparser import use_kwargs
import time
from datetime import datetime, timedelta
from models.models import Block, Transaction
from models.ResponseCodes import ResponseCodes
from models.ResponseCodes import ResponseDescriptions
from models.models import db_session


def serialize_block(block):
    return {'BlockId': block.id, 'Hash': block.hash.strip(), 'HashOfPreviousBlock': block.hashprev.strip(),
            'Timestamp': datetime.utcfromtimestamp(block.ntime).strftime('%Y-%m-%d %H:%M:%S'),
            'Nnonce': block.nnonce, 'Version': block.version, 'HashOfMerkleRoot': block.hashmerkleroot.strip(),
            'BlockSizeInBits': block.nbits}


def serialize_transaction(transaction):
    return {'TransactionId': transaction.id,
            'Hash': transaction.hash.strip(),
            'Version': transaction.version,
            'LockTime': transaction.locktime}


# Validate Block Input of GetBlockDataByDateEndpoint endpoint
def ValidateBlockInput(self, year, month, day, date_offset):
    validationErrorList = []
    if day > 31 or day <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidDayInput.value})
    if year > int(datetime.now().year) or year < 2009:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidYearInput.value})
    if month > 12 or month <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidMonthInput.value})
    if date_offset > 31 or date_offset <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidDateOffsetInput.value})
    return validationErrorList


# Returns the blocks by day of the year
class GetBlockDataByDateEndpoint(Resource):
    args = {'day': fields.Integer(),
            'month': fields.Integer(),
            'year': fields.Integer(),
            'date_offset': fields.Integer()
            }

    @use_kwargs(args)
    def get(self, year, month, day, date_offset):
        # Validate User Input
        validations_result = ValidateBlockInput(self, year, month, day, date_offset)
        if validations_result is not None and len(validations_result) > 0:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ValidationErrors": validations_result}
        else:  # all valid
            try:
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
                    return {
                        'ResponseCode': ResponseCodes.Success.value,
                        'ResponseDesc': ResponseCodes.Success.name,
                        'FromDate': from_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'ToDate': to_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'NumberOfBlocks': len(block_list),
                        'Blocks': block_list}

                else:
                    return {"ResponseCode": ResponseCodes.NoDataFound.value,
                            "ResponseDesc": ResponseCodes.NoDataFound.name,
                            "ErrorMessage": ResponseDescriptions.NoDataFound.value}
            except Exception as ex:
                return {"ResponseCode": ResponseCodes.InternalError.value,
                        "ResponseDesc": ResponseCodes.InternalError.name,
                        "ErrorMessage": str(ex)}


# Validate Block Ids Input of GetTransactionDataByBlockID endpoint
def ValidateBlockIds(self, block_ids):
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


# Get Transaction Data belonging to list of Block Ids
class GetTransactionDataByBlockID(Resource):
    args_block = {
        'block_ids': fields.List(fields.Integer())
    }

    @use_kwargs(args_block)
    def get(self, block_ids):
        # Validate User Input
        validations_result = ValidateBlockIds(self, block_ids)
        if validations_result is not None and len(validations_result) > 0:
            return {"ResponseCode": ResponseCodes.InvalidRequestParameter.value,
                    "ResponseDesc": ResponseCodes.InvalidRequestParameter.name,
                    "ValidationErrors": validations_result}
        try:
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
                block_transactions_dict[blk_id] = {"NumberOfTransactions": len(trans_list), 'Transactions': trans_list}

            if block_transactions_dict is not None and num_of_empty_blocks != len(block_ids):
                return {'ResponseCode': ResponseCodes.Success.value,
                        'ResponseDesc': ResponseCodes.Success.name,
                        'BlockTransactionData': block_transactions_dict}
            else:
                return {"ResponseCode": ResponseCodes.NoDataFound.value,
                        "ResponseDesc": ResponseCodes.NoDataFound.name,
                        "ErrorMessage": ResponseDescriptions.NoDataFound.value}
        except Exception as ex:
            return {"ResponseCode": ResponseCodes.InternalError.value,
                    "ResponseDesc": ResponseCodes.InternalError.name,
                    "ErrorMessage": str(ex)}
