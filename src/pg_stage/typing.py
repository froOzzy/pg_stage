from typing import List
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


ConditionTypeMany = List[ConditionType]
