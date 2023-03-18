COMMENT ON COLUMN table_1.email IS 'anon: [{"mutation_name": "email", "conditions": [{"column_name": "email", "operation": "by_pattern", "value": "\\w+\\@\\w+\\.\\w{2}"}]}]';
COPY table_1 (id, email, active) FROM stdin;
1	test@mail.ru	t
2	test@mail.ru	f
\.