from dataclasses import dataclass

from domain.kernel.enums.attrs_names import PublicAttrNamesEnum


@dataclass(frozen=True, kw_only=True, slots=True)
class PublicAttr:
    attr_name: str
    alias: str | None = None

    def __iter__(self):
        return iter((self.attr_name, self.alias))


BASE_PUBLIC_ATTRS = (
    PublicAttr(attr_name="id", alias=str(PublicAttrNamesEnum.id)),
    PublicAttr(attr_name="_built_at", alias=str(PublicAttrNamesEnum.built_at)),
    PublicAttr(attr_name="_updated_at", alias=str(PublicAttrNamesEnum.updated_at)),
    PublicAttr(attr_name="_created_at", alias=str(PublicAttrNamesEnum.created_at)),
)

USER_PUBLIC_ATTRS = BASE_PUBLIC_ATTRS + (
    PublicAttr(attr_name="_username", alias=str(PublicAttrNamesEnum.username)),
    PublicAttr(attr_name="_firstname", alias=str(PublicAttrNamesEnum.firstname)),
    PublicAttr(attr_name="_lastname", alias=str(PublicAttrNamesEnum.lastname)),
    PublicAttr(attr_name="_is_active", alias=str(PublicAttrNamesEnum.is_active)),
    PublicAttr(attr_name="_role", alias=str(PublicAttrNamesEnum.role)),
    PublicAttr(attr_name="is_superuser", alias=str(PublicAttrNamesEnum.is_superuser)),
    PublicAttr(attr_name="_organization", alias=str(PublicAttrNamesEnum.organization)),
    PublicAttr(attr_name="_email", alias=str(PublicAttrNamesEnum.email)),
    PublicAttr(attr_name="_phone_number", alias=str(PublicAttrNamesEnum.phone_number)),
    PublicAttr(attr_name="_telegram", alias=str(PublicAttrNamesEnum.telegram)),
    PublicAttr(attr_name="_description", alias="description"),
)

REGIONS_PUBLIC_ATTRS = BASE_PUBLIC_ATTRS + (
    PublicAttr(attr_name="_name", alias=str(PublicAttrNamesEnum.name)),
    PublicAttr(attr_name="_code", alias=str(PublicAttrNamesEnum.code)),
)

PASSPORT_GROUPS_PUBLIC_ATTRS = BASE_PUBLIC_ATTRS + (
    PublicAttr(attr_name="_name", alias=str(PublicAttrNamesEnum.name)),
    PublicAttr(attr_name="_description", alias=str(PublicAttrNamesEnum.description)),
)

TRAFFIC_LIGHT_OBJECTS_PUBLIC_ATTRS = BASE_PUBLIC_ATTRS + (
    PublicAttr(attr_name="name", alias=str(PublicAttrNamesEnum.name)),
    PublicAttr(attr_name="region_id", alias=str(PublicAttrNamesEnum.region_id)),
    PublicAttr(attr_name="traffic_controller_type", alias=str(PublicAttrNamesEnum.traffic_controller_type)),
    PublicAttr(attr_name="created_by_user_id", alias=str(PublicAttrNamesEnum.created_by_user_id)),
    PublicAttr(attr_name="updated_by_user_id", alias=str(PublicAttrNamesEnum.updated_by_user_id)),
    PublicAttr(attr_name="latitude", alias=str(PublicAttrNamesEnum.latitude)),
    PublicAttr(attr_name="longitude", alias=str(PublicAttrNamesEnum.longitude)),
    PublicAttr(attr_name="district", alias=str(PublicAttrNamesEnum.district)),
    PublicAttr(attr_name="address", alias=str(PublicAttrNamesEnum.address)),
    PublicAttr(attr_name="note", alias=str(PublicAttrNamesEnum.note)),
)
