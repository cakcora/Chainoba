#!/usr/bin/env python3
# Name: serialize.py
# Usecase: Serialize ethereum data

from datetime import datetime


def serialize_ponzi_data(ponzi_anomaly_data):
    """
    Method to serialize ponzi scheme data
    :param ponzi_anomaly_data:
    """
    return {"Id": ponzi_anomaly_data.id,
            "Address": ponzi_anomaly_data.address,
            "Name": ponzi_anomaly_data.name,
            "Label": ponzi_anomaly_data.label
            }


def serialize_transaction(transaction_data):
    """
    Method to serialize transaction data
    :param transaction_data:
    """
    return {"TransactionId": transaction_data.id,
            "InputNodeAddress": transaction_data.from_node,
            "OutputNodeAddress": transaction_data.to_node,
            "Timestamp": datetime.utcfromtimestamp(transaction_data.ntime).strftime('%Y-%m-%d %H:%M:%S'),
            "TokenAmount": transaction_data.tk_amount
            }


def serialize_transaction_with_token_data(transaction_data, token):
    """
    Method to serialize transaction with token data
    :param transaction_data:
    :param token:
    """
    return {"TransactionId": transaction_data.id,
            "InputNodeAddress": transaction_data.from_node,
            "OutputNodeAddress": transaction_data.to_node,
            "Timestamp": datetime.utcfromtimestamp(transaction_data.ntime).strftime('%Y-%m-%d %H:%M:%S'),
            "TokenAmount": transaction_data.tk_amount,
            'TokenId': token is not None and token.token_id or '',
            'TokenName': token is not None and token.token_name or '',
            }
