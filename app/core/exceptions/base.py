"""
Модуль, содержащий базовые исключения.
"""

class ApplicationException(Exception):
    """ Ошибка приложения. """


class NotFoundException(ApplicationException):
    """ Ошибка поиска объекта. """

