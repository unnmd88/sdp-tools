class ApplicationException(Exception):
    """
    Базовое исключение приложения.
    """
    # def __init__(self, detail: str = 'Ошибка приложения'):
    #     self.detail = detail
    #     super().__init__(detail)

    # @property
    # def detail(self):
    #     return self.detail

    detail: str = 'Ошибка приложения'


class NotFoundException(ApplicationException):
    """
    Исключение поиска любого объекта.
    """

    detail: str = 'Объект не найден'
