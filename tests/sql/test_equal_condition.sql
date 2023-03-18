COMMENT ON COLUMN table_1.email IS 'anon: [{"mutation_name": "email", "conditions": [{"column_name": "active", "operation": "equal", "value": "t"}]}]';
COPY table_1 (id, email, active) FROM stdin;
1	test@mail.ru	t
2	test@mail.ru	f
\.