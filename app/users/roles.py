from enum import StrEnum


class Roles(StrEnum):
    superuser = 'superuser'
    admin = 'admin'
    worker = 'worker'