from core.error_data import ErrorData
from core.exceptions import BaseAppError


class UseCaseError(BaseAppError):
    code: str = ErrorData.USER_CASE_ERROR.code
    message: str = ErrorData.USER_CASE_ERROR.message
    http_status: int = ErrorData.USER_CASE_ERROR.http_status_code
