"""Загрузить сценарии в PostgreSQL и сохранить неизменённый вывод pg_dump -Fp."""

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESTINATION = Path(__file__).resolve().parent / 'fixtures'
COPY = re.compile(r'COPY ([\w.]+) \(([^)]+)\) FROM stdin;')


def qualified(table):
    return table if '.' in table else f'public.{table}'


def literal(value):
    return "'" + value.replace("'", "''") + "'"


def table_seed(table, columns, rows, comments=()):
    ddl = ', '.join(f'"{column}" text' for column in columns)
    return (
        f'CREATE TABLE {table} ({ddl});\n'
        + '\n'.join(comments)
        + '\n'
        + f'COPY {table} ({", ".join(columns)}) FROM stdin;\n'
        + '\n'.join(rows)
        + '\n\\.\n'
    )


def column_comment(table, column, mutations):
    return f'COMMENT ON COLUMN {table}.{column} IS {literal("anon: " + json.dumps(mutations))};'


def legacy_seed(path):
    """Сохранить исходные сценарии, добавив DDL, схемы и недостающие nullable-поля."""
    sql = path.read_text()
    tables = {}
    for match in COPY.finditer(sql):
        tables[qualified(match[1])] = [column.strip() for column in match[2].split(',')]
    comments = []
    for line in sql.splitlines():
        if not line.startswith('COMMENT '):
            continue
        match = re.fullmatch(r"COMMENT ON (COLUMN|TABLE) ([\w.]+) IS 'anon: (.*)';", line)
        kind, target, config = match.groups()
        config = json.loads(config)
        if kind == 'COLUMN':
            table, column = target.rsplit('.', 1)
            table = qualified(table)
            if column not in tables[table]:
                tables[table].append(column)
            for mutation in config:
                for relation in mutation.get('relations', []):
                    relation['table_name'] = qualified(relation['table_name'])
            target = f'{table}.{column}'
        else:
            target = qualified(target)
        comments.append(f'COMMENT ON {kind} {target} IS {literal("anon: " + json.dumps(config))};')
    rows = {table: [] for table in tables}
    current = None
    for line in sql.splitlines():
        match = COPY.fullmatch(line)
        if match:
            current = qualified(match[1])
        elif line == '\\.':
            current = None
        elif current is not None:
            fields = line.split('\t')
            fields.extend(['\\N'] * (len(tables[current]) - len(fields)))
            rows[current].append('\t'.join(fields))
    return 'CREATE SCHEMA IF NOT EXISTS schema;\n' + ''.join(
        table_seed(
            table,
            columns,
            rows[table],
            [
                comment
                for comment in comments
                if comment.startswith((f'COMMENT ON COLUMN {table}.', f'COMMENT ON TABLE {table} '))
            ],
        )
        for table, columns in tables.items()
    )


def metadata_seed():
    sql = 'CREATE SCHEMA schema;\n'
    for schema in ('public', 'schema'):
        for table in ('plain_values', '_table'):
            sql += table_seed(f'{schema}.{table}', ['column_1', 'column_2'], ['1\tvalue'])
        for table, config in (
            ('null_column', 'anon: [{"mutation_name":"null"}]'),
            ('unknown_column', 'anon: [{"mutation_name":"not_found"}]'),
            ('invalid_column', 'anon: {\'mutation_name": "null"}'),
            ('deleted_table', 'anon: {"mutation_name":"delete"}'),
            ('kept_table', 'anon: {"mutation_name":"set"}'),
        ):
            target = f'{schema}.{table}'
            kind = 'COLUMN' if table.endswith('_column') else 'TABLE'
            subject = f'{target}.field_value' if kind == 'COLUMN' else target
            comment = f'COMMENT ON {kind} {subject} IS {literal(config)};'
            sql += table_seed(target, ['field_value'], ['value'], [comment])
    return sql


