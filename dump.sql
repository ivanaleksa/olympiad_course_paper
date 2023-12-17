--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-1.pgdg20.04+1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-1.pgdg20.04+1)

-- Started on 2023-12-17 18:24:30 +04

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
-- TOC entry 9 (class 2615 OID 33364)
-- Name: olympiad; Type: SCHEMA; Schema: -; Owner: student
--

CREATE SCHEMA olympiad;


ALTER SCHEMA olympiad OWNER TO student;

--
-- TOC entry 264 (class 1255 OID 34165)
-- Name: result_log_trigger_function(); Type: FUNCTION; Schema: olympiad; Owner: student
--

CREATE FUNCTION olympiad.result_log_trigger_function() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
INSERT INTO olympiad.result_log (date_happened, happened_action, result_id)
	VALUES (current_timestamp, 'INSERT', new.id);
RETURN NEW;
END;
$$;


ALTER FUNCTION olympiad.result_log_trigger_function() OWNER TO student;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 230 (class 1259 OID 33946)
-- Name: countries; Type: TABLE; Schema: olympiad; Owner: student
--

CREATE TABLE olympiad.countries (
    id integer NOT NULL,
    country_code text,
    country_name text
);


ALTER TABLE olympiad.countries OWNER TO student;

--
-- TOC entry 229 (class 1259 OID 33944)
-- Name: countries_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.countries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.countries_id_seq OWNER TO student;

--
-- TOC entry 3221 (class 0 OID 0)
-- Dependencies: 229
-- Name: countries_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.countries_id_seq OWNED BY olympiad.countries.id;


--
-- TOC entry 232 (class 1259 OID 33959)
-- Name: participants; Type: TABLE; Schema: olympiad; Owner: student
--

CREATE TABLE olympiad.participants (
    id integer NOT NULL,
    country_code text,
    name text,
    surname text,
    birthdate date
);


ALTER TABLE olympiad.participants OWNER TO student;

--
-- TOC entry 253 (class 1259 OID 34084)
-- Name: start_results; Type: TABLE; Schema: olympiad; Owner: student
--

CREATE TABLE olympiad.start_results (
    id integer NOT NULL,
    sport_type_id integer NOT NULL,
    participant_id integer NOT NULL,
    sport_ground_id integer NOT NULL,
    result_sec numeric(8,2),
    "position" integer
);


ALTER TABLE olympiad.start_results OWNER TO student;

--
-- TOC entry 254 (class 1259 OID 34110)
-- Name: country_medal; Type: VIEW; Schema: olympiad; Owner: student
--

CREATE VIEW olympiad.country_medal AS
 SELECT c.country_name,
    r."position",
    count(*) AS count
   FROM ((olympiad.start_results r
     JOIN olympiad.participants p ON ((r.participant_id = p.id)))
     JOIN olympiad.countries c ON ((p.country_code = c.country_code)))
  WHERE (r."position" <= 3)
  GROUP BY c.country_name, r."position"
  ORDER BY r."position", (count(*)) DESC;


ALTER TABLE olympiad.country_medal OWNER TO student;

--
-- TOC entry 259 (class 1259 OID 34141)
-- Name: medals_per_cuntries; Type: VIEW; Schema: olympiad; Owner: student
--

CREATE VIEW olympiad.medals_per_cuntries AS
 SELECT p.country_code,
    count(
        CASE
            WHEN (res."position" = 1) THEN 1
            ELSE NULL::integer
        END) AS gold_count,
    count(
        CASE
            WHEN (res."position" = 2) THEN 1
            ELSE NULL::integer
        END) AS silver_count,
    count(
        CASE
            WHEN (res."position" = 3) THEN 1
            ELSE NULL::integer
        END) AS bronze_count
   FROM (olympiad.start_results res
     JOIN olympiad.participants p ON ((res.participant_id = p.id)))
  WHERE (res."position" <= 3)
  GROUP BY p.country_code
  ORDER BY (count(
        CASE
            WHEN (res."position" = 1) THEN 1
            ELSE NULL::integer
        END)) DESC, (count(
        CASE
            WHEN (res."position" = 2) THEN 1
            ELSE NULL::integer
        END)) DESC, (count(
        CASE
            WHEN (res."position" = 3) THEN 1
            ELSE NULL::integer
        END)) DESC;


ALTER TABLE olympiad.medals_per_cuntries OWNER TO student;

--
-- TOC entry 236 (class 1259 OID 33986)
-- Name: sports_type; Type: TABLE; Schema: olympiad; Owner: student
--

CREATE TABLE olympiad.sports_type (
    id integer NOT NULL,
    name text,
    type text DEFAULT 'индивидуальный'::text,
    description text,
    season text DEFAULT 'лето'::text,
    CONSTRAINT descr_length_check CHECK ((char_length(description) < 255)),
    CONSTRAINT season_check CHECK (((season = 'зима'::text) OR (season = 'лето'::text))),
    CONSTRAINT sport_type_check CHECK (((type = 'командный'::text) OR (type = 'индивидуальный'::text)))
);


