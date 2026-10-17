--
-- PostgreSQL database dump
--

\restrict FuFYknFjhAUDOxdayPtHUcYg2tHekFo221vXukWwgQICxnAFNOjyE1DTezIjkGJ

-- Dumped from database version 15.19
-- Dumped by pg_dump version 15.19

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
-- Name: context_0_0; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA context_0_0;


--
-- Name: context_0_1; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA context_0_1;


--
-- Name: context_1_0; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA context_1_0;


--
-- Name: context_1_1; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA context_1_1;


--
-- Name: json_applies_mutations_recursively; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_applies_mutations_recursively;


--
-- Name: json_combined_operations; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_combined_operations;


--
-- Name: json_delete_existing_key; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_delete_existing_key;


--
-- Name: json_delete_missing_key_is_noop; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_delete_missing_key_is_noop;


--
-- Name: json_existing_key_is_replaced; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_existing_key_is_replaced;


--
-- Name: json_existing_key_passes_current_value; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_existing_key_passes_current_value;


--
-- Name: json_invalid_json_raises; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_invalid_json_raises;


--
-- Name: json_json_array_passthrough; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_json_array_passthrough;


--
-- Name: json_json_scalar_passthrough; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_json_scalar_passthrough;


--
-- Name: json_key_name_can_be_current_value; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_key_name_can_be_current_value;


--
-- Name: json_missing_key_is_added; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_missing_key_is_added;


--
-- Name: json_null_existing_key; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_null_existing_key;


--
-- Name: json_null_missing_key_adds_null; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_null_missing_key_adds_null;


--
-- Name: json_postgres_null_passthrough; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_postgres_null_passthrough;


--
-- Name: json_preserving_the_numeric_type; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_preserving_the_numeric_type;


--
-- Name: json_unknown_mutation_raises; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA json_unknown_mutation_raises;


--
-- Name: metadata; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA metadata;


--
-- Name: metadata__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA metadata__schema;


--
-- Name: original_conditions; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA original_conditions;


--
-- Name: relations_source; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA relations_source;


--
-- Name: relations_target; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA relations_target;


--
-- Name: source_0; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA source_0;


--
-- Name: source_1; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA source_1;


--
-- Name: test_by_pattern_condition; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_by_pattern_condition;


--
-- Name: test_by_pattern_condition__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_by_pattern_condition__schema;


--
-- Name: test_equal_condition; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_equal_condition;


--
-- Name: test_equal_condition__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_equal_condition__schema;


--
-- Name: test_not_equal_condition; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_not_equal_condition;


--
-- Name: test_not_equal_condition__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_not_equal_condition__schema;


--
-- Name: test_obfuscate_uuid_by_source_value; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_obfuscate_uuid_by_source_value;


--
-- Name: test_obfuscate_uuid_by_source_value__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_obfuscate_uuid_by_source_value__schema;


--
-- Name: test_parse_copy_values_with_delete_tables; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_parse_copy_values_with_delete_tables;


--
-- Name: test_parse_copy_values_with_delete_tables__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_parse_copy_values_with_delete_tables__schema;


--
-- Name: test_parse_copy_values_with_mutation; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_parse_copy_values_with_mutation;


--
-- Name: test_parse_copy_values_with_mutation__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_parse_copy_values_with_mutation__schema;


--
-- Name: test_parse_copy_values_with_relations; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_parse_copy_values_with_relations;


--
-- Name: test_parse_copy_values_with_relations__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_parse_copy_values_with_relations__schema;


--
-- Name: test_parse_copy_values_with_self_relation; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_parse_copy_values_with_self_relation;


--
-- Name: test_parse_copy_values_with_self_relation__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_parse_copy_values_with_self_relation__schema;


--
-- Name: test_two_mutation_for_one_column; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_two_mutation_for_one_column;


--
-- Name: test_two_mutation_for_one_column__schema; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA test_two_mutation_for_one_column__schema;


--
-- Name: typed_restore; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA typed_restore;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: context_0_0; Owner: -
--

CREATE TABLE context_0_0.users (
    value text,
    id text,
    name text
);


--
-- Name: COLUMN users.value; Type: COMMENT; Schema: context_0_0; Owner: -
--

COMMENT ON COLUMN context_0_0.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name"}}]';


--
-- Name: users; Type: TABLE; Schema: context_0_1; Owner: -
--

CREATE TABLE context_0_1.users (
    value text,
    id text,
    name text
);


--
-- Name: COLUMN users.value; Type: COMMENT; Schema: context_0_1; Owner: -
--

COMMENT ON COLUMN context_0_1.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name"}, "relations": [{"table_name": "context_0_1.peers", "column_name": "value", "from_column_name": "id", "to_column_name": "id"}]}]';


--
-- Name: users; Type: TABLE; Schema: context_1_0; Owner: -
--

CREATE TABLE context_1_0.users (
    value text,
    id text,
    name text
);


--
-- Name: COLUMN users.value; Type: COMMENT; Schema: context_1_0; Owner: -
--

COMMENT ON COLUMN context_1_0.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name", "current_value": "fixed", "obfuscated_values": {"name": "configured"}}}]';


--
-- Name: users; Type: TABLE; Schema: context_1_1; Owner: -
--

CREATE TABLE context_1_1.users (
    value text,
    id text,
    name text
);


--
-- Name: COLUMN users.value; Type: COMMENT; Schema: context_1_1; Owner: -
--

COMMENT ON COLUMN context_1_1.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name", "current_value": "fixed", "obfuscated_values": {"name": "configured"}}, "relations": [{"table_name": "context_1_1.peers", "column_name": "value", "from_column_name": "id", "to_column_name": "id"}]}]';


--
-- Name: json_values; Type: TABLE; Schema: json_applies_mutations_recursively; Owner: -
--

CREATE TABLE json_applies_mutations_recursively.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_applies_mutations_recursively; Owner: -
--

