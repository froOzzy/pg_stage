import re
import datetime
from typing import Any, Callable, Dict

from mimesis import Person, Address, Datetime, Internet, Numeric
from mimesis.builtins import RussiaSpecProvider

timedelta_pattern: str = r''
for name, sym in [
    ('years', 'y'),
    ('months', 'M'),
    ('weeks', 'w'),
    ('days', 'd'),
    ('hours', 'h'),
    ('minutes', 'm'),
    ('seconds', 's'),
]:
    timedelta_pattern += rf'((?P<{name}>(?:\+|-)\d+?){sym})?'

regex = re.compile(timedelta_pattern)


def _parse_date_string(value: str) -> Dict[str, float]:
    """
    Метод для парсинга строки с датой.
    :param value: значение для парсинга
    :return: список параметров для datetime.timedelta
    """
    parts = regex.match(value)
    if not parts:
        raise ValueError(f"Can't parse date string `{value}`")

    parts = parts.groupdict()  # type: ignore
    time_params: Dict[str, float] = {}
    for name_, param_ in parts.items():  # type: ignore
        if param_:
            time_params[name_] = int(param_)

    if 'years' in time_params:
        if 'days' not in time_params:
            time_params['days'] = 0

        time_params['days'] += 365.24 * time_params.pop('years')

    if 'months' in time_params:
        if 'days' not in time_params:
            time_params['days'] = 0

        time_params['days'] += 30.42 * time_params.pop('months')

    if not time_params:
        raise ValueError(f"Can't parse date string `{value}`")

    return time_params


def _parse_date(now: datetime.datetime, value: Any) -> datetime.date:
    """
    Метод для парсинга даты из строки.
    :param now: текущая дата и время
    :param value: значение для парсинга
    :return: дата
    """
    if isinstance(value, datetime.datetime):
        return value.date()

    if isinstance(value, datetime.date):
        return value

    if isinstance(value, datetime.timedelta):
        return (now + value).date()

    if isinstance(value, str):
        if value in ('today', 'now'):
            return now.date()

        time_params = _parse_date_string(value)
        return (now + datetime.timedelta(**time_params)).date()
    if isinstance(value, int):
        return (now + datetime.timedelta(value)).date()

    raise ValueError(f"Invalid format for date {value!r}")


class UniqueInterface:
    """Интерфейс для уникальных значений как у faker."""

    def __init__(self, locale: str = 'en') -> None:
        self._locale = locale
        self._is_russian_locale = locale == 'ru'
        self._unique_value = set()  # type: ignore
        self._person = Person(locale=self._locale)
        self._address = Address(locale=self._locale)
        self._datetime = Datetime(locale=self._locale)
        self._internet = Internet()
        self._numeric = Numeric()
        self._russian_provider = RussiaSpecProvider()
        self._current_year = datetime.date.today().year
        self._now = datetime.datetime.now()
        self._cache = {}  # type: ignore

    def _generate_unique_value(self, func: Callable[[Any], Any], *args: Any, **kwargs: Any) -> Any:
        """Метод для генерации уникального значения."""
        while True:
            value = func(*args, **kwargs)
            if not set(value) & self._unique_value:
                self._unique_value.add(value)
                break

        return value

    def clear(self) -> None:
        """Метод для очистки уникальных значений."""
        self._unique_value.clear()

    def email(self) -> str:
        """
        Метод для формирования уникального email-а.
        :return: email
        """
        return self._generate_unique_value(func=self._person.email)

    def name(self) -> str:
        """
        Метод для формирования уникального ФИО.
        :return: ФИО
        """
        while True:
            if self._is_russian_locale:
                value = f'{self._person.full_name(reverse=True)} {self._russian_provider.patronymic()}'
            else:
                value = self._person.full_name(reverse=True)

            if not set(value) & self._unique_value:
                self._unique_value.add(value)
                break

        return value

    def first_name(self) -> str:
        """
        Метод для формирования уникального имени.
        :return: имя
        """
        return self._generate_unique_value(func=self._person.name)

    def middle_name(self) -> str:
        """
        Метод для формирования уникального отчества (работает только с ru).
        :return: отчество
        """
        return self._generate_unique_value(func=self._russian_provider.patronymic)

    def last_name(self) -> str:
        """
        Метод для формирования уникальной фамилии.
        :return: фамилия
        """
        return self._generate_unique_value(func=self._person.surname)

    def numerify(self, mask: str) -> str:
        """
        Метод для формирования уникальной строки по маске.
        :param mask: маска
        :return: стока
        """
        return self._generate_unique_value(func=self._person.identifier, mask=mask)

    def address(self) -> str:
        """
        Метод для формирования уникального адреса.
        :return: адрес
        """
        return self._generate_unique_value(func=self._address.address)

    def past_date(self, start_date: Any) -> datetime.date:
        """
        Метод для формирования уникальной даты между start_date и прошлым годом (относительно инициализации класса).
        :param start_date: дата начала
        :return: дата
        """
        start = self._cache.get(start_date)
        if not start:
            start = _parse_date(now=self._now, value=start_date).year
            self._cache[start_date] = start

        end = self._current_year - 1
        if start >= end:
            start -= 2

        return self._generate_unique_value(func=self._datetime.date, start=start, end=end)

    def future_date(self, end_date: Any) -> datetime.date:
        """
        Метод для формирования уникальной даты между следущим годом (относительно инициализации класса) и end_date.
        :param end_date: дата окончания
        :return: дата
        """
        end = self._cache.get(end_date)
        if not end:
            end = _parse_date(now=self._now, value=end_date).year
            self._cache[end_date] = end

        start = self._current_year + 1
        if end <= start:
            end += 2

        return self._generate_unique_value(func=self._datetime.date, start=start, end=end)

    def uri(self) -> str:
        """
        Метод для получения уникального uri.
        :return: uri
        """
        return self._generate_unique_value(func=self._internet.uri)

    def ipv4_public(self) -> str:
        """
        Метод для получения уникального IPV4
        :return: IPV4
        """
        return self._generate_unique_value(func=self._internet.ip_v4)

    def ipv4_private(self) -> str:
        """
        Метод для получения уникального IPV4
        :return: IPV4
        """
        return self._generate_unique_value(func=self._internet.ip_v4)

    def ipv6(self) -> str:
        """
        Метод для получения уникального IPV6
        :return: IPV6
        """
        return self._generate_unique_value(func=self._internet.ip_v6)

    def random_int(self, min: int, max: int) -> int:
        """
        Метод для получения случайного уникального числа.
        :param min: минимальное значение
        :param max: максимальное значение
        """
        return self._generate_unique_value(func=self._numeric.integer_number, start=min, end=max)

    def pydecimal(self, left_digits: int, right_digits: int, min_value: float, max_value: float):
        """
        Метод для получения уникального числа с плавающей точкой.
        :param left_digits: количество символов до запятой
        :param right_digits: количество символов после запятой
        :param min_value: минимальное значение
        :param max_value: максимальное значение
        """
        return self._generate_unique_value(
            func=self._numeric.float_number,
            start=min_value,
            end=max_value,
            precision=right_digits,
        )


