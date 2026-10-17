--
-- PostgreSQL database dump
--

\restrict hIrehzzDwY44l8sLCD4kF4R5UY47uNjtX20CYpagQLm5AieCz3ftFXHCTDVK7tq

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

COMMENT ON COLUMN public.table_1.first_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "public.table_2", "column_name": "f_name", "from_column_name": "id", "to_column_name": "uuid"}, {"table_name": "public.table_3", "column_name": "fir_name", "from_column_name": "id", "to_column_name": "identifier"}]}]';


--
-- Name: table_2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.table_2 (
    uuid text,
    f_name text,
    l_name text
);


--
-- Name: COLUMN table_2.f_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.table_2.f_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "public.table_1", "column_name": "first_name", "from_column_name": "uuid", "to_column_name": "id"}, {"table_name": "public.table_3", "column_name": "fir_name", "from_column_name": "uuid", "to_column_name": "identifier"}]}]';


--
-- Name: table_3; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.table_3 (
    identifier text,
    fir_name text,
    las_name text
);


--
-- Name: COLUMN table_3.fir_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.table_3.fir_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "public.table_1", "column_name": "first_name", "from_column_name": "identifier", "to_column_name": "id"}, {"table_name": "public.table_2", "column_name": "f_name", "from_column_name": "identifier", "to_column_name": "uuid"}]}]';


--
-- Name: table_4; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.table_4 (
    identifier text,
    fir_name text,
    las_name text
);


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.table_1 (id, first_name, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.


--
-- Data for Name: table_2; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.table_2 (uuid, f_name, l_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.


--
-- Data for Name: table_3; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.table_3 (identifier, fir_name, las_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.


--
-- Data for Name: table_4; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.table_4 (identifier, fir_name, las_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.


--
-- PostgreSQL database dump complete
--

\unrestrict hIrehzzDwY44l8sLCD4kF4R5UY47uNjtX20CYpagQLm5AieCz3ftFXHCTDVK7tq