def regression_seeds():
    cases = {}
    for configured in (False, True):
        for relations in (False, True):
            kwargs = {'source_column': 'name'}
            if configured:
                kwargs.update(current_value='fixed', obfuscated_values={'name': 'configured'})
            mutation = {'mutation_name': 'echo', 'mutation_kwargs': kwargs}
            if relations:
                mutation['relations'] = [
                    {
                        'table_name': 'public.peers',
                        'column_name': 'value',
                        'from_column_name': 'id',
                        'to_column_name': 'id',
                    }
                ]
            cases[f'context-{int(configured)}-{int(relations)}'] = table_seed(
                'public.users',
                ['value', 'id', 'name'],
                ['first\t1\tAlice', 'second\t2\tBob'],
                [column_comment('public.users', 'value', [mutation])],
            )
    choice = {'mutation_name': 'random_choice', 'mutation_kwargs': {'choices': ['hidden']}}
    cases['original_conditions'] = table_seed(
        'public.users',
        ['id', 'status', 'email', 'notes', 'empty'],
        ['1\toriginal\tprivate\t\\N\t', '2\tother\tprivate\tliteral\\ttext\t'],
        [
            column_comment('public.users', 'status', [{**choice, 'mutation_kwargs': {'choices': ['changed']}}]),
            column_comment(
                'public.users',
                'email',
                [
                    {
                        **choice,
                        'conditions': [
                            {'column_name': 'status', 'operation': 'equal', 'value': 'original'},
                        ],
                    }
                ],
            ),
        ],
    ) + table_seed('public.zz_untouched', ['id', 'name'], ['3\toriginal'])
    for mutate in (False, True):
        comments = [
            column_comment(
                'public.users',
                'token',
                [
                    {
                        'mutation_name': 'uuid5_by_source_value',
                        'mutation_kwargs': {
                            'source_column': 'name',
                            'namespace': '6ba7b810-9dad-11d1-80b4-00c04fd430c8',
                        },
                    }
                ],
            )
        ]
        if mutate:
            comments.append(column_comment('public.users', 'name', [choice]))
        cases[f'source-{int(mutate)}'] = table_seed(
            'public.users',
            ['token', 'id', 'name', 'notes'],
            ['old-token\t1\toriginal\t\\N'],
            comments,
        )
    for first in ('source', 'target'):
        tables = {
            'source': 'public.a_source' if first == 'source' else 'public.b_source',
            'target': 'public.b_target' if first == 'source' else 'public.a_target',
        }
        seed = ''
        for alias, other, columns, source_columns, target_columns, rows in [
            (
                'source',
                'target',
                ['name', 'id', 'alternate_id'],
                ['id', 'alternate_id'],
                ['ref', 'alternate_ref'],
                ['Alice\t1\ta', 'Bob\t2\tb'],
            ),
            (
                'target',
                'source',
                ['alternate_ref', 'name', 'ref'],
                ['ref', 'alternate_ref'],
                ['id', 'alternate_id'],
                ['a\tCarol\tmissing-1', 'b\tDave\tmissing-2'],
            ),
        ]:
            mutation = {
                'mutation_name': 'first_name',
                'relations': [
                    {
                        'table_name': tables[other],
                        'column_name': 'name',
                        'from_column_name': source,
                        'to_column_name': target,
                    }
                    for source, target in zip(source_columns, target_columns)
                ],
            }
            seed += table_seed(tables[alias], columns, rows, [column_comment(tables[alias], 'name', [mutation])])
        cases[f'relations-{first}'] = seed
    return cases


