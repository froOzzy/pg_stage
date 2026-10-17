--
-- PostgreSQL database dump
--

\restrict fi13d6hZ8CodjBYshtVm4af4RUHYjs15g0PNvq6Uxqzic5akxwzyYkLsI9q8ddL

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
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    token text,
    id text,
    name text,
    notes text
);


--
-- Name: COLUMN users.token; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.token IS 'anon: [{"mutation_name": "uuid5_by_source_value", "mutation_kwargs": {"source_column": "name", "namespace": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';


--
-- Name: COLUMN users.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.name IS 'anon: [{"mutation_name": "random_choice", "mutation_kwargs": {"choices": ["hidden"]}}]';


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (token, id, name, notes) FROM stdin;
old-token	1	original	\N
\.


--
-- PostgreSQL database dump complete
--

\unrestrict fi13d6hZ8CodjBYshtVm4af4RUHYjs15g0PNvq6Uxqzic5akxwzyYkLsI9q8ddL

