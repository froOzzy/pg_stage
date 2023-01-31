from faker import Faker


class Mutator:
    """Класс с описанием основных методо для мутации значений полей"""

    def __init__(self, locale: str = 'en_US'):
        """Метод инициализации"""
        self._faker = Faker(locale=locale)

    def mutation_email(self, **_) -> str:
        """
        Метод для создания фейкового email-а
        :return: емейл
        """
        return self._faker.email()

    @staticmethod
    def mutation_empty_string(**_) -> str:
        """
        Метод для создания пустой строки
        :return: пустая строка
        """
        return ''

    def mutation_first_name(self, **_) -> str:
        """
        Метод для формирования фамилии
        :return:
        """
        return self._faker.first_name()

    def mutation_last_name(self, **_) -> str:
        """
        Метод для формирования фамилии
        :return:
        """
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
        return self._faker.numerify(kwargs['format'])

    def mutator_address(self, **_) -> str:
        """Метод для формирования адреса"""
        return self._faker.address()

    def mutator_uri(self, **kwargs) -> str:
        """Метод для формирования uri"""
        max_length = kwargs.get('max_length', 2048)
        return self._faker.uri()[:max_length]
