CREATE TABLE bitcoin.blocks
(
	hash 				VARCHAR,
	size 				BIGINT,
	stripped_size 		BIGINT,
	weight 				BIGINT,
	number 				BIGINT,
	version 			BIGINT,
	merkle_root 		VARCHAR,
	timestamp 			BIGINT,
	nonce 				VARCHAR,
	bits 				VARCHAR,
	coinbase_param 		VARCHAR,
	transaction_count 	BIGINT
);


CREATE TABLE bitcoin.transactions(

	hash 				VARCHAR,
	size 				BIGINT,
	virtual_size 		BIGINT,
	version 			BIGINT,
	lock_time 			BIGINT,
	block_number		BIGINT,
	block_hash			VARCHAR,
	block_timestamp		BIGINT,
	is_coinbase			BOOLEAN,
	index				BIGINT,
	inputs				JSONB,
	outputs				JSONB,
	input_count			BIGINT,
	output_count		BIGINT,
	input_value			BIGINT,
	output_value		BIGINT,
	fee					BIGINT
);
