-- Source data for the single PG15 plain snapshot. Regenerate with tools.generate_fixtures.

-- Scenario: test_by_pattern_condition
CREATE SCHEMA test_by_pattern_condition;
CREATE SCHEMA test_by_pattern_condition__schema;
CREATE TABLE test_by_pattern_condition.table_1 ("id" text, "email" text, "active" text);
COMMENT ON COLUMN test_by_pattern_condition.table_1.email IS 'anon: [{"mutation_name": "email", "conditions": [{"column_name": "email", "operation": "by_pattern", "value": "\\w+\\@\\w+\\.\\w{2}"}]}]';
COPY test_by_pattern_condition.table_1 (id, email, active) FROM stdin;
1	test@mail.ru	t
2	test@mail.ru	f
\.

-- Scenario: test_equal_condition
CREATE SCHEMA test_equal_condition;
CREATE SCHEMA test_equal_condition__schema;
CREATE TABLE test_equal_condition.table_1 ("id" text, "email" text, "active" text);
COMMENT ON COLUMN test_equal_condition.table_1.email IS 'anon: [{"mutation_name": "email", "conditions": [{"column_name": "active", "operation": "equal", "value": "t"}]}]';
COPY test_equal_condition.table_1 (id, email, active) FROM stdin;
1	test@mail.ru	t
2	test@mail.ru	f
\.

-- Scenario: test_not_equal_condition
CREATE SCHEMA test_not_equal_condition;
CREATE SCHEMA test_not_equal_condition__schema;
CREATE TABLE test_not_equal_condition.table_1 ("id" text, "email" text, "active" text);
COMMENT ON COLUMN test_not_equal_condition.table_1.email IS 'anon: [{"mutation_name": "email", "conditions": [{"column_name": "active", "operation": "not_equal", "value": "t"}]}]';
COPY test_not_equal_condition.table_1 (id, email, active) FROM stdin;
1	test@mail.ru	t
2	test@mail.ru	f
\.

