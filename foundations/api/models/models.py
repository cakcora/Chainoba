from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, BigInteger, DateTime, Float
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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns()}


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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns()}


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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns()}


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


# Graph group date
class AddressFeature(Base):
    __tablename__ = 'graph_address_feature'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    address = Column(Integer)
    date = Column(DateTime)
    no_of_scc = Column(Integer)
    no_of_wcc = Column(Integer)
    btc_received = Column(Integer)
    btc_sent = Column(Integer)
    activity_level = Column(Integer)
    clustering_coeff = Column(Float)
    pearsoncc = Column(Float)
    maximal_balance = Column(Integer)
    current_balance = Column(Integer)


class AddressDistribution(Base):
    __tablename__ = 'graph_address_distribution'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    receive_only_per = Column(Float)
    send_receive_per = Column(Float)


class TotalBtcReceived(Base):
    __tablename__ = 'graph_total_btc_received'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    btcreclt1 = Column(Integer)
    btcreclt10 = Column(Integer)
    btcreclt100 = Column(Integer)
    btcreclt1000 = Column(Integer)
    btcreclt10000 = Column(Integer)
    btcreclt50000 = Column(Integer)
    btcrecgt50000 = Column(Integer)


class ActivityLevel(Base):
    __tablename__ = 'graph_activity_level'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    loalt2 = Column(Integer)
    loalt5 = Column(Integer)
    loalt10 = Column(Integer)
    loalt100 = Column(Integer)
    loalt1000 = Column(Integer)
    loalt5000 = Column(Integer)
    loagt5000 = Column(Integer)


class StronglyConnectedComponent(Base):
    __tablename__ = 'graph_strongly_connected_component'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    scc = Column(Integer)


class WeaklyConnectedComponent(Base):
    __tablename__ = 'graph_weakly_connected_component'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    wcc = Column(Integer)


class TransactionSize(Base):
    __tablename__ = 'graph_transaction_size'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    trans_size_lt1 = Column(Integer)
    trans_size_lt10 = Column(Integer)
    trans_size_lt100 = Column(Integer)
    trans_size_lt5000 = Column(Integer)
    trans_size_lt20000 = Column(Integer)
    trans_size_lt50000 = Column(Integer)
    trans_size_gt50000 = Column(Integer)


class AssortativityCoefficient(Base):
    __tablename__ = 'graph_assortativity_coefficient'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    assort_coeff = Column(Float)


class PearsonCoefficient(Base):
    __tablename__ = 'graph_pearson_coefficient'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    pear_coeff = Column(Float)


class ClusteringCoefficient(Base):
    __tablename__ = 'graph_clustering_coefficient'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    clust_coeff = Column(Float)


class BitcoinCirculation(Base):
    __tablename__ = 'graph_bitcoin_circulation'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    tot_btc = Column(Float)
    circ_percent = Column(Float)
    not_circu_percent = Column(Float)


class MostActiveEntity(Base):
    __tablename__ = 'graph_most_active_entity'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    addr = Column(String)
    no_of_trans = Column(Integer)


class ChainletsOccurance(Base):
    __tablename__ = 'graph_chainlets_occurance'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    split_chlt = Column(Integer)
    merge_chlt = Column(Integer)
    transition_chlt = Column(Integer)


class ChainletsOccuranceAmount(Base):
    __tablename__ = 'graph_chainlets_occurance_amount'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    split_chlt_amt = Column(Float)
    merge_chlt_amt = Column(Float)
    transition_chlt_amt = Column(Float)


class CurrentBalance(Base):
    __tablename__ = 'graph_current_balance'
    __table_args__ = {'schema': CONSTANTS['schema']}
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime)
    currbal1 = Column(Integer)
    currbal10 = Column(Integer)
    currbal100 = Column(Integer)
    currbal1000 = Column(Integer)
    currbal10000 = Column(Integer)
    currbal50000 = Column(Integer)
    currbalgt50000 = Column(Integer)


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
