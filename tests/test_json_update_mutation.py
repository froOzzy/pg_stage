import json

import pytest

from pg_stage.obfuscators.plain import PlainObfuscator
from src.pg_stage.mutator import Mutator
from tests.plain.helpers import copy_rows, obfuscate


@pytest.fixture()
def mutator() -> Mutator:
    return Mutator(locale='en')


@pytest.fixture
def plain_json(plain_dump, mutator, request):
    def run():
        case = 'json-' + request.node.originalname.removeprefix('test_json_update_')
        parser = PlainObfuscator()
        parser._mutator = mutator
        rows = copy_rows(obfuscate(parser, plain_dump.read(case)))['public.json_values']
        assert len(rows) == 1
        fields = rows[0].split('\t')
        assert len(fields) == 2 and fields[0] == '1'
        return fields[1]

    return run


# ---------------------------------------------------------------------------
# Обновление существующего ключа
# ---------------------------------------------------------------------------


def test_json_update_existing_key_is_replaced(mutator: Mutator, plain_json) -> None:
    """
    Arrange: JSON с ключом `name`; мутация fixed_value заменяет его на заданное значение
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: значение `name` изменилось, остальные ключи не тронуты
    """
    result = json.loads(plain_json())

    assert result['name'] == 'John'  # nosec
    assert isinstance(result['name'], str) and result['name']  # nosec
    assert result['score'] == 42  # nosec


