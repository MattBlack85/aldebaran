CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS "regions"(
    name TEXT,
    type INTEGER
);

ALTER TABLE regions ADD CONSTRAINT unique_region UNIQUE (type);

CREATE TABLE IF NOT EXISTS "transmission_classifications"(
    name TEXT,
    type INTEGER
);

ALTER TABLE transmission_classifications ADD CONSTRAINT unique_type UNIQUE (type);

INSERT INTO regions(type, name) VALUES
(1, 'Asia'),
(2, 'Europe'),
(3, 'Africa'),
(4, 'Oceania'),
(5, 'America'),
(6, 'International')
ON CONFLICT ON CONSTRAINT unique_region DO NOTHING;

INSERT INTO transmission_classifications(type, name) VALUES
(1, 'Imported case only'),
(2, 'Local transmission'),
(3, 'Under investigation')
ON CONFLICT ON CONSTRAINT unique_type DO NOTHING;;

CREATE TABLE IF NOT EXISTS "corona"(
    country TEXT,
    total_cases NUMERIC,
    new_cases NUMERIC,
    total_deaths NUMERIC,
    new_deaths NUMERIC,
    report_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    region INTEGER
);

SELECT create_hypertable('corona', 'report_datetime', 'region', 2, create_default_indexes=>FALSE);

CREATE INDEX IF NOT EXISTS country_rp ON corona (country, report_datetime DESC);
CREATE INDEX IF NOT EXISTS rp_country ON corona (report_datetime DESC, country);
CREATE INDEX IF NOT EXISTS tc_rp ON corona (total_cases, report_datetime DESC);
CREATE INDEX IF NOT EXISTS td_rp ON corona (total_deaths, report_datetime DESC);
CREATE INDEX IF NOT EXISTS nc_rp ON corona (new_cases, report_datetime DESC);
CREATE INDEX IF NOT EXISTS nd_rp ON corona (new_deaths, report_datetime DESC);
CREATE INDEX IF NOT EXISTS region_rp ON corona (region, report_datetime DESC);
ALTER TABLE corona DROP CONSTRAINT IF EXISTS region_name_fkey;
ALTER TABLE corona ADD CONSTRAINT region_name_fkey FOREIGN KEY (region) REFERENCES regions (type);
