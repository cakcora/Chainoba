from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, BigInteger, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import cfg as CONFIG

Base = declarative_base()

# PostgreSQL DB URL setup
DB_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=CONFIG.POSTGRES_USER, pw=CONFIG.POSTGRES_PW,
                                                               url=CONFIG.POSTGRES_HOST, db=CONFIG.POSTGRES_DB)

Base = declarative_base()
engine = create_engine(DB_URI)

# Session to connect to the postgres sqlalchemy engine
Session = sessionmaker(bind=engine)

db_session = Session()

CONSTANTS = {
    'schema': 'ethereum'
}


class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = {'schema': CONSTANTS['schema']}
    input_address = Column(BigInteger)
    id = Column(Integer, primary_key=True)
    output_address = Column(BigInteger)
    ntime = Column(BigInteger)
    token_amount = Column(String),
    token_id = Column(BigInteger, ForeignKey('tokens.token_id'))

    def __repr__(self):
        return "<Transaction(id={}, input_address={}, output_address={}, ntime={},token_amount='{}',token_id = {})>".format(
            self.id,
            self.input_address,
            self.output_address,
            self.ntime,
            self.token_amount,
            self.token_id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns()}


class PonziAnomaly(Base):
    __tablename__ = 'ponzi_anomaly'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(Integer, primary_key=True)
    address = Column(String)
    name = Column(String)
    label = Column(String)

    def __repr__(self):
        return "<PonziAnomaly(id={}, address='{}', name='{}', label='{}')>".format(
            self.id,
            self.address,
            self.name,
            self.label)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns()}


class EthereumToken(Base):
    __tablename__ = 'tokens'
    __table_args__ = {'schema': CONSTANTS['schema']}
    token_id = Column(Integer, primary_key=True)
    tk_name = Column(String)

    def __repr__(self):
        return "<EthereumTokens(token_id={}, tk_name='{}')>".format(
            self.token_id,
            self.tk_name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns()}


if __name__ == '__main__':
    s = Session()
    print(s.query(Transaction).first())
    print(s.query(PonziAnomaly).first())
    print(s.query(EthereumTokens).first())
    s.close()
