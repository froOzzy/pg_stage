--
-- PostgreSQL database dump
--

\restrict pu9b3GQbmpxm0jgQb8AlhuX6jw0Odl1UCy2vPNOakFAAujGSMgQr6YPguFMb26f

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

COMMENT ON COLUMN public.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name"}, "relations": [{"table_name": "public.peers", "column_name": "value", "from_column_name": "id", "to_column_name": "id"}]}]';


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

\unrestrict pu9b3GQbmpxm0jgQb8AlhuX6jw0Odl1UCy2vPNOakFAAujGSMgQr6YPguFMb26f