ALTER TABLE olympiad.sports_type OWNER TO student;

--
-- TOC entry 258 (class 1259 OID 34137)
-- Name: participant_results; Type: VIEW; Schema: olympiad; Owner: student
--

CREATE VIEW olympiad.participant_results AS
 SELECT res.id,
    t.name AS type,
    p.name,
    p.surname,
    res.result_sec,
    res."position"
   FROM ((olympiad.start_results res
     JOIN olympiad.participants p ON ((p.id = res.participant_id)))
     JOIN olympiad.sports_type t ON ((t.id = res.sport_type_id)));


ALTER TABLE olympiad.participant_results OWNER TO student;

--
-- TOC entry 244 (class 1259 OID 34032)
-- Name: participant_sport_type; Type: TABLE; Schema: olympiad; Owner: student
--

CREATE TABLE olympiad.participant_sport_type (
    id bigint NOT NULL,
    participant_id integer NOT NULL,
    sport_type_id integer NOT NULL
);


ALTER TABLE olympiad.participant_sport_type OWNER TO student;

--
-- TOC entry 241 (class 1259 OID 34026)
-- Name: participant_sport_type_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.participant_sport_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.participant_sport_type_id_seq OWNER TO student;

--
-- TOC entry 3222 (class 0 OID 0)
-- Dependencies: 241
-- Name: participant_sport_type_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.participant_sport_type_id_seq OWNED BY olympiad.participant_sport_type.id;


--
-- TOC entry 242 (class 1259 OID 34028)
-- Name: participant_sport_type_participant_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.participant_sport_type_participant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.participant_sport_type_participant_id_seq OWNER TO student;

--
-- TOC entry 3223 (class 0 OID 0)
-- Dependencies: 242
-- Name: participant_sport_type_participant_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.participant_sport_type_participant_id_seq OWNED BY olympiad.participant_sport_type.participant_id;


--
-- TOC entry 243 (class 1259 OID 34030)
-- Name: participant_sport_type_sport_type_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.participant_sport_type_sport_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.participant_sport_type_sport_type_id_seq OWNER TO student;

--
-- TOC entry 3224 (class 0 OID 0)
-- Dependencies: 243
-- Name: participant_sport_type_sport_type_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.participant_sport_type_sport_type_id_seq OWNED BY olympiad.participant_sport_type.sport_type_id;


--
-- TOC entry 231 (class 1259 OID 33957)
-- Name: participants_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.participants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.participants_id_seq OWNER TO student;

--
-- TOC entry 3225 (class 0 OID 0)
-- Dependencies: 231
-- Name: participants_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.participants_id_seq OWNED BY olympiad.participants.id;


--
-- TOC entry 262 (class 1259 OID 34150)
-- Name: result_log; Type: TABLE; Schema: olympiad; Owner: student
--

CREATE TABLE olympiad.result_log (
    id integer NOT NULL,
    date_happened timestamp without time zone,
    happened_action text,
    result_id integer NOT NULL
);


ALTER TABLE olympiad.result_log OWNER TO student;

--
-- TOC entry 260 (class 1259 OID 34146)
-- Name: result_log_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.result_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.result_log_id_seq OWNER TO student;

--
-- TOC entry 3226 (class 0 OID 0)
-- Dependencies: 260
-- Name: result_log_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.result_log_id_seq OWNED BY olympiad.result_log.id;


--
-- TOC entry 261 (class 1259 OID 34148)
-- Name: result_log_result_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.result_log_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.result_log_result_id_seq OWNER TO student;

--
-- TOC entry 3227 (class 0 OID 0)
-- Dependencies: 261
-- Name: result_log_result_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.result_log_result_id_seq OWNED BY olympiad.result_log.result_id;


--
-- TOC entry 234 (class 1259 OID 33975)
-- Name: sports_grounds; Type: TABLE; Schema: olympiad; Owner: student
--

CREATE TABLE olympiad.sports_grounds (
    id integer NOT NULL,
    name text,
    city text
);


ALTER TABLE olympiad.sports_grounds OWNER TO student;

--
-- TOC entry 255 (class 1259 OID 34115)
-- Name: results_table_view; Type: VIEW; Schema: olympiad; Owner: student
--

CREATE VIEW olympiad.results_table_view AS
 SELECT sr.id,
    st.name AS sport_type,
    p.name AS participant_name,
    p.surname,
    sg.name AS sport_ground,
    sr.result_sec,
    sr."position"
   FROM (((olympiad.start_results sr
     JOIN olympiad.sports_type st ON ((sr.sport_type_id = st.id)))
     JOIN olympiad.participants p ON ((p.id = sr.participant_id)))
     JOIN olympiad.sports_grounds sg ON ((sg.id = sr.sport_ground_id)));


