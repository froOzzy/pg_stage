--
-- PostgreSQL database dump
--

\restrict 5yyvSANiLtaypjnWCZTfcEzNXsyIsrZfx65K17aQi5ZNqIit5SsWPSgVz6MDWjk

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
    username text,
    last_name text
);


--
-- Name: COLUMN table_1.username; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.table_1.username IS 'anon: [{"mutation_name": "phone_number", "mutation_kwargs": {"mask": "790########", "unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^7[0-9]{10}$"}, {"column_name": "username", "operation": "by_pattern", "value": "^8[0-9]{10}$"}]}, {"mutation_name": "email", "mutation_kwargs": {"unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^\\S+@\\S+\\.\\S+$"}]}]';


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.table_1 (id, username, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	79999999999	111n
20f654fe-b27d-4051-9fd4-000000000002	test@mail.ru	222n
20f654fe-b27d-4051-9fd4-000000000003	89999999999	333n
\.


--
-- PostgreSQL database dump complete
--

\unrestrict 5yyvSANiLtaypjnWCZTfcEzNXsyIsrZfx65K17aQi5ZNqIit5SsWPSgVz6MDWjk

