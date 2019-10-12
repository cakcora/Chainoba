import time
from datetime import datetime, timedelta

from flask_restful import Resource
from models.models import Block
from models.models import db_session
from sqlalchemy import and_
from webargs import fields, validate
from webargs.flaskparser import use_kwargs


class BlockEndpoint(Resource):
    """Resource class endpoint to serve block related requests

    TODO: Complete the API
    """

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

        from_unixtime = time.mktime(from_time.timetuple())
        to_unixtime = time.mktime(to_time.timetuple())

        block_data = db_session.query(Block).filter(
            and_(Block.ntime >= from_unixtime, Block.ntime <= to_unixtime)).order_by(Block.ntime.asc())
        blk_counter = 0

        for blk in block_data:
            print(blk.__dict__)
            blk_counter += 1
            date = blk.__dict__['ntime']
            print("Date: {}".format(datetime.fromtimestamp(date)))

        return {'year': year, 'month': month, 'day': day, 'date_offset': date_offset, 'from_unix_time': from_unixtime,
                'to_unix_time': to_unixtime, 'num_blocks': blk_counter}
