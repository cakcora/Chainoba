create schema ethereum

create table ethereum.transaction
(
    id             bigserial not null
        constraint ethereum_transaction_pk
            unique,
    input_address        bigint  not null,
    output_address       bigint  not null,
    ntime          bigint not null,
    token_amount          varchar(100)   not null
);
