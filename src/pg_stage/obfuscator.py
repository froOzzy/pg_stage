import re
import sys
import json
from collections import defaultdict
from typing import Optional
from uuid import uuid4

from pg_stage.mutator import Mutator


class Obfuscator:
    """Главный класс для работы с обфускатором"""

    not_found_relation = 'Not found relation!'

    def __init__(self, delimiter: str = '\t', locale: str = 'en_US'):
        """Метод инициализации класса"""
        self.delimiter = delimiter
        self._map_tables = defaultdict(dict)
        self._mutator = Mutator(locale=locale)
        self._relation_values = {}
        self._relation_fk = defaultdict(dict)
        self._is_data = False
        self._table_name = None
        self._table_columns = []
        self._enumerate_table_columns = {}
        self._delete_tables = set()
        self._is_delete = False

    def _prepare_variables(self, line: str) -> Optional[str]:
        self._is_data = False
        self._table_name = None
        self._table_columns = []
        self._enumerate_table_columns = {}
        self._is_delete = False
        return line

    def _parse_comment_column(self, line: str) -> str:
        """
        Метод для обработки комментария колонки для составления карты
        :param line: строка sql
        """
        pattern_for_comment = r'COMMENT ON COLUMN ([\d\w\_\.]+) IS \'anon: ([\w\W]*)\'\;'
        result = re.search(pattern=pattern_for_comment, string=line)
        if not result:
            return line

        try:
            mutation_params = json.loads(result.group(2))
        except Exception:
            return line

        mutation_name = mutation_params['mutation_name']
        mutation_func = getattr(self._mutator, f'mutation_{mutation_name}', None)
        if not mutation_func:
            raise ValueError(f'Not found mutation {mutation_name}.')

        try:
            table_name, column_name = result.group(1).split('.')
        except ValueError:
            schema, table_name, column_name = result.group(1).split('.')
            table_name = f'{schema}.{table_name}'

        mutation_relations = mutation_params.get('relations', [])
        self._map_tables[table_name][column_name] = {
            'mutation_name': mutation_name,
            'mutation_func': mutation_func,
            'mutation_kwargs': mutation_params.get('mutation_kwargs', {}),
            'mutation_relations': mutation_relations,
        }
        return line

    def _parse_comment_table(self, line: str) -> str:
        """
        Метод для обработки комментария таблицы
        :param line: строка sql
        """
        pattern_for_comment = r'COMMENT ON TABLE ([\d\w\_\.]*) IS \'anon: ([\w\W]*)\'\;'
        result = re.search(pattern=pattern_for_comment, string=line)
        if not result:
            return line

        try:
            mutation_params = json.loads(result.group(2))
        except Exception:
            return line

        mutation_name = mutation_params['mutation_name']
        if mutation_name == 'delete':
            self._delete_tables.add(result.group(1))

        return line

    def _prepared_data(self, line: str) -> Optional[str]:
        """
        Метод для обработки данных
        :return: новая строка с данными
        """
        if self._is_delete:
            return None

        table_mutations_by_column = self._map_tables.get(self._table_name)
        if not table_mutations_by_column:
            return line

        result = []
        table_values = line.split(self.delimiter)
        for column_name, index in self._enumerate_table_columns.items():
            mutation_for_column = table_mutations_by_column.get(column_name)
            if not mutation_for_column:
                result.append(table_values[index])
                continue

            mutation_func = mutation_for_column['mutation_func']
            mutation_kwargs = mutation_for_column['mutation_kwargs']
            mutation_relations = mutation_for_column['mutation_relations']
            if not mutation_relations:
                result.append(mutation_func(**mutation_kwargs))
                continue

            new_value = None
            for mutation_relation in mutation_relations:
                key_table = f'{mutation_relation["table_name"]}:{mutation_relation["column_name"]}'
                from_column_name = mutation_relation['from_column_name']
                to_column_name = mutation_relation['to_column_name']
                relation_key_value = table_values[self._enumerate_table_columns[from_column_name]]
                relation_fk = self._relation_fk.get(key_table, {}).get(to_column_name, {}).get(relation_key_value)
                if not relation_fk:
                    continue

                new_value = self._relation_values.get(relation_fk)
                if new_value is None:
                    raise ValueError('Invalid relation fk!')

                break

            if new_value is None:
                relation_fk = str(uuid4())
                new_value = mutation_func(**mutation_kwargs)
                for mutation_relation in mutation_relations:
                    key_table = f'{self._table_name}:{column_name}'
                    from_column_name = mutation_relation['from_column_name']
                    relation_key_value = table_values[self._enumerate_table_columns[from_column_name]]
                    self._relation_fk[key_table].setdefault(from_column_name, {})
                    self._relation_fk[key_table][from_column_name][relation_key_value] = relation_fk

                self._relation_values[relation_fk] = new_value

            result.append(new_value)

        return self.delimiter.join(result)

    def _parse_copy_values(self, line: str) -> Optional[str]:
        """
        Метод для обработки строк с COPY
        :param line: строка sql
        """
        pattern = r'COPY ([\d\w\_\.]+) \(([\w\W]+)\) FROM stdin;'
        result = re.search(pattern=pattern, string=line)
        if not result:
            return

        self._table_name = result.group(1)
        self._table_columns = [item.strip() for item in result.group(2).split(',')]
        self._enumerate_table_columns = {column_name: index for index, column_name in enumerate(self._table_columns)}
        if self._table_name in self._delete_tables:
            self._is_delete = True

        self._is_data = True
        return line

    def _parse_line(self, line: str) -> Optional[str]:
        """Метод для парсинга строки из дампа"""
        if line.startswith('\.'):
            return self._prepare_variables(line=line)

        if self._is_data:
            return self._prepared_data(line=line)

        if line.startswith('COMMENT ON COLUMN'):
            return self._parse_comment_column(line=line)

        if line.startswith('COMMENT ON TABLE'):
            return self._parse_comment_table(line=line)

        if line.startswith('COPY'):
            return self._parse_copy_values(line=line)

        return line

    def execute(self, stdin=None) -> None:
        """Метод для выполнения обхода карты таблиц и выполнения фейка"""
        if not stdin:
            stdin = sys.stdin

        for line in stdin:
            new_line = self._parse_line(line=line)
            if isinstance(new_line, str):
                sys.stdout.write(new_line)
