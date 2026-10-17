--
-- PostgreSQL database dump
--

\restrict y9J4otsyZa29acDLwzDLz9yYtedCZ76gGeftM0h7aRIl48f5PSsUguDcyINgA1W

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
    message text,
    recipient text,
    notes text
);


--
-- Name: TABLE table_1; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.table_1 IS 'anon: {"mutation_name": "delete"}';


--
-- Name: table_2; Type: TABLE; Schema: schema; Owner: -
--

CREATE TABLE schema.table_2 (
    id text,
    message text,
    recipient text,
    notes text
);


--
-- Name: TABLE table_2; Type: COMMENT; Schema: schema; Owner: -
--

COMMENT ON TABLE schema.table_2 IS 'anon: {"mutation_name": "delete"}';


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.table_1 (id, message, recipient, notes) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	Hello -\nI'm writing in regards to the stuff I've been receiving. Double quotes are "awesome"!	support@example.com	\N
20f654fe-b27d-4051-9fd4-000000000002	Anything	\N	\N
\.


--
-- Data for Name: table_2; Type: TABLE DATA; Schema: schema; Owner: -
--

COPY schema.table_2 (id, message, recipient, notes) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	Hello -\nI'm writing in regards to the stuff I've been receiving. Double quotes are "awesome"!	support@example.com	\N
20f654fe-b27d-4051-9fd4-000000000002	Anything	\N	\N
\.


--
-- PostgreSQL database dump complete
--

\unrestrict y9J4otsyZa29acDLwzDLz9yYtedCZ76gGeftM0h7aRIl48f5PSsUguDcyINgA1W

