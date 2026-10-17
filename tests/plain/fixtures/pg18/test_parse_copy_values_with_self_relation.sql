--
-- PostgreSQL database dump
--

\restrict g6EfQ1e8LvrOeVbaHizGh1EK2J7SIGOxnA18jkYSUstykwdHQQOaORZyde4NZ5v

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
    first_name text,
    last_name text
);


--
-- Name: COLUMN table_1.first_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.table_1.first_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "public.table_1", "column_name": "last_name", "from_column_name": "id", "to_column_name": "id"}]}]';


--
-- Name: COLUMN table_1.last_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.table_1.last_name IS 'anon: [{"mutation_name": "last_name", "relations": [{"table_name": "public.table_1", "column_name": "first_name", "from_column_name": "id", "to_column_name": "id"}]}]';


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.table_1 (id, first_name, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	111n
20f654fe-b27d-4051-9fd4-000000000002	222n	222n
\.


--
-- PostgreSQL database dump complete
--

\unrestrict g6EfQ1e8LvrOeVbaHizGh1EK2J7SIGOxnA18jkYSUstykwdHQQOaORZyde4NZ5v

