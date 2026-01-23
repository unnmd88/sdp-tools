from enum import StrEnum


class PublicAttrNamesEnum(StrEnum):
    id = "id"
    built_at = "built_at"
    updated_at = "updated_at"
    created_at = "created_at"

    username = "username"
    firstname = "firstname"
    lastname = "lastname"
    is_active = "is_active"
    is_superuser = "is_superuser"
    role = "role"
    organization = "organization"
    email = "email"
    phone_number = "phone_number"
    telegram = "telegram"
    description = "description"


class PrivateAttrNamesEnum(StrEnum):
    password = "password"
