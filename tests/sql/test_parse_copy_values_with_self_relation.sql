COMMENT ON COLUMN table_1.first_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "table_1", "column_name": "last_name", "from_column_name": "id", "to_column_name": "id"}]}]';
COMMENT ON COLUMN table_1.last_name IS 'anon: [{"mutation_name": "last_name", "relations": [{"table_name": "table_1", "column_name": "first_name", "from_column_name": "id", "to_column_name": "id"}]}]';
COPY table_1 (id, first_name, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	111n
20f654fe-b27d-4051-9fd4-000000000002	222n	222n
\.