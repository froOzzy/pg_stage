"""Проверка реального восстановления после обфускации, включая типы и ограничения."""

from pg_stage.obfuscators.plain import PlainObfuscator
from tests.helpers import obfuscate


def test_obfuscated_dump_restores_with_types_and_constraints(postgres, plain_dump) -> None:
    """
    Arrange: Реальный дамп с UUID, date, JSONB, числом, PK, FK и CHECK
    Act: Обфускация через публичный run и восстановление результата в пустую PostgreSQL-базу
    Assert: Восстановление успешно, секреты заменены, типы, связь и прочие значения сохранены
    """
    original = plain_dump.read('typed_restore')
    result = obfuscate(PlainObfuscator(), original)
    assert result != original
    postgres.create_database('obfuscated_restore')
    postgres.sql('obfuscated_restore', result)
    values = postgres.sql(
        'obfuscated_restore',
        """
        SELECT u.email <> 'private@example.com',
               u.birthday BETWEEN DATE '2000-01-01' AND DATE '2024-12-31',
               u.details = '{"secret":"hidden","untouched":42}'::jsonb,
               u.salt IS NULL, o.amount = 12.50
        FROM typed_restore.users u JOIN typed_restore.orders o ON o.user_id = u.id;
    """,
    )
    assert values.strip() == 't|t|t|t|t'
