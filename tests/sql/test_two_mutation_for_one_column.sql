COMMENT ON COLUMN table_1.username IS 'anon: [{"mutation_name": "phone_number", "mutation_kwargs": {"mask": "790########", "unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^7[0-9]{10}$"}, {"column_name": "username", "operation": "by_pattern", "value": "^8[0-9]{10}$"}]}, {"mutation_name": "email", "mutation_kwargs": {"unique": true}, "conditions": [{"column_name": "username", "operation": "by_pattern", "value": "^\\S+@\\S+\\.\\S+$"}]}]';
COPY table_1 (id, username, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	79999999999	111n
20f654fe-b27d-4051-9fd4-000000000002	test@mail.ru	222n
20f654fe-b27d-4051-9fd4-000000000003	89999999999	333n
\.