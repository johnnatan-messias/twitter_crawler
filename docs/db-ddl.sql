CREATE TABLE access_token(
	id serial,
	token jsonb not null,
	last_usage text not null,
	PRIMARY KEY (id)
);

