BEGIN;
CREATE TABLE "raw_blocks" (
    "id" integer NOT NULL PRIMARY KEY,
    "specific" varchar(8) NOT NULL DEFAULT 'new'
)
;
CREATE TABLE "raw_words" (
    "id" integer NOT NULL PRIMARY KEY,
    "word" varchar(512) NOT NULL,
    "parent_word_id" integer NOT NULL REFERENCES "raw_words" ("id") DEFERRABLE INITIALLY DEFERRED,
    "block_id" integer NOT NULL REFERENCES "raw_blocks" ("id") DEFERRABLE INITIALLY DEFERRED,
    "root" varchar(512) NOT NULL,
    "specific" varchar(512) NOT NULL,
    "num" bigint NOT NULL
)
;

COMMIT;
