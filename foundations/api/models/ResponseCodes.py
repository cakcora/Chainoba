from enum import Enum

class ResponseCodes(Enum):
    Success = 200
    InvalidRequestParameter = 422
    NoDataFound = 404
    InternalError = 500


class ResponseDescriptions(Enum):
    DayInputMissing = "Value of Input Parameter day is missing."
    MonthInputMissing = "Value of Input Parameter month is missing."
    YearInputMissing = "Value of Input Parameter year is missing."
    DateOffsetInputMissing = "Value of Input Parameter data_offset is missing."
    BlockIdsInputMissing = "Value of block_ids Input is missing."
    TransactionIdsInputMissing = "Value of transaction_ids Input is missing."
    TransactionIdInputMissing = "Value of transaction_id Input is missing."
    TransactionOutputIdInputMissing = "Value of transaction_output_id Input is missing."
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
