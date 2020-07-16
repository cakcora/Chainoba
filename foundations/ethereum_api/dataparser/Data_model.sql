create table ethereum.blocks
(
    number BIGINT,
    hash VARCHAR,
    parent_hash VARCHAR,
    nonce VARCHAR,
    sha3_uncles VARCHAR,
    logs_bloom VARCHAR,
    transactions_root VARCHAR,
    state_root VARCHAR,
    receipts_root VARCHAR,
    miner VARCHAR,
    difficulty numeric,
    total_difficulty numeric,
    size BIGINT,
    extra_data VARCHAR,
    gas_limit BIGINT,
    gas_used BIGINT,
    time_stamp VARCHAR,
    transaction_count BIGINT
);

create table ethereum.contracts
(
    address varchar,
    bytecode varchar,
    function_sighashes varchar,
    is_erc20 BOOLEAN,
    is_erc721 BOOLEAN,
    block_number bigint
);

create table ethereum.logs
(
    log_index BIGINT,
    transaction_hash varchar,
    transaction_index BIGINT,
    block_hash varchar,
    block_number BIGINT,
    address varchar,
    data varchar,
    topics varchar
);

create table ethereum.receipts
(
    transaction_hash varchar,
    transaction_index BIGINT,
    block_hash varchar,
    block_number BIGINT,
    cumulative_gas_used BIGINT,
    gas_used BIGINT,
    contract_address varchar,
    root varchar,
    status BIGINT
);

create table ethereum.token_transfers
(
    token_address varchar,
    from_address varchar,
    to_address varchar,
    value numeric,
    transaction_hash varchar,
    log_index BIGINT,
    block_number BIGINT
);

create table ethereum.tokens
(
    address varchar,
    symbol varchar,
    name varchar,
    decimals BIGINT,
    total_supply numeric,
    block_number bigint
);

create table ethereum.traces
(
    transaction_hash varchar(66),
    transaction_index bigint,
    from_address varchar(42),
    to_address varchar(42),
    value numeric(38),
    input varchar,
    output varchar,
    trace_type varchar(16),
    call_type varchar(16),
    reward_type varchar(16),
    gas bigint,
    gas_used bigint,
    subtraces bigint,
    trace_address varchar(8192),
    error text,
    status BIGINT,
    block_number bigint,
    trace_id text
);

create table ethereum.transactions
(
    hash VARCHAR,
    nonce BIGINT,
    block_hash VARCHAR,
    block_number BIGINT,
    transaction_index BIGINT,
    from_address VARCHAR,
    to_address VARCHAR,
    value numeric,
    gas BIGINT,
    gas_price BIGINT,
    input VARCHAR,
    block_timestamp BIGINT
);
