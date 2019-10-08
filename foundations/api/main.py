from config import cfg as CONFIG
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=CONFIG.POSTGRES_USER, pw=CONFIG.POSTGRES_PW,
                                                               url=CONFIG.POSTGRES_URL, db=CONFIG.POSTGRES_DB)

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'my_database',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


# TODO
# Add a database connection to PostgreSQL

class Address(Resource):
    def get(self):
        return {'hello': 'world'}


class Block(Resource):
    def get(self):
        return {'hello': 'world'}


class Transaction(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(Address, '/bitcoin/address')
api.add_resource(Block, '/bitcoin/block')
api.add_resource(Transaction, '/bitcoin/transaction')

if __name__ == '__main__':
    app.run(debug=True)