-- Scenario: test_obfuscate_uuid_by_source_value
CREATE SCHEMA test_obfuscate_uuid_by_source_value;
CREATE SCHEMA test_obfuscate_uuid_by_source_value__schema;
CREATE TABLE test_obfuscate_uuid_by_source_value.table_1 ("uuid" text, "username" text, "last_name" text);
COMMENT ON COLUMN test_obfuscate_uuid_by_source_value.table_1.username IS 'anon: [{"mutation_name": "phone_number", "mutation_kwargs": {"mask": "791########", "unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^7[0-9]{10}$"}]}]';
COMMENT ON COLUMN test_obfuscate_uuid_by_source_value.table_1.uuid IS 'anon: [{"mutation_name": "uuid5_by_source_value", "mutation_kwargs": {"source_column": "username", "namespace": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';
COPY test_obfuscate_uuid_by_source_value.table_1 (uuid, username, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	79999999999	111n
20f654fe-b27d-4051-9fd4-000000000002	79888888888	222n
20f654fe-b27d-4051-9fd4-000000000003	79777777777	333n
\.

-- Scenario: test_parse_copy_values_with_delete_tables
CREATE SCHEMA test_parse_copy_values_with_delete_tables;
CREATE SCHEMA test_parse_copy_values_with_delete_tables__schema;
CREATE TABLE test_parse_copy_values_with_delete_tables.table_1 ("id" text, "message" text, "recipient" text, "notes" text);
COMMENT ON TABLE test_parse_copy_values_with_delete_tables.table_1 IS 'anon: {"mutation_name": "delete"}';
COPY test_parse_copy_values_with_delete_tables.table_1 (id, message, recipient, notes) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	Hello -\nI'm writing in regards to the stuff I've been receiving. Double quotes are "awesome"!	support@example.com	\N
20f654fe-b27d-4051-9fd4-000000000002	Anything	\N	\N
\.
CREATE TABLE test_parse_copy_values_with_delete_tables__schema.table_2 ("id" text, "message" text, "recipient" text, "notes" text);
COMMENT ON TABLE test_parse_copy_values_with_delete_tables__schema.table_2 IS 'anon: {"mutation_name": "delete"}';
COPY test_parse_copy_values_with_delete_tables__schema.table_2 (id, message, recipient, notes) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	Hello -\nI'm writing in regards to the stuff I've been receiving. Double quotes are "awesome"!	support@example.com	\N
20f654fe-b27d-4051-9fd4-000000000002	Anything	\N	\N
\.

-- Scenario: test_parse_copy_values_with_mutation
CREATE SCHEMA test_parse_copy_values_with_mutation;
CREATE SCHEMA test_parse_copy_values_with_mutation__schema;
CREATE TABLE test_parse_copy_values_with_mutation.table_1 ("id" text, "crypted_password" text, "persistence_token" text, "text" text);
COMMENT ON COLUMN test_parse_copy_values_with_mutation.table_1.persistence_token IS 'anon: [{"mutation_name": "empty_string"}]';
COMMENT ON COLUMN test_parse_copy_values_with_mutation.table_1.crypted_password IS 'anon: [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3125d3bd1ett18ffc4a8092e2616b9e5ca7954b2c52504"}}]';
COMMENT ON COLUMN test_parse_copy_values_with_mutation.table_1.text IS 'anon: [{"mutation_name": "string_by_mask", "mutation_kwargs": {"mask": "test chars: @@@@@; test digits: #####;"}}]';
COPY test_parse_copy_values_with_mutation.table_1 (id, crypted_password, persistence_token, text) FROM stdin;
07750c56-fb37-46e1-b7b6-da530704c056	400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3255d3bd1edd18ffc4a8092e2616b9e5ca7954b2c52504	86a97ff982e87ed5af7d90ab2ce31d4e89a3af3e6a0490b067bb8213aea7a4ee0eeafae1d8fe3c6f990aead095092fcf852004b18e484ef22569aebf64c3747f	Test Text
d489bda7-3212-4026-aef9-879d3242ad0c	400$8$50$5555852e67bf920f$161b41afd99159609151f22fbc4efdccb925244606a87fc635954a71e8f7606f	630aaf10f3edcb396181535476bccfd369e1ee9281cbc218d0861e6117b9839219cb403abed3b59468b2564c229d78b0cb610d0e16fa4a03dc4d93ed3d55deb3	Happy New Year
ab344f75-d78a-47ba-a4f7-121275b3b241	400$8$4a$fb1a833f95079502$8b6ddd327381860e18bce53ee1a3249d5237de4f4344c06ad940ba8cfc6a2259	06fa5d0f3a4d62ff60717ff3315301129a5bcd152f63f073b67d2e6a835b098524b1d097367283c97ca75db9154cf61d6a918248eb68eaf8cd83d1a87cdd92dc	Hello
f7bd4a7f-b63f-41c3-83bd-9683f33bb4b3	400$8$50$8368e20d878ef1b1$b271e3af024b424b7256592439a35d6eb224b4dc769ac9f2fa564b282efb8a47	02cbd8d1e9690c7786375f9f6ec4da6fa3c2ead70d41a7aa1d7fe631477b42635210f0e8fa7579f6f4b5afdb364d9465623a2861ecff75fa3a052c9b2a9fc2dd	Nice Try
abe9fd39-f0b3-4ec6-9006-9783fbdade07	400$8$50$ef1eb813f8d8b99d$2932a9dc75d10f13525e43c29726061d99b4ebdff2e9f9951eb6e2393f36d221	b09909b6e83938dd41ffb5e931eeb3d646b1856dfb74a81acb1697b6d8466468047fe92286e011a4634c71b8d8775c7d5a31e19ce111bd31d0a61a4faf93d6af	Every Day
\.
CREATE TABLE test_parse_copy_values_with_mutation__schema.table_1 ("id" text, "email" text, "crypted_password" text, "dt_birthday" text, "password_salt" text);
COMMENT ON COLUMN test_parse_copy_values_with_mutation__schema.table_1.email IS 'anon: [{"mutation_name": "email"}]';
COMMENT ON COLUMN test_parse_copy_values_with_mutation__schema.table_1.password_salt IS 'anon: [{"mutation_name": "null"}]';
COMMENT ON COLUMN test_parse_copy_values_with_mutation__schema.table_1.dt_birthday IS 'anon: [{"mutation_name": "date", "mutation_kwargs": {"start": 2000, "end": 2024}}]';
COMMENT ON COLUMN test_parse_copy_values_with_mutation__schema.table_1.crypted_password IS 'anon: [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3125d3bd1ett18ffc4a8092e2616b9e5ca7954b2c52504"}}]';
COPY test_parse_copy_values_with_mutation__schema.table_1 (id, email, crypted_password, dt_birthday, password_salt) FROM stdin;
07750c56-fb37-46e1-b7b6-da530704c056	cj@example.com	400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3255d3bd1edd18ffc4a8092e2616b9e5ca7954b2c52504	1996-10-02	v8BMktHnOeokEBTy6As
d489bda7-3212-4026-aef9-879d3242ad0c	leo@example.com	400$8$50$5555852e67bf920f$161b41afd99159609151f22fbc4efdccb925244606a87fc635954a71e8f7606f	1996-10-03	c5d6v3NS97D3wYkUltFQ
ab344f75-d78a-47ba-a4f7-121275b3b241	donna@example.com	400$8$4a$fb1a833f95079502$8b6ddd327381860e18bce53ee1a3249d5237de4f4344c06ad940ba8cfc6a2259	2005-01-02	2IcBeSh6IVVCJyZpqBt
f7bd4a7f-b63f-41c3-83bd-9683f33bb4b3	charlie@example.com	400$8$50$8368e20d878ef1b1$b271e3af024b424b7256592439a35d6eb224b4dc769ac9f2fa564b282efb8a47	2005-10-02	QOqWQ24CMiRNuPUz8f5
abe9fd39-f0b3-4ec6-9006-9783fbdade07	fun@example.com	400$8$50$ef1eb813f8d8b99d$2932a9dc75d10f13525e43c29726061d99b4ebdff2e9f9951eb6e2393f36d221	2022-12-31	uMYA6c3A7uGoI0aEbJ8R
\.

-- Scenario: test_parse_copy_values_with_relations
CREATE SCHEMA test_parse_copy_values_with_relations;
CREATE SCHEMA test_parse_copy_values_with_relations__schema;
CREATE TABLE test_parse_copy_values_with_relations.table_1 ("id" text, "first_name" text, "last_name" text);
COMMENT ON COLUMN test_parse_copy_values_with_relations.table_1.first_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "test_parse_copy_values_with_relations.table_2", "column_name": "f_name", "from_column_name": "id", "to_column_name": "uuid"}, {"table_name": "test_parse_copy_values_with_relations.table_3", "column_name": "fir_name", "from_column_name": "id", "to_column_name": "identifier"}]}]';
COPY test_parse_copy_values_with_relations.table_1 (id, first_name, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.
CREATE TABLE test_parse_copy_values_with_relations.table_2 ("uuid" text, "f_name" text, "l_name" text);
COMMENT ON COLUMN test_parse_copy_values_with_relations.table_2.f_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "test_parse_copy_values_with_relations.table_1", "column_name": "first_name", "from_column_name": "uuid", "to_column_name": "id"}, {"table_name": "test_parse_copy_values_with_relations.table_3", "column_name": "fir_name", "from_column_name": "uuid", "to_column_name": "identifier"}]}]';
COPY test_parse_copy_values_with_relations.table_2 (uuid, f_name, l_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.
CREATE TABLE test_parse_copy_values_with_relations.table_3 ("identifier" text, "fir_name" text, "las_name" text);
COMMENT ON COLUMN test_parse_copy_values_with_relations.table_3.fir_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "test_parse_copy_values_with_relations.table_1", "column_name": "first_name", "from_column_name": "identifier", "to_column_name": "id"}, {"table_name": "test_parse_copy_values_with_relations.table_2", "column_name": "f_name", "from_column_name": "identifier", "to_column_name": "uuid"}]}]';
COPY test_parse_copy_values_with_relations.table_3 (identifier, fir_name, las_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.
CREATE TABLE test_parse_copy_values_with_relations.table_4 ("identifier" text, "fir_name" text, "las_name" text);

COPY test_parse_copy_values_with_relations.table_4 (identifier, fir_name, las_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.

-- Scenario: test_parse_copy_values_with_self_relation
CREATE SCHEMA test_parse_copy_values_with_self_relation;
CREATE SCHEMA test_parse_copy_values_with_self_relation__schema;
CREATE TABLE test_parse_copy_values_with_self_relation.table_1 ("id" text, "first_name" text, "last_name" text);
COMMENT ON COLUMN test_parse_copy_values_with_self_relation.table_1.first_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "test_parse_copy_values_with_self_relation.table_1", "column_name": "last_name", "from_column_name": "id", "to_column_name": "id"}]}]';
COMMENT ON COLUMN test_parse_copy_values_with_self_relation.table_1.last_name IS 'anon: [{"mutation_name": "last_name", "relations": [{"table_name": "test_parse_copy_values_with_self_relation.table_1", "column_name": "first_name", "from_column_name": "id", "to_column_name": "id"}]}]';
COPY test_parse_copy_values_with_self_relation.table_1 (id, first_name, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	111n
20f654fe-b27d-4051-9fd4-000000000002	222n	222n
\.

-- Scenario: test_two_mutation_for_one_column
CREATE SCHEMA test_two_mutation_for_one_column;
CREATE SCHEMA test_two_mutation_for_one_column__schema;
CREATE TABLE test_two_mutation_for_one_column.table_1 ("id" text, "username" text, "last_name" text);
COMMENT ON COLUMN test_two_mutation_for_one_column.table_1.username IS 'anon: [{"mutation_name": "phone_number", "mutation_kwargs": {"mask": "790########", "unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^7[0-9]{10}$"}, {"column_name": "username", "operation": "by_pattern", "value": "^8[0-9]{10}$"}]}, {"mutation_name": "email", "mutation_kwargs": {"unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^\\S+@\\S+\\.\\S+$"}]}]';
COPY test_two_mutation_for_one_column.table_1 (id, username, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	79999999999	111n
20f654fe-b27d-4051-9fd4-000000000002	test@mail.ru	222n
20f654fe-b27d-4051-9fd4-000000000003	89999999999	333n
\.

-- Scenario: metadata
CREATE SCHEMA metadata;
CREATE SCHEMA metadata__schema;
CREATE TABLE metadata.plain_values ("column_1" text, "column_2" text);

COPY metadata.plain_values (column_1, column_2) FROM stdin;
1	value
\.
CREATE TABLE metadata._table ("column_1" text, "column_2" text);

COPY metadata._table (column_1, column_2) FROM stdin;
1	value
\.
CREATE TABLE metadata.null_column ("field_value" text);
COMMENT ON COLUMN metadata.null_column.field_value IS 'anon: [{"mutation_name": "null"}]';
COPY metadata.null_column (field_value) FROM stdin;
value
\.
CREATE TABLE metadata.unknown_column ("field_value" text);
COMMENT ON COLUMN metadata.unknown_column.field_value IS 'anon: [{"mutation_name": "not_found"}]';
COPY metadata.unknown_column (field_value) FROM stdin;
value
\.
CREATE TABLE metadata.invalid_column ("field_value" text);
COMMENT ON COLUMN metadata.invalid_column.field_value IS 'anon: {''mutation_name": "null"}';
COPY metadata.invalid_column (field_value) FROM stdin;
value
\.
CREATE TABLE metadata.deleted_table ("field_value" text);
COMMENT ON TABLE metadata.deleted_table IS 'anon: {"mutation_name": "delete"}';
COPY metadata.deleted_table (field_value) FROM stdin;
value
\.
CREATE TABLE metadata.kept_table ("field_value" text);
COMMENT ON TABLE metadata.kept_table IS 'anon: {"mutation_name": "set"}';
COPY metadata.kept_table (field_value) FROM stdin;
value
\.
CREATE TABLE metadata__schema.plain_values ("column_1" text, "column_2" text);

COPY metadata__schema.plain_values (column_1, column_2) FROM stdin;
1	value
\.
CREATE TABLE metadata__schema._table ("column_1" text, "column_2" text);

COPY metadata__schema._table (column_1, column_2) FROM stdin;
1	value
\.
CREATE TABLE metadata__schema.null_column ("field_value" text);
COMMENT ON COLUMN metadata__schema.null_column.field_value IS 'anon: [{"mutation_name": "null"}]';
COPY metadata__schema.null_column (field_value) FROM stdin;
value
\.
CREATE TABLE metadata__schema.unknown_column ("field_value" text);
COMMENT ON COLUMN metadata__schema.unknown_column.field_value IS 'anon: [{"mutation_name": "not_found"}]';
COPY metadata__schema.unknown_column (field_value) FROM stdin;
value
\.
CREATE TABLE metadata__schema.invalid_column ("field_value" text);
COMMENT ON COLUMN metadata__schema.invalid_column.field_value IS 'anon: {''mutation_name": "null"}';
COPY metadata__schema.invalid_column (field_value) FROM stdin;
value
\.
CREATE TABLE metadata__schema.deleted_table ("field_value" text);
COMMENT ON TABLE metadata__schema.deleted_table IS 'anon: {"mutation_name": "delete"}';
COPY metadata__schema.deleted_table (field_value) FROM stdin;
value
\.
CREATE TABLE metadata__schema.kept_table ("field_value" text);
COMMENT ON TABLE metadata__schema.kept_table IS 'anon: {"mutation_name": "set"}';
COPY metadata__schema.kept_table (field_value) FROM stdin;
value
\.

-- Scenario: context-0-0
CREATE SCHEMA context_0_0;
CREATE TABLE context_0_0.users ("value" text, "id" text, "name" text);
COMMENT ON COLUMN context_0_0.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name"}}]';
COPY context_0_0.users (value, id, name) FROM stdin;
first	1	Alice
second	2	Bob
\.

-- Scenario: context-0-1
CREATE SCHEMA context_0_1;
CREATE TABLE context_0_1.users ("value" text, "id" text, "name" text);
COMMENT ON COLUMN context_0_1.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name"}, "relations": [{"table_name": "context_0_1.peers", "column_name": "value", "from_column_name": "id", "to_column_name": "id"}]}]';
COPY context_0_1.users (value, id, name) FROM stdin;
first	1	Alice
second	2	Bob
\.

-- Scenario: context-1-0
CREATE SCHEMA context_1_0;
CREATE TABLE context_1_0.users ("value" text, "id" text, "name" text);
COMMENT ON COLUMN context_1_0.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name", "current_value": "fixed", "obfuscated_values": {"name": "configured"}}}]';
COPY context_1_0.users (value, id, name) FROM stdin;
first	1	Alice
second	2	Bob
\.

-- Scenario: context-1-1
CREATE SCHEMA context_1_1;
CREATE TABLE context_1_1.users ("value" text, "id" text, "name" text);
COMMENT ON COLUMN context_1_1.users.value IS 'anon: [{"mutation_name": "echo", "mutation_kwargs": {"source_column": "name", "current_value": "fixed", "obfuscated_values": {"name": "configured"}}, "relations": [{"table_name": "context_1_1.peers", "column_name": "value", "from_column_name": "id", "to_column_name": "id"}]}]';
COPY context_1_1.users (value, id, name) FROM stdin;
first	1	Alice
second	2	Bob
\.

-- Scenario: original_conditions
CREATE SCHEMA original_conditions;
CREATE TABLE original_conditions.users ("id" text, "status" text, "email" text, "notes" text, "empty" text);
COMMENT ON COLUMN original_conditions.users.status IS 'anon: [{"mutation_name": "random_choice", "mutation_kwargs": {"choices": ["changed"]}}]';
COMMENT ON COLUMN original_conditions.users.email IS 'anon: [{"mutation_name": "random_choice", "mutation_kwargs": {"choices": ["hidden"]}, "conditions": [{"column_name": "status", "operation": "equal", "value": "original"}]}]';
COPY original_conditions.users (id, status, email, notes, empty) FROM stdin;
1	original	private	\N	
2	other	private	literal\ttext	
\.
CREATE TABLE original_conditions.zz_untouched ("id" text, "name" text);

COPY original_conditions.zz_untouched (id, name) FROM stdin;
3	original
\.

-- Scenario: source-0
CREATE SCHEMA source_0;
CREATE TABLE source_0.users ("token" text, "id" text, "name" text, "notes" text);
COMMENT ON COLUMN source_0.users.token IS 'anon: [{"mutation_name": "uuid5_by_source_value", "mutation_kwargs": {"source_column": "name", "namespace": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';
COPY source_0.users (token, id, name, notes) FROM stdin;
old-token	1	original	\N
\.

-- Scenario: source-1
CREATE SCHEMA source_1;
CREATE TABLE source_1.users ("token" text, "id" text, "name" text, "notes" text);
COMMENT ON COLUMN source_1.users.token IS 'anon: [{"mutation_name": "uuid5_by_source_value", "mutation_kwargs": {"source_column": "name", "namespace": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';
COMMENT ON COLUMN source_1.users.name IS 'anon: [{"mutation_name": "random_choice", "mutation_kwargs": {"choices": ["hidden"]}}]';
COPY source_1.users (token, id, name, notes) FROM stdin;
old-token	1	original	\N
\.

-- Scenario: relations-source
CREATE SCHEMA relations_source;
CREATE TABLE relations_source.a_source ("name" text, "id" text, "alternate_id" text);
COMMENT ON COLUMN relations_source.a_source.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "relations_source.b_target", "column_name": "name", "from_column_name": "id", "to_column_name": "ref"}, {"table_name": "relations_source.b_target", "column_name": "name", "from_column_name": "alternate_id", "to_column_name": "alternate_ref"}]}]';
COPY relations_source.a_source (name, id, alternate_id) FROM stdin;
Alice	1	a
Bob	2	b
\.
CREATE TABLE relations_source.b_target ("alternate_ref" text, "name" text, "ref" text);
COMMENT ON COLUMN relations_source.b_target.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "relations_source.a_source", "column_name": "name", "from_column_name": "ref", "to_column_name": "id"}, {"table_name": "relations_source.a_source", "column_name": "name", "from_column_name": "alternate_ref", "to_column_name": "alternate_id"}]}]';
COPY relations_source.b_target (alternate_ref, name, ref) FROM stdin;
a	Carol	missing-1
b	Dave	missing-2
\.