COMMENT ON COLUMN json_applies_mutations_recursively.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"phone": [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "MASKED"}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_combined_operations; Owner: -
--

CREATE TABLE json_combined_operations.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_combined_operations; Owner: -
--

COMMENT ON COLUMN json_combined_operations.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"first_name": [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "John"}}], "secret": [{"mutation_name": "delete", "mutation_kwargs": {}}], "notes": [{"mutation_name": "null", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_delete_existing_key; Owner: -
--

CREATE TABLE json_delete_existing_key.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_delete_existing_key; Owner: -
--

COMMENT ON COLUMN json_delete_existing_key.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"secret": [{"mutation_name": "delete", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_delete_missing_key_is_noop; Owner: -
--

CREATE TABLE json_delete_missing_key_is_noop.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_delete_missing_key_is_noop; Owner: -
--

COMMENT ON COLUMN json_delete_missing_key_is_noop.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"ghost": [{"mutation_name": "delete", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_existing_key_is_replaced; Owner: -
--

CREATE TABLE json_existing_key_is_replaced.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_existing_key_is_replaced; Owner: -
--

COMMENT ON COLUMN json_existing_key_is_replaced.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "John"}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_existing_key_passes_current_value; Owner: -
--

CREATE TABLE json_existing_key_passes_current_value.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_existing_key_passes_current_value; Owner: -
--

COMMENT ON COLUMN json_existing_key_passes_current_value.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"phone": [{"mutation_name": "test_echo", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_invalid_json_raises; Owner: -
--

CREATE TABLE json_invalid_json_raises.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_invalid_json_raises; Owner: -
--

COMMENT ON COLUMN json_invalid_json_raises.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "first_name", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_json_array_passthrough; Owner: -
--

CREATE TABLE json_json_array_passthrough.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_json_array_passthrough; Owner: -
--

COMMENT ON COLUMN json_json_array_passthrough.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "first_name", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_json_scalar_passthrough; Owner: -
--

CREATE TABLE json_json_scalar_passthrough.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_json_scalar_passthrough; Owner: -
--

COMMENT ON COLUMN json_json_scalar_passthrough.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "first_name", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_key_name_can_be_current_value; Owner: -
--

CREATE TABLE json_key_name_can_be_current_value.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_key_name_can_be_current_value; Owner: -
--

COMMENT ON COLUMN json_key_name_can_be_current_value.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"current_value": [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "safe"}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_missing_key_is_added; Owner: -
--

CREATE TABLE json_missing_key_is_added.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_missing_key_is_added; Owner: -
--

COMMENT ON COLUMN json_missing_key_is_added.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"email": [{"mutation_name": "email", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_null_existing_key; Owner: -
--

CREATE TABLE json_null_existing_key.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_null_existing_key; Owner: -
--

COMMENT ON COLUMN json_null_existing_key.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"notes": [{"mutation_name": "null"}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_null_missing_key_adds_null; Owner: -
--

CREATE TABLE json_null_missing_key_adds_null.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_null_missing_key_adds_null; Owner: -
--

COMMENT ON COLUMN json_null_missing_key_adds_null.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"notes": [{"mutation_name": "null", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_postgres_null_passthrough; Owner: -
--

CREATE TABLE json_postgres_null_passthrough.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_postgres_null_passthrough; Owner: -
--

COMMENT ON COLUMN json_postgres_null_passthrough.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "first_name", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_preserving_the_numeric_type; Owner: -
--

CREATE TABLE json_preserving_the_numeric_type.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_preserving_the_numeric_type; Owner: -
--

COMMENT ON COLUMN json_preserving_the_numeric_type.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"score": [{"mutation_name": "numeric_integer", "mutation_kwargs": {}}]}}}]';


--
-- Name: json_values; Type: TABLE; Schema: json_unknown_mutation_raises; Owner: -
--

CREATE TABLE json_unknown_mutation_raises.json_values (
    id text,
    details text
);


--
-- Name: COLUMN json_values.details; Type: COMMENT; Schema: json_unknown_mutation_raises; Owner: -
--

COMMENT ON COLUMN json_unknown_mutation_raises.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"key": [{"mutation_name": "nonexistent", "mutation_kwargs": {}}]}}}]';


--
-- Name: _table; Type: TABLE; Schema: metadata; Owner: -
--

CREATE TABLE metadata._table (
    column_1 text,
    column_2 text
);


--
-- Name: deleted_table; Type: TABLE; Schema: metadata; Owner: -
--

CREATE TABLE metadata.deleted_table (
    field_value text
);


--
-- Name: TABLE deleted_table; Type: COMMENT; Schema: metadata; Owner: -
--

COMMENT ON TABLE metadata.deleted_table IS 'anon: {"mutation_name": "delete"}';


--
-- Name: invalid_column; Type: TABLE; Schema: metadata; Owner: -
--

CREATE TABLE metadata.invalid_column (
    field_value text
);


--
-- Name: COLUMN invalid_column.field_value; Type: COMMENT; Schema: metadata; Owner: -
--

COMMENT ON COLUMN metadata.invalid_column.field_value IS 'anon: {''mutation_name": "null"}';


--
-- Name: kept_table; Type: TABLE; Schema: metadata; Owner: -
--

CREATE TABLE metadata.kept_table (
    field_value text
);


--
-- Name: TABLE kept_table; Type: COMMENT; Schema: metadata; Owner: -
--

COMMENT ON TABLE metadata.kept_table IS 'anon: {"mutation_name": "set"}';


--
-- Name: null_column; Type: TABLE; Schema: metadata; Owner: -
--

CREATE TABLE metadata.null_column (
    field_value text
);


--
-- Name: COLUMN null_column.field_value; Type: COMMENT; Schema: metadata; Owner: -
--

COMMENT ON COLUMN metadata.null_column.field_value IS 'anon: [{"mutation_name": "null"}]';


--
-- Name: plain_values; Type: TABLE; Schema: metadata; Owner: -
--

CREATE TABLE metadata.plain_values (
    column_1 text,
    column_2 text
);


--
-- Name: unknown_column; Type: TABLE; Schema: metadata; Owner: -
--

CREATE TABLE metadata.unknown_column (
    field_value text
);


--
-- Name: COLUMN unknown_column.field_value; Type: COMMENT; Schema: metadata; Owner: -
--

COMMENT ON COLUMN metadata.unknown_column.field_value IS 'anon: [{"mutation_name": "not_found"}]';


--
-- Name: _table; Type: TABLE; Schema: metadata__schema; Owner: -
--

CREATE TABLE metadata__schema._table (
    column_1 text,
    column_2 text
);


--
-- Name: deleted_table; Type: TABLE; Schema: metadata__schema; Owner: -
--

CREATE TABLE metadata__schema.deleted_table (
    field_value text
);


--
-- Name: TABLE deleted_table; Type: COMMENT; Schema: metadata__schema; Owner: -
--

COMMENT ON TABLE metadata__schema.deleted_table IS 'anon: {"mutation_name": "delete"}';


--
-- Name: invalid_column; Type: TABLE; Schema: metadata__schema; Owner: -
--

CREATE TABLE metadata__schema.invalid_column (
    field_value text
);


--
-- Name: COLUMN invalid_column.field_value; Type: COMMENT; Schema: metadata__schema; Owner: -
--

COMMENT ON COLUMN metadata__schema.invalid_column.field_value IS 'anon: {''mutation_name": "null"}';


--
-- Name: kept_table; Type: TABLE; Schema: metadata__schema; Owner: -
--

CREATE TABLE metadata__schema.kept_table (
    field_value text
);


--
-- Name: TABLE kept_table; Type: COMMENT; Schema: metadata__schema; Owner: -
--

COMMENT ON TABLE metadata__schema.kept_table IS 'anon: {"mutation_name": "set"}';


--
-- Name: null_column; Type: TABLE; Schema: metadata__schema; Owner: -
--

CREATE TABLE metadata__schema.null_column (
    field_value text
);


--
-- Name: COLUMN null_column.field_value; Type: COMMENT; Schema: metadata__schema; Owner: -
--

COMMENT ON COLUMN metadata__schema.null_column.field_value IS 'anon: [{"mutation_name": "null"}]';


--
-- Name: plain_values; Type: TABLE; Schema: metadata__schema; Owner: -
--

CREATE TABLE metadata__schema.plain_values (
    column_1 text,
    column_2 text
);


--
-- Name: unknown_column; Type: TABLE; Schema: metadata__schema; Owner: -
--

CREATE TABLE metadata__schema.unknown_column (
    field_value text
);


--
-- Name: COLUMN unknown_column.field_value; Type: COMMENT; Schema: metadata__schema; Owner: -
--

COMMENT ON COLUMN metadata__schema.unknown_column.field_value IS 'anon: [{"mutation_name": "not_found"}]';


--
-- Name: users; Type: TABLE; Schema: original_conditions; Owner: -
--

CREATE TABLE original_conditions.users (
    id text,
    status text,
    email text,
    notes text,
    empty text
);


--
-- Name: COLUMN users.status; Type: COMMENT; Schema: original_conditions; Owner: -
--

COMMENT ON COLUMN original_conditions.users.status IS 'anon: [{"mutation_name": "random_choice", "mutation_kwargs": {"choices": ["changed"]}}]';


--
-- Name: COLUMN users.email; Type: COMMENT; Schema: original_conditions; Owner: -
--

COMMENT ON COLUMN original_conditions.users.email IS 'anon: [{"mutation_name": "random_choice", "mutation_kwargs": {"choices": ["hidden"]}, "conditions": [{"column_name": "status", "operation": "equal", "value": "original"}]}]';


--
-- Name: zz_untouched; Type: TABLE; Schema: original_conditions; Owner: -
--

CREATE TABLE original_conditions.zz_untouched (
    id text,
    name text
);


--
-- Name: a_source; Type: TABLE; Schema: relations_source; Owner: -
--

CREATE TABLE relations_source.a_source (
    name text,
    id text,
    alternate_id text
);


--
-- Name: COLUMN a_source.name; Type: COMMENT; Schema: relations_source; Owner: -
--

COMMENT ON COLUMN relations_source.a_source.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "relations_source.b_target", "column_name": "name", "from_column_name": "id", "to_column_name": "ref"}, {"table_name": "relations_source.b_target", "column_name": "name", "from_column_name": "alternate_id", "to_column_name": "alternate_ref"}]}]';


