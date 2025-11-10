from fastapi import HTTPException
from starlette import status


class NotFoundByIdException(HTTPException):

    def __init__(
            self,
            entity_name: str,
            num_id: int,
            headers: dict[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{entity_name} with id={num_id} not found',
            headers=headers
        )