ALTER TABLE olympiad.results_table_view OWNER TO student;

--
-- TOC entry 248 (class 1259 OID 34058)
-- Name: starts_schedule; Type: TABLE; Schema: olympiad; Owner: student
--

CREATE TABLE olympiad.starts_schedule (
    id integer NOT NULL,
    sport_type_id integer NOT NULL,
    start_date date NOT NULL,
    start_time time without time zone NOT NULL,
    sport_ground_id integer NOT NULL
);


ALTER TABLE olympiad.starts_schedule OWNER TO student;

--
-- TOC entry 256 (class 1259 OID 34120)
-- Name: schedule_table_view; Type: VIEW; Schema: olympiad; Owner: student
--

CREATE VIEW olympiad.schedule_table_view AS
 SELECT ss.id,
    st.name AS sport_type,
    ss.start_date,
    ss.start_time,
    sg.name AS sport_ground
   FROM ((olympiad.starts_schedule ss
     JOIN olympiad.sports_type st ON ((ss.sport_type_id = st.id)))
     JOIN olympiad.sports_grounds sg ON ((sg.id = ss.sport_ground_id)));


ALTER TABLE olympiad.schedule_table_view OWNER TO student;

--
-- TOC entry 240 (class 1259 OID 34006)
-- Name: sports_ground_sport_type; Type: TABLE; Schema: olympiad; Owner: student
--

CREATE TABLE olympiad.sports_ground_sport_type (
    id bigint NOT NULL,
    sport_type_id integer NOT NULL,
    sport_ground_id integer NOT NULL
);


ALTER TABLE olympiad.sports_ground_sport_type OWNER TO student;

--
-- TOC entry 237 (class 1259 OID 34000)
-- Name: sports_ground_sport_type_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.sports_ground_sport_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.sports_ground_sport_type_id_seq OWNER TO student;

--
-- TOC entry 3228 (class 0 OID 0)
-- Dependencies: 237
-- Name: sports_ground_sport_type_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.sports_ground_sport_type_id_seq OWNED BY olympiad.sports_ground_sport_type.id;


--
-- TOC entry 239 (class 1259 OID 34004)
-- Name: sports_ground_sport_type_sport_ground_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.sports_ground_sport_type_sport_ground_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.sports_ground_sport_type_sport_ground_id_seq OWNER TO student;

--
-- TOC entry 3229 (class 0 OID 0)
-- Dependencies: 239
-- Name: sports_ground_sport_type_sport_ground_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.sports_ground_sport_type_sport_ground_id_seq OWNED BY olympiad.sports_ground_sport_type.sport_ground_id;


--
-- TOC entry 238 (class 1259 OID 34002)
-- Name: sports_ground_sport_type_sport_type_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.sports_ground_sport_type_sport_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.sports_ground_sport_type_sport_type_id_seq OWNER TO student;

--
-- TOC entry 3230 (class 0 OID 0)
-- Dependencies: 238
-- Name: sports_ground_sport_type_sport_type_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.sports_ground_sport_type_sport_type_id_seq OWNED BY olympiad.sports_ground_sport_type.sport_type_id;


--
-- TOC entry 233 (class 1259 OID 33973)
-- Name: sports_grounds_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.sports_grounds_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.sports_grounds_id_seq OWNER TO student;

--
-- TOC entry 3231 (class 0 OID 0)
-- Dependencies: 233
-- Name: sports_grounds_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.sports_grounds_id_seq OWNED BY olympiad.sports_grounds.id;


--
-- TOC entry 235 (class 1259 OID 33984)
-- Name: sports_type_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.sports_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.sports_type_id_seq OWNER TO student;

--
-- TOC entry 3232 (class 0 OID 0)
-- Dependencies: 235
-- Name: sports_type_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.sports_type_id_seq OWNED BY olympiad.sports_type.id;


--
-- TOC entry 249 (class 1259 OID 34076)
-- Name: start_results_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.start_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.start_results_id_seq OWNER TO student;

--
-- TOC entry 3233 (class 0 OID 0)
-- Dependencies: 249
-- Name: start_results_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.start_results_id_seq OWNED BY olympiad.start_results.id;


--
-- TOC entry 251 (class 1259 OID 34080)
-- Name: start_results_participant_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.start_results_participant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.start_results_participant_id_seq OWNER TO student;

--
-- TOC entry 3234 (class 0 OID 0)
-- Dependencies: 251
-- Name: start_results_participant_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.start_results_participant_id_seq OWNED BY olympiad.start_results.participant_id;


--
-- TOC entry 252 (class 1259 OID 34082)
-- Name: start_results_sport_ground_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.start_results_sport_ground_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.start_results_sport_ground_id_seq OWNER TO student;