-- Scenario: relations-target
CREATE SCHEMA relations_target;
CREATE TABLE relations_target.b_source ("name" text, "id" text, "alternate_id" text);
COMMENT ON COLUMN relations_target.b_source.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "relations_target.a_target", "column_name": "name", "from_column_name": "id", "to_column_name": "ref"}, {"table_name": "relations_target.a_target", "column_name": "name", "from_column_name": "alternate_id", "to_column_name": "alternate_ref"}]}]';
COPY relations_target.b_source (name, id, alternate_id) FROM stdin;
Alice	1	a
Bob	2	b
\.
CREATE TABLE relations_target.a_target ("alternate_ref" text, "name" text, "ref" text);
COMMENT ON COLUMN relations_target.a_target.name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "relations_target.b_source", "column_name": "name", "from_column_name": "ref", "to_column_name": "id"}, {"table_name": "relations_target.b_source", "column_name": "name", "from_column_name": "alternate_ref", "to_column_name": "alternate_id"}]}]';
COPY relations_target.a_target (alternate_ref, name, ref) FROM stdin;
a	Carol	missing-1
b	Dave	missing-2
\.

-- Scenario: json-existing_key_is_replaced
CREATE SCHEMA json_existing_key_is_replaced;
CREATE TABLE json_existing_key_is_replaced.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_existing_key_is_replaced.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "John"}}]}}}]';
COPY json_existing_key_is_replaced.json_values (id, details) FROM stdin;
1	{"name": "Alice", "score": 42}
\.

