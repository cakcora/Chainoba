from enum import Enum
from json import JSONEncoder


class ResponseCodes(Enum):
    Success = 00
    InternalError = 99
    DayInputMissing = 101
    MonthInputMissing = 102
    YearInputMissing = 103
    DateOffsetInputMissing = 104
    BlockIdsInputMissing = 105
    TransactionIdsInputMissing = 106
    TransactionIdInputMissing = 107
    TransactionOutputIdInputMissing = 108
    InvalidRequest = 200
    InvalidDayInput = 201
    InvalidYearInput = 202
    InvalidMonthInput = 203
    InvalidDateOffsetInput = 204
    InvalidBlockIdsInputValues = 205
    NumberOfBlockIdsLimitExceeded = 206
    InvalidTransactionIdsInputValues = 207
    NumberOfTransactionIdsLimitExceeded = 208
    InvalidTransactionIdInputValue = 209
    InvalidTransactionOutputIdInputValue = 210
    OutputDoesNotBelongToTransaction = 211
    NoDataFound = 300
    ErrorFromDataBase = 501


class ResponseDescriptions(Enum):
    DayInputMissing = "Value of Input Parameter day is missing."
    MonthInputMissing = "Value of Input Parameter month is missing."
    YearInputMissing = "Value of Input Parameter year is missing."
    DateOffsetInputMissing = "Value of Input Parameter data_offset is missing."
    BlockIdsInputMissing = "Value of block_ids Input is missing."
    TransactionIdsInputMissing = "Value of transaction_ids Input is missing."
    TransactionIdInputMissing = "Value of transaction_id Input is missing."
    TransactionOutputIdInputMissing = "Value of transaction_output_id Input is missing."
    InvalidRequest = "Input request is Invalid."
    InvalidDayInput = "Value of Input Parameter day is invalid. It must be positive integer  with value range between 1 to 31."
    InvalidYearInput = "Value of Input Parameter year is invalid. It must be positive integer and in YYYY format with value range between 2009 and current year."
    InvalidMonthInput = "Value of Input Parameter month is invalid. It must be positive integer with value range between 1 to 12."
    InvalidDateOffsetInput = "Value of Input Parameter date_offset is invalid. It must be positive integer."
    InvalidBlockIdsInputValues = "Value of block_ids is invalid. It must be a positive integer"
    NumberOfBlockIdsLimitExceeded = "Only upto 5 Blocks_ids are allowed."
    InvalidTransactionIdsInputValues = "Value of transaction_ids is invalid. It must be a positive integer"
    NumberOfTransactionIdsLimitExceeded = "Only upto 10 transaction_ids Blocks_ids are allowed."
    InvalidTransactionIdInputValue = "Value of Input Parameter is invalid. It transaction_id must be positive integer."
    InvalidTransactionOutputIdInputValue = "Value of Input Parameter transaction_output_id is invalid. It must be positive integer."
    OutputDoesNotBelongToTransaction = "transaction_output_id does not belong to the transaction_id."
    NoDataFound = "No Data found."
    ErrorFromDataBase = "Value of Input Parameter Day is missing."
