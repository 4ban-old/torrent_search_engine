BEGIN;
CREATE TABLE "chewed" (
    "id" bigserial PRIMARY KEY,
    "domain_id" integer NOT NULL REFERENCES "domains" ("id") DEFERRABLE INITIALLY DEFERRED, --
    "source_id" bigint NOT NULL, --REFERENCES "source" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "nibbler_status" int NOT NULL DEFAULT 0,
    "page" text NOT NULL,
    "version" integer NOT NULL, --
    "specific" text NOT NULL DEFAULT '{}'
);


CREATE OR REPLACE FUNCTION chewed_partition_function()
	RETURNS TRIGGER AS '
		DECLARE
			table_name varchar := ''chewed_'' ||  NEW.domain_id;
			v_count integer;
		BEGIN
			SELECT count(*) INTO v_count from pg_catalog.pg_tables WHERE schemaname = ''partitions'' AND tablename = table_name;
			IF v_count = 0 THEN
				EXECUTE ''CREATE TABLE  partitions.'' || table_name || ''(
						PRIMARY KEY(id),
						FOREIGN KEY(domain_id) REFERENCES public.domains(id) DEFERRABLE INITIALLY DEFERRED,
						CHECK(domain_id = '' || NEW.domain_id || '')
					) INHERITS (public.chewed)'';
				EXECUTE ''CREATE INDEX '' || table_name || ''_domain_id_index ON partitions.'' || table_name || ''(domain_id)'';
				EXECUTE ''CREATE INDEX '' || table_name || ''_version_index ON partitions.'' || table_name || ''(version)'';
			END IF;
			EXECUTE ''INSERT INTO partitions.'' || quote_ident(table_name) || '' VALUES ($1.*)'' USING NEW;
			return null;
		END
' language 'plpgsql';


CREATE TRIGGER trg_chewed_insert
	BEFORE INSERT ON chewed
	FOR EACH ROW EXECUTE PROCEDURE chewed_partition_function();

COMMIT;