-- Scenario: json-existing_key_passes_current_value
CREATE SCHEMA json_existing_key_passes_current_value;
CREATE TABLE json_existing_key_passes_current_value.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_existing_key_passes_current_value.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"phone": [{"mutation_name": "test_echo", "mutation_kwargs": {}}]}}}]';
COPY json_existing_key_passes_current_value.json_values (id, details) FROM stdin;
1	{"phone": "+70000000000", "role": "admin"}
\.

-- Scenario: json-preserving_the_numeric_type
CREATE SCHEMA json_preserving_the_numeric_type;
CREATE TABLE json_preserving_the_numeric_type.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_preserving_the_numeric_type.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"score": [{"mutation_name": "numeric_integer", "mutation_kwargs": {}}]}}}]';
COPY json_preserving_the_numeric_type.json_values (id, details) FROM stdin;
1	{"score": 42}
\.

-- Scenario: json-missing_key_is_added
CREATE SCHEMA json_missing_key_is_added;
CREATE TABLE json_missing_key_is_added.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_missing_key_is_added.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"email": [{"mutation_name": "email", "mutation_kwargs": {}}]}}}]';
COPY json_missing_key_is_added.json_values (id, details) FROM stdin;
1	{"name": "Bob"}
\.

-- Scenario: json-delete_existing_key
CREATE SCHEMA json_delete_existing_key;
CREATE TABLE json_delete_existing_key.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_delete_existing_key.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"secret": [{"mutation_name": "delete", "mutation_kwargs": {}}]}}}]';
COPY json_delete_existing_key.json_values (id, details) FROM stdin;
1	{"name": "Carol", "secret": "topsecret"}
\.

