
CREATE USER norloc WITH PASSWORD 'norloc';

ALTER ROLE norloc SET client_encoding TO 'utf8';
ALTER ROLE norloc SET default_transaction_isolation TO 'read committed';
ALTER ROLE norloc SET timezone TO 'UTC';

CREATE DATABASE norloc WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'C.UTF-8';

ALTER DATABASE norloc OWNER TO norloc;

\connect norloc

CREATE EXTENSION postgis;
