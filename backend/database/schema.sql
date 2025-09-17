CREATE TABLE public.emission_records (
	id_record serial NOT NULL,
	person_name varchar NOT NULL,
	emission_amount numeric NOT NULL,
	distance numeric (5, 2) NOT NULL,
	people_amount int,
	vehicle varchar NOT NULL,
	fuel varchar NOT NULL,
	CONSTRAINT emission_records_pk PRIMARY KEY (id_record)
);