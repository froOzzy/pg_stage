import random
from typing import Any, Union, List

from faker import Faker


class Mutator:
    """Класс с описанием основных методов для мутации значений полей."""

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

    def mutation_phone_number(self, **kwargs: Union[bool, str]) -> str:
        """
        Метод для генерации номера телефона.
        :param kwargs:
            format - формат номера, например +7 (XXX) XXX XX XX
            unique - сгенерировать уникальный номер
        :return: номер телефона
        """
        format: str = kwargs['format']
        if kwargs.get('unique'):
            return self._faker.unique.numerify(format)

        return self._faker.numerify(format)

    def mutation_address(self, **kwargs) -> str:
        """
        Метод для генерации адреса.
        :param kwargs:
            unique - сгенерировать уникальный адрес
        :return: адрес
        """
        if kwargs.get('unique'):
            return self._faker.unique.address()

        return self._faker.address()

    def mutation_past_date(self, **kwargs: Union[bool, str]) -> str:
        """
        Метод для генерации даты в прошедшем времени.
        :param kwargs:
            start_date - самая ранняя допустимая дата в strtotime() формате, по умолчанию -30d
            date_format - формат даты, по умолчанию '%Y-%m-%d'
        :return: дата в прошедшем времени
        """
        start_date: str = kwargs.get('start_date', '-30d')
        date_format: str = kwargs.get('date_format', '%Y-%m-%d')
        if kwargs.get('unique'):
            return self._faker.unique.past_date(start_date=start_date).strftime(date_format)

        return self._faker.past_date(start_date=start_date).strftime(date_format)

    def mutation_future_date(self, **kwargs: Union[bool, str]) -> str:
        """
        Метод для генерации даты в будущем времени.
        :param kwargs:
            end_date - самая поздняя допустимая дата в strtotime() формате, по умолчанию +30d
            date_format - формат даты, по умолчанию '%Y-%m-%d'
        :return: дата в будущем времени
        """
        end_date = kwargs.get('end_date', '+30d')
        date_format = kwargs.get('date_format', '%Y-%m-%d')
        if kwargs.get('unique'):
            return self._faker.unique.future_date(end_date=end_date).strftime(date_format)

        return self._faker.future_date(end_date=end_date).strftime(date_format)

    def mutation_uri(self, **kwargs: Union[bool, int]) -> str:
        """
        Метод для генерации uri.
        :param kwargs:
            unique - сгенерировать уникальный uri
        :return: uri
        """
        max_length: int = kwargs.get('max_length', 2048)
        if kwargs.get('unique'):
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
    def mutation_random_choice(**kwargs: List[str]) -> str:
        """
        Метод для формирования случайного значения из списка
        :param kwargs:
            choices - список значений
        :return: случайное значение
        """
        choices = kwargs.get('choices', [])
        if not choices:
            raise ValueError('Key choices not found!')

        return str(random.choice(seq=choices))
