#!/bin/bash
set -e
set +x
if [ "$( psql "postgresql://$DB_USER:$DB_PASSWORD@$DB_ADDR:5432" -XtAc "SELECT 1 FROM pg_database WHERE datname='midpoint'" )" = '1' ]
then
    echo "Database already exists!"
    exit 0;
fi

psql "postgresql://$DB_USER:$DB_PASSWORD@$DB_ADDR:5432" -v ON_ERROR_STOP=1 <<-EOSQL
--
-- PostgreSQL database dump
--
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
-- DROP DATABASE IF EXISTS keycloak;
--
CREATE DATABASE midpoint ENCODING = 'UTF8'; 
-- # LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
ALTER DATABASE midpoint OWNER TO midpoint;
--
-- PostgreSQL database dump complete
--
EOSQL

exit 0
