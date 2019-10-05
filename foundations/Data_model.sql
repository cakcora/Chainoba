create table bitcoin.block
(
	hash char(64) not null
		constraint block_hash
			primary key,
	id bigserial not null
		constraint block_pk
			unique,
	version integer,
	hashprev char(64) not null
		constraint block_hashprev
			unique,
	hashmerkleroot char(64) not null,
	ntime bigint,
	nbits integer not null,
	nnonce bigint not null
);


create table bitcoin.transaction
(
	hash char(64) not null
		constraint transaction_hash
			primary key,
	id bigserial not null
		constraint transaction_pk
			unique,
	version integer,
	locktime integer,
	block_id bigint
		constraint transaction_block_id_fk
			references bitcoin.block (id)
);


create unique index transaction_id_uindex
	on bitcoin.transaction (id);


create table bitcoin.input
(
	id bigserial not null
		constraint input_pk
			primary key,
	prevout_hash char(64) not null,
	prevout_n bigint not null,
	scriptsig bytea,
	sequence bigint,
	transaction_id bigint not null
		constraint input_transaction_id_fk
			references bitcoin.transaction (id),
	prev_output_id bigint
		constraint input_output_id_fk
			references bitcoin.output
);

create table bitcoin.output
(
	id bigserial not null
		constraint output_pkey
			primary key,
	value bigint,
	scriptpubkey bytea,
	transaction_id bigint not null
		constraint output_transaction_id_fk
			references bitcoin.transaction (id),
	index integer not null,
	script_type char(10)
);


create table bitcoin.address
(
	id bigserial not null
		constraint address_pk
			primary key,
	hash char(64) not null,
	public_key char(140),
	address char(64) not null
);


create unique index address_id_uindex
	on bitcoin.address (id);

create unique index address_hash_uindex
	on bitcoin.address (hash);

create table bitcoin.output_address
(
	id bigserial not null
		constraint output_address_pk
			primary key,
	output_id bigint not null
		constraint output_address_output_id_fk
			references bitcoin.output,
	address_id bigint not null
		constraint output_address_address_id_fk
			references bitcoin.address
);


