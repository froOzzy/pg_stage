COMMENT ON COLUMN table_1.username IS 'anon: [{"mutation_name": "phone_number", "mutation_kwargs": {"mask": "791########", "unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^7[0-9]{10}$"}]}]';
COMMENT ON COLUMN table_1.uuid IS 'anon: [{"mutation_name": "uuid5_by_source_value", "mutation_kwargs": {"source_column": "username", "namespace": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';
COPY table_1 (uuid, username, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	79999999999	111n
20f654fe-b27d-4051-9fd4-000000000002	79888888888	222n
20f654fe-b27d-4051-9fd4-000000000003	79777777777	333n
\.