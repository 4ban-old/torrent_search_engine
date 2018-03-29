BEGIN;

--------------------------------------- 1 -------------------------------------------------
------------------------------- Создать таблицы ------------------------------------------
CREATE TABLE "domains" (
    "id" SERIAL PRIMARY KEY,
    "domain" varchar(1024) UNIQUE NOT NULL,
    "specific" text DEFAULT '{}'
);
CREATE TABLE "durls" (
    "id" bigserial PRIMARY KEY,
    "domain_id" integer NOT NULL REFERENCES "domains" ("id") DEFERRABLE INITIALLY DEFERRED,
    "pargs" text NOT NULL,
    "actual" boolean NOT NULL DEFAULT true,
    "hooked" boolean NOT NULL DEFAULT false,
    "specific" text NOT NULL DEFAULT '{}',
    "dtime" timestamp NOT NULL DEFAULT now()
);
CREATE TABLE "source" (
    "id" bigserial PRIMARY KEY,
    "domain_id" integer NOT NULL REFERENCES "domains" ("id") DEFERRABLE INITIALLY DEFERRED,
    "durl_id" bigint NOT NULL REFERENCES "durls" ("id") DEFERRABLE INITIALLY DEFERRED,
    "http_status" integer NOT NULL DEFAULT 200, --
    "pudge_status" integer NOT NULL DEFAULT 0, --
    "http" text NOT NULL,
    "html" text NOT NULL,
    "specific" text NOT NULL DEFAULT '{}',
    "dtime" timestamp NOT NULL DEFAULT now() --
);

--------------------------------------------------- 2 ----------------------------------------------
------------------------------------------ Индексы на таблицы --------------------------------------
CREATE INDEX durls_actual_index ON durls ("actual");
CREATE INDEX source_http_code_index ON source("http_status");
CREATE INDEX source_pudge_code_index ON source("pudge_status");
CREATE INDEX source_dtime_index ON source("dtime");

---------------------------------------------------- 3 ------------------------------------------------
--------------------------------------- Создание схемы partition -------------------------------------
CREATE SCHEMA partitions;

----------------------------------------------------- 4 -------------------------------------------------
------------------------------------  Создать тригеры на таблицы ---------------------------------------

-- таблица durls
CREATE or REPLACE FUNCTION durls_partition_function() 
		RETURNS TRIGGER as '
		DECLARE
			-- Получаем название таблицы
			table_name varchar := ''durls_'' || NEW.domain_id;
			v_count integer;
		BEGIN 
			-- Прверяем есть ли таблица в БД
			SELECT count(*) INTO v_count FROM pg_catalog.pg_tables WHERE schemaname = ''partitions'' AND tablename = table_name;
			IF v_count = 0 THEN
				-- Если таблицы нет создаем, наследуя от родителя
				EXECUTE ''CREATE TABLE partitions.'' || table_name || ''(
						PRIMARY KEY(id),
						FOREIGN KEY(domain_id) REFERENCES public.domains (id) DEFERRABLE INITIALLY DEFERRED,
						CHECK(domain_id = '' || NEW.domain_id || '')
					) INHERITS(public.durls)'';
				EXECUTE ''CREATE INDEX '' || table_name || ''_actual_index ON partitions.'' || table_name || '' (actual)'';
				EXECUTE ''CREATE INDEX '' || table_name || ''_domain_id_index ON partitions.'' || table_name || '' (domain_id)'';
			END IF;
			-- Вносим в таблицу данные
			EXECUTE ''INSERT INTO partitions.'' || quote_ident(table_name) || '' VALUES ($1.*)'' USING NEW;
			return null;
		END;
	 'language 'plpgsql';


-- таблица source
CREATE or REPLACE FUNCTION source_partition_function() RETURNS TRIGGER as '
	DECLARE
		domain_id integer := NEW.domain_id;
		table_name varchar := ''source_'' || domain_id;
		v_count integer;
	BEGIN
		SELECT count(*) INTO v_count from pg_catalog.pg_tables WHERE schemaname = ''partitions'' AND tablename = table_name;
		IF v_count = 0 THEN
			EXECUTE '' CREATE TABLE partitions.'' || table_name || '' (
					PRIMARY KEY(id),
					FOREIGN KEY(domain_id) REFERENCES public.domains (id) DEFERRABLE INITIALLY DEFERRED,
					CHECK(domain_id = '' || NEW.domain_id || '')
				) INHERITS (public.source)'';
			EXECUTE ''CREATE INDEX '' || table_name || ''_http_code_index ON partitions.'' || table_name || ''(http_status)'';
			EXECUTE ''CREATE INDEX '' || table_name || ''_pudge_code_index ON partitions.'' || table_name || ''(pudge_status)'';
			EXECUTE ''CREATE INDEX '' || table_name || ''_dtime_index ON partitions.'' || table_name || ''(dtime)'';
		END IF;
		EXECUTE ''INSERT INTO partitions.'' || quote_ident(table_name) || '' VALUES ($1.*)'' USING NEW;
		return null;
	END;
' language 'plpgsql';

-------------------------------------------------- 5 ----------------------------------------------------------
------------------------------------------ Вешаем тригеры на таблицы ---------------------------
-- тригер на таблицу durls
CREATE TRIGGER trg_durl_insert
	before INSERT ON public.durls
	FOR EACH ROW EXECUTE PROCEDURE durls_partition_function();

--тригер на таблицу sources
CREATE TRIGGER trg_source_insert 
	before INSERT ON source
	FOR EACH ROW EXECUTE PROCEDURE source_partition_function();


-- Твое правило я не разбирался 
CREATE OR REPLACE RULE db_table_ignore_duplicates as
on INSERT to durls
where exists (
select 1 from durls where domain_id=new.domain_id AND pargs=new.pargs)
DO INSTEAD NOTHING;

COMMIT;
