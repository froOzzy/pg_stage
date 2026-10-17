--
-- PostgreSQL database dump
--

\restrict 81jK4YoccmnzswSleHd6xPC1KVQN3rHgd3wdfdQqqPA3B7nWtS52Nt8RcR43YN3

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: json_values; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"current_value": [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "safe"}}]}}}]';


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.json_values (id, details) FROM stdin;
1	{"current_value": "sensitive"}
\.


--
-- PostgreSQL database dump complete
--

\unrestrict 81jK4YoccmnzswSleHd6xPC1KVQN3rHgd3wdfdQqqPA3B7nWtS52Nt8RcR43YN3