--
-- Name: b_target; Type: TABLE; Schema: relations_source; Owner: -
--

CREATE TABLE relations_source.b_target (
    alternate_ref text,
    name text,
    ref text
);


--
-- Name: COLUMN b_target.name; Type: COMMENT; Schema: relations_source; Owner: -
--

COMMENT ON COLUMN relations_source.b_target.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "relations_source.a_source", "column_name": "name", "from_column_name": "ref", "to_column_name": "id"}, {"table_name": "relations_source.a_source", "column_name": "name", "from_column_name": "alternate_ref", "to_column_name": "alternate_id"}]}]';


--
-- Name: a_target; Type: TABLE; Schema: relations_target; Owner: -
--

CREATE TABLE relations_target.a_target (
    alternate_ref text,
    name text,
    ref text
);


--
-- Name: COLUMN a_target.name; Type: COMMENT; Schema: relations_target; Owner: -
--

COMMENT ON COLUMN relations_target.a_target.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "relations_target.b_source", "column_name": "name", "from_column_name": "ref", "to_column_name": "id"}, {"table_name": "relations_target.b_source", "column_name": "name", "from_column_name": "alternate_ref", "to_column_name": "alternate_id"}]}]';


--
-- Name: b_source; Type: TABLE; Schema: relations_target; Owner: -
--

