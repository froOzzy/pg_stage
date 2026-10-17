--
-- PostgreSQL database dump
--

\restrict lKfyPZYp1Ma7zhbMnDqGBLWEg8a8z2AwMRKWAYQCCkd0pQfhLmzKtHKdvTcDm2H

-- Dumped from database version 15.19
-- Dumped by pg_dump version 15.19

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
    uuid text,
    username text,
    last_name text
);


--
-- Name: COLUMN table_1.uuid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.table_1.uuid IS 'anon: [{"mutation_name": "uuid5_by_source_value", "mutation_kwargs": {"source_column": "username", "namespace": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';


--
-- Name: COLUMN table_1.username; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.table_1.username IS 'anon: [{"mutation_name": "phone_number", "mutation_kwargs": {"mask": "791########", "unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^7[0-9]{10}$"}]}]';


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.table_1 (uuid, username, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	79999999999	111n
20f654fe-b27d-4051-9fd4-000000000002	79888888888	222n
20f654fe-b27d-4051-9fd4-000000000003	79777777777	333n
\.


--
-- PostgreSQL database dump complete
--

\unrestrict lKfyPZYp1Ma7zhbMnDqGBLWEg8a8z2AwMRKWAYQCCkd0pQfhLmzKtHKdvTcDm2H

