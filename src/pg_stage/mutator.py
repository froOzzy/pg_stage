import functools
from typing import List, Dict

from faker import Faker


def unique_object(function):
    """Декоратор для формирования уникального значения"""

    @functools.wraps(function)
    def wrapper(self, *args, **kwargs) -> str:
        """Обработчик декоратора"""
        result = function(self, *args, **kwargs)
        if not kwargs.get('unique'):
            return result

        recursion_count = 0
        while result in self.unique_objects:
            if recursion_count > self.max_count_recursion:
                raise ValueError('Recursion limit exceeded')

            recursion_count += 1
            result = function(self, *args, **kwargs)

        return result

    return wrapper


class Mutator:
    """Класс с описанием основных методов для мутации значений полей"""

    unique_objects = set()
    max_count_recursion = 20

    def __init__(self, locale: str = 'en_US'):
        """Метод инициализации"""
        self._faker = Faker(locale=locale)

    @unique_object
    def mutation_email(self, **_) -> str:
        """
        Метод для создания фейкового email-а
        :return: email
        """
        return self._faker.email()

    @unique_object
    def mutation_empty_string(self, **_) -> str:
        """
        Метод для создания пустой строки
        :return: пустая строка
        """
        return ''

    @unique_object
    def mutation_fixed_value(self, **kwargs) -> str:
        """
        Метод для вставки значения из параметров
        :return: строка со значением
        """
        return str(kwargs['value'])

    @unique_object
    def mutation_full_name(self, **_) -> str:
        """
        Метод для формирования ФИО
        :return: ФИО
        """
        return self._faker.name()

    @unique_object
    def mutation_first_name(self, **_) -> str:
        """
        Метод для формирования имени
        :return: имя
        """
        return self._faker.first_name()

    @unique_object
    def mutation_middle_name(self, **_) -> str:
        """
        Метод для формирования отчества (работает только с ru_RU)
        :return: отчество
        """
        return self._faker.middle_name()

    @unique_object
    def mutation_last_name(self, **_) -> str:
        """
        Метод для формирования фамилии
        :return: фамилия
        """
        return self._faker.last_name()

    @unique_object
    def mutation_null(self, **_) -> str:
        """
        Метод для возвращения NULL значения
        :return: NULL
        """
        return '\\N'

    @unique_object
    def mutation_phone_number(self, **kwargs) -> str:
        """Метод для формирования номера телефона"""
        return self._faker.numerify(kwargs['format'])

    @unique_object
    def mutation_address(self, **_) -> str:
        """Метод для формирования адреса"""
        return self._faker.address()

    @unique_object
    def mutation_past_date(self, **kwargs) -> str:
        """
        Метод для формирования даты в прошедшем времени.
        start_date - самая ранняя допустимая дата в strtotime() формате
        """
        start_date = kwargs.get('start_date', '-30d')
        date_format = kwargs.get('date_format', '%Y-%m-%d')
        return self._faker.past_date(start_date=start_date).strftime(date_format)

    @unique_object
    def mutation_future_date(self, **kwargs) -> str:
        """
        Метод для формирования даты в будущем времени
        end_date - самая поздняя допустимая дата в strtotime() формате
        """
        end_date = kwargs.get('end_date', '+30d')
        date_format = kwargs.get('date_format', '%Y-%m-%d')
        return self._faker.future_date(end_date=end_date).strftime(date_format)

    @unique_object
    def mutation_uri(self, **kwargs) -> str:
        """Метод для формирования uri"""
        max_length = kwargs.get('max_length', 2048)
        return self._faker.uri()[:max_length]

    @unique_object
    def mutation_ipv4_public(self, **_) -> str:
        """Метод для формирования публичного ip-адреса 4 версии"""
        return self._faker.ipv4_public()

    @unique_object
    def mutation_ipv4_private(self, **_) -> str:
        """Метод для формирования приватного ip-адреса 4-й версии"""
        return self._faker.ipv4_private()

    @unique_object
    def mutation_ipv6(self, **_) -> str:
        """Метод для формирования ip-адреса 6-й версии"""
        return self._faker.ipv6()
