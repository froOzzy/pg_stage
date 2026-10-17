import json
from typing import Any, Callable, Optional


def get_mutation_func(*, mutation_owner: Any, mutation_name: str) -> Callable[..., Any]:
    """
    Метод для получения callable мутации по имени из объекта
    :param mutation_owner: объект, содержащий методы mutation_<name>
    :param mutation_name: название мутации (без префикса 'mutation_')
    :return: callable функция мутации
    """
    mutation_func = getattr(mutation_owner, f'mutation_{mutation_name}', None)
    if not mutation_func:
        msg = f'Not found mutation "{mutation_name}"'
        raise ValueError(msg)
    return mutation_func


def extract_mutation_kwargs(*, mutation_config: dict[str, Any]) -> dict[str, Any]:
    """
    Метод для получения kwargs из конфигурации мутации.
    :param mutation_config: словарь конфигурации мутации
    :return: словарь kwargs для передачи в функцию мутации
    """
    mutation_kwargs = mutation_config.get('mutation_kwargs')
    if mutation_kwargs is None:
        msg = 'mutation_kwargs is required in mutation config'
        raise ValueError(msg)
    if not isinstance(mutation_kwargs, dict):
        msg = 'mutation_kwargs must be an object (dict)'
        raise ValueError(msg)
    return mutation_kwargs


def run_mutation(
    *,
    mutation_owner: Any,
    mutation_name: str,
    mutation_kwargs: Optional[dict[str, Any]] = None,
    current_value: Any = None,
    obfuscated_values: Optional[dict[str, Any]] = None,
    mutation_func: Optional[Callable[..., Any]] = None,
) -> Any:
    """
    Выполнить мутацию с контекстом строки, сохранив исходные параметры.

    Аргументы копируются поверхностно: явно заданные current_value и
    obfuscated_values имеют приоритет над runtime-контекстом. Если передана
    mutation_func, поиск по имени не выполняется; вызывающий код отвечает
    за соответствие подготовленной функции текущему Mutator и конфигурации.

    :param mutation_owner: объект, содержащий методы mutation_<name>
    :param mutation_name: название мутации (без префикса 'mutation_')
    :param mutation_kwargs: параметры мутации, опционально
    :param current_value: текущее значение поля, опционально
    :param obfuscated_values: словарь обфусцированных значений для cross-column операций, опционально
    :param mutation_func: заранее подготовленная функция мутации, опционально
    :return: результат применения мутации
    """
    call_kwargs: dict[str, Any] = dict(mutation_kwargs or {})
    call_kwargs.setdefault('current_value', current_value)
    if obfuscated_values is not None:
        call_kwargs.setdefault('obfuscated_values', obfuscated_values)

    if mutation_func is None:
        mutation_func = get_mutation_func(mutation_owner=mutation_owner, mutation_name=mutation_name)
    return mutation_func(**call_kwargs)


def normalize_json_current_value(value: Any) -> Any:
    """
    Метод для подготовки вложенного JSON-значения перед передачей в мутацию.
    Преобразует объекты в JSON-строку, сохраняя строки и None без изменений.
    :param value: значение для подготовки
    :return: подготовленное значение (строка или JSON)
    """
    if value is None or isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def restore_json_numeric_type(*, original_value: Any, new_value: Any) -> Any:
    """
    Метод для сохранения числовых типов после мутации.
    Преобразует результат обратно в int или float, если исходное значение было числом.
    :param original_value: исходное значение (для определения типа)
    :param new_value: новое значение после мутации
    :return: результат с восстановленным числовым типом
    """
    if isinstance(original_value, bool):
        return new_value

    if isinstance(original_value, int):
        try:
            return int(new_value)
        except (TypeError, ValueError):
            return new_value

    if isinstance(original_value, float):
        try:
            return float(new_value)
        except (TypeError, ValueError):
            return new_value

    return new_value


def apply_mutations_to_json_value(
    *,
    mutation_owner: Any,
    value: Any,
    key_mutations: list[dict[str, Any]],
    obfuscated_values: Optional[dict[str, Any]] = None,
) -> tuple[bool, Any]:
    """
    Метод для применения последовательности мутаций к одному JSON-значению.
    :param mutation_owner: объект, содержащий методы mutation_<name>
    :param value: текущее значение ключа
    :param key_mutations: список словарей с конфигурациями мутаций для применения подряд
    :param obfuscated_values: словарь обфусцированных значений для cross-column операций, опционально
    :return: кортеж (нужно_ли_удалить_ключ, новое_значение)
    """
    result_value = value
    for key_mutation in key_mutations:
        if not isinstance(key_mutation, dict):
            msg = f'Each mutation must be an object (dict), but got {type(key_mutation).__name__}'
            raise ValueError(msg)

        mutation_name: str = key_mutation.get('mutation_name', '')
        if not mutation_name:
            msg = 'mutation_name not specified for json key'
            raise ValueError(msg)

        if mutation_name == 'delete':
            return True, None

        if mutation_name == 'null':
            result_value = None
            continue

        mutation_kwargs = extract_mutation_kwargs(mutation_config=key_mutation)
        original_value = result_value
        new_value = run_mutation(
            mutation_owner=mutation_owner,
            mutation_name=mutation_name,
            mutation_kwargs=mutation_kwargs,
            current_value=normalize_json_current_value(result_value),
            obfuscated_values=obfuscated_values,
        )
        result_value = restore_json_numeric_type(original_value=original_value, new_value=new_value)

    return False, result_value
