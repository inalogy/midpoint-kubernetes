#!/bin/bash
set -e
set -e
set +x
if [ "$( psql "postgresql://$DB_USER:$DB_PASSWORD@$DB_ADDR:5432" -XtAc "SELECT 1 FROM pg_database WHERE datname='hr'" )" = '1' ]
then
    echo "Database already exists!"
    exit 0;
fi

psql "postgresql://$DB_USER:$DB_PASSWORD@$DB_ADDR:5432" -v ON_ERROR_STOP=1 <<-EOSQL

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
CREATE DATABASE hr ENCODING = 'UTF8';
-- # LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
ALTER DATABASE addressbook OWNER TO midpoint;

\connect hr 

--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: emp; Type: TYPE; Schema: public; Owner: midpoint
--

CREATE TYPE emp AS ENUM (
    'FTE',
    'PTE',
    'CONTRACTOR',
    'RETIRED'
);


ALTER TYPE public.emp OWNER TO midpoint;

--
-- Name: hibernate_sequence; Type: SEQUENCE; Schema: public; Owner: midpoint
--

CREATE SEQUENCE hibernate_sequence
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hibernate_sequence OWNER TO midpoint;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: usershr; Type: TABLE; Schema: public; Owner: midpoint; Tablespace: 
--

CREATE TABLE usershr (
    id integer NOT NULL,
    artname character varying(255),
    emailaddress character varying(255),
    employeenumber integer,
    emptype character varying(255),
    firstname character varying(255),
    surname character varying(255)
);


ALTER TABLE public.usershr OWNER TO midpoint;

--
-- Name: hibernate_sequence; Type: SEQUENCE SET; Schema: public; Owner: midpoint
--

SELECT pg_catalog.setval('hibernate_sequence', 19, true);


--
-- Data for Name: usershr; Type: TABLE DATA; Schema: public; Owner: midpoint
--

COPY usershr (id, artname, emailaddress, employeenumber, emptype, firstname, surname) FROM stdin;
2	Leonardo	\N	1	FTE	Leonardo	da Vinci
3	Donatello	\N	2	RETIRED	Donatello	di Niccolo di Betto Bardi
4	Raphael	\N	3	CONTRACTOR	Raffaello	Sanzio da Urbino
5	Michelangelo	\N	4	FTE	Michelangelo	di Lodovico Buonarroti Simoni
\.


--
-- Name: usershr_pkey; Type: CONSTRAINT; Schema: public; Owner: midpoint; Tablespace: 
--

ALTER TABLE ONLY usershr
    ADD CONSTRAINT usershr_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

EOSQL
