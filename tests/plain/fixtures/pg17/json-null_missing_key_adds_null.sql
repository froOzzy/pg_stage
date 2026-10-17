--
-- PostgreSQL database dump
--

\restrict J55hkczRgGah26Ww1xaWkTDcLKEBGdy2kuvo06sKBpHa7tQHp9FDmG4Sbe26R8B

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
-- Name: json_values; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"notes": [{"mutation_name": "null", "mutation_kwargs": {}}]}}}]';


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.json_values (id, details) FROM stdin;
1	{"name": "Frank"}
\.


--
-- PostgreSQL database dump complete
--

\unrestrict J55hkczRgGah26Ww1xaWkTDcLKEBGdy2kuvo06sKBpHa7tQHp9FDmG4Sbe26R8B

