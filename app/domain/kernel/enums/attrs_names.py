from enum import StrEnum


class PublicAttrNamesEnum(StrEnum):
    id = "id"
    built_at = "built_at"
    updated_at = "updated_at"
    created_at = "created_at"
    region_id ="region_id"
    traffic_controller_type ="traffic_controller_type"
    created_by_user_id = "created_by_user_id"
    updated_by_user_id = "updated_by_user_id"
    latitude = "latitude"
    longitude = "longitude"
    district = "district"
    address = "address"
    note = "note"


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
    code = "code"
    name = "name"
    region = "region"
    type_controller = "type_controller"


class PrivateAttrNamesEnum(StrEnum):
    password = "password"
