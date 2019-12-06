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
    InvalidNodeAddress = "Value of Node Address is invalid.."
    NoDataFound = "No Data found for requested parameters."
    ErrorFromDataBase = "Database Error has occurred."
