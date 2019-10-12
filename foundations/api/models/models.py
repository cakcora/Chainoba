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
    'schema': 'bitcoin'
}


class Block(Base):
    __tablename__ = 'block'
    __table_args__ = {'schema': CONSTANTS['schema']}
    hash = Column(String, primary_key=True)
    id = Column(Integer)
    version = Column(Integer)
    hashprev = Column(String)
    hashmerkleroot = Column(String)
    ntime = Column(Integer)
    nbits = Column(Integer)
    nnonce = Column(Integer)

    def __repr__(self):
        return "<Block(hash='{}', id='{}', version={}, hashprev={}, hashmerkleroot={}, ntime={}, nbits={}, nnonce={})>" \
            .format(self.hash, self.id, self.version, self.hashprev, self.hashmerkleroot, self.ntime, self.nbits,
                    self.nnonce)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns()}


class Address(Base):
    __tablename__ = 'address'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(Integer, primary_key=True)
    hash = Column(String)
    public_key = Column(String)
    address = Column(String)

    def __repr__(self):
        return "<Address(id='{}', hash={}, public_key={}, address={})>".format(self.id, self.hash, self.public_key,
                                                                               self.address)


class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = {'schema': CONSTANTS['schema']}
    hash = Column(String, primary_key=True)
    id = Column(Integer)
    version = Column(Integer)
    locktime = Column(Integer)
    block_id = Column(Integer, ForeignKey('block.id'))

    def __repr__(self):
        return "<Transaction(hash='{}', id={}, version={}, locktime={}, block_id={})>".format(self.hash, self.id,
                                                                                              self.version,
                                                                                              self.locktime,
                                                                                              self.block_id)


class Input(Base):
    __tablename__ = 'input'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(Integer, primary_key=True)
    prevout_hash = Column(String)
    prevout_n = Column(Integer)
    scriptsig = Column(LargeBinary)
    sequence = Column(Integer)
    transaction_id = Column(Integer, ForeignKey('transaction.id'))
    prev_output_id = Column(Integer, ForeignKey('output.id'))

    def __repr__(self):
        return "<Input(id='{}', prevout_hash={}, prevout_n={}, scriptsig={}, sequence={}, transaction_id={}, prev_output_id={})>".format(
            self.id, self.prevout_hash, self.prevout_n, self.scriptsig, self.sequence, self.transaction_id,
            self.prev_output_id)


class Output(Base):
    __tablename__ = 'output'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    value = Column(Integer)
    scriptpubkey = Column(LargeBinary)
    transaction_id = Column(Integer, ForeignKey('transaction.id'))
    index = Column(Integer)
    script_type = Column(String)

    def __repr__(self):
        return "<Output(id='{}', value={}, scriptpubkey={}, transaction_id={}, index={}, script_type={})>".format(
            self.id, self.value, self.scriptpubkey, self.transaction_id, self.index, self.script_type)


class OutputAddress(Base):
    __tablename__ = 'output_address'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    output_id = Column(Integer, ForeignKey('output.id'))
    address_id = Column(Integer, ForeignKey('address.id'))

    def __repr__(self):
        return "<OutputAddress(id='{}', output_id={}, address_id={})>".format(
            self.id, self.output_id, self.address_id)


class BlockReadableTime(Base):
    __tablename__ = 'block_readable_time'
    __table_args__ = {'schema': CONSTANTS['schema']}
    hash = Column(String)
    id = Column(Integer, primary_key=True)
    version = Column(Integer)
    hashprev = Column(String)
    hashmerkleroot = Column(String)
    ntime = Column(Integer)
    nbits = Column(Integer)
    nnonce = Column(Integer)
    timestamp = Column(DateTime)

    def __repr__(self):
        return "<Block(hash='{}', id='{}', version={}, hashprev={}, hashmerkleroot={}, ntime={}, nbits={}, nnonce={}, timstamp={}>" \
            .format(self.hash, self.id, self.version, self.hashprev, self.hashmerkleroot, self.ntime, self.nbits,
                    self.nnonce, self.timestamp)


if __name__ == '__main__':
    s = Session()
    print(s.query(Block).first())
    print(s.query(Address).first())
    print(s.query(Transaction).first())
    print(s.query(Input).first())
    print(s.query(Output).first())
    print(s.query(OutputAddress).first())
    print(s.query(BlockReadableTime).first())
    s.close()