def json_seeds():
    def mutation(name, **kwargs):
        return {'mutation_name': name, 'mutation_kwargs': kwargs}

    first_name = {'name': [mutation('first_name')]}
    cases = {
        'existing_key_is_replaced': ({'name': 'Alice', 'score': 42}, {'name': [mutation('fixed_value', value='John')]}),
        'existing_key_passes_current_value': (
            {'phone': '+70000000000', 'role': 'admin'},
            {'phone': [mutation('test_echo')]},
        ),
        'preserving_the_numeric_type': ({'score': 42}, {'score': [mutation('numeric_integer')]}),
        'missing_key_is_added': ({'name': 'Bob'}, {'email': [mutation('email')]}),
        'delete_existing_key': ({'name': 'Carol', 'secret': 'topsecret'}, {'secret': [mutation('delete')]}),
        'delete_missing_key_is_noop': ({'name': 'Dave'}, {'ghost': [mutation('delete')]}),
        'null_existing_key': ({'name': 'Eve', 'notes': 'some private notes'}, {'notes': [{'mutation_name': 'null'}]}),
        'null_missing_key_adds_null': ({'name': 'Frank'}, {'notes': [mutation('null')]}),
        'invalid_json_raises': ('not-json-at-all', first_name),
        'json_array_raises': ('[1, 2, 3]', first_name),
        'json_scalar_raises': ('42', first_name),
        'postgres_null_passthrough': (None, first_name),
        'combined_operations': (
            {'first_name': 'Alice', 'secret': 'topsecret', 'notes': 'private', 'untouched': 'keep me'},
            {
                'first_name': [mutation('fixed_value', value='John')],
                'secret': [mutation('delete')],
                'notes': [mutation('null')],
            },
        ),
        'unknown_mutation_raises': ({'key': 'value'}, {'key': [mutation('nonexistent')]}),
        'applies_mutations_recursively': (
            {'profile': {'phone': '+70000000001'}, 'contacts': [{'phone': '+70000000002'}, {'phone': '+70000000003'}]},
            {'phone': [mutation('fixed_value', value='MASKED')]},
        ),
        'key_name_can_be_current_value': (
            {'current_value': 'sensitive'},
            {'current_value': [mutation('fixed_value', value='safe')]},
        ),
    }
    seeds = {}
    for name, (value, mutations) in cases.items():
        data = '\\N' if value is None else json.dumps(value) if isinstance(value, dict) else value
        comment = column_comment(
            'public.json_values',
            'details',
            [
                {
                    'mutation_name': 'json_update',
                    'mutation_kwargs': {'mutations_by_key': mutations},
                }
            ],
        )
        seeds[f'json-{name}'] = table_seed('public.json_values', ['id', 'details'], [f'1\t{data}'], [comment])
    return seeds


def generate(expected_major, selected_cases=None):
    version = subprocess.check_output(['pg_dump', '--version'], text=True)
    detected = re.search(r'(\d+)\.', version)
    if detected is None or int(detected.group(1)) != expected_major:
        message = f'Unexpected pg_dump version: {version.strip()} (expected {expected_major})'
        raise ValueError(message)
    destination = DESTINATION / f'pg{expected_major}'
    destination.mkdir(parents=True, exist_ok=True)
    seeds = {path.stem: legacy_seed(path) for path in sorted((ROOT / 'tests' / 'sql').glob('test_*.sql'))}
    seeds.update(metadata=metadata_seed(), **regression_seeds(), **json_seeds())
    if selected_cases:
        unknown = set(selected_cases) - seeds.keys()
        if unknown:
            message = f'Unknown fixture cases: {sorted(unknown)}'
            raise ValueError(message)
        seeds = {case: seeds[case] for case in selected_cases}
    with tempfile.TemporaryDirectory(prefix='pg-stage-plain-') as directory:
        root = Path(directory)
        cluster = root / 'data'
        subprocess.run(
            [
                'initdb',
                '-D',
                str(cluster),
                '-U',
                'fixture',
                '--auth-local=trust',
                '--auth-host=reject',
                '--no-locale',
                '--encoding=UTF8',
            ],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                'pg_ctl',
                '-D',
                str(cluster),
                '-l',
                str(root / 'postgres.log'),
                '-o',
                f"-F -h '' -k {root} -p 55432",
                '-w',
                'start',
            ],
            check=True,
            capture_output=True,
        )
        connection = ['-h', str(root), '-p', '55432', '-U', 'fixture']
        try:
            for index, (case, seed) in enumerate(seeds.items()):
                database = f'case_{index}'
                subprocess.run(['createdb', *connection, database], check=True, capture_output=True)
                subprocess.run(
                    ['psql', *connection, '-d', database, '-v', 'ON_ERROR_STOP=1'],
                    input=seed,
                    text=True,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    [
                        'pg_dump',
                        *connection,
                        '-d',
                        database,
                        '-Fp',
                        '--no-owner',
                        '--no-privileges',
                        '-f',
                        str(destination / f'{case}.sql'),
                    ],
                    check=True,
                )
                subprocess.run(['dropdb', *connection, database], check=True, capture_output=True)
        finally:
            subprocess.run(['pg_ctl', '-D', str(cluster), '-m', 'immediate', '-w', 'stop'], check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-major', type=int, choices=(15, 16, 17, 18), required=True)
    parser.add_argument('--case', action='append', help='Regenerate only selected cases')
    args = parser.parse_args()
    generate(args.expected_major, args.case)
