create table ethereum.transactions
(
    id  bigserial not null
        constraint transaction_pk
        unique,
    from_node   bigint  not null,
    to_node   bigint  not null,
    tk_amount bigint not null,
    ntime          bigint not null,
    token_id bigint
        constraint token_id_fk
        references ethereum.tokens(token_id)
);
CREATE TABLE  ethereum.tokens
(
  token_id  bigserial PRIMARY KEY,
  tk_name varchar(255) not null
);
create table ethereum.ponzi_anomaly
(
    id  bigserial not null unique,
    address varchar(255) not null,
    name varchar(255) not null,
    label varchar(255) not null
);