from enum import Enum
from typing import Any, Callable, Dict, List, NamedTuple

from typing_extensions import TypedDict


class OperationChoices(Enum):
    """Описание видов операций"""

    equal = 'equal'
    not_equal = 'not_equal'
    by_pattern = 'by_pattern'


class ConditionType(TypedDict):
    """Описание типа условий для обфускации"""

    column_name: str
    operation: OperationChoices
    value: str


class RelationType(TypedDict):
    """Описание типа зависимых таблиц"""

    table_name: str
    column_name: str
    from_column_name: str
    to_column_name: str


ConditionTypeMany = List[ConditionType]
RelationTypeMany = List[RelationType]


class MapTablesValueType(TypedDict):
    """Описание типа значения карты таблиц"""

    mutation_name: str
    mutation_kwargs: Dict[str, Any]
    mutation_relations: RelationTypeMany
    mutation_conditions: ConditionTypeMany


MapTablesValueTypeMany = List[MapTablesValueType]


class PreparedRelation(NamedTuple):
    """Ключи и индекс одной связи, вычисленные при входе в COPY.

    source_key и target_key имеют формат «таблица:мутируемая_колонка» и адресуют
    кэш связей текущей и связанной таблиц. source_column/target_column — имена
    колонок соединения, source_index — позиция source_column в исходной COPY-строке.
    Индекс действителен только для порядка колонок, с которым подготовлена связь.
    """

    target_key: str
    target_column: str
    source_column: str
    source_index: int
    source_key: str


class PreparedMutation(NamedTuple):
    """План одной мутации для текущего COPY без поиска функции на каждой строке.

    config ссылается на исходную конфигурацию, которую обработчик не изменяет;
    relations хранит подготовленные ключи и индексы, mutation_func — связанную
    функцию текущего Mutator. Замена Mutator или конфигурации требует новой
    подготовки плана. NamedTuple не делает вложенные словари и списки неизменяемыми.
    """

    config: MapTablesValueType
    relations: List[PreparedRelation]
    mutation_func: Callable[..., Any]


Version = tuple[int, int, int]
DumpId = int
Offset = int
