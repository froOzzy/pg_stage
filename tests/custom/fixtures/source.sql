CREATE TABLE public.users (id text, name text, email text, status text, token text, details text);
INSERT INTO public.users VALUES
    ('1', 'Алиса', 'alice@example.com', 'active', 'old-1', '{"secret":"private","keep":42}'),
    ('2', 'Борис', 'bob@example.com', 'inactive', 'old-2', '{"secret":"private","keep":43}');
COMMENT ON COLUMN public.users.name IS 'anon: [{"mutation_name":"random_choice","mutation_kwargs":{"choices":["hidden"]}}]';
COMMENT ON COLUMN public.users.email IS 'anon: [{"mutation_name":"random_choice","mutation_kwargs":{"choices":["masked@example.com"]},"conditions":[{"column_name":"status","operation":"equal","value":"active"}]}]';
COMMENT ON COLUMN public.users.token IS 'anon: [{"mutation_name":"uuid5_by_source_value","mutation_kwargs":{"source_column":"name","namespace":"6ba7b810-9dad-11d1-80b4-00c04fd430c8"}}]';
COMMENT ON COLUMN public.users.details IS 'anon: [{"mutation_name":"json_update","mutation_kwargs":{"mutations_by_key":{"secret":[{"mutation_name":"random_choice","mutation_kwargs":{"choices":["hidden"]}}]}}}]';

CREATE TABLE public.deleted (id text, secret text);
INSERT INTO public.deleted VALUES ('1', 'private');
COMMENT ON TABLE public.deleted IS 'anon: {"mutation_name":"delete"}';

CREATE TABLE public.related_a (id text, name text);
CREATE TABLE public.related_b (id text, name text);
INSERT INTO public.related_a VALUES ('1', 'private-a'), ('2', 'private-b');
INSERT INTO public.related_b VALUES ('1', 'private-c'), ('2', 'private-d');
COMMENT ON COLUMN public.related_a.name IS 'anon: [{"mutation_name":"random_choice","mutation_kwargs":{"choices":["shared"]},"relations":[{"table_name":"public.related_b","column_name":"name","from_column_name":"id","to_column_name":"id"}]}]';
COMMENT ON COLUMN public.related_b.name IS 'anon: [{"mutation_name":"random_choice","mutation_kwargs":{"choices":["different"]},"relations":[{"table_name":"public.related_a","column_name":"name","from_column_name":"id","to_column_name":"id"}]}]';

CREATE TABLE public.untouched (id text, value text);
INSERT INTO public.untouched VALUES ('1', E'кириллица\tтабуляция\nстрока'), ('2', NULL);
