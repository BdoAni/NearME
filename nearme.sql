--
-- PostgreSQL database dump
--

-- Dumped from database version 13.8 (Ubuntu 13.8-1.pgdg20.04+1)
-- Dumped by pg_dump version 13.8 (Ubuntu 13.8-1.pgdg20.04+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: reservations; Type: TABLE; Schema: public; Owner: bdo_ani
--

CREATE TABLE public.reservations (
    reservation_id integer NOT NULL,
    tool_id integer,
    user_id integer,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    price integer NOT NULL,
    total integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.reservations OWNER TO bdo_ani;

--
-- Name: reservations_reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: bdo_ani
--

CREATE SEQUENCE public.reservations_reservation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reservations_reservation_id_seq OWNER TO bdo_ani;

--
-- Name: reservations_reservation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bdo_ani
--

ALTER SEQUENCE public.reservations_reservation_id_seq OWNED BY public.reservations.reservation_id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: bdo_ani
--

CREATE TABLE public.reviews (
    review_id integer NOT NULL,
    tool_id integer,
    user_id integer,
    name character varying(255),
    rating integer,
    comment text,
    created_at timestamp without time zone
);


ALTER TABLE public.reviews OWNER TO bdo_ani;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: bdo_ani
--

CREATE SEQUENCE public.reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_review_id_seq OWNER TO bdo_ani;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bdo_ani
--

ALTER SEQUENCE public.reviews_review_id_seq OWNED BY public.reviews.review_id;


--
-- Name: tools; Type: TABLE; Schema: public; Owner: bdo_ani
--

CREATE TABLE public.tools (
    tool_id integer NOT NULL,
    user_id integer,
    tool_name character varying(255) NOT NULL,
    description text,
    price integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    tool_image character varying
);


ALTER TABLE public.tools OWNER TO bdo_ani;

--
-- Name: tools_tool_id_seq; Type: SEQUENCE; Schema: public; Owner: bdo_ani
--

CREATE SEQUENCE public.tools_tool_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tools_tool_id_seq OWNER TO bdo_ani;

--
-- Name: tools_tool_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bdo_ani
--

ALTER SEQUENCE public.tools_tool_id_seq OWNED BY public.tools.tool_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: bdo_ani
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    email character varying NOT NULL,
    password character varying(255) NOT NULL,
    phone_number character varying(20),
    address character varying(255) NOT NULL,
    about text,
    profile_image character varying,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO bdo_ani;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: bdo_ani
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO bdo_ani;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bdo_ani
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: reservations reservation_id; Type: DEFAULT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.reservations ALTER COLUMN reservation_id SET DEFAULT nextval('public.reservations_reservation_id_seq'::regclass);


--
-- Name: reviews review_id; Type: DEFAULT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.reviews ALTER COLUMN review_id SET DEFAULT nextval('public.reviews_review_id_seq'::regclass);


--
-- Name: tools tool_id; Type: DEFAULT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.tools ALTER COLUMN tool_id SET DEFAULT nextval('public.tools_tool_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: reservations; Type: TABLE DATA; Schema: public; Owner: bdo_ani
--

COPY public.reservations (reservation_id, tool_id, user_id, start_date, end_date, price, total, created_at, updated_at) FROM stdin;
1	1	2	\N	\N	3	5	\N	\N
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: bdo_ani
--

COPY public.reviews (review_id, tool_id, user_id, name, rating, comment, created_at) FROM stdin;
1	1	2	emy	5	the best tool ever I have had used	\N
2	2	4	Ally	5	the best tool!!	\N
3	1	3	\N	5	the best tool!!	\N
\.


--
-- Data for Name: tools; Type: TABLE DATA; Schema: public; Owner: bdo_ani
--

COPY public.tools (tool_id, user_id, tool_name, description, price, created_at, updated_at, tool_image) FROM stdin;
1	2	hammer	bbbblalalal	3	\N	\N	\N
2	4	hammer	bbbblalalal	3	\N	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: bdo_ani
--

COPY public.users (user_id, first_name, last_name, email, password, phone_number, address, about, profile_image, created_at, updated_at) FROM stdin;
2	emy	testMe	test@test.test	test	\N	Seattle WA	\N	\N	\N	\N
3	Ally	testMe	test@test.com	test	\N	Seattle WA	\N	\N	\N	\N
4	Artur	testMe	test@mail.com	test	\N	Seattle WA	\N	\N	\N	\N
\.


--
-- Name: reservations_reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bdo_ani
--

SELECT pg_catalog.setval('public.reservations_reservation_id_seq', 1, true);


--
-- Name: reviews_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bdo_ani
--

SELECT pg_catalog.setval('public.reviews_review_id_seq', 3, true);


--
-- Name: tools_tool_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bdo_ani
--

SELECT pg_catalog.setval('public.tools_tool_id_seq', 2, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bdo_ani
--

SELECT pg_catalog.setval('public.users_user_id_seq', 4, true);


--
-- Name: reservations reservations_pkey; Type: CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_pkey PRIMARY KEY (reservation_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- Name: tools tools_pkey; Type: CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.tools
    ADD CONSTRAINT tools_pkey PRIMARY KEY (tool_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: reservations reservations_tool_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_tool_id_fkey FOREIGN KEY (tool_id) REFERENCES public.tools(tool_id);


--
-- Name: reservations reservations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: reviews reviews_tool_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_tool_id_fkey FOREIGN KEY (tool_id) REFERENCES public.tools(tool_id);


--
-- Name: reviews reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: tools tools_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bdo_ani
--

ALTER TABLE ONLY public.tools
    ADD CONSTRAINT tools_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

