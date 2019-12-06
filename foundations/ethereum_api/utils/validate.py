#!/usr/bin/env python3
# Name: validate.py
# Usecase: Validate ethereum data

from datetime import datetime

from models.response_codes import ResponseDescriptions


def validate_node_input(node_address):
    """
    Method to validate node input data
    :param node_address:
    """
    validationErrorList = []
    if node_address <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidNodeAddress.value})
    return validationErrorList


def validate_input(year, month, day, date_offset):
    """
    Method to validate input data
    :param year:
    :param month:
    :param day:
    :param date_offset:
    """
    validationErrorList = []
    if day > 31 or day <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidDayInput.value})
    if year > int(datetime.now().year) or year < 2016:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidYearInput.value})
    if month > 12 or month <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidMonthInput.value})
    if date_offset <= 0:
        validationErrorList.append({"ErrorMessage": ResponseDescriptions.InvalidDateOffsetInput.value})
    return validationErrorList