class MimesisInterface:
    """
    Интерфейс для подключения mimesis аналогично faker.
    TODO: Удалить класс и все методы перенести в mutator, если будет прирост в скорости.
    """

    def __init__(self, locale: str = 'en_US') -> None:
        """
        Метод инициализации класса.
        :param locale: локализация для mimesis
        """
        # Локализация для faker использует _, поэтому выбираем первую часть строки
        self._locale = locale.split('_')[0]
        self._is_russian_locale = locale == 'ru'
        self.unique = UniqueInterface(locale=self._locale)
        self._person = Person(locale=self._locale)
        self._address = Address(locale=self._locale)
        self._datetime = Datetime(locale=self._locale)
        self._internet = Internet()
        self._numeric = Numeric()
        self._russian_provider = RussiaSpecProvider()
        self._current_year = datetime.date.today().year
        self._now = datetime.datetime.now()
        self._cache = {}  # type: ignore

    def email(self) -> str:
        """
        Метод для формирования email-а.
        :return: email
        """
        return self._person.email()

    def name(self) -> str:
        """
        Метод для формирования ФИО.
        :return: ФИО
        """
        if self._is_russian_locale:
            f'{self._person.full_name(reverse=True)} {self._russian_provider.patronymic()}'

        return self._person.full_name(reverse=True)

    def first_name(self) -> str:
        """
        Метод для формирования имени.
        :return: имя
        """
        return self._person.name()

    def middle_name(self) -> str:
        """
        Метод для формирования отчества (работает только с ru).
        :return: отчество
        """
        return self._russian_provider.patronymic()

    def last_name(self) -> str:
        """
        Метод для формирования фамилии.
        :return: фамилия
        """
        return self._person.surname()

    def numerify(self, mask: str) -> str:
        """
        Метод для формирования строки по маске.
        :param mask: маска
        :return: строка
        """
        return self._person.identifier(mask=mask)

    def address(self) -> str:
        """
        Метод для формирования адреса.
        :return: адрес
        """
        return self._address.address()

    def past_date(self, start_date: Any) -> datetime.date:
        """
        Метод для формирования даты между start_date и прошым годом (относительно инициализации класса).
        :param start_date: дата начала
        :return: дата
        """
        start = self._cache.get(start_date)
        if not start:
            start = _parse_date(now=self._now, value=start_date).year
            self._cache[start_date] = start

        end = self._current_year - 1
        if start >= end:
            start -= 2

        return self._datetime.date(start=start, end=end)

    def future_date(self, end_date: Any) -> datetime.date:
        """
        Метод для формирования даты между следующим годом (относительно инициализации класса) и end_date.
        :param end_date: дата окончания
        :return: дата
        """
        end = self._cache.get(end_date)
        if not end:
            end = _parse_date(now=self._now, value=end_date).year
            self._cache[end_date] = end

        start = self._current_year + 1
        if end <= start:
            end += 2

        return self._datetime.date(start=start, end=end)

    def uri(self) -> str:
        """
        Метод для получения uri.
        :return: uri
        """
        return self._internet.uri()

    def ipv4_public(self) -> str:
        """
        Метод для получения IPV4
        :return: IPV4
        """
        return self._internet.ip_v4()

    def ipv4_private(self) -> str:
        """
        Метод для получения IPV4
        :return: IPV4
        """
        return self._internet.ip_v4()

    def ipv6(self) -> str:
        """
        Метод для получения IPV6
        :return: IPV6
        """
        return self._internet.ip_v6()

    def random_int(self, min: int, max: int) -> int:
        """
        Метод для получения случайного числа.
        :param min: минимальное значение
        :param max: максимальное значение
        """
        return self._numeric.integer_number(start=min, end=max)

    def pydecimal(self, left_digits: int, right_digits: int, min_value: float, max_value: float):
        """
        Метод для получения числа с плавающей точкой.
        :param left_digits: количество символов до запятой
        :param right_digits: количество символов после запятой
        :param min_value: минимальное значение
        :param max_value: максимальное значение
        """
        return self._numeric.float_number(start=min_value, end=max_value, precision=right_digits)
