--
-- PostgreSQL database dump
--

\restrict FdG2XNhVdHebiuopky8Z72jTdo22H4avkZVPKgesv63O6rWInXdBufkTooIRDYc

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

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

--
-- Name: schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA schema;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: table_1; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.table_1 (
    id text,
    email text,
    active text
);


--
-- Name: COLUMN table_1.email; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.table_1.email IS 'anon: [{"mutation_name": "email", "conditions": [{"column_name": "active", "operation": "equal", "value": "t"}]}]';


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.table_1 (id, email, active) FROM stdin;
1	test@mail.ru	t
2	test@mail.ru	f
\.


--
-- PostgreSQL database dump complete
--

\unrestrict FdG2XNhVdHebiuopky8Z72jTdo22H4avkZVPKgesv63O6rWInXdBufkTooIRDYc

