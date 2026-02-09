import json
import time
from datetime import datetime

from core.error_codes import ErrorCodes
from domain.contract2.contract_field_enum import ContractFieldEnum
from domain.entities.base_entity import Entity
from domain.contract2.contract_field import ContractField
from domain.contract2.require import Require
from domain.entities_public_attrs import USER_PUBLIC_ATTRS
from domain.enums.attrs_names import PublicAttrNamesEnum

from domain.enums.unsorted import Organizations, Roles

from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainError, DomainInvariantError
from domain.value_objects.password_vo import PasswordVO

from domain.validators import (
    BooleanValidator,
    EmailRegexpValidator,
    PhoneNumberRegexpValidator,
    TelegramRegexpValidator,
    UserEntityValidator,
)
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)


class UserEntity(Entity):
    __public_attrs__ = USER_PUBLIC_ATTRS

    username = ContractField(
        field_name=str(PublicAttrNamesEnum.username),
        nullable=False,
        use_cache=True,
        requires=[Require(handler=UserEntityValidator.username)],
    )
    firstname = ContractField(
        field_name=str(PublicAttrNamesEnum.firstname),
        nullable=False,
        use_cache=True,
        requires=[Require(handler=UserEntityValidator.firstname)],
    )
    lastname = ContractField(
        field_name=str(PublicAttrNamesEnum.firstname),
        nullable=False,
        use_cache=True,
        requires=[Require(handler=UserEntityValidator.lastname)],
    )

    organization = ContractFieldEnum(
        enum=Organizations,
        field_name=str(PublicAttrNamesEnum.organization),
        nullable=False,
        use_cache=True,
    )
    email = ContractField(
        field_name=str(PublicAttrNamesEnum.email),
        nullable=True,
        use_cache=True,
        requires=[EmailRegexpValidator(field_name=str(PublicAttrNamesEnum.email))],
    )
    is_active = ContractField(
        field_name=str(PublicAttrNamesEnum.is_active),
        nullable=False,
        use_cache=True,
        preprocess_value=BooleanValidator(
            field_name=str(PublicAttrNamesEnum.is_active), allowed_like_bool={1, 0}
        ),
    )
    role = ContractFieldEnum(
        enum=Roles,
        field_name=str(PublicAttrNamesEnum.organization),
        nullable=False,
        use_cache=True,
    )
    phone_number = ContractField(
        field_name=str(PublicAttrNamesEnum.phone_number),
        nullable=True,
        use_cache=True,
        requires=[
            PhoneNumberRegexpValidator(field_name=str(PublicAttrNamesEnum.phone_number))
        ],
    )
    telegram = ContractField(
        field_name=str(PublicAttrNamesEnum.telegram),
        nullable=True,
        use_cache=True,
        requires=[
            TelegramRegexpValidator(field_name=str(PublicAttrNamesEnum.telegram))
        ],
    )
    description = ContractField(
        field_name=str(PublicAttrNamesEnum.description),
        nullable=False,
        use_cache=True,
    )

    def __init__(
        self,
        id: int | None,
        username: str,
        firstname: str,
        lastname: str,
        organization: str,
        email: str | None,
        password: str | bytes,
        is_active: bool,
        role: str,
        phone_number: str | None,
        telegram: str | None,
        description: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.organization: Organizations = organization
        self.email = email
        self._password = PasswordVO(password=password, subject=self.__class__.__name__)
        self.is_active = is_active
        self.role: Roles = role
        self.phone_number = phone_number
        self.telegram = telegram
        self.description = description
        self.invariant_names()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._username == other.username
        raise NotImplementedError

    @property
    def password(self) -> bytes | str:
        return self._password.password

    @property
    def is_superuser(self) -> bool:
        return self._role == Roles.SUPERUSER

    def invariant_names(self):
        if (self._username != self._lastname) and (self._username != self._firstname):
            return
        if self._username == self._lastname:
            rule = ErrorMessages.cannot_be_equal.format(
                repr(str(PublicAttrNamesEnum.username)),
                repr(str(PublicAttrNamesEnum.lastname)),
            )
        elif self._username == self._firstname:
            rule = ErrorMessages.cannot_be_equal.format(
                repr(str(PublicAttrNamesEnum.username)),
                repr(str(PublicAttrNamesEnum.firstname)),
            )
        else:
            raise DomainError
        ctx = ContractViolationContextVO(
            subject=self.__class__.__name__,
            field_name=str(PublicAttrNamesEnum.username),
            handler=f"{self.__class__.__name__}:{self.invariant_names.__name__}",
            contract_code=ErrorCodes.BUSINESS_RULE_VIOLATION.code,
            violation=Violations.invariant_violation,
            value=self._username,
            rule=rule,
            message=rule,
        )
        raise DomainInvariantError(
            private_message=ctx.message,
            context=ctx,
        )

    @classmethod
    def create_new_user(
        cls,
        *,
        username: str,
        firstname: str,
        lastname: str,
        organization: str,
        email: str | None,
        password: bytes,
        is_active: bool,
        role: str,
        phone_number: str | None,
        telegram: str | None,
        description: str,
    ) -> "UserEntity":
        return cls(
            id=None,
            username=username,
            firstname=firstname,
            lastname=lastname,
            organization=organization,
            email=email,
            password=password,
            is_active=is_active,
            role=role,
            phone_number=phone_number,
            telegram=telegram,
            description=description,
        )


if __name__ == "__main__":
    pass

    start_time = time.perf_counter()
    try:
        user = UserEntity(
            id=1,
            firstname="Junkers",
            lastname="Junkers",
            username="Junkers2",
            organization=Organizations.SDP,
            password="118",
            is_active=True,
            role=Roles.ADMIN,
            email=None,
            phone_number=None,
            telegram=None,
            created_at=datetime.now(),
            updated_at=None,
            description="",
        )
    except DomainError as e:
        print(e)
        print(e.to_dict())
        print(json.dumps(e.to_dict(), indent=2, ensure_ascii=False))

    print(f"Время выполнения с валидацией: {time.perf_counter() - start_time} секунд")

    # print(user.to_json())
