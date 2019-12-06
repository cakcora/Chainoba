#!/usr/bin/env python3
# Name: serialize.py
# Usecase: Serialize bitcoin data

from datetime import datetime

from models.models import Address
from models.models import db_session


def serialize_block(block):
    """
    Method to serialize block data
    API: Bitcoin Block API
    :param block:
    """
    return {"BlockId": block.id, "Hash": block.hash.strip(), "HashOfPreviousBlock": block.hashprev.strip(),
            "Timestamp": datetime.utcfromtimestamp(block.ntime).strftime('%Y-%m-%d %H:%M:%S'),
            "Nnonce": block.nnonce, "Version": block.version, "HashOfMerkleRoot": block.hashmerkleroot.strip(),
            "BlockSizeInBits": block.nbits}


def serialize_transaction(transaction):
    """
    Method to serialize transaction data
    API: Bitcoin Block API
    :param transaction:
    """
    return {"TransactionId": transaction.id,
            "Hash": transaction.hash.strip(),
            "Version": transaction.version,
            "LockTime": transaction.locktime,
            "BlockId": transaction.block_id}


def serialize_transactions(transaction_data, input_response, output_response, transaction_id):
    """
    Method to validate transaction details
    API: Bitcoin Transactions API
    :param transaction_data:
    :param input_response:
    :param output_response:
    :param transaction_id:
    """
    return {"TransactionId": transaction_id,
            "Hash": transaction_data.hash.strip(), "Version": transaction_data.version,
            "LockTime": transaction_data.locktime, "BlockId": transaction_data.block_id,
            "NumberOfInputs": (input_response["TransactionInputData"][str(transaction_id)])["NumberOfInputs"],
            "TransactionInputs": (input_response["TransactionInputData"][str(transaction_id)])["TransactionInputs"],
            "NumberOfOutputs": (output_response["TransactionOutputData"][str(transaction_id)])["NumberOfOutputs"],
            "TransactionOutputs": (output_response["TransactionOutputData"][str(transaction_id)])["TransactionOutputs"]
            }


def serialize_transaction_input(trans_input):
    """
    Method to serialize transaction input data
    API: Bitcoin Transactions input API
    :param trans_input:
    """
    return {'InputId': trans_input.id,
            'HashOfPreviousTransaction': trans_input.prevout_hash.strip(),
            'PreviousOutputNumber': trans_input.prevout_n,
            'ScriptSignature': str(trans_input.scriptsig).strip(),
            'SequenceNumber': trans_input.sequence,
            'PreviousTransactionOutputId': trans_input.prev_output_id
            }


def serialize_address(address):
    """
    Method to serialize transaction address data
    API: Bitcoin Transactions input API
    :param address:
    """
    return {'AddressId': address.id,
            'Hash': address.hash.strip(),
            'PublicKey': address.public_key.strip(),
            'Address': address.address.strip()
            }


def serialize_transaction_output(trans_output, num_of_output_addresses, output_address_as_dict):
    """
    Method to serialize transaction output data
    API: Bitcoin Transactions output API
    :param trans_output:
    :param num_of_output_addresses:
    :param output_address_as_dict:
    """
    return {"OutputId": trans_output.id, "Value": trans_output.value,
            "ScriptPublicKey": str(trans_output.scriptpubkey),
            "Index": trans_output.index,
            "ScriptType": str(trans_output.script_type).strip(),
            "NumberOfOutputAddresses": num_of_output_addresses,
            "OutputAddresses": output_address_as_dict
            }


def serialize_transaction_output_address(address_id):
    """
    Method to serialize transaction output address data
    API: Bitcoin transaction output address API
    :param address_id:
    """
    address_list = db_session.query(Address).filter(
        Address.id == address_id).order_by(Address.id.asc())
    for address in address_list:
        address_as_dict = serialize_address(address)
        return address_as_dict
