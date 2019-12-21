#!/usr/bin/env python3
# Name: validate.py
# Usecase: Validate bitcoin data

from datetime import datetime

from models.response_codes import ResponseDescriptions


def validate_block_input(year, month, day, date_offset):
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


def validate_block_ids(block_ids):
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


def validate_transaction_hash(transaction_hash):
    """
    Validate transaction hash data
    :param self:
    :param transaction_hash:
    """
    validationErrorList = []
    if not transaction_hash or len(transaction_hash) == 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.TransactionHashInputMissing.value})
    return validationErrorList


def validate_transaction_ids(transaction_ids):
    """
    Method to validate transaction ids
    :param transaction_ids:
    """
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

def validate_transaction_id_and_transaction_output_id(transaction_id, transaction_output_id):
    """
    Method to validate transaction id and transaction output id
    :param transaction_id:
    :param transaction_output_id:
    """
    validationErrorList = []
    if transaction_id <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidTransactionIdInputValue.value})
    if transaction_output_id <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidTransactionOutputIdInputValue.value})
    return validationErrorList