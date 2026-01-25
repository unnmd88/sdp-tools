import logging
import time
from datetime import datetime

from app_logging.dev.config import DOMAIN
from core.error_data import ErrorData
from domain.base_entity import AbstractEntity
from domain.contract2.contract_field import ContractField
from domain.contract2.require import Require
from domain.entities_public_attrs import USER_PUBLIC_ATTRS
from domain.enums.attrs_names import PublicAttrNamesEnum

from domain.enums.unsorted import Organizations, Roles

from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions.base import DomainError
from domain.exceptions.contract_violation_exc import (
    DomainInvariantViolationBusinessRuleError,
)
from domain.users.business_rules import forbidden_patterns_in_username
from domain.users.value_objects.password_vo import PasswordVO


from domain.validators import (
    BooleanValidator,
    EmailRegexpValidator,
    PhoneNumberRegexpValidator,
    TelegramRegexpValidator,
    EnumValidator,
    UserEntityValidator,
)


logger = logging.getLogger(DOMAIN)


class UserEntity(AbstractEntity):
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
        # preprocess_value=UserEntityValidator.repair_firstname_or_lastname,
        requires=[Require(handler=UserEntityValidator.firstname)],
    )
    lastname = ContractField(
        field_name=str(PublicAttrNamesEnum.firstname),
        nullable=False,
        use_cache=True,
        # preprocess_value=UserEntityValidator.repair_firstname_or_lastname,
        requires=[Require(handler=UserEntityValidator.lastname)],
    )
    organization = ContractField(
        field_name=str(PublicAttrNamesEnum.organization),
        nullable=False,
        use_cache=True,
        preprocess_value=EnumValidator(
            field_name=str(PublicAttrNamesEnum.organization), enum_class=Organizations
        ),
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
    role = ContractField(
        field_name=str(PublicAttrNamesEnum.organization),
        nullable=False,
        use_cache=True,
        preprocess_value=EnumValidator(
            field_name=str(PublicAttrNamesEnum.role), enum_class=Roles
        ),
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

    def __init__(
        self,
        id: int | None,
        username: str,
        firstname: str,
        lastname: str,
        organization: Organizations,
        email: str | None,
        password: str | bytes,
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
        self.organization = organization
        self.email = email
        self._password = PasswordVO(password=password, subject=self.__class__.__name__)
        self.is_active = is_active
        self.role = role
        self.phone_number = phone_number
        self.telegram = telegram
        self._description = description
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
        return self._role == Roles.superuser

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
        raise DomainInvariantViolationBusinessRuleError(
            subject=self.__class__.__name__,
            field_name=str(PublicAttrNamesEnum.username),
            handler=repr(self.invariant_names.__name__),
            contract_code=ErrorData.BUSINESS_RULE_VIOLATION.code,
            violation=Violations.invariant_violation,
            value=self._username,
            rule=rule,
            message=rule,
        )


if __name__ == "__main__":
    pass

    start_time = time.perf_counter()
    try:
        user = UserEntity(
            id="1",
            firstname="Junkers",
            lastname="Junkers",
            username="Junkers2",
            organization=Organizations.SDP,
            password="118",
            is_active=True,
            role=Roles.admin,
            email=None,
            phone_number=None,
            telegram=None,
            created_at=datetime.now(),
            updated_at=None,
            description="",
        )
    except DomainError as domain_error:
        logger.info(domain_error.to_dict())
        raise domain_error
    # try:
    #     for _ in range(1000):
    #         user = UserEntity(
    #             id="1",
    #             firstname="Junkers",
    #             lastname="Junkers",
    #             username="Junkers2",
    #             created_at=datetime.now(),
    #             organization=Organizations.SDP,
    #             updated_at=None,
    #             password=b"118",
    #             is_active=True,
    #             role=Roles.admin,
    #             email=None,
    #             phone_number=None,
    #             telegram=None,
    #             description="",
    #         )
    # except DomainError as e:
    #     print(e.to_dict())
    #     raise e
    print(f"Время выполнения с валидацией: {time.perf_counter() - start_time} секунд")

    print(user.to_dict())
    print(user.to_json())

    # print(user.to_json())