--
-- TOC entry 3235 (class 0 OID 0)
-- Dependencies: 252
-- Name: start_results_sport_ground_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.start_results_sport_ground_id_seq OWNED BY olympiad.start_results.sport_ground_id;


--
-- TOC entry 250 (class 1259 OID 34078)
-- Name: start_results_sport_type_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.start_results_sport_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.start_results_sport_type_id_seq OWNER TO student;

--
-- TOC entry 3236 (class 0 OID 0)
-- Dependencies: 250
-- Name: start_results_sport_type_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.start_results_sport_type_id_seq OWNED BY olympiad.start_results.sport_type_id;


--
-- TOC entry 257 (class 1259 OID 34133)
-- Name: start_schedule_on_date; Type: VIEW; Schema: olympiad; Owner: student
--

CREATE VIEW olympiad.start_schedule_on_date AS
 SELECT ss.id,
    sg.name,
    ss.start_date,
    ss.start_time
   FROM (olympiad.starts_schedule ss
     JOIN olympiad.sports_grounds sg ON ((sg.id = ss.sport_ground_id)));


ALTER TABLE olympiad.start_schedule_on_date OWNER TO student;

--
-- TOC entry 245 (class 1259 OID 34052)
-- Name: starts_schedule_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.starts_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.starts_schedule_id_seq OWNER TO student;

--
-- TOC entry 3237 (class 0 OID 0)
-- Dependencies: 245
-- Name: starts_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.starts_schedule_id_seq OWNED BY olympiad.starts_schedule.id;


--
-- TOC entry 247 (class 1259 OID 34056)
-- Name: starts_schedule_sport_ground_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.starts_schedule_sport_ground_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.starts_schedule_sport_ground_id_seq OWNER TO student;

--
-- TOC entry 3238 (class 0 OID 0)
-- Dependencies: 247
-- Name: starts_schedule_sport_ground_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.starts_schedule_sport_ground_id_seq OWNED BY olympiad.starts_schedule.sport_ground_id;


--
-- TOC entry 246 (class 1259 OID 34054)
-- Name: starts_schedule_sport_type_id_seq; Type: SEQUENCE; Schema: olympiad; Owner: student
--

CREATE SEQUENCE olympiad.starts_schedule_sport_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE olympiad.starts_schedule_sport_type_id_seq OWNER TO student;

--
-- TOC entry 3239 (class 0 OID 0)
-- Dependencies: 246
-- Name: starts_schedule_sport_type_id_seq; Type: SEQUENCE OWNED BY; Schema: olympiad; Owner: student
--

ALTER SEQUENCE olympiad.starts_schedule_sport_type_id_seq OWNED BY olympiad.starts_schedule.sport_type_id;


--
-- TOC entry 2992 (class 2604 OID 33949)
-- Name: countries id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.countries ALTER COLUMN id SET DEFAULT nextval('olympiad.countries_id_seq'::regclass);


--
-- TOC entry 3004 (class 2604 OID 34035)
-- Name: participant_sport_type id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participant_sport_type ALTER COLUMN id SET DEFAULT nextval('olympiad.participant_sport_type_id_seq'::regclass);


--
-- TOC entry 3005 (class 2604 OID 34036)
-- Name: participant_sport_type participant_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participant_sport_type ALTER COLUMN participant_id SET DEFAULT nextval('olympiad.participant_sport_type_participant_id_seq'::regclass);


--
-- TOC entry 3006 (class 2604 OID 34037)
-- Name: participant_sport_type sport_type_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participant_sport_type ALTER COLUMN sport_type_id SET DEFAULT nextval('olympiad.participant_sport_type_sport_type_id_seq'::regclass);


--
-- TOC entry 2993 (class 2604 OID 33962)
-- Name: participants id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participants ALTER COLUMN id SET DEFAULT nextval('olympiad.participants_id_seq'::regclass);


--
-- TOC entry 3014 (class 2604 OID 34153)
-- Name: result_log id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.result_log ALTER COLUMN id SET DEFAULT nextval('olympiad.result_log_id_seq'::regclass);


--
-- TOC entry 3015 (class 2604 OID 34154)
-- Name: result_log result_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.result_log ALTER COLUMN result_id SET DEFAULT nextval('olympiad.result_log_result_id_seq'::regclass);


--
-- TOC entry 3001 (class 2604 OID 34009)
-- Name: sports_ground_sport_type id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_ground_sport_type ALTER COLUMN id SET DEFAULT nextval('olympiad.sports_ground_sport_type_id_seq'::regclass);


--
-- TOC entry 3002 (class 2604 OID 34010)
-- Name: sports_ground_sport_type sport_type_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_ground_sport_type ALTER COLUMN sport_type_id SET DEFAULT nextval('olympiad.sports_ground_sport_type_sport_type_id_seq'::regclass);


