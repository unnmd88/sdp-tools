import time
from datetime import datetime
from typing import Any, Self

from core.base_entity import AbstractEntity, PublicAttr
from core.contracts import (
    ContractStringField,
    contract,
)
from core.contracts.field_contracts.boolean_contract import ContractBooleanField
from core.contracts.field_contracts.email_contract import ContractEmailField
from core.contracts.field_contracts.enum_contract import ContactEnumField
from core.contracts.field_contracts.password_contract import ContractHashedPasswordField

from core.enums import (
    Organizations,
    Roles,
)
from core.contracts.exc import (
    ContractViolationError,
)
from core.exceptions.base import DomainValidationError
from core.users.business_rules import (
    MIN_LEN_USERNAME,
    MAX_LEN_USERNAME,
    MIN_LEN_FIRSTNAME,
    MAX_LEN_FIRSTNAME,
    MIN_LEN_LASTNAME,
    MAX_LEN_LASTNAME,
    MIN_LEN_PASSWORD,
    MAX_LEN_PASSWORD,
    FIRST_NAME_PATTERN,
    LAST_NAME_PATTERN,
    USERNAME_PATTERN,
    PASSWORD_PATTERN,
    TELEGRAM_PATTERN,
    MAX_LEN_DESCRIPTION,
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
    _contract_username = ContractStringField(
        field_name="username",
        nullable=False,
        use_cache=True,
        min_length=MIN_LEN_USERNAME,
        max_length=MAX_LEN_USERNAME,
        pattern=USERNAME_PATTERN,
    )
    _contract_firstname = ContractStringField(
        field_name="firstname",
        nullable=True,
        use_cache=True,
        min_length=MIN_LEN_FIRSTNAME,
        max_length=MAX_LEN_FIRSTNAME,
        pattern=FIRST_NAME_PATTERN,
    )
    _contract_lastname = ContractStringField(
        field_name="lastname",
        nullable=True,
        use_cache=True,
        min_length=MIN_LEN_LASTNAME,
        max_length=MAX_LEN_LASTNAME,
        pattern=LAST_NAME_PATTERN,
    )
    _contract_organization = ContactEnumField(
        field_name="organization",
        nullable=False,
        use_cache=True,
        enum=Organizations,
    )
    _contract_email = ContractEmailField(
        field_name="email",
        nullable=True,
        use_cache=True,
    )
    _contract_password = ContractHashedPasswordField(field_name="password")
    _contract_is_active = ContractBooleanField(
        field_name="is_active",
        nullable=False,
        allow_1_and_0_as_true_and_false=True,
    )
    _contract_role = ContactEnumField(
        field_name="role",
        nullable=False,
        use_cache=True,
        enum=Roles,
    )
    _contract_phone_number = ContractStringField(
        field_name="phone_number",
        nullable=True,
        use_cache=True,
        pattern=PASSWORD_PATTERN,
    )
    _contract_telegram = ContractStringField(
        field_name="telegram",
        nullable=True,
        use_cache=True,
        pattern=TELEGRAM_PATTERN,
    )
    _contract_description = ContractStringField(
        field_name="description",
        nullable=False,
        use_cache=True,
        max_length=MAX_LEN_DESCRIPTION,
    )

    @classmethod
    def validate(
        cls,
        *,
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
    ) -> Self:
        try:
            return cls(
                id=cls._contract_id(id),
                username=cls._contract_username(username),
                firstname=cls._contract_firstname(firstname),
                lastname=cls._contract_lastname(lastname),
                organization=cls._contract_organization(organization),
                email=cls._contract_email(email),
                password=cls._contract_password(password),
                is_active=is_active,
                role=cls._contract_role(role),
                phone_number=phone_number,
                telegram=telegram,
                description=description,
                created_at=cls._contract_created_at(created_at),
                updated_at=cls._contract_updated_at(updated_at),
            )
        except ContractViolationError as e:
            raise DomainValidationError(e.detail)

    @classmethod
    def create_new(
        cls,
        *,
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
    ) -> Self:
        try:
            return cls(
                id=None,
                username=cls._contract_username(username),
                firstname=cls._contract_firstname(firstname),
                lastname=cls._contract_lastname(lastname),
                organization=cls._contract_organization(organization),
                email=cls._contract_email(email),
                password=cls._contract_password(password),
                is_active=is_active,
                role=cls._contract_role(role),
                phone_number=phone_number,
                telegram=telegram,
                description=description,
                created_at=None,
                updated_at=None,
            )
        except ContractViolationError as e:
            raise DomainValidationError(e.detail)

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
        # preconditions=username_pre_requires,
        # postconditions=username_post_requires if not os.environ.get("PROD") else None,
    )
    def _validate_username(
        self,
        username: str,
        _locals: dict[str, Any] = None,
    ) -> str:
        return username

    # @contract(preconditions=firstname_pre_requires)
    def _validate_first_name(
        self,
        first_name: str,
        _locals: dict[str, Any] = None,
    ) -> str:
        return first_name

    # @contract(preconditions=lastname_pre_requires)
    def _validate_last_name(self, lastname: str) -> str:
        return lastname

    def invariant_names(self):
        if self._username == self._lastname:
            raise DomainValidationError(
                BusinessRulesViolationsMessages.username_and_lastname_must_be_different
            )
        if self._username == self._firstname:
            raise DomainValidationError(
                BusinessRulesViolationsMessages.username_and_firstname_must_be_different
            )

    def invariant_password(self) -> None:
        if self._password is None:
            # TODO: Обязательно добавить логирование!!
            raise ContractViolationInvariantError("Пароль не может быть пустым")
        if not isinstance(self._password, bytes):
            # TODO: Обязательно добавить логирование!!
            raise ContractViolationInvariantError("Пароль должен быть типа bytes")


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
    start_time = time.perf_counter()
    for _ in range(1000):
        user = UserEntity.validate(
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
    print(f"Время выполнения с валидацией: {time.perf_counter() - start_time} секунд")

    print(user)
    print(repr(user))
    print(user.to_dict())
    print(user.to_json())

    # print(user.to_json())
