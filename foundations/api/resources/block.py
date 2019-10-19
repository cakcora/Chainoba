import time
from datetime import datetime, timedelta

from flask_restful import Resource
from models.models import Block
from models.models import db_session
from sqlalchemy import and_
from webargs import fields, validate
from webargs.flaskparser import use_kwargs


def serialize_block(block):
    return {'id': block.id, 'hash_prev': block.hashprev, 'hash': block.hash, 'n_time': block.ntime,
            'nnonce': block.nnonce, 'version': block.version, 'hash_merkle_root': block.hashmerkleroot,
            'nbits': block.nbits}


# Returns the blocks by day of the year
class BlockEndpoint(Resource):
    args = {
        'year': fields.Integer(
            required=True,
            validate=validate.OneOf([2009]),
            location='query'
        ),
        'month': fields.Integer(
            required=True,
            validate=validate.OneOf(list(range(1, 13))),
            location='query'
        ),
        'day': fields.Integer(
            required=True,
            validate=validate.OneOf(range(1, 32)),
            location='query'
        ),
        'date_offset': fields.Integer(
            required=True,
            validate=validate.OneOf(list(range(1, 6))),
            location='query'
        )
    }

    @use_kwargs(args)
    def get(self, year, month, day, date_offset):
        from_time = datetime(year, month, day)
        to_time = from_time + timedelta(days=date_offset)

        from_unixtime = time.mktime(from_time.timetuple())  # get the unix time to form the query
        to_unixtime = time.mktime(to_time.timetuple())

        # perform the query
        block_data = db_session.query(Block).filter(
            and_(Block.ntime >= from_unixtime, Block.ntime <= to_unixtime)).order_by(Block.ntime.asc())

        block_list = dict()  # the list of blocks returned by the API
        for block in block_data:
            block_as_dict = serialize_block(block)
            block_list[block_as_dict['hash']] = block_as_dict

        return {'from_date': from_unixtime, 'to_date': to_unixtime, 'num_blocks': len(block_list), 'blocks': block_list}