--
-- TOC entry 3003 (class 2604 OID 34011)
-- Name: sports_ground_sport_type sport_ground_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_ground_sport_type ALTER COLUMN sport_ground_id SET DEFAULT nextval('olympiad.sports_ground_sport_type_sport_ground_id_seq'::regclass);


--
-- TOC entry 2994 (class 2604 OID 33978)
-- Name: sports_grounds id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_grounds ALTER COLUMN id SET DEFAULT nextval('olympiad.sports_grounds_id_seq'::regclass);


--
-- TOC entry 2995 (class 2604 OID 33989)
-- Name: sports_type id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_type ALTER COLUMN id SET DEFAULT nextval('olympiad.sports_type_id_seq'::regclass);


--
-- TOC entry 3010 (class 2604 OID 34087)
-- Name: start_results id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.start_results ALTER COLUMN id SET DEFAULT nextval('olympiad.start_results_id_seq'::regclass);


--
-- TOC entry 3011 (class 2604 OID 34088)
-- Name: start_results sport_type_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.start_results ALTER COLUMN sport_type_id SET DEFAULT nextval('olympiad.start_results_sport_type_id_seq'::regclass);


--
-- TOC entry 3012 (class 2604 OID 34089)
-- Name: start_results participant_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.start_results ALTER COLUMN participant_id SET DEFAULT nextval('olympiad.start_results_participant_id_seq'::regclass);


--
-- TOC entry 3013 (class 2604 OID 34090)
-- Name: start_results sport_ground_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.start_results ALTER COLUMN sport_ground_id SET DEFAULT nextval('olympiad.start_results_sport_ground_id_seq'::regclass);


--
-- TOC entry 3007 (class 2604 OID 34061)
-- Name: starts_schedule id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.starts_schedule ALTER COLUMN id SET DEFAULT nextval('olympiad.starts_schedule_id_seq'::regclass);


--
-- TOC entry 3008 (class 2604 OID 34062)
-- Name: starts_schedule sport_type_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.starts_schedule ALTER COLUMN sport_type_id SET DEFAULT nextval('olympiad.starts_schedule_sport_type_id_seq'::regclass);


--
-- TOC entry 3009 (class 2604 OID 34063)
-- Name: starts_schedule sport_ground_id; Type: DEFAULT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.starts_schedule ALTER COLUMN sport_ground_id SET DEFAULT nextval('olympiad.starts_schedule_sport_ground_id_seq'::regclass);


--
-- TOC entry 3189 (class 0 OID 33946)
-- Dependencies: 230
-- Data for Name: countries; Type: TABLE DATA; Schema: olympiad; Owner: student
--

INSERT INTO olympiad.countries (id, country_code, country_name) VALUES (1, 'RU', 'Russia');
INSERT INTO olympiad.countries (id, country_code, country_name) VALUES (2, 'US', 'United States of America');
INSERT INTO olympiad.countries (id, country_code, country_name) VALUES (3, 'EN', 'England');
INSERT INTO olympiad.countries (id, country_code, country_name) VALUES (4, 'CN', 'China');
INSERT INTO olympiad.countries (id, country_code, country_name) VALUES (5, 'IND', 'India');
INSERT INTO olympiad.countries (id, country_code, country_name) VALUES (6, 'JPN', 'Japan');
INSERT INTO olympiad.countries (id, country_code, country_name) VALUES (7, 'GRM', 'Germany');
INSERT INTO olympiad.countries (id, country_code, country_name) VALUES (8, 'BRZ', 'Brazil');


--
-- TOC entry 3203 (class 0 OID 34032)
-- Dependencies: 244
-- Data for Name: participant_sport_type; Type: TABLE DATA; Schema: olympiad; Owner: student
--



--
-- TOC entry 3191 (class 0 OID 33959)
-- Dependencies: 232
-- Data for Name: participants; Type: TABLE DATA; Schema: olympiad; Owner: student
--

INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (1, 'RU', 'Иван', 'Иванов', '1990-01-01');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (2, 'US', 'John', 'Doe', '1985-05-15');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (3, 'EN', 'Alice', 'Smith', '1992-08-20');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (4, 'CN', '王', '张', '1988-03-10');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (5, 'IND', 'Raj', 'Patel', '1995-12-05');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (6, 'JPN', '太郎', '山田', '1980-07-25');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (7, 'GRM', 'Hans', 'Schmidt', '1987-11-30');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (8, 'BRZ', 'Maria', 'Silva', '1998-04-18');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (9, 'RU', 'Ольга', 'Иванова', '1994-04-15');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (10, 'US', 'Christopher', 'Anderson', '1983-10-05');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (11, 'GRM', 'Anna', 'Müller', '1990-12-20');
INSERT INTO olympiad.participants (id, country_code, name, surname, birthdate) VALUES (12, 'BRZ', 'Antônio José', 'da Silva e Oliveira', '1975-08-08');