-- Scenario: json-delete_missing_key_is_noop
CREATE SCHEMA json_delete_missing_key_is_noop;
CREATE TABLE json_delete_missing_key_is_noop.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_delete_missing_key_is_noop.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"ghost": [{"mutation_name": "delete", "mutation_kwargs": {}}]}}}]';
COPY json_delete_missing_key_is_noop.json_values (id, details) FROM stdin;
1	{"name": "Dave"}
\.

-- Scenario: json-null_existing_key
CREATE SCHEMA json_null_existing_key;
CREATE TABLE json_null_existing_key.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_null_existing_key.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"notes": [{"mutation_name": "null"}]}}}]';
COPY json_null_existing_key.json_values (id, details) FROM stdin;
1	{"name": "Eve", "notes": "some private notes"}
\.

-- Scenario: json-null_missing_key_adds_null
CREATE SCHEMA json_null_missing_key_adds_null;
CREATE TABLE json_null_missing_key_adds_null.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_null_missing_key_adds_null.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"notes": [{"mutation_name": "null", "mutation_kwargs": {}}]}}}]';
COPY json_null_missing_key_adds_null.json_values (id, details) FROM stdin;
1	{"name": "Frank"}
\.

-- Scenario: json-invalid_json_raises
CREATE SCHEMA json_invalid_json_raises;
CREATE TABLE json_invalid_json_raises.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_invalid_json_raises.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "first_name", "mutation_kwargs": {}}]}}}]';
COPY json_invalid_json_raises.json_values (id, details) FROM stdin;
1	not-json-at-all
\.

