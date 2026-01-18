from collections.abc import MutableSet, Iterable
from typing import TypeAlias

from domain.enums import Permissions

type T_Permissions = set[Permissions] | frozenset[Permissions]


class UserPermissions:
    def __init__(self, *permissions: Permissions):
        self._permissions: T_Permissions = set(permissions)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._permissions})"

    def get_all(self) -> T_Permissions:
        return self._permissions

    def add(self, *permissions: Permissions):
        self._permissions |= set(permissions)

    def add_all_user_permissions(self, exclude: set[Permissions] = None):
        exclude = exclude or set()
        self._permissions |= {p for p in Permissions if p not in exclude}

    def revoke(self, *permissions: Permissions):
        for permission in permissions:
            self._permissions.remove(Permissions(permission))

    def revoke_all(self) -> int:
        cnt = 0
        while self._permissions:
            self._permissions.pop()
            cnt += 1
        return cnt

    def frozen_permissions(self):
        self._permissions = frozenset(self._permissions)

    def has_difference(self, permissions: set[Permissions]) -> set[Permissions]:
        if not permissions:
            raise ValueError("permissions cant be empty.")
        if not permissions.issubset(self._permissions):
            raise ValueError("Bad members in permissions.")
        return self._permissions - permissions  # Разность множеств

    def has(self, permission: Permissions):
        return permission in self._permissions

    def has_to_update_users(self) -> bool:
        return Permissions.UPDATE_USERS in self._permissions

    def update_any_user(self) -> bool:
        return Permissions.UPDATE_USERS in self._permissions


if __name__ == "__main__":
    up = UserPermissions()
    print(up.read_users)
    up.add(Permissions.READ_USERS)
    print(up.read_users)
    print(up)
