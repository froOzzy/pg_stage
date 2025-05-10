import datetime
import random
import uuid
from typing import Any, Callable, List, Optional

from mimesis import Address, Datetime, Internet, Numbers, Person
from mimesis.builtins import RussiaSpecProvider


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

    def __init__(self, locale: str = 'en') -> None:
        """
        Метод инициализации класса.
        :param locale: локализация для Faker
        """
        self._locale = locale
        self._is_russian_locale = locale == 'ru'
        self._person = Person(locale=self._locale)
        self._address = Address(locale=self._locale)
        self._datetime = Datetime(locale=self._locale)
        self._internet = Internet()
        self._numeric = Numbers()
        self._russian_provider = RussiaSpecProvider()
        self._current_year = datetime.date.today().year
        self._now = datetime.datetime.now()
        self._today = self._now.date()
        self._cache = {}  # type: ignore
        self._unique_values = set()  # type: ignore

    def clear_unique_values(self) -> None:
        """Метод для сброса уникальных значений."""
        self._unique_values.clear()

    def _generate_unique_value(self, func: Callable[[Any], Any], *args: Any, **kwargs: Any) -> Any:
        """Метод для генерации уникального значения."""
        counter = 0
        while True:
            if counter > 1000:
                msg = 'Exceeded the number of attempts to generate a unique value!'
                raise RecursionError(msg)

            value = func(*args, **kwargs)
            if value not in self._unique_values:
                self._unique_values.add(value)
                break

            counter += 1

        return value

    @staticmethod
    def _random_int(a: int, b: int) -> int:
        b = b - a
        return int(random.random() * b) + a  # nosec

    def _generate_string_by_mask(self, mask: str, char: str = '@', digit: str = '#') -> str:
        """
        Метод для генерации строки по маске.
        :param mask: маска
        :param char: маска символов
        :param digit: маска цифр
        TODO: После обновления mimesis использовать mimesis.random.Random.generate_string_by_mask
        """
        char_code = ord(char)
        digit_code = ord(digit)

        if char_code == digit_code:
            msg = 'The same placeholder cannot be used for both numbers and characters'
            raise ValueError(msg)

        _mask = mask.encode()
        code = bytearray(len(_mask))
        for i, p in enumerate(_mask):
            if p == char_code:
                a = self._random_int(65, 91)  # A-Z
            elif p == digit_code:
                a = self._random_int(48, 58)  # 0-9
            else:
                a = p
            code[i] = a
        return code.decode()

    def mutation_email(self, **kwargs: bool) -> str:
        """
        Метод для генерации email-а.
        :param kwargs:
            unique - сгенерировать уникальный email
        :return: email
        """
        if kwargs.get('unique'):
            return self._generate_unique_value(func=self._person.email)

        return self._person.email()

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
            while True:
                if self._is_russian_locale:
                    value = f'{self._person.full_name(reverse=True)} {self._russian_provider.patronymic()}'
                else:
                    value = self._person.full_name(reverse=True)

                if not set(value) & self._unique_values:
                    self._unique_values.add(value)
                    break

            return value

        if self._is_russian_locale:
            return f'{self._person.full_name(reverse=True)} {self._russian_provider.patronymic()}'

        return self._person.full_name(reverse=True)

    def mutation_first_name(self, **kwargs: bool) -> str:
        """
        Метод для генерации имени.
        :param kwargs:
            unique - сгенерировать уникальное имя
        :return: имя
        """
        if kwargs.get('unique'):
            return self._generate_unique_value(func=self._person.name)

        return self._person.name()

    def mutation_middle_name(self, **kwargs: bool) -> str:
        """
        Метод для генерации отчества (работает только с ru_RU).
        :param kwargs:
            unique - сгенерировать уникальное отчество
        :return: отчество
        """
        if not self._is_russian_locale:
            msg = 'Mutation middle_name dont work not Russian locale!'
            raise ValueError(msg)

        if kwargs.get('unique'):
            return self._generate_unique_value(func=self._russian_provider.patronymic)

        return self._russian_provider.patronymic()

    def mutation_last_name(self, **kwargs: bool) -> str:
        """
        Метод для генерации фамилии.
        :param kwargs:
            unique - сгенерировать уникальную фамилию
        :return: фамилия
        """
        if kwargs.get('unique'):
            return self._generate_unique_value(func=self._person.surname)

        return self._person.surname()

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
            mask - формат номера, например +7 (XXX) XXX XX XX
            unique - сгенерировать уникальный номер
        :return: номер телефона
        """
        phone_format: str = kwargs['mask']
        unique: bool = kwargs.get('unique', False)
        if unique:
            return self._generate_unique_value(func=self._person.identifier, mask=phone_format)

        return self._person.identifier(mask=phone_format)

    def mutation_address(self, **kwargs: bool) -> str:
        """
        Метод для генерации адреса.
        :param kwargs:
            unique - сгенерировать уникальный адрес
        :return: адрес
        """
        if kwargs.get('unique'):
            return self._generate_unique_value(func=self._address.address)

        return self._address.address()

    def mutation_date(self, **kwargs: Any) -> str:
        """
        Метод для генерации даты между start и end годами.
        :param kwargs:
            start - год начала
            end - год окончания
            date_format - формат даты, по умолчанию '%Y-%m-%d'
        :return: дата в прошедшем времени
        """
        start: int = kwargs.get('start', self._now.year - 1)
        end: int = kwargs.get('end', self._now.year)
        date_format: int = kwargs.get('date_format', '%Y-%m-%d')
        unique: bool = kwargs.get('unique', False)
        if unique:
            return self._generate_unique_value(func=self._datetime.date, start=start, end=end).strftime(date_format)

        return self._datetime.date(start=start, end=end).strftime(date_format)

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
            return self._generate_unique_value(func=self._internet.home_page)[:max_length]

        return self._internet.home_page()[:max_length]

    def mutation_ipv4(self, **kwargs: bool) -> str:
        """
        Метод для генерации ip-адреса 4 версии.
        :param kwargs:
            unique - сгенерировать уникальный ip-адрес
        :return: ip-адрес
        """
        if kwargs.get('unique'):
            return self._generate_unique_value(func=self._internet.ip_v4)

        return self._internet.ip_v4()

    def mutation_ipv6(self, **kwargs: bool) -> str:
        """
        Метод для формирования ip-адреса 6-й версии.
        :param kwargs:
            unique - сгенерировать уникальный ip-адрес
        :return: ip-адрес
        """
        if kwargs.get('unique'):
            return self._generate_unique_value(func=self._internet.ip_v6)

        return self._internet.ip_v6()

    @staticmethod
    def mutation_random_choice(**kwargs: List[Any]) -> str:
        """
        Метод для формирования случайного значения из списка.
        :param kwargs:
            choices - список значений
        :return: случайное значение
        """
        choices = kwargs.get('choices', [])
        if not choices:
            msg = 'Key choices not found!'
            raise ValueError(msg)

        return str(random.choice(seq=choices))  # nosec

    def mutation_numeric_smallint(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата smallint.
        :param kwargs:
            start - минимальное значение
            end - максимальное значение
            unique - сгенерировать уникальное значение
        :return: случайное значение в пределах [start, end]
        """
        start = kwargs.get('start', self.min_value_smallint)
        end = kwargs.get('end', self.max_value_smallint)
        if start < self.min_value_smallint or end > self.max_value_smallint:
            msg = f'The start and end values must be between {self.min_value_smallint} and {self.max_value_smallint}.'
            raise ValueError(msg)

        if kwargs.get('unique'):
            return str(self._generate_unique_value(func=self._numeric.integer_number, start=start, end=end))

        return str(self._numeric.integer_number(start=start, end=end))

    def mutation_numeric_integer(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата int.
        :param kwargs:
            start - минимальное значение
            end - максимальное значение
            unique - сгенерировать уникальное значение
        :return: случайное значение в пределах [start, end]
        """
        start = kwargs.get('start', self.min_value_integer)
        end = kwargs.get('end', self.max_value_integer)
        if start < self.min_value_integer or end > self.max_value_integer:
            msg = f'The start and end values must be between {self.min_value_integer} and {self.max_value_integer}.'
            raise ValueError(msg)

        if kwargs.get('unique'):
            return str(self._generate_unique_value(func=self._numeric.integer_number, start=start, end=end))

        return str(self._numeric.integer_number(start=start, end=end))

    def mutation_numeric_bigint(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата bigint.
        :param kwargs:
            start - минимальное значение
            end - максимальное значение
            unique - сгенерировать уникальное значение
        :return: случайное значение в пределах [start, end]
        """
        start = kwargs.get('start', self.min_value_bigint)
        end = kwargs.get('end', self.max_value_bigint)
        if start < self.min_value_bigint or end > self.max_value_bigint:
            msg = f'The start and end values must be between {self.min_value_bigint} and {self.max_value_bigint}.'
            raise ValueError(msg)

        if kwargs.get('unique'):
            return str(self._generate_unique_value(func=self._numeric.integer_number, start=start, end=end))

        return str(self._numeric.integer_number(start=start, end=end))

    def mutation_numeric_decimal(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата decimal.
        :param kwargs:
            start - минимальное значение
            end - максимальное значение
            precision - количество символов после запятой
            unique - сгенерировать уникальное значение
        :return: случайное значение в пределах [start, end]
        """
        start = kwargs['start']
        end = kwargs['end']
        precision = kwargs['precision']
        if kwargs.get('unique'):
            return str(
                self._generate_unique_value(
                    func=self._numeric.float_number,
                    start=start,
                    end=end,
                    precision=precision,
                ),
            )

        return str(self._numeric.float_number(start=start, end=end, precision=precision))

    def mutation_numeric_real(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата real.
        :param kwargs:
            start - минимальное значение
            end - максимальное значение
            unique - сгенерировать уникальное значение
        :return: случайное значение в пределах [start, end]
        """
        start = kwargs['start']
        end = kwargs['end']
        if kwargs.get('unique'):
            return str(
                self._generate_unique_value(
                    func=self._numeric.float_number,
                    start=start,
                    end=end,
                    precision=6,
                ),
            )

        return str(self._numeric.float_number(start=start, end=end, precision=6))

    def mutation_numeric_double_precision(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата double precision.
        :param kwargs:
            start - минимальное значение
            end - максимальное значение
            unique - сгенерировать уникальное значение
        :return: случайное значение в пределах [start, end]
        """
        start = kwargs['start']
        end = kwargs['end']
        if kwargs.get('unique'):
            return str(
                self._generate_unique_value(
                    func=self._numeric.float_number,
                    start=start,
                    end=end,
                    precision=15,
                ),
            )

        return str(self._numeric.float_number(start=start, end=end, precision=15))

    def mutation_numeric_smallserial(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата smallserial.
        :param kwargs:
            start - минимальное значение
            end - максимальное значение
            unique - сгенерировать уникальное значение
        :return: случайное значение в пределах [start, end]
        """
        start = kwargs.get('start', self.min_value_smallserial)
        end = kwargs.get('end', self.max_value_smallserial)
        if start < self.min_value_smallserial or end > self.max_value_smallserial:
            msg = (
                f'The start and end values must be between {self.min_value_smallserial} '
                f'and {self.max_value_smallserial}.'
            )
            raise ValueError(msg)

        if kwargs.get('unique'):
            return str(self._generate_unique_value(func=self._numeric.integer_number, start=start, end=end))

        return str(self._numeric.integer_number(start=start, end=end))

    def mutation_numeric_serial(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата serial.
        :param kwargs:
            start - минимальное значение
            end - максимальное значение
            unique - сгенерировать уникальное значение
        :return: случайное значение в пределах [start, end]
        """
        start = kwargs.get('start', self.min_value_serial)
        end = kwargs.get('end', self.max_value_serial)
        if start < self.min_value_serial or end > self.max_value_serial:
            msg = f'The start and end values must be between {self.min_value_serial} and {self.max_value_serial}.'
            raise ValueError(msg)

        if kwargs.get('unique'):
            return str(self._generate_unique_value(func=self._numeric.integer_number, start=start, end=end))

        return str(self._numeric.integer_number(start=start, end=end))

    def mutation_numeric_bigserial(self, **kwargs: int) -> str:
        """
        Метод для формирования случайного числа формата bigserial.
        :param kwargs:
            start - минимальное значение
            end - максимальное значение
            unique - сгенерировать уникальное значение
        :return: случайное значение в пределах [start, end]
        """
        start = kwargs.get('start', self.min_value_bigserial)
        end = kwargs.get('end', self.max_value_bigserial)
        if start < self.min_value_bigserial or end > self.max_value_bigserial:
            msg = f'The start and end values must be between {self.min_value_bigserial} and {self.max_value_bigserial}.'
            raise ValueError(msg)

        if kwargs.get('unique'):
            return str(self._generate_unique_value(func=self._numeric.integer_number, start=start, end=end))

        return str(self._numeric.integer_number(start=start, end=end))

    def mutation_string_by_mask(self, **kwargs: Any) -> str:
        """
        Метод для формирования строки по маске.
        :param kwargs:
            mask - маска
            char - маска для символов
            digit - маска для цифр
            unique - сгенерировать уникальное значение
        """
        mask = kwargs['mask']
        char = kwargs.get('char', '@')
        digit = kwargs.get('digit', '#')
        if kwargs.get('unique'):
            return self._generate_unique_value(func=self._generate_string_by_mask, mask=mask, char=char, digit=digit)

        return self._generate_string_by_mask(mask=mask, char=char, digit=digit)

    @staticmethod
    def mutation_uuid4(**_: Any) -> str:
        """
        Метод для формирования uuid4
        :param kwargs: параметры мутации - не используются
        :return: строка uuid4
        """
        return str(uuid.uuid4())

    def mutation_uuid5_by_source_value(self, **kwargs: Any) -> str:
        """
        Метод для формирования uuid5 с использованием значения из указанной колонки,
        текущей даты и переданного uuid namespace.
        :param kwargs:
            source_column: название колонки, значение которой хотим использовать.
            namespace: uuid namespace.
        :return: строка uuid5.
        """
        source_column: Optional[str] = kwargs.get('source_column')
        if not source_column:
            msg = 'Argument "source_column" not found.'
            raise ValueError(msg)

        obfuscated_values: dict[str, Any] = kwargs.get('obfuscated_values', {})
        source_value: Optional[str] = obfuscated_values.get(source_column)
        if not source_value:
            msg = 'Value of "source_column" not found.'
            raise ValueError(msg)

        namespace: Optional[str] = kwargs.get('namespace')
        if namespace is None:
            msg = 'Argument "namespace" not found.'
            raise ValueError(msg)

        try:
            uuid_namespace: uuid.UUID = uuid.UUID(namespace)
        except Exception as error:
            msg = 'Invalid uuid namespace given.'
            raise ValueError(msg) from error

        return str(uuid.uuid5(uuid_namespace, f'{source_value}-{self._today}'))