CREATE TABLE relations_target.b_source (
    name text,
    id text,
    alternate_id text
);


--
-- Name: COLUMN b_source.name; Type: COMMENT; Schema: relations_target; Owner: -
--

COMMENT ON COLUMN relations_target.b_source.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "relations_target.a_target", "column_name": "name", "from_column_name": "id", "to_column_name": "ref"}, {"table_name": "relations_target.a_target", "column_name": "name", "from_column_name": "alternate_id", "to_column_name": "alternate_ref"}]}]';


--
-- Name: users; Type: TABLE; Schema: source_0; Owner: -
--

CREATE TABLE source_0.users (
    token text,
    id text,
    name text,
    notes text
);


--
-- Name: COLUMN users.token; Type: COMMENT; Schema: source_0; Owner: -
--

COMMENT ON COLUMN source_0.users.token IS 'anon: [{"mutation_name": "uuid5_by_source_value", "mutation_kwargs": {"source_column": "name", "namespace": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';


--
-- Name: users; Type: TABLE; Schema: source_1; Owner: -
--

CREATE TABLE source_1.users (
    token text,
    id text,
    name text,
    notes text
);


--
-- Name: COLUMN users.token; Type: COMMENT; Schema: source_1; Owner: -
--

COMMENT ON COLUMN source_1.users.token IS 'anon: [{"mutation_name": "uuid5_by_source_value", "mutation_kwargs": {"source_column": "name", "namespace": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';


--
-- Name: COLUMN users.name; Type: COMMENT; Schema: source_1; Owner: -
--

COMMENT ON COLUMN source_1.users.name IS 'anon: [{"mutation_name": "random_choice", "mutation_kwargs": {"choices": ["hidden"]}}]';


--
-- Name: table_1; Type: TABLE; Schema: test_by_pattern_condition; Owner: -
--

CREATE TABLE test_by_pattern_condition.table_1 (
    id text,
    email text,
    active text
);


--
-- Name: COLUMN table_1.email; Type: COMMENT; Schema: test_by_pattern_condition; Owner: -
--

COMMENT ON COLUMN test_by_pattern_condition.table_1.email IS 'anon: [{"mutation_name": "email", "conditions": [{"column_name": "email", "operation": "by_pattern", "value": "\\w+\\@\\w+\\.\\w{2}"}]}]';


--
-- Name: table_1; Type: TABLE; Schema: test_equal_condition; Owner: -
--

CREATE TABLE test_equal_condition.table_1 (
    id text,
    email text,
    active text
);


--
-- Name: COLUMN table_1.email; Type: COMMENT; Schema: test_equal_condition; Owner: -
--

COMMENT ON COLUMN test_equal_condition.table_1.email IS 'anon: [{"mutation_name": "email", "conditions": [{"column_name": "active", "operation": "equal", "value": "t"}]}]';


--
-- Name: table_1; Type: TABLE; Schema: test_not_equal_condition; Owner: -
--

CREATE TABLE test_not_equal_condition.table_1 (
    id text,
    email text,
    active text
);


--
-- Name: COLUMN table_1.email; Type: COMMENT; Schema: test_not_equal_condition; Owner: -
--

COMMENT ON COLUMN test_not_equal_condition.table_1.email IS 'anon: [{"mutation_name": "email", "conditions": [{"column_name": "active", "operation": "not_equal", "value": "t"}]}]';


--
-- Name: table_1; Type: TABLE; Schema: test_obfuscate_uuid_by_source_value; Owner: -
--

CREATE TABLE test_obfuscate_uuid_by_source_value.table_1 (
    uuid text,
    username text,
    last_name text
);


--
-- Name: COLUMN table_1.uuid; Type: COMMENT; Schema: test_obfuscate_uuid_by_source_value; Owner: -
--

COMMENT ON COLUMN test_obfuscate_uuid_by_source_value.table_1.uuid IS 'anon: [{"mutation_name": "uuid5_by_source_value", "mutation_kwargs": {"source_column": "username", "namespace": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';


--
-- Name: COLUMN table_1.username; Type: COMMENT; Schema: test_obfuscate_uuid_by_source_value; Owner: -
--

COMMENT ON COLUMN test_obfuscate_uuid_by_source_value.table_1.username IS 'anon: [{"mutation_name": "phone_number", "mutation_kwargs": {"mask": "791########", "unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^7[0-9]{10}$"}]}]';


--
-- Name: table_1; Type: TABLE; Schema: test_parse_copy_values_with_delete_tables; Owner: -
--

CREATE TABLE test_parse_copy_values_with_delete_tables.table_1 (
    id text,
    message text,
    recipient text,
    notes text
);


--
-- Name: TABLE table_1; Type: COMMENT; Schema: test_parse_copy_values_with_delete_tables; Owner: -
--

COMMENT ON TABLE test_parse_copy_values_with_delete_tables.table_1 IS 'anon: {"mutation_name": "delete"}';


--
-- Name: table_2; Type: TABLE; Schema: test_parse_copy_values_with_delete_tables__schema; Owner: -
--

CREATE TABLE test_parse_copy_values_with_delete_tables__schema.table_2 (
    id text,
    message text,
    recipient text,
    notes text
);


--
-- Name: TABLE table_2; Type: COMMENT; Schema: test_parse_copy_values_with_delete_tables__schema; Owner: -
--

COMMENT ON TABLE test_parse_copy_values_with_delete_tables__schema.table_2 IS 'anon: {"mutation_name": "delete"}';


--
-- Name: table_1; Type: TABLE; Schema: test_parse_copy_values_with_mutation; Owner: -
--

CREATE TABLE test_parse_copy_values_with_mutation.table_1 (
    id text,
    crypted_password text,
    persistence_token text,
    text text
);


