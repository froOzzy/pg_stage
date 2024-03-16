import datetime
from typing import Any, Callable, Optional

from mimesis import Person, Address, Datetime
from mimesis.locales import Locale
from mimesis.builtins import RussiaSpecProvider


class UniqueInterface:
    """Интерфейс для уникальных значений как у faker."""

    def __init__(self, locale: str = 'en') -> None:
        self._locale = locale
        self._is_russian_locale = locale == Locale.RU
        self._unique_value = set()
        self._person = Person(locale=self._locale)
        self._address = Address(locale=self._locale)
        self._russian_provider = RussiaSpecProvider()

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
        return self._generate_unique_value(self._address.address)


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
        self._is_russian_locale = locale == Locale.RU.value
        self.unique = UniqueInterface(locale=self._locale)
        self._person = Person(locale=self._locale)
        self._address = Address(locale=self._locale)
        self._datetime = Datetime(locale=self._locale)
        self._russian_provider = RussiaSpecProvider()
        self._current_year = datetime.date.today().year

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

    def past_date(self, start_date: str) -> datetime.date:
        """
        Метод для формирования даты между start_date и секундой назад.
        :param start_date: дата начала
        :return: дата
        """
        return self._datetime.date()
