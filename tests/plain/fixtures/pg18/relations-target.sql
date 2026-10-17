--
-- PostgreSQL database dump
--

\restrict Vcvh11QobCEacuoo6sfaAc2MdruDJgv22wwrN0x92I6F0yrBfUCVmx0F3uXhdvD

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
-- Name: a_target; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.a_target (
    alternate_ref text,
    name text,
    ref text
);


--
-- Name: COLUMN a_target.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.a_target.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "public.b_source", "column_name": "name", "from_column_name": "ref", "to_column_name": "id"}, {"table_name": "public.b_source", "column_name": "name", "from_column_name": "alternate_ref", "to_column_name": "alternate_id"}]}]';


--
-- Name: b_source; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.b_source (
    name text,
    id text,
    alternate_id text
);


--
-- Name: COLUMN b_source.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.b_source.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "public.a_target", "column_name": "name", "from_column_name": "id", "to_column_name": "ref"}, {"table_name": "public.a_target", "column_name": "name", "from_column_name": "alternate_id", "to_column_name": "alternate_ref"}]}]';


--
-- Data for Name: a_target; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.a_target (alternate_ref, name, ref) FROM stdin;
a	Carol	missing-1
b	Dave	missing-2
\.


--
-- Data for Name: b_source; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.b_source (name, id, alternate_id) FROM stdin;
Alice	1	a
Bob	2	b
\.


--
-- PostgreSQL database dump complete
--

\unrestrict Vcvh11QobCEacuoo6sfaAc2MdruDJgv22wwrN0x92I6F0yrBfUCVmx0F3uXhdvD