--
-- Name: COLUMN table_1.crypted_password; Type: COMMENT; Schema: test_parse_copy_values_with_mutation; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_mutation.table_1.crypted_password IS 'anon: [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3125d3bd1ett18ffc4a8092e2616b9e5ca7954b2c52504"}}]';


--
-- Name: COLUMN table_1.persistence_token; Type: COMMENT; Schema: test_parse_copy_values_with_mutation; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_mutation.table_1.persistence_token IS 'anon: [{"mutation_name": "empty_string"}]';


--
-- Name: COLUMN table_1.text; Type: COMMENT; Schema: test_parse_copy_values_with_mutation; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_mutation.table_1.text IS 'anon: [{"mutation_name": "string_by_mask", "mutation_kwargs": {"mask": "test chars: @@@@@; test digits: #####;"}}]';


--
-- Name: table_1; Type: TABLE; Schema: test_parse_copy_values_with_mutation__schema; Owner: -
--

CREATE TABLE test_parse_copy_values_with_mutation__schema.table_1 (
    id text,
    email text,
    crypted_password text,
    dt_birthday text,
    password_salt text
);


--
-- Name: COLUMN table_1.email; Type: COMMENT; Schema: test_parse_copy_values_with_mutation__schema; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_mutation__schema.table_1.email IS 'anon: [{"mutation_name": "email"}]';


--
-- Name: COLUMN table_1.crypted_password; Type: COMMENT; Schema: test_parse_copy_values_with_mutation__schema; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_mutation__schema.table_1.crypted_password IS 'anon: [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3125d3bd1ett18ffc4a8092e2616b9e5ca7954b2c52504"}}]';


--
-- Name: COLUMN table_1.dt_birthday; Type: COMMENT; Schema: test_parse_copy_values_with_mutation__schema; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_mutation__schema.table_1.dt_birthday IS 'anon: [{"mutation_name": "date", "mutation_kwargs": {"start": 2000, "end": 2024}}]';


--
-- Name: COLUMN table_1.password_salt; Type: COMMENT; Schema: test_parse_copy_values_with_mutation__schema; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_mutation__schema.table_1.password_salt IS 'anon: [{"mutation_name": "null"}]';


--
-- Name: table_1; Type: TABLE; Schema: test_parse_copy_values_with_relations; Owner: -
--

CREATE TABLE test_parse_copy_values_with_relations.table_1 (
    id text,
    first_name text,
    last_name text
);


--
-- Name: COLUMN table_1.first_name; Type: COMMENT; Schema: test_parse_copy_values_with_relations; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_relations.table_1.first_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "test_parse_copy_values_with_relations.table_2", "column_name": "f_name", "from_column_name": "id", "to_column_name": "uuid"}, {"table_name": "test_parse_copy_values_with_relations.table_3", "column_name": "fir_name", "from_column_name": "id", "to_column_name": "identifier"}]}]';


--
-- Name: table_2; Type: TABLE; Schema: test_parse_copy_values_with_relations; Owner: -
--

CREATE TABLE test_parse_copy_values_with_relations.table_2 (
    uuid text,
    f_name text,
    l_name text
);


--
-- Name: COLUMN table_2.f_name; Type: COMMENT; Schema: test_parse_copy_values_with_relations; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_relations.table_2.f_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "test_parse_copy_values_with_relations.table_1", "column_name": "first_name", "from_column_name": "uuid", "to_column_name": "id"}, {"table_name": "test_parse_copy_values_with_relations.table_3", "column_name": "fir_name", "from_column_name": "uuid", "to_column_name": "identifier"}]}]';


--
-- Name: table_3; Type: TABLE; Schema: test_parse_copy_values_with_relations; Owner: -
--

CREATE TABLE test_parse_copy_values_with_relations.table_3 (
    identifier text,
    fir_name text,
    las_name text
);


--
-- Name: COLUMN table_3.fir_name; Type: COMMENT; Schema: test_parse_copy_values_with_relations; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_relations.table_3.fir_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "test_parse_copy_values_with_relations.table_1", "column_name": "first_name", "from_column_name": "identifier", "to_column_name": "id"}, {"table_name": "test_parse_copy_values_with_relations.table_2", "column_name": "f_name", "from_column_name": "identifier", "to_column_name": "uuid"}]}]';


--
-- Name: table_4; Type: TABLE; Schema: test_parse_copy_values_with_relations; Owner: -
--

CREATE TABLE test_parse_copy_values_with_relations.table_4 (
    identifier text,
    fir_name text,
    las_name text
);


--
-- Name: table_1; Type: TABLE; Schema: test_parse_copy_values_with_self_relation; Owner: -
--

CREATE TABLE test_parse_copy_values_with_self_relation.table_1 (
    id text,
    first_name text,
    last_name text
);


--
-- Name: COLUMN table_1.first_name; Type: COMMENT; Schema: test_parse_copy_values_with_self_relation; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_self_relation.table_1.first_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "test_parse_copy_values_with_self_relation.table_1", "column_name": "last_name", "from_column_name": "id", "to_column_name": "id"}]}]';


--
-- Name: COLUMN table_1.last_name; Type: COMMENT; Schema: test_parse_copy_values_with_self_relation; Owner: -
--

COMMENT ON COLUMN test_parse_copy_values_with_self_relation.table_1.last_name IS 'anon: [{"mutation_name": "last_name", "relations": [{"table_name": "test_parse_copy_values_with_self_relation.table_1", "column_name": "first_name", "from_column_name": "id", "to_column_name": "id"}]}]';


--
-- Name: table_1; Type: TABLE; Schema: test_two_mutation_for_one_column; Owner: -
--

CREATE TABLE test_two_mutation_for_one_column.table_1 (
    id text,
    username text,
    last_name text
);


--
-- Name: COLUMN table_1.username; Type: COMMENT; Schema: test_two_mutation_for_one_column; Owner: -
--