--
-- TOC entry 3215 (class 0 OID 34150)
-- Dependencies: 262
-- Data for Name: result_log; Type: TABLE DATA; Schema: olympiad; Owner: student
--

INSERT INTO olympiad.result_log (id, date_happened, happened_action, result_id) VALUES (1, '2023-12-17 17:09:54.033754', 'INSERT', 12);
INSERT INTO olympiad.result_log (id, date_happened, happened_action, result_id) VALUES (2, '2023-12-17 17:15:29.127874', 'INSERT', 13);


--
-- TOC entry 3199 (class 0 OID 34006)
-- Dependencies: 240
-- Data for Name: sports_ground_sport_type; Type: TABLE DATA; Schema: olympiad; Owner: student
--

INSERT INTO olympiad.sports_ground_sport_type (id, sport_type_id, sport_ground_id) VALUES (2, 4, 2);
INSERT INTO olympiad.sports_ground_sport_type (id, sport_type_id, sport_ground_id) VALUES (3, 2, 4);
INSERT INTO olympiad.sports_ground_sport_type (id, sport_type_id, sport_ground_id) VALUES (4, 3, 1);
INSERT INTO olympiad.sports_ground_sport_type (id, sport_type_id, sport_ground_id) VALUES (5, 4, 3);


--
-- TOC entry 3193 (class 0 OID 33975)
-- Dependencies: 234
-- Data for Name: sports_grounds; Type: TABLE DATA; Schema: olympiad; Owner: student
--

INSERT INTO olympiad.sports_grounds (id, name, city) VALUES (1, 'Cross Stadium', 'Moscow');
INSERT INTO olympiad.sports_grounds (id, name, city) VALUES (2, 'Super Puper Stadium', 'Izhevsk');
INSERT INTO olympiad.sports_grounds (id, name, city) VALUES (3, 'Some New Stadium', 'Vladivostok');
INSERT INTO olympiad.sports_grounds (id, name, city) VALUES (4, 'Gazpop Stadium', 'St.Petersburg');


--
-- TOC entry 3195 (class 0 OID 33986)
-- Dependencies: 236
-- Data for Name: sports_type; Type: TABLE DATA; Schema: olympiad; Owner: student
--

INSERT INTO olympiad.sports_type (id, name, type, description, season) VALUES (1, 'Бокс', 'индивидуальный', 'Боевое искусство бить в лицо', 'лето');
INSERT INTO olympiad.sports_type (id, name, type, description, season) VALUES (2, 'Футбол', 'командный', 'Бей, беги', 'лето');
INSERT INTO olympiad.sports_type (id, name, type, description, season) VALUES (3, 'Биатлон', 'индивидуальный', 'Катись на лыжах и стреляй', 'зима');
INSERT INTO olympiad.sports_type (id, name, type, description, season) VALUES (4, 'Хоккей', 'командный', 'Акуратно! Шайба в лицо!', 'зима');


--
-- TOC entry 3212 (class 0 OID 34084)
-- Dependencies: 253
-- Data for Name: start_results; Type: TABLE DATA; Schema: olympiad; Owner: student
--

INSERT INTO olympiad.start_results (id, sport_type_id, participant_id, sport_ground_id, result_sec, "position") VALUES (5, 2, 4, 2, 5000.00, 5);
INSERT INTO olympiad.start_results (id, sport_type_id, participant_id, sport_ground_id, result_sec, "position") VALUES (6, 1, 2, 3, 0.00, 4);
INSERT INTO olympiad.start_results (id, sport_type_id, participant_id, sport_ground_id, result_sec, "position") VALUES (7, 4, 6, 3, 0.00, 3);
INSERT INTO olympiad.start_results (id, sport_type_id, participant_id, sport_ground_id, result_sec, "position") VALUES (8, 3, 10, 2, 500.00, 30);


--
-- TOC entry 3207 (class 0 OID 34058)
-- Dependencies: 248
-- Data for Name: starts_schedule; Type: TABLE DATA; Schema: olympiad; Owner: student
--

INSERT INTO olympiad.starts_schedule (id, sport_type_id, start_date, start_time, sport_ground_id) VALUES (2, 1, '2023-12-17', '17:30:00', 1);
INSERT INTO olympiad.starts_schedule (id, sport_type_id, start_date, start_time, sport_ground_id) VALUES (3, 2, '2023-12-16', '14:50:00', 2);
INSERT INTO olympiad.starts_schedule (id, sport_type_id, start_date, start_time, sport_ground_id) VALUES (4, 3, '2023-12-12', '10:00:00', 3);


--
-- TOC entry 3240 (class 0 OID 0)
-- Dependencies: 229
-- Name: countries_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.countries_id_seq', 8, true);


--
-- TOC entry 3241 (class 0 OID 0)
-- Dependencies: 241
-- Name: participant_sport_type_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.participant_sport_type_id_seq', 1, false);