-- Scenario: json-json_array_passthrough
CREATE SCHEMA json_json_array_passthrough;
CREATE TABLE json_json_array_passthrough.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_json_array_passthrough.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "first_name", "mutation_kwargs": {}}]}}}]';
COPY json_json_array_passthrough.json_values (id, details) FROM stdin;
1	[1, 2, 3]
\.

-- Scenario: json-json_scalar_passthrough
CREATE SCHEMA json_json_scalar_passthrough;
CREATE TABLE json_json_scalar_passthrough.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_json_scalar_passthrough.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "first_name", "mutation_kwargs": {}}]}}}]';
COPY json_json_scalar_passthrough.json_values (id, details) FROM stdin;
1	42
\.

-- Scenario: json-postgres_null_passthrough
CREATE SCHEMA json_postgres_null_passthrough;
CREATE TABLE json_postgres_null_passthrough.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_postgres_null_passthrough.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"name": [{"mutation_name": "first_name", "mutation_kwargs": {}}]}}}]';
COPY json_postgres_null_passthrough.json_values (id, details) FROM stdin;
1	\N
\.

-- Scenario: json-combined_operations
CREATE SCHEMA json_combined_operations;
CREATE TABLE json_combined_operations.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_combined_operations.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"first_name": [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "John"}}], "secret": [{"mutation_name": "delete", "mutation_kwargs": {}}], "notes": [{"mutation_name": "null", "mutation_kwargs": {}}]}}}]';
COPY json_combined_operations.json_values (id, details) FROM stdin;
1	{"first_name": "Alice", "secret": "topsecret", "notes": "private", "untouched": "keep me"}
\.

