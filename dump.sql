--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13
-- Dumped by pg_dump version 14.13

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: graintrack
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO graintrack;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: graintrack
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying NOT NULL,
    parent_category_id integer,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.categories OWNER TO graintrack;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: graintrack
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO graintrack;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: graintrack
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: graintrack
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    price numeric(10,2) NOT NULL,
    discount_percent numeric(10,2),
    stock_quantity integer DEFAULT 0 NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    is_discount boolean DEFAULT false NOT NULL,
    category_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.products OWNER TO graintrack;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: graintrack
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO graintrack;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: graintrack
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: reserves; Type: TABLE; Schema: public; Owner: graintrack
--

CREATE TABLE public.reserves (
    id integer NOT NULL,
    user_id uuid NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.reserves OWNER TO graintrack;

--
-- Name: reserves_id_seq; Type: SEQUENCE; Schema: public; Owner: graintrack
--

CREATE SEQUENCE public.reserves_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reserves_id_seq OWNER TO graintrack;

--
-- Name: reserves_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: graintrack
--

ALTER SEQUENCE public.reserves_id_seq OWNED BY public.reserves.id;


--
-- Name: sales; Type: TABLE; Schema: public; Owner: graintrack
--

CREATE TABLE public.sales (
    id integer NOT NULL,
    user_id uuid NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.sales OWNER TO graintrack;

--
-- Name: sales_id_seq; Type: SEQUENCE; Schema: public; Owner: graintrack
--

CREATE SEQUENCE public.sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sales_id_seq OWNER TO graintrack;

--
-- Name: sales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: graintrack
--

ALTER SEQUENCE public.sales_id_seq OWNED BY public.sales.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: graintrack
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    username character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_admin boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO graintrack;

--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: reserves id; Type: DEFAULT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.reserves ALTER COLUMN id SET DEFAULT nextval('public.reserves_id_seq'::regclass);


--
-- Name: sales id; Type: DEFAULT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.sales ALTER COLUMN id SET DEFAULT nextval('public.sales_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: graintrack
--

COPY public.alembic_version (version_num) FROM stdin;
e07b38d37e2c
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: graintrack
--

COPY public.categories (id, name, parent_category_id, created_at, updated_at) FROM stdin;
1	food	\N	2024-08-31 13:21:12.172023+00	2024-08-31 13:21:12.172023+00
2	vegatables	1	2024-08-31 13:28:34.96106+00	2024-08-31 13:28:34.96106+00
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: graintrack
--

COPY public.products (id, name, description, price, discount_percent, stock_quantity, is_active, is_discount, category_id, created_at, updated_at) FROM stdin;
1	apples	white apples	200.00	50.00	4	t	t	1	2024-08-31 15:07:05.447227+00	2024-09-01 13:18:53.00124+00
3	apple	red apples	200.00	\N	3	t	f	2	2024-08-31 15:07:59.607374+00	2024-09-01 13:45:07.751322+00
\.


--
-- Data for Name: reserves; Type: TABLE DATA; Schema: public; Owner: graintrack
--

COPY public.reserves (id, user_id, product_id, quantity, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: sales; Type: TABLE DATA; Schema: public; Owner: graintrack
--

COPY public.sales (id, user_id, product_id, quantity, created_at, updated_at) FROM stdin;
1	a3542b76-8532-4d8c-965b-0a333e103f13	1	1	2024-09-01 13:18:53.00124+00	2024-09-01 13:18:53.00124+00
2	a3542b76-8532-4d8c-965b-0a333e103f13	3	2	2024-09-01 13:45:07.751322+00	2024-09-01 13:45:07.751322+00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: graintrack
--

COPY public.users (id, username, hashed_password, is_admin, created_at, updated_at) FROM stdin;
a3542b76-8532-4d8c-965b-0a333e103f13	admin	$2b$12$NNv9iZyJizy0OQ.4p00kJO4dpTUsYHDqQ2.VXQw1ZwmftHymEi6XW	t	2024-08-31 12:37:35.973302+00	2024-08-31 12:37:35.973302+00
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: graintrack
--

SELECT pg_catalog.setval('public.categories_id_seq', 2, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: graintrack
--

SELECT pg_catalog.setval('public.products_id_seq', 3, true);


--
-- Name: reserves_id_seq; Type: SEQUENCE SET; Schema: public; Owner: graintrack
--

SELECT pg_catalog.setval('public.reserves_id_seq', 10, true);


--
-- Name: sales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: graintrack
--

SELECT pg_catalog.setval('public.sales_id_seq', 2, true);


--
-- Name: reserves _user_product_uc; Type: CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT _user_product_uc UNIQUE (user_id, product_id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: reserves reserves_pkey; Type: CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT reserves_pkey PRIMARY KEY (id);


--
-- Name: sales sales_pkey; Type: CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: graintrack
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- Name: ix_products_id; Type: INDEX; Schema: public; Owner: graintrack
--

CREATE INDEX ix_products_id ON public.products USING btree (id);


--
-- Name: ix_reserves_id; Type: INDEX; Schema: public; Owner: graintrack
--

CREATE INDEX ix_reserves_id ON public.reserves USING btree (id);


--
-- Name: ix_sales_id; Type: INDEX; Schema: public; Owner: graintrack
--

CREATE INDEX ix_sales_id ON public.sales USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: graintrack
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: categories categories_parent_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_parent_category_id_fkey FOREIGN KEY (parent_category_id) REFERENCES public.categories(id);


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: reserves reserves_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT reserves_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: reserves reserves_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT reserves_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: sales sales_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: sales sales_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: graintrack
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

