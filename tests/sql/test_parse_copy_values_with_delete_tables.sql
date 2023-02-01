COMMENT ON TABLE table_1 IS 'anon: {"mutation_name": "delete"}';
COPY table_1 (id, message, recipient, notes) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	Hello -\nI'm writing in regards to the stuff I've been receiving. Double quotes are "awesome"!	support@example.com	\N
20f654fe-b27d-4051-9fd4-000000000002	Anything
\.

COMMENT ON TABLE schema.table_2 IS 'anon: {"mutation_name": "delete"}';
COPY schema.table_2 (id, message, recipient, notes) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	Hello -\nI'm writing in regards to the stuff I've been receiving. Double quotes are "awesome"!	support@example.com	\N
20f654fe-b27d-4051-9fd4-000000000002	Anything
\.
