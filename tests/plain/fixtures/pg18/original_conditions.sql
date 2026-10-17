--
-- PostgreSQL database dump
--

\restrict AFpPznNejfZfEaAFoXuH4wtD1IdbGBIAfh1rFJZgnRoSOsG677Gjx9t8gaSJnlN

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
    id text,
    status text,
    email text,
    notes text,
    empty text
);


--
-- Name: COLUMN users.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.status IS 'anon: [{"mutation_name": "random_choice", "mutation_kwargs": {"choices": ["changed"]}}]';


--
-- Name: COLUMN users.email; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.email IS 'anon: [{"mutation_name": "random_choice", "mutation_kwargs": {"choices": ["hidden"]}, "conditions": [{"column_name": "status", "operation": "equal", "value": "original"}]}]';


--
-- Name: zz_untouched; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.zz_untouched (
    id text,
    name text
);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, status, email, notes, empty) FROM stdin;
1	original	private	\N	
2	other	private	literal\ttext	
\.


--
-- Data for Name: zz_untouched; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.zz_untouched (id, name) FROM stdin;
3	original
\.


--
-- PostgreSQL database dump complete
--

\unrestrict AFpPznNejfZfEaAFoXuH4wtD1IdbGBIAfh1rFJZgnRoSOsG677Gjx9t8gaSJnlN

