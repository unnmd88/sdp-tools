from functools import lru_cache

from core.enums import Roles, Permissions
from core.users.entities.role_permissions import RolePermissions

_admin = set(Permissions) - {Permissions.CREATE_USERS, Permissions.UPDATE_USERS}
_worker = set(Permissions) - {
    Permissions.CREATE_USERS,
    Permissions.READ_USERS,
    Permissions.UPDATE_USERS,
}

_superuser_permissions = RolePermissions(
    role_name=Roles.superuser, permissions=frozenset(Permissions)
)
_admin_permissions = RolePermissions(
    role_name=Roles.admin,
    permissions=frozenset(Permissions(p) for p in _admin),
)
_worker_permissions = RolePermissions(
    role_name=Roles.worker,
    permissions=frozenset(Permissions(p) for p in _worker),
)


_all_roles = {
    Roles.superuser: _superuser_permissions,
    Roles.admin: _admin_permissions,
    Roles.worker: _worker_permissions,
}


@lru_cache
def get_role_permissions(role: Roles) -> RolePermissions:
    return _all_roles[role]
