


class ApplicationException(Exception):
    """
    Base application exception.
    """


class NotFoundException(ApplicationException):

    detail = "Not found"