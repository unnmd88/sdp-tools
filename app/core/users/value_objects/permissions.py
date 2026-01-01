from collections.abc import MutableSet, Iterable

from core.enums import Permissions


class UserPermissions:
    def __init__(self, *permissions: Permissions):
        self._permissions: MutableSet = set(permissions)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self._permissions}'
            f')'
        )

    def get_all(self) -> MutableSet[Permissions]:
        return self._permissions

    def add(self, *permissions: Permissions):
        self._permissions |= {p for p in permissions}

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


if __name__ == '__main__':

    up = UserPermissions()
    print(up.read_users)
    up.add(Permissions.READ_USERS)
    print(up.read_users)
    print(up)
