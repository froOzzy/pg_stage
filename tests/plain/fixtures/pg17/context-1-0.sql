--
-- PostgreSQL database dump
--

\restrict Bidm2bKXiUncXfVb8SklTYGNO0kNBkADsQE5ThJVv4j1nRfr8QOhcH6sCb49eTe

-- Dumped from database version 17.11
-- Dumped by pg_dump version 17.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    value text,
    id text,
    name text
);


--
-- Name: COLUMN users.value; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name", "current_value": "fixed", "obfuscated_values": {"name": "configured"}}}]';


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (value, id, name) FROM stdin;
first	1	Alice
second	2	Bob
\.


--
-- PostgreSQL database dump complete
--

\unrestrict Bidm2bKXiUncXfVb8SklTYGNO0kNBkADsQE5ThJVv4j1nRfr8QOhcH6sCb49eTe