--
-- TOC entry 3242 (class 0 OID 0)
-- Dependencies: 242
-- Name: participant_sport_type_participant_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.participant_sport_type_participant_id_seq', 1, false);


--
-- TOC entry 3243 (class 0 OID 0)
-- Dependencies: 243
-- Name: participant_sport_type_sport_type_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.participant_sport_type_sport_type_id_seq', 1, false);


--
-- TOC entry 3244 (class 0 OID 0)
-- Dependencies: 231
-- Name: participants_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.participants_id_seq', 14, true);


--
-- TOC entry 3245 (class 0 OID 0)
-- Dependencies: 260
-- Name: result_log_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.result_log_id_seq', 2, true);


--
-- TOC entry 3246 (class 0 OID 0)
-- Dependencies: 261
-- Name: result_log_result_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.result_log_result_id_seq', 1, false);


--
-- TOC entry 3247 (class 0 OID 0)
-- Dependencies: 237
-- Name: sports_ground_sport_type_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.sports_ground_sport_type_id_seq', 5, true);


--
-- TOC entry 3248 (class 0 OID 0)
-- Dependencies: 239
-- Name: sports_ground_sport_type_sport_ground_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.sports_ground_sport_type_sport_ground_id_seq', 1, false);


--
-- TOC entry 3249 (class 0 OID 0)
-- Dependencies: 238
-- Name: sports_ground_sport_type_sport_type_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.sports_ground_sport_type_sport_type_id_seq', 1, false);


--
-- TOC entry 3250 (class 0 OID 0)
-- Dependencies: 233
-- Name: sports_grounds_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.sports_grounds_id_seq', 4, true);


--
-- TOC entry 3251 (class 0 OID 0)
-- Dependencies: 235
-- Name: sports_type_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.sports_type_id_seq', 5, true);


--
-- TOC entry 3252 (class 0 OID 0)
-- Dependencies: 249
-- Name: start_results_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.start_results_id_seq', 13, true);


--
-- TOC entry 3253 (class 0 OID 0)
-- Dependencies: 251
-- Name: start_results_participant_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.start_results_participant_id_seq', 1, false);


--
-- TOC entry 3254 (class 0 OID 0)
-- Dependencies: 252
-- Name: start_results_sport_ground_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.start_results_sport_ground_id_seq', 1, false);


--
-- TOC entry 3255 (class 0 OID 0)
-- Dependencies: 250
-- Name: start_results_sport_type_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.start_results_sport_type_id_seq', 1, false);


--
-- TOC entry 3256 (class 0 OID 0)
-- Dependencies: 245
-- Name: starts_schedule_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.starts_schedule_id_seq', 6, true);


--
-- TOC entry 3257 (class 0 OID 0)
-- Dependencies: 247
-- Name: starts_schedule_sport_ground_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.starts_schedule_sport_ground_id_seq', 1, false);


--
-- TOC entry 3258 (class 0 OID 0)
-- Dependencies: 246
-- Name: starts_schedule_sport_type_id_seq; Type: SEQUENCE SET; Schema: olympiad; Owner: student
--

SELECT pg_catalog.setval('olympiad.starts_schedule_sport_type_id_seq', 1, false);


--
-- TOC entry 3017 (class 2606 OID 33956)
-- Name: countries countries_country_code_key; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.countries
    ADD CONSTRAINT countries_country_code_key UNIQUE (country_code);


--
-- TOC entry 3019 (class 2606 OID 33954)
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- TOC entry 3032 (class 2606 OID 34041)
-- Name: participant_sport_type participant_sport_type_participant_id_sport_type_id_key; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participant_sport_type
    ADD CONSTRAINT participant_sport_type_participant_id_sport_type_id_key UNIQUE (participant_id, sport_type_id);


--
-- TOC entry 3034 (class 2606 OID 34039)
-- Name: participant_sport_type participant_sport_type_pkey; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participant_sport_type
    ADD CONSTRAINT participant_sport_type_pkey PRIMARY KEY (id);


--
-- TOC entry 3022 (class 2606 OID 33967)
-- Name: participants participants_pkey; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participants
    ADD CONSTRAINT participants_pkey PRIMARY KEY (id);


--
-- TOC entry 3041 (class 2606 OID 34159)
-- Name: result_log result_log_pkey; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.result_log
    ADD CONSTRAINT result_log_pkey PRIMARY KEY (id);


--
-- TOC entry 3028 (class 2606 OID 34013)
-- Name: sports_ground_sport_type sports_ground_sport_type_pkey; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_ground_sport_type
    ADD CONSTRAINT sports_ground_sport_type_pkey PRIMARY KEY (id);


