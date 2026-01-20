from dataclasses import dataclass

from domain.enums.public_attrs import PublicAttrsEnum


@dataclass(frozen=True, kw_only=True, slots=True)
class PublicAttr:
    attr_name: str
    alias: str | None = None


BASE_PUBLIC_ATTRS = (
    PublicAttr(attr_name="_id", alias=str(PublicAttrsEnum.id)),
    PublicAttr(attr_name="_built_at", alias=str(PublicAttrsEnum.built_at)),
    PublicAttr(attr_name="_updated_at", alias=str(PublicAttrsEnum.updated_at)),
    PublicAttr(attr_name="_created_at", alias=str(PublicAttrsEnum.created_at)),
)

USER_PUBLIC_ATTRS = BASE_PUBLIC_ATTRS + (
    PublicAttr(attr_name="_username", alias=str(PublicAttrsEnum.username)),
    PublicAttr(attr_name="_firstname", alias=str(PublicAttrsEnum.firstname)),
    PublicAttr(attr_name="_lastname", alias=str(PublicAttrsEnum.lastname)),
    PublicAttr(attr_name="_role", alias=str(PublicAttrsEnum.role)),
    PublicAttr(attr_name="_organization", alias=str(PublicAttrsEnum.organization)),
    PublicAttr(attr_name="_email", alias=str(PublicAttrsEnum.email)),
    PublicAttr(attr_name="_phone_number", alias=str(PublicAttrsEnum.phone_number)),
    PublicAttr(attr_name="_telegram", alias=str(PublicAttrsEnum.telegram)),
    PublicAttr(attr_name="_description", alias="description"),
)