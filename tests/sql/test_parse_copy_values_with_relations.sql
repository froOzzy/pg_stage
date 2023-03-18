COMMENT ON COLUMN table_1.first_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "table_2", "column_name": "f_name", "from_column_name": "id", "to_column_name": "uuid"}, {"table_name": "table_3", "column_name": "fir_name", "from_column_name": "id", "to_column_name": "identifier"}]}]';
COPY table_1 (id, first_name, last_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.

COMMENT ON COLUMN table_2.f_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "table_1", "column_name": "first_name", "from_column_name": "uuid", "to_column_name": "id"}, {"table_name": "table_3", "column_name": "fir_name", "from_column_name": "uuid", "to_column_name": "identifier"}]}]';
COPY table_2 (uuid, f_name, l_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.

COMMENT ON COLUMN table_3.fir_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "table_1", "column_name": "first_name", "from_column_name": "identifier", "to_column_name": "id"}, {"table_name": "table_2", "column_name": "f_name", "from_column_name": "identifier", "to_column_name": "uuid"}]}]';
COPY table_3 (identifier, fir_name, las_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.


COPY table_4 (identifier, fir_name, las_name) FROM stdin;
20f654fe-b27d-4051-9fd4-000000000001	111n	Lourense
20f654fe-b27d-4051-9fd4-000000000002	222n	Kent
\.
