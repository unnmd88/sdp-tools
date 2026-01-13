from datetime import datetime
from typing import Any

from core.base_entity import AbstractEntity, PublicAttr
from core.contracts import contract
from core.users.field_contracts import (
    ContractFieldUsername,
    ContractFieldFirstname,
    ContractFieldLastname,
)
from core.enums import (
    Organizations,
    Roles,
)
from core.contracts.exc import (
    ContractViolationBusinessRulesError,
    ContractViolationInvariantError,
)

from core.users.requires import (
    username_pre_requires,
    firstname_pre_requires,
    lastname_pre_requires,
)
from core.users.rules_messages import BusinessRulesViolationsMessages
from core.users.services.user_password import validate_password


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

    contract_username = ContractFieldUsername(use_cache=True, nullable=False)
    contract_firstname = ContractFieldFirstname(use_cache=True, nullable=True)
    contract_lastname = ContractFieldLastname(use_cache=True, nullable=True)

    def __init__(
        self,
        id: int,
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
        self._username = self.contract_username(username)
        self._firstname = self.contract_firstname(firstname)
        self._lastname = self.contract_lastname(lastname)
        self._organization = organization
        self._email = email
        self._password = password
        self._is_active = is_active
        self._role = role
        self._phone_number = phone_number
        self._telegram = telegram
        self._description = description
        self.invariant_names()
        self.invariant_password()

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

    def set_lastname(self, lastname: str | None) -> str | None:
        if lastname is None:
            self._lastname = None
            return self._lastname
        lastname = self._validate_last_name(lastname, _locals=locals())
        self._lastname = lastname
        return self._lastname

    def validate_password(self, password: str) -> bool:
        return validate_password(password, self._password)

    @contract(
        preconditions=username_pre_requires,
        # postconditions=username_post_requires if not os.environ.get("PROD") else None,
    )
    def _validate_username(
        self,
        username: str,
        _locals: dict[str, Any] = None,
    ) -> str:
        return username

    @contract(preconditions=firstname_pre_requires)
    def _validate_first_name(
        self,
        first_name: str,
        _locals: dict[str, Any] = None,
    ) -> str:
        return first_name

    @contract(preconditions=lastname_pre_requires)
    def _validate_last_name(self, lastname: str) -> str:
        return lastname

    def invariant_names(self):
        if self._username == self._lastname:
            raise ContractViolationBusinessRulesError(
                BusinessRulesViolationsMessages.username_and_lastname_must_be_different
            )
        if self._username == self._firstname:
            raise ContractViolationBusinessRulesError(
                BusinessRulesViolationsMessages.username_and_firstname_must_be_different
            )

    def invariant_password(self) -> None:
        if self._password is None:
            # TODO: Обязательно добавить логирование!!
            raise ContractViolationInvariantError("Пароль не может быть пустым")
        if not isinstance(self._password, bytes):
            # TODO: Обязательно добавить логирование!!
            raise ContractViolationInvariantError("Пароль должен быть типа bytes")

    def invariant_permissions(self) -> None:
        if not self._is_active and self._permissions:
            raise ContractViolationInvariantError(
                f"У пользователя с username: {self._username!r} не должно быть разрешений, т.к. он не активен."
            )
        # TODO: добавить проверку на наполнение разрешений в зависимости от роли.


if __name__ == "__main__":
    pass
    user = UserEntity(
        id=1,
        firstname="Junkers",
        lastname=None,
        username="Junker",
        created_at=datetime.now(),
        organization=Organizations.SDP,
        updated_at=None,
        password=b"12345678",
        is_active=True,
        role=Roles.admin,
        email=None,
        phone_number=None,
        telegram=None,
        description="",
    )
    print(user)
    print(repr(user))
    print(user.to_dict())
    print(user.to_json())

    # print(user.to_json())