-- Scenario: json-unknown_mutation_raises
CREATE SCHEMA json_unknown_mutation_raises;
CREATE TABLE json_unknown_mutation_raises.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_unknown_mutation_raises.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"key": [{"mutation_name": "nonexistent", "mutation_kwargs": {}}]}}}]';
COPY json_unknown_mutation_raises.json_values (id, details) FROM stdin;
1	{"key": "value"}
\.

-- Scenario: json-applies_mutations_recursively
CREATE SCHEMA json_applies_mutations_recursively;
CREATE TABLE json_applies_mutations_recursively.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_applies_mutations_recursively.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"phone": [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "MASKED"}}]}}}]';
COPY json_applies_mutations_recursively.json_values (id, details) FROM stdin;
1	{"profile": {"phone": "+70000000001"}, "contacts": [{"phone": "+70000000002"}, {"phone": "+70000000003"}]}
\.

-- Scenario: json-key_name_can_be_current_value
CREATE SCHEMA json_key_name_can_be_current_value;
CREATE TABLE json_key_name_can_be_current_value.json_values ("id" text, "details" text);
COMMENT ON COLUMN json_key_name_can_be_current_value.json_values.details IS 'anon: [{"mutation_name": "json_update", "mutation_kwargs": {"mutations_by_key": {"current_value": [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "safe"}}]}}}]';
COPY json_key_name_can_be_current_value.json_values (id, details) FROM stdin;
1	{"current_value": "sensitive"}
\.

