class ApplicationException(Exception):
    """
    Базовое исключение приложения.
    """

    detail: str = 'Ошибка приложения'


class NotFoundException(ApplicationException):
    """
    Исключение поиска любого объекта.
    """

    detail: str = 'Объект не найден'