COMMENT ON COLUMN test_two_mutation_for_one_column.table_1.username IS 'anon: [{"mutation_name": "phone_number", "mutation_kwargs": {"mask": "790########", "unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^7[0-9]{10}$"}, {"column_name": "username", "operation": "by_pattern", "value": "^8[0-9]{10}$"}]}, {"mutation_name": "email", "mutation_kwargs": {"unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^\\S+@\\S+\\.\\S+$"}]}]';


--
-- Name: orders; Type: TABLE; Schema: typed_restore; Owner: -
--

CREATE TABLE typed_restore.orders (
    id integer NOT NULL,
    user_id uuid NOT NULL,
    amount numeric(10,2) NOT NULL,
    CONSTRAINT orders_amount_check CHECK ((amount > (0)::numeric))
);


--
-- Name: users; Type: TABLE; Schema: typed_restore; Owner: -
--

CREATE TABLE typed_restore.users (
    id uuid NOT NULL,
    email text NOT NULL,
    birthday date NOT NULL,
    details jsonb NOT NULL,
    salt text,
    CONSTRAINT users_details_check CHECK ((details ? 'secret'::text)),
    CONSTRAINT users_email_check CHECK ((POSITION(('@'::text) IN (email)) > 1))
);


--
-- Name: COLUMN users.email; Type: COMMENT; Schema: typed_restore; Owner: -
--

COMMENT ON COLUMN typed_restore.users.email IS 'anon: [{"mutation_name":"email"}]';


--
-- Name: COLUMN users.birthday; Type: COMMENT; Schema: typed_restore; Owner: -
--

COMMENT ON COLUMN typed_restore.users.birthday IS 'anon: [{"mutation_name":"date","mutation_kwargs":{"start":2000,"end":2024}}]';


--
-- Name: COLUMN users.details; Type: COMMENT; Schema: typed_restore; Owner: -
--

COMMENT ON COLUMN typed_restore.users.details IS 'anon: [{"mutation_name":"json_update","mutation_kwargs":{"mutations_by_key":{"secret":[{"mutation_name":"fixed_value","mutation_kwargs":{"value":"hidden"}}]}}}]';


--
-- Name: COLUMN users.salt; Type: COMMENT; Schema: typed_restore; Owner: -
--

COMMENT ON COLUMN typed_restore.users.salt IS 'anon: [{"mutation_name":"null"}]';


--
-- Data for Name: users; Type: TABLE DATA; Schema: context_0_0; Owner: -
--

COPY context_0_0.users (value, id, name) FROM stdin;
first	1	Alice
second	2	Bob
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: context_0_1; Owner: -
--

COPY context_0_1.users (value, id, name) FROM stdin;
first	1	Alice
second	2	Bob
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: context_1_0; Owner: -
--

COPY context_1_0.users (value, id, name) FROM stdin;
first	1	Alice
second	2	Bob
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: context_1_1; Owner: -
--

COPY context_1_1.users (value, id, name) FROM stdin;
first	1	Alice
second	2	Bob
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_applies_mutations_recursively; Owner: -
--

COPY json_applies_mutations_recursively.json_values (id, details) FROM stdin;
1	{"profile": {"phone": "+70000000001"}, "contacts": [{"phone": "+70000000002"}, {"phone": "+70000000003"}]}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_combined_operations; Owner: -
--

COPY json_combined_operations.json_values (id, details) FROM stdin;
1	{"first_name": "Alice", "secret": "topsecret", "notes": "private", "untouched": "keep me"}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_delete_existing_key; Owner: -
--

COPY json_delete_existing_key.json_values (id, details) FROM stdin;
1	{"name": "Carol", "secret": "topsecret"}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_delete_missing_key_is_noop; Owner: -
--

COPY json_delete_missing_key_is_noop.json_values (id, details) FROM stdin;
1	{"name": "Dave"}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_existing_key_is_replaced; Owner: -
--

COPY json_existing_key_is_replaced.json_values (id, details) FROM stdin;
1	{"name": "Alice", "score": 42}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_existing_key_passes_current_value; Owner: -
--

COPY json_existing_key_passes_current_value.json_values (id, details) FROM stdin;
1	{"phone": "+70000000000", "role": "admin"}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_invalid_json_raises; Owner: -
--

COPY json_invalid_json_raises.json_values (id, details) FROM stdin;
1	not-json-at-all
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_json_array_passthrough; Owner: -
--

COPY json_json_array_passthrough.json_values (id, details) FROM stdin;
1	[1, 2, 3]
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_json_scalar_passthrough; Owner: -
--

COPY json_json_scalar_passthrough.json_values (id, details) FROM stdin;
1	42
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_key_name_can_be_current_value; Owner: -
--

COPY json_key_name_can_be_current_value.json_values (id, details) FROM stdin;
1	{"current_value": "sensitive"}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_missing_key_is_added; Owner: -
--

COPY json_missing_key_is_added.json_values (id, details) FROM stdin;
1	{"name": "Bob"}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_null_existing_key; Owner: -
--

COPY json_null_existing_key.json_values (id, details) FROM stdin;
1	{"name": "Eve", "notes": "some private notes"}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_null_missing_key_adds_null; Owner: -
--

COPY json_null_missing_key_adds_null.json_values (id, details) FROM stdin;
1	{"name": "Frank"}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_postgres_null_passthrough; Owner: -
--

COPY json_postgres_null_passthrough.json_values (id, details) FROM stdin;
1	\N
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_preserving_the_numeric_type; Owner: -
--

COPY json_preserving_the_numeric_type.json_values (id, details) FROM stdin;
1	{"score": 42}
\.


--
-- Data for Name: json_values; Type: TABLE DATA; Schema: json_unknown_mutation_raises; Owner: -
--

COPY json_unknown_mutation_raises.json_values (id, details) FROM stdin;
1	{"key": "value"}
\.


--
-- Data for Name: _table; Type: TABLE DATA; Schema: metadata; Owner: -
--

COPY metadata._table (column_1, column_2) FROM stdin;
1	value
\.


