import time
from datetime import datetime

from domain.base_entity import AbstractEntity, PublicAttr

from domain.enums.unsorted import (
    Organizations,
    Roles,
)
from domain.exceptions.business_rules_exc import DomainInvariantViolationBusinessRuleError


class UserEntity(AbstractEntity):
    __public_attrs__ = AbstractEntity.__public_attrs__ + (
        PublicAttr(attr_name="_username", alias="username"),
        PublicAttr(attr_name="_firstname", alias="firstname"),
        PublicAttr(attr_name="_lastname", alias="lastname"),
        PublicAttr(attr_name="_role", alias="role"),
        PublicAttr(attr_name="_organization", alias="organization"),
        PublicAttr(attr_name="_email", alias="email"),
        PublicAttr(attr_name="_phone_number", alias="phone_number"),
        PublicAttr(attr_name="_telegram", alias="telegram"),
    )

    def __init__(
        self,
        id: int | None,
        username: str,
        firstname: str | None,
        lastname: str | None,
        organization: Organizations,
        email: str | None,
        password: bytes,
        is_active: bool,
        role: Roles,
        phone_number: str | None,
        telegram: str | None,
        description: str,
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self._username = username
        self._firstname = firstname
        self._lastname = lastname
        self._organization = organization
        self._email = email
        self._password = password
        self._is_active = is_active
        self._role = role
        self._phone_number = phone_number
        self._telegram = telegram
        self._description = description
        self.invariant_names()

    def __eq__(self, other):
        if isinstance(other, UserEntity):
            return self._username == other.username
        raise NotImplementedError

    @property
    def username(self) -> str:
        return self._username

    @property
    def firstname(self) -> str | None:
        return self._firstname

    @property
    def lastname(self) -> str | None:
        return self._lastname

    @property
    def organization(self) -> Organizations:
        return self._organization

    @property
    def email(self) -> str | None:
        return self._email

    @property
    def password(self) -> bytes:
        return self._password

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def role(self) -> Roles:
        return self._role

    @property
    def phone_number(self) -> str | None:
        return self._phone_number

    @property
    def telegram(self) -> str | None:
        return self._telegram

    @property
    def description(self) -> str:
        return self._description

    @property
    def is_superuser(self) -> bool:
        return self._role == Roles.superuser

    def set_username(self, username: str) -> str:
        username = self._validate_username(username, _locals=locals())
        self._username = username
        return self._username

    def set_firstname(self, firstname: str | None) -> str | None:
        if firstname is None:
            self._firstname = None
            return self._firstname
        firstname = self._validate_first_name(firstname, _locals=locals())
        self._firstname = firstname
        return self._firstname

    # def set_lastname(self, lastname: str | None) -> str | None:
    #     if lastname is None:
    #         self._lastname = None
    #         return self._lastname
    #     lastname = self._validate_last_name(lastname, _locals=locals())
    #     self._lastname = lastname
    #     return self._lastname

    def invariant_names(self):
        if self._username == self._lastname:
            raise DomainInvariantViolationBusinessRuleError(
                detail="Поле 'username' должно отличаться от поля 'lastname'",
            )
        if self._username == self._firstname:
            raise DomainInvariantViolationBusinessRuleError(
                detail="Поле 'username' должно отличаться от поля 'firstname'",
            )


if __name__ == "__main__":
    pass

    start_time = time.perf_counter()
    for _ in range(1000):
        user = UserEntity(
            id=1,
            firstname="Junkers",
            lastname=None,
            username="Jr",
            created_at=datetime.now(),
            organization=Organizations.SDP,
            updated_at=None,
            password=b"118",
            is_active=True,
            role=Roles.admin,
            email=None,
            phone_number=None,
            telegram=None,
            description="",
        )
    print(f"Время выполнения без валидации: {time.perf_counter() - start_time} секунд")

    print(repr(user))
    print(user.to_dict())
    print(user.to_json())

    # print(user.to_json())