def test_json_update_existing_key_passes_current_value(
    mutator: Mutator, plain_json, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Arrange: JSON с ключом `phone`; подменяем внутреннюю мутацию,
             чтобы она возвращала значение на основе current_value
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: во внутреннюю мутацию автоматически передано текущее значение ключа
    """

    def fake_mutation(*, current_value: str, **kwargs) -> str:
        return f'masked:{current_value}'

    monkeypatch.setattr(
        mutator,
        'mutation_test_echo',
        fake_mutation,
        raising=False,
    )

    result = json.loads(plain_json())

    assert result['phone'] == 'masked:+70000000000'
    assert result['role'] == 'admin'


def test_json_update_preserving_the_numeric_type(mutator: Mutator, plain_json) -> None:
    """
    Arrange: JSON с числовым ключом `score`
    Act: обфускация реального дампа с numeric_integer внутри json_update
    Assert: исходный числовой тип ключа `score` сохранится
    """
    result = json.loads(plain_json())

    assert isinstance(result['score'], int)


# ---------------------------------------------------------------------------
# Добавление отсутствующего ключа
# ---------------------------------------------------------------------------


def test_json_update_missing_key_is_added(mutator: Mutator, plain_json) -> None:
    """
    Arrange: JSON не содержит ключа `email`; мутация применяет к нему email
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: ключ `email` появился в результате
    """
    result = json.loads(plain_json())

    assert 'email' in result  # nosec
    assert '@' in result['email']  # nosec
    assert result['name'] == 'Bob'  # nosec


# ---------------------------------------------------------------------------
# Удаление ключа (mutation_name: delete)
# ---------------------------------------------------------------------------


def test_json_update_delete_existing_key(mutator: Mutator, plain_json) -> None:
    """
    Arrange: JSON с ключом `secret`; мутация delete
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: ключ `secret` отсутствует в результате, остальные нетронуты
    """
    result = json.loads(plain_json())

    assert 'secret' not in result  # nosec
    assert result['name'] == 'Carol'  # nosec


def test_json_update_delete_missing_key_is_noop(mutator: Mutator, plain_json) -> None:
    """
    Arrange: JSON не содержит ключа `ghost`; мутация delete
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: ошибок нет, JSON не изменился
    """
    result = json.loads(plain_json())

    assert result == {'name': 'Dave'}  # nosec


# ---------------------------------------------------------------------------
# Обнуление ключа (mutation_name: null)
# ---------------------------------------------------------------------------


def test_json_update_null_existing_key(mutator: Mutator, plain_json) -> None:
    """
    Arrange: JSON с ключом `notes`; мутация null
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: значение `notes` стало JSON null (Python None)
    """
    result = json.loads(plain_json())

    assert result['notes'] is None  # nosec
    assert result['name'] == 'Eve'  # nosec


def test_json_update_null_missing_key_adds_null(mutator: Mutator, plain_json) -> None:
    """
    Arrange: JSON не содержит ключа `notes`; мутация null
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: ключ `notes` добавлен со значением null
    """
    result = json.loads(plain_json())

    assert 'notes' in result  # nosec
    assert result['notes'] is None  # nosec


# ---------------------------------------------------------------------------
# Некорректный / не-объектный JSON
# ---------------------------------------------------------------------------


def test_json_update_invalid_json_raises(mutator: Mutator, plain_json) -> None:
    """
    Arrange: реальный дамп с невалидной JSON-строкой в текстовом поле
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: поднимается ValueError с понятным сообщением
    """
    with pytest.raises(ValueError, match='Invalid JSON value'):
        plain_json()


def test_json_update_json_array_raises(mutator: Mutator, plain_json) -> None:
    """
    Arrange: current_value — JSON-массив, а не объект
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: значение проходит без изменений
    """
    result = plain_json()

    # Non-dict JSON is passed through unchanged (warning logged)
    assert result == '[1, 2, 3]'


def test_json_update_json_scalar_raises(mutator: Mutator, plain_json) -> None:
    """
    Arrange: current_value — JSON-скаляр (число)
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: значение проходит без изменений
    """
    result = plain_json()

    # JSON scalar is passed through unchanged (warning logged)
    assert result == '42'


# ---------------------------------------------------------------------------
# NULL-значение из БД (PostgreSQL \N)
# ---------------------------------------------------------------------------


def test_json_update_postgres_null_passthrough(mutator: Mutator, plain_json) -> None:
    """
    Arrange: current_value равен PostgreSQL NULL (\\N)
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: возвращается \\N без изменений и без ошибок
    """
    result = plain_json()

    assert result == '\\N'  # nosec


# ---------------------------------------------------------------------------
# Комбинированные сценарии
# ---------------------------------------------------------------------------


def test_json_update_combined_operations(mutator: Mutator, plain_json) -> None:
    """
    Arrange: JSON с несколькими ключами; одновременно замена, удаление и обнуление
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: каждая операция применена независимо и корректно
    """
    result = json.loads(plain_json())

    assert result['first_name'] == 'John'  # nosec
    assert 'secret' not in result  # nosec
    assert result['notes'] is None  # nosec
    assert result['untouched'] == 'keep me'  # nosec


def test_json_update_unknown_mutation_raises(mutator: Mutator, plain_json) -> None:
    """
    Arrange: mutation_kwargs указывает несуществующую мутацию
    Act: обфускация реального plain-дампа через PlainObfuscator.run
    Assert: поднимается ValueError с именем мутации в сообщении
    """
    with pytest.raises(ValueError, match='Not found mutation "nonexistent"'):
        plain_json()


def test_json_update_applies_mutations_recursively(mutator: Mutator, plain_json) -> None:
    """
    Arrange: целевой ключ находится в nested dict и в dict внутри списка.
    Act: обрабатываем реальный plain-дамп с мутацией json_update.
    Assert: мутация применена ко всем совпавшим ключам рекурсивно.
    """

    result = json.loads(plain_json())

    assert result['profile']['phone'] == 'MASKED'
    assert result['contacts'][0]['phone'] == 'MASKED'
    assert result['contacts'][1]['phone'] == 'MASKED'


def test_json_update_key_name_can_be_current_value(mutator: Mutator, plain_json) -> None:
    """
    Arrange: в JSON есть ключ с именем current_value.
    Act: обрабатываем реальный plain-дамп с mutations_by_key.
    Assert: ключ не конфликтует со служебными параметрами вызова.
    """
    result = json.loads(plain_json())

    assert result['current_value'] == 'safe'
