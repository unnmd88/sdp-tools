import time
from datetime import datetime

from core.error_data import ErrorData
from domain.base_entity import AbstractEntity
from domain.contract2.contract_field import ContractField
from domain.contract2.require import Require
from domain.entities_public_attrs import PublicAttr, USER_PUBLIC_ATTRS
from domain.enums.public_attrs import PublicAttrsEnum

from domain.enums.unsorted import (
    Organizations,
    Roles,
)
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions.base import DomainError
from domain.exceptions.contract_violation_exc import (
    DomainInvariantViolationBusinessRuleError, DomainBusinessRuleError,
)
from domain.users.business_rules import forbidden_patterns_in_username
from domain.validators.user_validator import UserEntityValidator


class UserEntity(AbstractEntity):
    __public_attrs__ = USER_PUBLIC_ATTRS

    username = ContractField(
        field_name=str(PublicAttrsEnum.username),
        nullable=False,
        requires=[Require(handler=UserEntityValidator.username)],
    )
    firstname = ContractField(
        field_name=str(PublicAttrsEnum.firstname),
        nullable=False,
        preprocess_value=UserEntityValidator.repair_name,
        requires=[Require(handler=UserEntityValidator.firstname)],
    )
    lastname = ContractField(
        field_name=str(PublicAttrsEnum.firstname),
        nullable=False,
        preprocess_value=UserEntityValidator.repair_name,
        requires=[Require(handler=UserEntityValidator.lastname)],
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
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
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

    # def set_username(self, username: str) -> str:
    #     username = self._validate_username(username, _locals=locals())
    #     self._username = username
    #     return self._username
    #
    # def set_firstname(self, firstname: str | None) -> str | None:
    #     if firstname is None:
    #         self._firstname = None
    #         return self._firstname
    #     firstname = self._validate_first_name(firstname, _locals=locals())
    #     self._firstname = firstname
    #     return self._firstname

    # def set_lastname(self, lastname: str | None) -> str | None:
    #     if lastname is None:
    #         self._lastname = None
    #         return self._lastname
    #     lastname = self._validate_last_name(lastname, _locals=locals())
    #     self._lastname = lastname
    #     return self._lastname

    def invariant_names(self):
        if (self._username != self._lastname) and (self._username != self._firstname) and (self._username not in forbidden_patterns_in_username):
            return

        if self._username == self._lastname:
            rule = ErrorMessages.cannot_be_equal.format(
                repr(str(PublicAttrsEnum.username)), repr(str(PublicAttrsEnum.lastname))
            )
        elif self._username == self._firstname:
            rule = ErrorMessages.cannot_be_equal.format(
                repr(str(PublicAttrsEnum.username)), repr(str(PublicAttrsEnum.firstname))
            )
        elif self._username in forbidden_patterns_in_username:
            rule = ErrorMessages.name_not_allowed.format(repr(str(self.username)), self._username)
        else:
            raise DomainError

        raise DomainInvariantViolationBusinessRuleError(
            subject=self.__class__.__name__,
            field_name=str(PublicAttrsEnum.username),
            handler=repr(self.invariant_names.__name__),
            contract_name=ErrorData.BUSINESS_RULE_VIOLATION.code,
            violation=Violations.invariant_violation,
            value=self._username,
            rule=rule,
            message=rule,
        )
        if self._username == self._fullname.firstname:
            raise DomainBusinessRuleError(
                context="Поле 'username' должно отличаться от поля 'firstname'",
            )
        if self._username in forbidden_patterns_in_username:
            raise DomainBusinessRuleError(
                context=f"Поле 'username' не должно содержать {forbidden_patterns_in_username}",
            )


if __name__ == "__main__":
    pass

    start_time = time.perf_counter()
    try:
        for _ in range(1000):
            user = UserEntity(
                id="1",
                firstname="Junkers",
                lastname="Junkers",
                username="Junkers2",
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
    except DomainError as e:
        print(e.to_dict())
    print(f"Время выполнения без валидации: {time.perf_counter() - start_time} секунд")

    print(user.to_dict())
    print(user.to_json())
    print(user.__dict__)

    # print(user.to_json())
