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
    InvalidRequest = 200
    InvalidDayInput = 201
    InvalidYearInput = 202
    InvalidMonthInput = 203
    InvalidDateOffsetInput = 204
    InvalidYearValue = 205
    InvalidMonthValue = 206
    InvalidDayValue = 207
    InvalidBlockIdsInputValues = 208
    NumberOfBlockIdsLimitExceeded = 209
    InvalidTransactionIdsInputValues = 210
    NumberOfTransactionIdsLimitExceeded = 211
    NoDataFound = 300
    ErrorFromDataBase = 501


class ResponseDescriptions(Enum):
    DayInputMissing = "Value of Input Parameter Day is missing."
    MonthInputMissing = "Value of Input Parameter Month is missing."
    YearInputMissing = "Value of Input Parameter Year is missing."
    DateOffsetInputMissing = "Value of Input Parameter DateOffset is missing."
    BlockIdsInputMissing = "Value of block_ids Input is missing."
    TransactionIdsInputMissing = "Value of transaction_ids Input is missing."
    InvalidRequest = "Input request is Invalid."
    InvalidDayInput = "Value of Input Parameter day must be positive integer  with value range between 1 to 31."
    InvalidYearInput = "Value of Input Parameter year must be positive integer and in YYYY format with value range between 2009 and current year."
    InvalidMonthInput = "Value of Input Parameter month must be positive integer with value range between 1 to 12."
    InvalidDateOffsetInput = "Value of Input Parameter date_offset must be positive integer."
    InvalidBlockIdsInputValues = "Value of block_ids must be a positive integer"
    NumberOfBlockIdsLimitExceeded = "Only upto 5 Blocks_ids are allowed."
    InvalidTransactionIdsInputValues = "Value of transaction_ids must be a positive integer"
    NumberOfTransactionIdsLimitExceeded = "Only upto 10 transaction_ids Blocks_ids are allowed."
    NoDataFound = "No Data found."
    ErrorFromDataBase = "Value of Input Parameter Day is missing."
