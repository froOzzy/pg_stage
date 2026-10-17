--
-- PostgreSQL database dump
--

\restrict 9W9p96731YvdEgee7wkHE20Vd9u81UNYjQ6TnpI1c1Qg3DamAzvP6LCKQEQYMK8

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

--
-- Name: schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA schema;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: _table; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public._table (
    column_1 text,
    column_2 text
);


--
-- Name: deleted_table; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.deleted_table (
    field_value text
);


--
-- Name: TABLE deleted_table; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.deleted_table IS 'anon: {"mutation_name":"delete"}';


--
-- Name: invalid_column; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.invalid_column (
    field_value text
);


--
-- Name: COLUMN invalid_column.field_value; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.invalid_column.field_value IS 'anon: {''mutation_name": "null"}';


--
-- Name: kept_table; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kept_table (
    field_value text
);


--
-- Name: TABLE kept_table; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.kept_table IS 'anon: {"mutation_name":"set"}';


--
-- Name: null_column; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.null_column (
    field_value text
);


--
-- Name: COLUMN null_column.field_value; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.null_column.field_value IS 'anon: [{"mutation_name":"null"}]';


--
-- Name: plain_values; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plain_values (
    column_1 text,
    column_2 text
);


--
-- Name: unknown_column; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.unknown_column (
    field_value text
);


--
-- Name: COLUMN unknown_column.field_value; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.unknown_column.field_value IS 'anon: [{"mutation_name":"not_found"}]';


--
-- Name: _table; Type: TABLE; Schema: schema; Owner: -
--

CREATE TABLE schema._table (
    column_1 text,
    column_2 text
);


--
-- Name: deleted_table; Type: TABLE; Schema: schema; Owner: -
--

CREATE TABLE schema.deleted_table (
    field_value text
);


--
-- Name: TABLE deleted_table; Type: COMMENT; Schema: schema; Owner: -
--

COMMENT ON TABLE schema.deleted_table IS 'anon: {"mutation_name":"delete"}';


--
-- Name: invalid_column; Type: TABLE; Schema: schema; Owner: -
--

CREATE TABLE schema.invalid_column (
    field_value text
);


--
-- Name: COLUMN invalid_column.field_value; Type: COMMENT; Schema: schema; Owner: -
--

COMMENT ON COLUMN schema.invalid_column.field_value IS 'anon: {''mutation_name": "null"}';


--
-- Name: kept_table; Type: TABLE; Schema: schema; Owner: -
--

CREATE TABLE schema.kept_table (
    field_value text
);


--
-- Name: TABLE kept_table; Type: COMMENT; Schema: schema; Owner: -
--

COMMENT ON TABLE schema.kept_table IS 'anon: {"mutation_name":"set"}';


--
-- Name: null_column; Type: TABLE; Schema: schema; Owner: -
--

CREATE TABLE schema.null_column (
    field_value text
);


--
-- Name: COLUMN null_column.field_value; Type: COMMENT; Schema: schema; Owner: -
--

COMMENT ON COLUMN schema.null_column.field_value IS 'anon: [{"mutation_name":"null"}]';


--
-- Name: plain_values; Type: TABLE; Schema: schema; Owner: -
--

CREATE TABLE schema.plain_values (
    column_1 text,
    column_2 text
);


--
-- Name: unknown_column; Type: TABLE; Schema: schema; Owner: -
--

CREATE TABLE schema.unknown_column (
    field_value text
);


--
-- Name: COLUMN unknown_column.field_value; Type: COMMENT; Schema: schema; Owner: -
--

COMMENT ON COLUMN schema.unknown_column.field_value IS 'anon: [{"mutation_name":"not_found"}]';


--
-- Data for Name: _table; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public._table (column_1, column_2) FROM stdin;
1	value
\.


--
-- Data for Name: deleted_table; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.deleted_table (field_value) FROM stdin;
value
\.


--
-- Data for Name: invalid_column; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.invalid_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: kept_table; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kept_table (field_value) FROM stdin;
value
\.


--
-- Data for Name: null_column; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.null_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: plain_values; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.plain_values (column_1, column_2) FROM stdin;
1	value
\.


--
-- Data for Name: unknown_column; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.unknown_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: _table; Type: TABLE DATA; Schema: schema; Owner: -
--

COPY schema._table (column_1, column_2) FROM stdin;
1	value
\.


--
-- Data for Name: deleted_table; Type: TABLE DATA; Schema: schema; Owner: -
--

COPY schema.deleted_table (field_value) FROM stdin;
value
\.


--
-- Data for Name: invalid_column; Type: TABLE DATA; Schema: schema; Owner: -
--

COPY schema.invalid_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: kept_table; Type: TABLE DATA; Schema: schema; Owner: -
--

COPY schema.kept_table (field_value) FROM stdin;
value
\.


--
-- Data for Name: null_column; Type: TABLE DATA; Schema: schema; Owner: -
--

COPY schema.null_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: plain_values; Type: TABLE DATA; Schema: schema; Owner: -
--

COPY schema.plain_values (column_1, column_2) FROM stdin;
1	value
\.


--
-- Data for Name: unknown_column; Type: TABLE DATA; Schema: schema; Owner: -
--

COPY schema.unknown_column (field_value) FROM stdin;
value
\.


--
-- PostgreSQL database dump complete
--

\unrestrict 9W9p96731YvdEgee7wkHE20Vd9u81UNYjQ6TnpI1c1Qg3DamAzvP6LCKQEQYMK8

