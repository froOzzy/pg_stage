from typing import List, Callable, Any, Dict
from enum import Enum

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
    mutation_func: Callable[..., str]
    mutation_kwargs: Dict[str, Any]
    mutation_relations: RelationTypeMany
    mutation_conditions: ConditionTypeMany


MapTablesValueTypeMany = List[MapTablesValueType]