--
-- Data for Name: deleted_table; Type: TABLE DATA; Schema: metadata; Owner: -
--

COPY metadata.deleted_table (field_value) FROM stdin;
value
\.


--
-- Data for Name: invalid_column; Type: TABLE DATA; Schema: metadata; Owner: -
--

COPY metadata.invalid_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: kept_table; Type: TABLE DATA; Schema: metadata; Owner: -
--

COPY metadata.kept_table (field_value) FROM stdin;
value
\.


--
-- Data for Name: null_column; Type: TABLE DATA; Schema: metadata; Owner: -
--

COPY metadata.null_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: plain_values; Type: TABLE DATA; Schema: metadata; Owner: -
--

COPY metadata.plain_values (column_1, column_2) FROM stdin;
1	value
\.


--
-- Data for Name: unknown_column; Type: TABLE DATA; Schema: metadata; Owner: -
--

COPY metadata.unknown_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: _table; Type: TABLE DATA; Schema: metadata__schema; Owner: -
--

COPY metadata__schema._table (column_1, column_2) FROM stdin;
1	value
\.


--
-- Data for Name: deleted_table; Type: TABLE DATA; Schema: metadata__schema; Owner: -
--

COPY metadata__schema.deleted_table (field_value) FROM stdin;
value
\.


--
-- Data for Name: invalid_column; Type: TABLE DATA; Schema: metadata__schema; Owner: -
--

COPY metadata__schema.invalid_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: kept_table; Type: TABLE DATA; Schema: metadata__schema; Owner: -
--

COPY metadata__schema.kept_table (field_value) FROM stdin;
value
\.


--
-- Data for Name: null_column; Type: TABLE DATA; Schema: metadata__schema; Owner: -
--

COPY metadata__schema.null_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: plain_values; Type: TABLE DATA; Schema: metadata__schema; Owner: -
--

COPY metadata__schema.plain_values (column_1, column_2) FROM stdin;
1	value
\.


--
-- Data for Name: unknown_column; Type: TABLE DATA; Schema: metadata__schema; Owner: -
--

COPY metadata__schema.unknown_column (field_value) FROM stdin;
value
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: original_conditions; Owner: -
--

COPY original_conditions.users (id, status, email, notes, empty) FROM stdin;
1	original	private	\N	
2	other	private	literal\ttext	
\.


--
-- Data for Name: zz_untouched; Type: TABLE DATA; Schema: original_conditions; Owner: -
--

COPY original_conditions.zz_untouched (id, name) FROM stdin;
3	original
\.


--
-- Data for Name: a_source; Type: TABLE DATA; Schema: relations_source; Owner: -
--

COPY relations_source.a_source (name, id, alternate_id) FROM stdin;
Alice	1	a
Bob	2	b
\.


--
-- Data for Name: b_target; Type: TABLE DATA; Schema: relations_source; Owner: -
--

COPY relations_source.b_target (alternate_ref, name, ref) FROM stdin;
a	Carol	missing-1
b	Dave	missing-2
\.


--
-- Data for Name: a_target; Type: TABLE DATA; Schema: relations_target; Owner: -
--

COPY relations_target.a_target (alternate_ref, name, ref) FROM stdin;
a	Carol	missing-1
b	Dave	missing-2
\.


--
-- Data for Name: b_source; Type: TABLE DATA; Schema: relations_target; Owner: -
--

COPY relations_target.b_source (name, id, alternate_id) FROM stdin;
Alice	1	a
Bob	2	b
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: source_0; Owner: -
--

COPY source_0.users (token, id, name, notes) FROM stdin;
old-token	1	original	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: source_1; Owner: -
--

COPY source_1.users (token, id, name, notes) FROM stdin;
old-token	1	original	\N
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_by_pattern_condition; Owner: -
--

COPY test_by_pattern_condition.table_1 (id, email, active) FROM stdin;
1	test@mail.ru	t
2	test@mail.ru	f
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_equal_condition; Owner: -
--

COPY test_equal_condition.table_1 (id, email, active) FROM stdin;
1	test@mail.ru	t
2	test@mail.ru	f
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_not_equal_condition; Owner: -
--

COPY test_not_equal_condition.table_1 (id, email, active) FROM stdin;
1	test@mail.ru	t
2	test@mail.ru	f
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_obfuscate_uuid_by_source_value; Owner: -
--

