from config import cfg as CONFIG
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from resources.address import Address
from resources.block import Block
from resources.transaction import Transaction

# Flask application initialization
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

# PostgreSQL DB URL setup
DB_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=CONFIG.POSTGRES_USER, pw=CONFIG.POSTGRES_PW,
                                                               url=CONFIG.POSTGRES_HOST, db=CONFIG.POSTGRES_DB)
# SQLALCHEMY ORM setup
# For more information: https://www.sqlalchemy.org/
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TODO
# 1. Update the API endpoints for
#    a. Block
#    b. Transaction
#    c. Address

# Endpoints
api.add_resource(Address, '/bitcoin/addresses', endpoint='address')
api.add_resource(Block, '/bitcoin/blocks', endpoint='block')
api.add_resource(Transaction, '/bitcoin/transactions', endpoint='transaction')

if __name__ == '__main__':
    # debug=True in development mode, for production set debug=False
    app.run(debug=True)
