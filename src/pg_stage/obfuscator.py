import re
import sys
import json
from collections import defaultdict
from typing import Optional, List, Set, Dict
from uuid import uuid4

from pg_stage.mutator import Mutator
from pg_stage.typing import ConditionTypeMany, MapTablesValueTypeMany


class Obfuscator:
    """Главный класс для работы с обфускатором."""

    copy_parse_pattern = r'COPY ([\d\w\_\.]+) \(([\w\W]+)\) FROM stdin;'
    comment_table_parse_pattern = r'COMMENT ON TABLE ([\d\w\_\.]*) IS \'anon: ([\w\W]*)\'\;'
    comment_column_parse_pattern = r'COMMENT ON COLUMN ([\d\w\_\.]+) IS \'anon: ([\w\W]*)\'\;'

    def __init__(
        self,
        delimiter: str = '\t',
        locale: str = 'en_US',
        delete_tables_by_pattern: Optional[List[str]] = None,
    ) -> None:
        """
        Метод инициализации класса.
        :param delimiter: разделитель
        :param locale: локализация для Faker
        :param delete_tables_by_pattern: список таблиц, которые нужно очистить по паттерну
        """
        self.delimiter = delimiter
        self.delete_tables_by_pattern: List[str] = delete_tables_by_pattern or []
        self._map_tables: Dict[str, Dict[str, MapTablesValueTypeMany]] = defaultdict(dict)
        self._mutator = Mutator(locale=locale)
        self._relation_values: Dict[str, str] = {}
        self._relation_fk: Dict[str, Dict[str, Dict[str, str]]] = defaultdict(dict)
        self._is_data: bool = False
        self._table_name: str = ''
        self._table_columns: List[str] = []
        self._enumerate_table_columns: Dict[str, int] = {}
        self._delete_tables: Set[str] = set()
        self._is_delete: bool = False

    def _prepare_variables(self, *, line: str) -> Optional[str]:
        """
        Метод для установки начальных значений основных переменных.
        :param line: строка sql
        :return: строка sql
        """
        self._is_data = False
        self._table_name = ''
        self._table_columns = []
        self._enumerate_table_columns = {}
        self._is_delete = False
        return line

    def _checking_conditions(self, *, conditions: ConditionTypeMany, table_values: List[str]) -> bool:
        """
        Метод для проверки условий обфускации.
        :param conditions: условия
        :param table_values: значения вставляемой строки из дампа
        :return: флаг об выполнение обфускации для столбца
        """
        if not conditions:
            return True

        flag = False
        for condition in conditions:
            if flag:
                break

            column_name = condition['column_name']
            operation = condition['operation']
            value = condition['value']

            column_value = table_values[self._enumerate_table_columns[column_name]]
            if operation == 'equal':
                flag = column_value == value
                continue

            if operation == 'not_equal':
                flag = column_value != value
                continue

            if operation == 'by_pattern':
                flag = re.search(pattern=value, string=column_value) is not None
                continue

            raise ValueError('Invalid condition operation')

        return flag

    def _parse_comment_column(self, *, line: str) -> str:
        """
        Метод для обработки комментария колонки для составления карты.
        :param line: строка sql
        :return: строка sql
        """
        result = re.search(pattern=self.comment_column_parse_pattern, string=line)
        if not result:
            return line

        try:
            mutations_params = json.loads(result.group(2))
        except ValueError:
            return line

        for mutation_param in mutations_params:
            mutation_name = mutation_param['mutation_name']
            mutation_func = getattr(self._mutator, f'mutation_{mutation_name}', None)
            if not mutation_func:
                raise ValueError(f'Not found mutation {mutation_name}.')

            try:
                table_name, column_name = result.group(1).split('.')
            except ValueError:
                schema, table_name, column_name = result.group(1).split('.')
                table_name = f'{schema}.{table_name}'

            self._map_tables[table_name].setdefault(column_name, [])
            self._map_tables[table_name][column_name].append(
                {
                    'mutation_name': mutation_name,
                    'mutation_func': mutation_func,
                    'mutation_kwargs': mutation_param.get('mutation_kwargs', {}),
                    'mutation_relations': mutation_param.get('relations', []),
                    'mutation_conditions': mutation_param.get('conditions', []),
                },
            )

        return line

    def _parse_comment_table(self, *, line: str) -> str:
        """
        Метод для обработки комментария таблицы.
        :param line: строка sql
        :return: строка sql
        """
        result = re.search(pattern=self.comment_table_parse_pattern, string=line)
        if not result:
            return line

        try:
            mutation_params = json.loads(result.group(2))
        except ValueError:
            return line

        mutation_name = mutation_params['mutation_name']
        if mutation_name == 'delete':
            self._delete_tables.add(result.group(1))

        return line

    def _prepared_data(self, *, line: str) -> Optional[str]:
        """
        Метод для обработки данных.
        :return: новая строка с данными
        """
        if self._is_delete:
            return None

        table_mutations_by_column = self._map_tables.get(self._table_name)
        if not table_mutations_by_column:
            return line

        result = []
        table_values = line.split(self.delimiter)
        for column_name, column_index in self._enumerate_table_columns.items():
            mutations_for_column = table_mutations_by_column.get(column_name)
            if not mutations_for_column:
                result.append(table_values[column_index])
                continue

            is_obfuscated = False
            len_mutations_for_column = len(mutations_for_column)
            for mutation_index, mutation_for_column in enumerate(mutations_for_column):
                if is_obfuscated:
                    break

                mutation_func = mutation_for_column['mutation_func']
                mutation_kwargs = mutation_for_column['mutation_kwargs']
                mutation_relations = mutation_for_column['mutation_relations']
                mutation_conditions = mutation_for_column['mutation_conditions']
                if not self._checking_conditions(conditions=mutation_conditions, table_values=table_values):
                    if mutation_index + 1 == len_mutations_for_column:
                        result.append(table_values[column_index])
                        break

                    continue

                if not mutation_relations:
                    is_obfuscated = True
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
                is_obfuscated = True

        return self.delimiter.join(result)

    def _parse_copy_values(self, *, line: str) -> Optional[str]:
        """
        Метод для обработки строк с COPY.
        :param line: строка sql
        :return: строка sql
        """

        result = re.search(pattern=self.copy_parse_pattern, string=line)
        if not result:
            return None

        self._table_name = result.group(1)
        self._table_columns = [item.strip() for item in result.group(2).split(',')]
        self._enumerate_table_columns = {column_name: index for index, column_name in enumerate(self._table_columns)}
        self._is_delete = self._table_name in self._delete_tables or any(
            re.search(pattern, self._table_name) for pattern in self.delete_tables_by_pattern
        )
        self._is_data = True
        return line

    def _parse_line(self, *, line: str) -> Optional[str]:
        """
        Метод для парсинга строки из дампа.
        :param line: строка sql
        :return: обработанная строка sql
        """
        if line.startswith('\\.'):
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

    def run(self, *, stdin=None) -> None:
        """
        Метод для запуска обфускации.
        :param stdin: поток, с которого приходит информация в виде строк sql
        """
        if not stdin:
            stdin = sys.stdin

        for line in stdin:
            new_line = self._parse_line(line=line.rstrip('\n'))
            if isinstance(new_line, str):
                sys.stdout.write(new_line + '\n')