COPY test_obfuscate_uuid_by_source_value.table_1 (uuid, username, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	79999999999	111n
20f654fe-b27d-4051-9fd4-000000000002	79888888888	222n
20f654fe-b27d-4051-9fd4-000000000003	79777777777	333n
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_parse_copy_values_with_delete_tables; Owner: -
--

COPY test_parse_copy_values_with_delete_tables.table_1 (id, message, recipient, notes) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	Hello -\nI'm writing in regards to the stuff I've been receiving. Double quotes are "awesome"!	support@example.com	\N
20f654fe-b27d-4051-9fd4-000000000002	Anything	\N	\N
\.


--
-- Data for Name: table_2; Type: TABLE DATA; Schema: test_parse_copy_values_with_delete_tables__schema; Owner: -
--

COPY test_parse_copy_values_with_delete_tables__schema.table_2 (id, message, recipient, notes) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	Hello -\nI'm writing in regards to the stuff I've been receiving. Double quotes are "awesome"!	support@example.com	\N
20f654fe-b27d-4051-9fd4-000000000002	Anything	\N	\N
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_parse_copy_values_with_mutation; Owner: -
--

COPY test_parse_copy_values_with_mutation.table_1 (id, crypted_password, persistence_token, text) FROM stdin;
07750c56-fb37-46e1-b7b6-da530704c056	400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3255d3bd1edd18ffc4a8092e2616b9e5ca7954b2c52504	86a97ff982e87ed5af7d90ab2ce31d4e89a3af3e6a0490b067bb8213aea7a4ee0eeafae1d8fe3c6f990aead095092fcf852004b18e484ef22569aebf64c3747f	Test Text
d489bda7-3212-4026-aef9-879d3242ad0c	400$8$50$5555852e67bf920f$161b41afd99159609151f22fbc4efdccb925244606a87fc635954a71e8f7606f	630aaf10f3edcb396181535476bccfd369e1ee9281cbc218d0861e6117b9839219cb403abed3b59468b2564c229d78b0cb610d0e16fa4a03dc4d93ed3d55deb3	Happy New Year
ab344f75-d78a-47ba-a4f7-121275b3b241	400$8$4a$fb1a833f95079502$8b6ddd327381860e18bce53ee1a3249d5237de4f4344c06ad940ba8cfc6a2259	06fa5d0f3a4d62ff60717ff3315301129a5bcd152f63f073b67d2e6a835b098524b1d097367283c97ca75db9154cf61d6a918248eb68eaf8cd83d1a87cdd92dc	Hello
f7bd4a7f-b63f-41c3-83bd-9683f33bb4b3	400$8$50$8368e20d878ef1b1$b271e3af024b424b7256592439a35d6eb224b4dc769ac9f2fa564b282efb8a47	02cbd8d1e9690c7786375f9f6ec4da6fa3c2ead70d41a7aa1d7fe631477b42635210f0e8fa7579f6f4b5afdb364d9465623a2861ecff75fa3a052c9b2a9fc2dd	Nice Try
abe9fd39-f0b3-4ec6-9006-9783fbdade07	400$8$50$ef1eb813f8d8b99d$2932a9dc75d10f13525e43c29726061d99b4ebdff2e9f9951eb6e2393f36d221	b09909b6e83938dd41ffb5e931eeb3d646b1856dfb74a81acb1697b6d8466468047fe92286e011a4634c71b8d8775c7d5a31e19ce111bd31d0a61a4faf93d6af	Every Day
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_parse_copy_values_with_mutation__schema; Owner: -
--

COPY test_parse_copy_values_with_mutation__schema.table_1 (id, email, crypted_password, dt_birthday, password_salt) FROM stdin;
07750c56-fb37-46e1-b7b6-da530704c056	cj@example.com	400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3255d3bd1edd18ffc4a8092e2616b9e5ca7954b2c52504	1996-10-02	v8BMktHnOeokEBTy6As
d489bda7-3212-4026-aef9-879d3242ad0c	leo@example.com	400$8$50$5555852e67bf920f$161b41afd99159609151f22fbc4efdccb925244606a87fc635954a71e8f7606f	1996-10-03	c5d6v3NS97D3wYkUltFQ
ab344f75-d78a-47ba-a4f7-121275b3b241	donna@example.com	400$8$4a$fb1a833f95079502$8b6ddd327381860e18bce53ee1a3249d5237de4f4344c06ad940ba8cfc6a2259	2005-01-02	2IcBeSh6IVVCJyZpqBt
f7bd4a7f-b63f-41c3-83bd-9683f33bb4b3	charlie@example.com	400$8$50$8368e20d878ef1b1$b271e3af024b424b7256592439a35d6eb224b4dc769ac9f2fa564b282efb8a47	2005-10-02	QOqWQ24CMiRNuPUz8f5
abe9fd39-f0b3-4ec6-9006-9783fbdade07	fun@example.com	400$8$50$ef1eb813f8d8b99d$2932a9dc75d10f13525e43c29726061d99b4ebdff2e9f9951eb6e2393f36d221	2022-12-31	uMYA6c3A7uGoI0aEbJ8R
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_parse_copy_values_with_relations; Owner: -
--

COPY test_parse_copy_values_with_relations.table_1 (id, first_name, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.


--
-- Data for Name: table_2; Type: TABLE DATA; Schema: test_parse_copy_values_with_relations; Owner: -
--

COPY test_parse_copy_values_with_relations.table_2 (uuid, f_name, l_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.


--
-- Data for Name: table_3; Type: TABLE DATA; Schema: test_parse_copy_values_with_relations; Owner: -
--

COPY test_parse_copy_values_with_relations.table_3 (identifier, fir_name, las_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.


--
-- Data for Name: table_4; Type: TABLE DATA; Schema: test_parse_copy_values_with_relations; Owner: -
--

COPY test_parse_copy_values_with_relations.table_4 (identifier, fir_name, las_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_parse_copy_values_with_self_relation; Owner: -
--

COPY test_parse_copy_values_with_self_relation.table_1 (id, first_name, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	111n
20f654fe-b27d-4051-9fd4-000000000002	222n	222n
\.


--
-- Data for Name: table_1; Type: TABLE DATA; Schema: test_two_mutation_for_one_column; Owner: -
--

COPY test_two_mutation_for_one_column.table_1 (id, username, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	79999999999	111n
20f654fe-b27d-4051-9fd4-000000000002	test@mail.ru	222n
20f654fe-b27d-4051-9fd4-000000000003	89999999999	333n
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: typed_restore; Owner: -
--

COPY typed_restore.orders (id, user_id, amount) FROM stdin;
1	07750c56-fb37-46e1-b7b6-da530704c056	12.50
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: typed_restore; Owner: -
--

COPY typed_restore.users (id, email, birthday, details, salt) FROM stdin;
07750c56-fb37-46e1-b7b6-da530704c056	private@example.com	1990-01-01	{"secret": "private", "untouched": 42}	private-salt
\.


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: typed_restore; Owner: -
--

ALTER TABLE ONLY typed_restore.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: typed_restore; Owner: -
--

ALTER TABLE ONLY typed_restore.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: typed_restore; Owner: -
--

ALTER TABLE ONLY typed_restore.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES typed_restore.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict FuFYknFjhAUDOxdayPtHUcYg2tHekFo221vXukWwgQICxnAFNOjyE1DTezIjkGJ

