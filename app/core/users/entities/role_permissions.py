from collections.abc import Iterable
from dataclasses import dataclass, field

from core.enums import Permissions, Roles
from core.users.services.role_permissions import superuser_permissions

"""
Описание ролей юзеров.
superuser - полный доступ ко всем ресурсам
admin - доступ к ресурсам, кроме создания и редактирования пользователей
worker - доступ к ресурсам, кроме создания, чтения и редактирования пользователей и ролей
"""

@dataclass(frozen=True, kw_only=True, slots=True)
class RolePermissions:

    role_name: Roles
    permissions: Iterable[Permissions | str]

    def __post_init__(self) -> None:
        Roles(self.role_name)
        [Roles(p) for p in self.permissions]

    def __contains__(self, item: Permissions) -> bool:
        return item in self.permissions


if __name__ == '__main__':
    print(superuser_permissions)