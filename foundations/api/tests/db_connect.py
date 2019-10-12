from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from ..config import cfg as CONFIG

# Flask application initialization
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

# PostgreSQL DB URL setup
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=CONFIG.POSTGRES_USER, pw=CONFIG.POSTGRES_PW,
                                                               url=CONFIG.POSTGRES_HOST, db=CONFIG.POSTGRES_DB)
# SQLALCHEMY ORM setup
# For more information: https://www.sqlalchemy.org/
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TODO
# 1. Update the API endpoints for
#    a. Block
#    b. Transaction
#    c. Address


if __name__ == '__main__':
    # debug=True in development mode, for production set debug=False
    
