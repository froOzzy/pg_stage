from faker import Faker


class Mutator:
    """Класс с описанием основных методов для мутации значений полей"""

    def __init__(self, locale: str = 'en_US'):
        """Метод инициализации"""
        self._faker = Faker(locale=locale)

    def mutation_email(self, **kwargs) -> str:
        """
        Метод для создания фейкового email-а
        :return: email
        """
        if kwargs.get('unique'):
            return self._faker.unique.email()

        return self._faker.email()

    @staticmethod
    def mutation_empty_string(**_) -> str:
        """
        Метод для создания пустой строки
        :return: пустая строка
        """
        return ''

    @staticmethod
    def mutation_fixed_value(**kwargs) -> str:
        """
        Метод для вставки значения из параметров
        :return: строка со значением
        """
        return str(kwargs['value'])

    def mutation_full_name(self, **kwargs) -> str:
        """
        Метод для формирования ФИО
        :return: ФИО
        """
        if kwargs.get('unique'):
            return self._faker.unique.name()

        return self._faker.name()

    def mutation_first_name(self, **kwargs) -> str:
        """
        Метод для формирования имени
        :return: имя
        """
        if kwargs.get('unique'):
            return self._faker.unique.first_name()

        return self._faker.first_name()

    def mutation_middle_name(self, **kwargs) -> str:
        """
        Метод для формирования отчества (работает только с ru_RU)
        :return: отчество
        """
        if kwargs.get('unique'):
            return self._faker.unique.middle_name()

        return self._faker.middle_name()

    def mutation_last_name(self, **kwargs) -> str:
        """
        Метод для формирования фамилии
        :return: фамилия
        """
        if kwargs.get('unique'):
            return self._faker.unique.last_name()

        return self._faker.last_name()

    @staticmethod
    def mutation_null(**_) -> str:
        """
        Метод для возвращения NULL значения
        :return: NULL
        """
        return '\\N'

    def mutation_phone_number(self, **kwargs) -> str:
        """Метод для формирования номера телефона"""
        format = kwargs['format']
        if kwargs.get('unique'):
            return self._faker.unique.numerify(format)

        return self._faker.numerify(format)

    def mutation_address(self, **kwargs) -> str:
        """Метод для формирования адреса"""
        if kwargs.get('unique'):
            return self._faker.unique.address()

        return self._faker.address()

    def mutation_past_date(self, **kwargs) -> str:
        """
        Метод для формирования даты в прошедшем времени.
        start_date - самая ранняя допустимая дата в strtotime() формате
        """
        start_date = kwargs.get('start_date', '-30d')
        date_format = kwargs.get('date_format', '%Y-%m-%d')
        if kwargs.get('unique'):
            return self._faker.unique.past_date(start_date=start_date).strftime(date_format)

        return self._faker.past_date(start_date=start_date).strftime(date_format)

    def mutation_future_date(self, **kwargs) -> str:
        """
        Метод для формирования даты в будущем времени
        end_date - самая поздняя допустимая дата в strtotime() формате
        """
        end_date = kwargs.get('end_date', '+30d')
        date_format = kwargs.get('date_format', '%Y-%m-%d')
        if kwargs.get('unique'):
            return self._faker.unique.future_date(end_date=end_date).strftime(date_format)

        return self._faker.future_date(end_date=end_date).strftime(date_format)

    def mutation_uri(self, **kwargs) -> str:
        """Метод для формирования uri"""
        max_length = kwargs.get('max_length', 2048)
        if kwargs.get('unique'):
            return self._faker.unique.uri()[:max_length]

        return self._faker.uri()[:max_length]

    def mutation_ipv4_public(self, **kwargs) -> str:
        """Метод для формирования публичного ip-адреса 4 версии"""
        if kwargs.get('unique'):
            return self._faker.unique.ipv4_public()

        return self._faker.ipv4_public()

    def mutation_ipv4_private(self, **kwargs) -> str:
        """Метод для формирования приватного ip-адреса 4-й версии"""
        if kwargs.get('unique'):
            return self._faker.unique.ipv4_private()

        return self._faker.ipv4_private()

    def mutation_ipv6(self, **kwargs) -> str:
        """Метод для формирования ip-адреса 6-й версии"""
        if kwargs.get('unique'):
            return self._faker.unique.ipv6()

        return self._faker.ipv6()