--
-- TOC entry 3030 (class 2606 OID 34015)
-- Name: sports_ground_sport_type sports_ground_sport_type_sport_type_id_sport_ground_id_key; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_ground_sport_type
    ADD CONSTRAINT sports_ground_sport_type_sport_type_id_sport_ground_id_key UNIQUE (sport_type_id, sport_ground_id);


--
-- TOC entry 3024 (class 2606 OID 33983)
-- Name: sports_grounds sports_grounds_pkey; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_grounds
    ADD CONSTRAINT sports_grounds_pkey PRIMARY KEY (id);


--
-- TOC entry 3026 (class 2606 OID 33999)
-- Name: sports_type sports_type_pkey; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_type
    ADD CONSTRAINT sports_type_pkey PRIMARY KEY (id);


--
-- TOC entry 3039 (class 2606 OID 34092)
-- Name: start_results start_results_pkey; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.start_results
    ADD CONSTRAINT start_results_pkey PRIMARY KEY (id);


--
-- TOC entry 3036 (class 2606 OID 34065)
-- Name: starts_schedule starts_schedule_pkey; Type: CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.starts_schedule
    ADD CONSTRAINT starts_schedule_pkey PRIMARY KEY (id);


--
-- TOC entry 3020 (class 1259 OID 34108)
-- Name: participant_index; Type: INDEX; Schema: olympiad; Owner: student
--

CREATE INDEX participant_index ON olympiad.participants USING btree (id, name, surname);


--
-- TOC entry 3037 (class 1259 OID 34109)
-- Name: results_index; Type: INDEX; Schema: olympiad; Owner: student
--

CREATE INDEX results_index ON olympiad.start_results USING btree (id, sport_type_id, participant_id);


--
-- TOC entry 3052 (class 2620 OID 34166)
-- Name: start_results result_insert_trigger; Type: TRIGGER; Schema: olympiad; Owner: student
--

CREATE TRIGGER result_insert_trigger AFTER INSERT ON olympiad.start_results FOR EACH ROW EXECUTE FUNCTION olympiad.result_log_trigger_function();


--
-- TOC entry 3045 (class 2606 OID 34042)
-- Name: participant_sport_type participant_sport_type_participant_id_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participant_sport_type
    ADD CONSTRAINT participant_sport_type_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES olympiad.participants(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3046 (class 2606 OID 34047)
-- Name: participant_sport_type participant_sport_type_sport_type_id_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participant_sport_type
    ADD CONSTRAINT participant_sport_type_sport_type_id_fkey FOREIGN KEY (sport_type_id) REFERENCES olympiad.sports_type(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3042 (class 2606 OID 33968)
-- Name: participants participants_country_code_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.participants
    ADD CONSTRAINT participants_country_code_fkey FOREIGN KEY (country_code) REFERENCES olympiad.countries(country_code);


--
-- TOC entry 3044 (class 2606 OID 34021)
-- Name: sports_ground_sport_type sports_ground_sport_type_sport_ground_id_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_ground_sport_type
    ADD CONSTRAINT sports_ground_sport_type_sport_ground_id_fkey FOREIGN KEY (sport_ground_id) REFERENCES olympiad.sports_grounds(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3043 (class 2606 OID 34016)
-- Name: sports_ground_sport_type sports_ground_sport_type_sport_type_id_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.sports_ground_sport_type
    ADD CONSTRAINT sports_ground_sport_type_sport_type_id_fkey FOREIGN KEY (sport_type_id) REFERENCES olympiad.sports_type(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3050 (class 2606 OID 34098)
-- Name: start_results start_results_participant_id_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.start_results
    ADD CONSTRAINT start_results_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES olympiad.participants(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3051 (class 2606 OID 34103)
-- Name: start_results start_results_sport_ground_id_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.start_results
    ADD CONSTRAINT start_results_sport_ground_id_fkey FOREIGN KEY (sport_ground_id) REFERENCES olympiad.sports_grounds(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3049 (class 2606 OID 34093)
-- Name: start_results start_results_sport_type_id_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.start_results
    ADD CONSTRAINT start_results_sport_type_id_fkey FOREIGN KEY (sport_type_id) REFERENCES olympiad.sports_type(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3048 (class 2606 OID 34071)
-- Name: starts_schedule starts_schedule_sport_ground_id_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.starts_schedule
    ADD CONSTRAINT starts_schedule_sport_ground_id_fkey FOREIGN KEY (sport_ground_id) REFERENCES olympiad.sports_grounds(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3047 (class 2606 OID 34066)
-- Name: starts_schedule starts_schedule_sport_type_id_fkey; Type: FK CONSTRAINT; Schema: olympiad; Owner: student
--

ALTER TABLE ONLY olympiad.starts_schedule
    ADD CONSTRAINT starts_schedule_sport_type_id_fkey FOREIGN KEY (sport_type_id) REFERENCES olympiad.sports_type(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2023-12-17 18:24:31 +04

--
-- PostgreSQL database dump complete
--

