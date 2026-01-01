from core.dto.users import UpdateUserDTO
from core.users.entities.user import UserEntity
from core.users.exceptions import ForbiddenUpdateError


def check_permission_to_update_entity(
    *,
    requestor_entity: UserEntity,
    to_update_entity: UserEntity,
    data: UpdateUserDTO
):
    if requestor_entity != to_update_entity and not requestor_entity.is_superuser:
        raise ForbiddenUpdateError('Нет прав для изменения другого пользователя.')
    if (data.is_admin or data.is_active or data.is_superuser or data.role) and not requestor_entity.is_superuser:
        raise ForbiddenUpdateError('Нет прав для изменения роли пользователя.')