-- Scenario: typed_restore. Native types and constraints validate the obfuscated dump.
CREATE SCHEMA typed_restore;
CREATE TABLE typed_restore.users (
    id uuid PRIMARY KEY,
    email text NOT NULL CHECK (position('@' in email) > 1),
    birthday date NOT NULL,
    details jsonb NOT NULL CHECK (details ? 'secret'),
    salt text
);
CREATE TABLE typed_restore.orders (
    id integer PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES typed_restore.users(id),
    amount numeric(10,2) NOT NULL CHECK (amount > 0)
);
COMMENT ON COLUMN typed_restore.users.email IS 'anon: [{"mutation_name":"email"}]';
COMMENT ON COLUMN typed_restore.users.birthday IS 'anon: [{"mutation_name":"date","mutation_kwargs":{"start":2000,"end":2024}}]';
COMMENT ON COLUMN typed_restore.users.details IS 'anon: [{"mutation_name":"json_update","mutation_kwargs":{"mutations_by_key":{"secret":[{"mutation_name":"fixed_value","mutation_kwargs":{"value":"hidden"}}]}}}]';
COMMENT ON COLUMN typed_restore.users.salt IS 'anon: [{"mutation_name":"null"}]';
INSERT INTO typed_restore.users VALUES
('07750c56-fb37-46e1-b7b6-da530704c056', 'private@example.com', '1990-01-01', '{"secret":"private","untouched":42}', 'private-salt');
INSERT INTO typed_restore.orders VALUES (1, '07750c56-fb37-46e1-b7b6-da530704c056', 12.50);
