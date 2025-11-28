# from fastapi import HTTPException
# from starlette import status
#
#
# class NotFoundException(HTTPException):
#     def __init__(
#         self,
#         table_column_name: str,
#         entity_name: str,
#         filters: dict,
#         headers: dict[str, str] | None = None,
#     ):
#         super().__init__(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=(
#                 f'{entity_name} '
#                 f'with filters {" ".join(f"{k!r}={v!r}" for k, v in filters.items())} '
#                 f'not found'
#             ),
#             headers=headers,
#         )
