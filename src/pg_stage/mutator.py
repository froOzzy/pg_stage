import random
from typing import Any, List

from faker import Faker


class Mutator:
    """Класс с описанием основных методов для мутации значений полей."""

    min_value_smallint = -32768
    max_value_smallint = -32767
    min_value_integer = -2147483648
    max_value_integer = 2147483647
    min_value_bigint = -9223372036854775808
    max_value_bigint = 9223372036854775807
    min_value_smallserial = 1
    max_value_smallserial = 32767
    min_value_serial = 1
    max_value_serial = 2147483647
    min_value_bigserial = 1
    max_value_bigserial = 9223372036854775807

    def __init__(self, locale: str = 'en_US') -> None:
        """
        Метод инициализации класса.
        :param locale:  локализация для Faker
        """
        self._faker = Faker(locale=locale)

    def mutation_email(self, **kwargs: bool) -> str:
        """
        Метод для генерации email-а.
        :param kwargs:
            unique - сгенерировать уникальный email
        :return: email
        """
        if kwargs.get('unique'):
            return self._faker.unique.email()

        return self._faker.email()

    @staticmethod
    def mutation_empty_string(**_: Any) -> str:
        """
        Метод для создания пустой строки.
        :param _: параметры генерации (не используются)
        :return: пустая строка
        """
        return ''

    @staticmethod
    def mutation_fixed_value(**kwargs: Any) -> str:
        """
        Метод для вставки значения из параметров.
        :param kwargs:
            value - значение, которое необходимо вернуть
        :return: строка со значением
        """
        return str(kwargs['value'])

    def mutation_full_name(self, **kwargs: bool) -> str:
        """
        Метод для генерации ФИО.
        :param kwargs:
            unique - сгенерировать уникальное ФИО
        :return: ФИО
        """
        if kwargs.get('unique'):
            return self._faker.unique.name()

        return self._faker.name()

    def mutation_first_name(self, **kwargs: bool) -> str:
        """
        Метод для генерации имени.
        :param kwargs:
            unique - сгенерировать уникальное имя
        :return: имя
        """
        if kwargs.get('unique'):
            return self._faker.unique.first_name()

        return self._faker.first_name()

    def mutation_middle_name(self, **kwargs: bool) -> str:
        """
        Метод для генерации отчества (работает только с ru_RU).
        :param kwargs:
            unique - сгенерировать уникальное отчество
        :return: отчество
        """
        if kwargs.get('unique'):
            return self._faker.unique.middle_name()

        return self._faker.middle_name()

    def mutation_last_name(self, **kwargs: bool) -> str:
        """
        Метод для генерации фамилии.
        :param kwargs:
            unique - сгенерировать уникальную фамилию
        :return: фамилия
        """
        if kwargs.get('unique'):
            return self._faker.unique.last_name()

        return self._faker.last_name()

    @staticmethod
    def mutation_null(**_: Any) -> str:
        """
        Метод для возвращения NULL значения.
        :param _: параметры генерации (не используются)
        :return: NULL
        """
        return '\\N'

    def mutation_phone_number(self, **kwargs: Any) -> str:
        """
        Метод для генерации номера телефона.
        :param kwargs:
            format - формат номера, например +7 (XXX) XXX XX XX
            unique - сгенерировать уникальный номер
        :return: номер телефона
        """
        phone_format: str = kwargs['format']
        unique: bool = kwargs.get('unique', False)
        if unique:
            return self._faker.unique.numerify(phone_format)

        return self._faker.numerify(phone_format)

    def mutation_address(self, **kwargs: bool) -> str:
        """
        Метод для генерации адреса.
        :param kwargs:
            unique - сгенерировать уникальный адрес
        :return: адрес
        """
        if kwargs.get('unique'):
            return self._faker.unique.address()

        return self._faker.address()

    def mutation_past_date(self, **kwargs: Any) -> str:
        """
        Метод для генерации даты в прошедшем времени.
        :param kwargs:
            start_date - самая ранняя допустимая дата в strtotime() формате, по умолчанию -30d
            date_format - формат даты, по умолчанию '%Y-%m-%d'
        :return: дата в прошедшем времени
        """
        start_date: str = kwargs.get('start_date', '-30d')
        date_format: str = kwargs.get('date_format', '%Y-%m-%d')
        unique: bool = kwargs.get('unique', False)
        if unique:
            return self._faker.unique.past_date(start_date=start_date).strftime(date_format)

        return self._faker.past_date(start_date=start_date).strftime(date_format)

    def mutation_future_date(self, **kwargs: Any) -> str:
        """
        Метод для генерации даты в будущем времени.
        :param kwargs:
            end_date - самая поздняя допустимая дата в strtotime() формате, по умолчанию +30d
            date_format - формат даты, по умолчанию '%Y-%m-%d'
        :return: дата в будущем времени
        """
        end_date: str = kwargs.get('end_date', '+30d')
        date_format: str = kwargs.get('date_format', '%Y-%m-%d')
        unique: bool = kwargs.get('unique', False)
        if unique:
            return self._faker.unique.future_date(end_date=end_date).strftime(date_format)

        return self._faker.future_date(end_date=end_date).strftime(date_format)

    def mutation_uri(self, **kwargs: Any) -> str:
        """
        Метод для генерации uri.
        :param kwargs:
            unique - сгенерировать уникальный uri
        :return: uri
        """
        max_length: int = kwargs.get('max_length', 2048)
        unique: bool = kwargs.get('unique', False)
        if unique:
            return self._faker.unique.uri()[:max_length]

        return self._faker.uri()[:max_length]

    def mutation_ipv4_public(self, **kwargs: bool) -> str:
        """
        Метод для генерации публичного ip-адреса 4 версии.
        :param kwargs:
            unique - сгенерировать уникальный ip-адрес
        :return: ip-адрес
        """
        if kwargs.get('unique'):
            return self._faker.unique.ipv4_public()

        return self._faker.ipv4_public()

    def mutation_ipv4_private(self, **kwargs: bool) -> str:
        """
        Метод для генерации приватного ip-адреса 4-й версии.
        :param kwargs:
            unique - сгенерировать уникальный ip-адрес
        :return: ip-адрес
        """
        if kwargs.get('unique'):
            return self._faker.unique.ipv4_private()

        return self._faker.ipv4_private()

    def mutation_ipv6(self, **kwargs: bool) -> str:
        """
        Метод для формирования ip-адреса 6-й версии.
        :param kwargs:
            unique - сгенерировать уникальный ip-адрес
        :return: ip-адрес
        """
        if kwargs.get('unique'):
            return self._faker.unique.ipv6()

        return self._faker.ipv6()

    @staticmethod
    def mutation_random_choice(**kwargs: List[Any]) -> str:
        """
        Метод для формирования случайного значения из списка
        :param kwargs:
            choices - список значений
        :return: случайное значение
        """
        choices = kwargs.get('choices', [])
        if not choices:
            raise ValueError('Key choices not found!')

        return str(random.choice(seq=choices))  # nosec

    def mutation_numeric_smallint(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата smallint
        :param kwargs:
            min_value - минимальное значение
            max_value - максимальное значение
        :return: случайное значение в пределах [min_value, max_value]
        """
        min_value = kwargs.get('min_value', self.min_value_smallint)
        max_value = kwargs.get('max_value', self.max_value_smallint)
        if min_value < self.min_value_smallint or max_value > self.max_value_smallint:
            raise ValueError(
                f'The min_value and max_value values must be between {self.min_value_smallint} '
                f'and {self.max_value_smallint}',
            )

        if kwargs.get('unique'):
            return str(self._faker.unique.random_int(min=min_value, max=max_value))

        return str(self._faker.random_int(min=min_value, max=max_value))

    def mutation_numeric_integer(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата int
        :param kwargs:
            min_value - минимальное значение
            max_value - максимальное значение
        :return: случайное значение в пределах [min_value, max_value]
        """
        min_value = kwargs.get('min_value', self.min_value_integer)
        max_value = kwargs.get('max_value', self.max_value_integer)
        if min_value < self.min_value_integer or max_value > self.max_value_integer:
            raise ValueError(
                f'The min_value and max_value values must be between {self.min_value_integer} '
                f'and {self.max_value_integer}',
            )

        if kwargs.get('unique'):
            return str(self._faker.unique.random_int(min=min_value, max=max_value))

        return str(self._faker.random_int(min=min_value, max=max_value))

    def mutation_numeric_bigint(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата bigint
        :param kwargs:
            min_value - минимальное значение
            max_value - максимальное значение
        :return: случайное значение в пределах [min_value, max_value]
        """
        min_value = kwargs.get('min_value', self.min_value_bigint)
        max_value = kwargs.get('max_value', self.max_value_bigint)
        if min_value < self.min_value_bigint or max_value > self.max_value_bigint:
            raise ValueError(
                f'The min_value and max_value values must be between {self.min_value_bigint} '
                f'and {self.max_value_bigint}',
            )

        if kwargs.get('unique'):
            return str(self._faker.unique.random_int(min=min_value, max=max_value))

        return str(self._faker.random_int(min=min_value, max=max_value))

    def mutation_numeric_decimal(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата decimal
        :param kwargs:
            left_digits - количество символов до запятой
            right_digits - количество символов после запятой
            min_value - минимальное значение
            max_value - максимальное значение
        :return: случайное значение в пределах [min_value, max_value]
        """
        left_digits = kwargs['left_digits']
        right_digits = kwargs['right_digits']
        min_value = kwargs['min_value']
        max_value = kwargs['max_value']
        if kwargs.get('unique'):
            return str(
                self._faker.unique.pydecimal(
                    left_digits=left_digits,
                    right_digits=right_digits,
                    min_value=min_value,
                    max_value=max_value,
                ),
            )

        return str(
            self._faker.pydecimal(
                left_digits=left_digits,
                right_digits=right_digits,
                min_value=min_value,
                max_value=max_value,
            ),
        )

    def mutation_numeric_real(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата real
        :param kwargs:
            left_digits - количество символов до запятой
            min_value - минимальное значение
            max_value - максимальное значение
        :return: случайное значение в пределах [min_value, max_value]
        """
        left_digits = kwargs['left_digits']
        min_value = kwargs['min_value']
        max_value = kwargs['max_value']
        if kwargs.get('unique'):
            return str(
                self._faker.unique.pydecimal(
                    left_digits=left_digits,
                    right_digits=6,
                    min_value=min_value,
                    max_value=max_value,
                ),
            )

        return str(
            self._faker.pydecimal(
                left_digits=left_digits,
                right_digits=6,
                min_value=min_value,
                max_value=max_value,
            ),
        )

    def mutation_numeric_double_precision(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата double precision
        :param kwargs:
            left_digits - количество символов до запятой
            right_digits - количество символов после запятой
            min_value - минимальное значение
            max_value - максимальное значение
        :return: случайное значение в пределах [min_value, max_value]
        """
        left_digits = kwargs['left_digits']
        min_value = kwargs['min_value']
        max_value = kwargs['max_value']
        if kwargs.get('unique'):
            return str(
                self._faker.unique.pydecimal(
                    left_digits=left_digits,
                    right_digits=15,
                    min_value=min_value,
                    max_value=max_value,
                ),
            )

        return str(
            self._faker.pydecimal(
                left_digits=left_digits,
                right_digits=15,
                min_value=min_value,
                max_value=max_value,
            ),
        )

    def mutation_numeric_smallserial(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата smallserial
        :param kwargs:
            min_value - минимальное значение
            max_value - максимальное значение
        :return: случайное значение в пределах [min_value, max_value]
        """
        min_value = kwargs.get('min_value', self.min_value_smallserial)
        max_value = kwargs.get('max_value', self.max_value_smallserial)
        if min_value < self.min_value_smallserial or max_value > self.max_value_smallserial:
            raise ValueError(
                f'The min_value and max_value values must be between {self.min_value_smallserial} '
                f'and {self.max_value_smallserial}',
            )

        if kwargs.get('unique'):
            return str(self._faker.unique.random_int(min=min_value, max=max_value))

        return str(self._faker.random_int(min=min_value, max=max_value))

    def mutation_numeric_serial(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата serial
        :param kwargs:
            min_value - минимальное значение
            max_value - максимальное значение
        :return: случайное значение в пределах [min_value, max_value]
        """
        min_value = kwargs.get('min_value', self.min_value_serial)
        max_value = kwargs.get('max_value', self.max_value_serial)
        if min_value < self.min_value_serial or max_value > self.max_value_serial:
            raise ValueError(
                f'The min_value and max_value values must be between {self.min_value_serial} '
                f'and {self.max_value_serial}',
            )

        if kwargs.get('unique'):
            return str(self._faker.unique.random_int(min=min_value, max=max_value))

        return str(self._faker.random_int(min=min_value, max=max_value))

    def mutation_numeric_bigserial(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата bigserial
        :param kwargs:
            min_value - минимальное значение
            max_value - максимальное значение
        :return: случайное значение в пределах [min_value, max_value]
        """
        min_value = kwargs.get('min_value', self.min_value_bigserial)
        max_value = kwargs.get('max_value', self.max_value_bigserial)
        if min_value < self.min_value_bigserial or max_value > self.max_value_bigserial:
            raise ValueError(
                f'The min_value and max_value values must be between {self.min_value_bigserial} '
                f'and {self.max_value_bigserial}',
            )

        if kwargs.get('unique'):
            return str(self._faker.unique.random_int(min=min_value, max=max_value))

        return str(self._faker.random_int(min=min_value, max=max_value))
