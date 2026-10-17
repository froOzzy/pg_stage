--
-- PostgreSQL database dump
--

\restrict YbzhIBRjWG5ZR0YPa9VQrnRuAgVcXArVewxLm3awhV0PJbCJ63McBgPG2TjNrKd

-- Dumped from database version 16.15
-- Dumped by pg_dump version 16.15

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: a_source; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.a_source (
    name text,
    id text,
    alternate_id text
);


--
-- Name: COLUMN a_source.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.a_source.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "public.b_target", "column_name": "name", "from_column_name": "id", "to_column_name": "ref"}, {"table_name": "public.b_target", "column_name": "name", "from_column_name": "alternate_id", "to_column_name": "alternate_ref"}]}]';


--
-- Name: b_target; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.b_target (
    alternate_ref text,
    name text,
    ref text
);


--
-- Name: COLUMN b_target.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.b_target.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "public.a_source", "column_name": "name", "from_column_name": "ref", "to_column_name": "id"}, {"table_name": "public.a_source", "column_name": "name", "from_column_name": "alternate_ref", "to_column_name": "alternate_id"}]}]';


--
-- Data for Name: a_source; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.a_source (name, id, alternate_id) FROM stdin;
Alice	1	a
Bob	2	b
\.


--
-- Data for Name: b_target; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.b_target (alternate_ref, name, ref) FROM stdin;
a	Carol	missing-1
b	Dave	missing-2
\.


--
-- PostgreSQL database dump complete
--

\unrestrict YbzhIBRjWG5ZR0YPa9VQrnRuAgVcXArVewxLm3awhV0PJbCJ63McBgPG2TjNrKd

