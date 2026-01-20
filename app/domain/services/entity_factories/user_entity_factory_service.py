import json
from dataclasses import field, dataclass
from datetime import datetime
from typing import Any

from core.error_data import ErrorData
from domain.contracts import (
    ContractStringField,
    ContractField,
)
from domain.contracts.exc import ContractViolationError, ContractViolationNotNoneError

from domain.contracts.field_contracts import (
    ContractBooleanField,
    ContractEmailField,
    ContactEnumField,
    ContractHashedPasswordField,
)
from domain.contracts.require_schemas import ContractRequireSchema
from domain.enums.business_rules import BusinessRulePatterns

from domain.enums.unsorted import (
    Organizations,
    Roles,
)
from domain.enums.violations import Violations
from domain.exceptions.contract_violation_exc import (
    DomainValidationError,
    DomainContractViolationError,
    DomainBusinessRuleError,
)

from domain.services.entity_factories.base_entity_factory_service import (
    AbstractEntityFactoryService,
)

from domain.users.business_rules import (
    MIN_LEN_USERNAME,
    MAX_LEN_USERNAME,
    MIN_LEN_FIRSTNAME,
    MAX_LEN_FIRSTNAME,
    MIN_LEN_LASTNAME,
    MAX_LEN_LASTNAME,
    FIRST_NAME_PATTERN,
    LAST_NAME_PATTERN,
    USERNAME_PATTERN,
    PASSWORD_PATTERN,
    TELEGRAM_PATTERN,
    MAX_LEN_DESCRIPTION,
)
from domain.users.entities.user import UserEntity
from domain.validators.domain_validators import username_validator, ValidatorException


@dataclass(frozen=True, kw_only=True, slots=True)
class ContractMetaData:
    contract: str
    violation: str
    expected_type: type = None
    rule: str = None
    message: str = ""
    context: dict[str, Any] = field(default_factory=dict)

    def load_value_to_context(self, value: Any):
        self.context.update(
            value=value,
            current_type=type(value),
        )

    def load_subject_to_context(self, subject: Any):
        self.context.update(subject=subject)

    def to_dict(self):
        return {
            "name": self.contract,
            "violation": self.violation,
            "expected_type": self.expected_type,
            "context": self.context,
        } | {
            k: v
            for k, v in zip(
                (("expected_type", self.expected_type), ("rule", self.rule))
            )
            if v is not None
        }


STR_ISINSTANCE_REQUIRE = ContractRequireSchema(
    handler=lambda x: isinstance(x, str),
    metadata=ContractMetaData(
        contract=ErrorData.DOMAIN_VALIDATION.code,
        violation=Violations.invalid_type,
        message="Значение должно быть строкой",
        expected_type=str,
    ),
)


class UserEntityFactoryService(AbstractEntityFactoryService[UserEntity]):

    contract_username = ContractField(
        field_name="username",
        nullable=False,
        use_cache=True,
        requires=[
            ContractRequireSchema(handler=username_validator),
            # STR_ISINSTANCE_REQUIRE,
            # ContractRequireSchema(
            #     handler=lambda x: MIN_LEN_USERNAME <= len(x) <= MAX_LEN_USERNAME,
            #     metadata=ContractMetaData(
            #         contract="business_rule",
            #         violation="value length",
            #         rule=f"Значение должно быть в диапазоне от {MIN_LEN_USERNAME} до {MAX_LEN_USERNAME} символов",
            #         message=f"Значение должно быть в диапазоне от {MIN_LEN_USERNAME} до {MAX_LEN_USERNAME} символов",
            #     ),
            # ),
        ],
    )
    contract_firstname = ContractField(
        field_name="firstname",
        nullable=True,
        use_cache=True,
        requires=[
            STR_ISINSTANCE_REQUIRE,
            ContractRequireSchema(
                handler=lambda x: MIN_LEN_FIRSTNAME <= len(x) <= MAX_LEN_FIRSTNAME,
                metadata=ContractMetaData(
                    contract=ErrorData.BUSINESS_RULE_VIOLATION.code,
                    violation=Violations.value_length,
                    rule=BusinessRulePatterns.value_str_length_range,
                    message=BusinessRulePatterns.value_str_length_range,
                ),
            ),
        ],
    )
    contract_lastname = ContractStringField(
        field_name="lastname",
        nullable=True,
        use_cache=True,
        requires=[
            STR_ISINSTANCE_REQUIRE,
            ContractRequireSchema(
                handler=lambda x: MIN_LEN_LASTNAME <= len(x) <= MAX_LEN_LASTNAME,
                metadata=ContractMetaData(
                    contract=ErrorData.BUSINESS_RULE_VIOLATION.code,
                    violation=Violations.value_length,
                    rule=BusinessRulePatterns.value_str_length_range,
                    message=BusinessRulePatterns.value_str_length_range,
                ),
            ),
        ],
        min_length=MIN_LEN_LASTNAME,
        max_length=MAX_LEN_LASTNAME,
        pattern=LAST_NAME_PATTERN,
    )
    contract_organization = ContactEnumField(
        field_name="organization",
        nullable=False,
        use_cache=True,
        enum=Organizations,
    )
    contract_email = ContractEmailField(
        field_name="email",
        nullable=True,
        use_cache=True,
    )
    contract_password = ContractHashedPasswordField(
        field_name="password",
    )
    contract_is_active = ContractBooleanField(
        field_name="is_active",
        nullable=False,
        allow_1_and_0_as_true_and_false=True,
    )
    contract_role = ContactEnumField(
        field_name="role",
        nullable=False,
        use_cache=True,
        enum=Roles,
    )
    contract_phone_number = ContractStringField(
        field_name="phone_number",
        nullable=True,
        use_cache=True,
        pattern=PASSWORD_PATTERN,
    )
    contract_telegram = ContractStringField(
        field_name="telegram",
        nullable=True,
        use_cache=True,
        pattern=TELEGRAM_PATTERN,
    )
    contract_description = ContractStringField(
        field_name="description",
        nullable=False,
        use_cache=True,
        max_length=MAX_LEN_DESCRIPTION,
    )

    @classmethod
    def create_existing(
        cls,
        *,
        id: int,
        username: str,
        firstname: str | None,
        lastname: str | None,
        organization: Organizations | str,
        email: str | None,
        password: bytes,
        is_active: bool,
        role: Roles | str,
        phone_number: str | None,
        telegram: str | None,
        description: str,
        created_at: datetime | None,
        updated_at: datetime | None,
    ) -> UserEntity:
        if id is None:
            # TODO: добавить логирование. Это ошибка в логике/инфраструктуре.
            raise DomainValidationError(
                "Значение id не может быть 'None' у существующего пользователя."
            )
        try:
            return UserEntity(
                id=cls.contract_id(id),
                username=cls.contract_username(username),
                firstname=cls.contract_firstname(firstname),
                lastname=cls.contract_lastname(lastname),
                organization=cls.contract_organization(organization),
                email=cls.contract_email(email),
                password=cls.contract_password(password),
                is_active=is_active,
                role=cls.contract_role(role),
                phone_number=phone_number,
                telegram=telegram,
                description=description,
                created_at=cls.contract_created_at(created_at),
                updated_at=cls.contract_updated_at(updated_at),
            )
        except ValidatorException as e:
            print("11111111111111111111")
            sub = f"{UserEntity.__name__!r}"
            contract = e.contract_name
            if contract == ErrorData.DOMAIN_VALIDATION.code:
                exc_class = DomainValidationError
            elif contract == ErrorData.BUSINESS_RULE_VIOLATION.code:
                exc_class = DomainBusinessRuleError
            else:
                exc_class = DomainContractViolationError
            exc = exc_class(
                subject=sub,
                field_name=e.field_name,
                contract_name=contract,
                violation=e.violation,
                expected_type=e.expected_type,
                rule=e.rule,
                value=e.value,
                message=e.message,
            )
            print(exc.context)
            # print(json.dumps(exc.context, indent=2))
            print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False))


        except ContractViolationNotNoneError as e:
            exc = DomainValidationError(
                subject=repr(UserEntity.__name__),
                field_name=e.field_name,
                contract_name="nullable",
                violation="value cannot be None",
                value=e.value,
                message=f"Ошибка валидации поля {e.field_name!r}. Значение не может быть None",
            )
            print(exc.context)
            print(
                json.dumps(
                    exc.context,
                    indent=2,
                )
            )
            print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False))

        except ContractViolationError as e:
            pass
            # sub = f"{UserEntity.__name__!r}"
            # meta: ContractMetaData = e.context
            # meta.context.update(handler=e.handler)
            # if meta.contract == "type_validation":
            #     exc_class = DomainValidationError
            # elif meta.contract == "business_rule":
            #     exc_class = DomainBusinessRuleError
            # else:
            #     exc_class = DomainContractViolationError
            # exc = exc_class(
            #     subject=sub,
            #     field_name=e.field_name,
            #     contract_name=meta.contract,
            #     violation=meta.violation,
            #     expected_type=meta.expected_type,
            #     rule=meta.rule,
            #     value=e.value,
            #     message=meta.message,
            # )
            # print(exc.context)
            # # print(json.dumps(exc.context, indent=2))
            # print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False))

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
    ) -> UserEntity:
        try:
            return UserEntity(
                id=None,
                username=cls.contract_username(username),
                firstname=cls.contract_firstname(firstname),
                lastname=cls.contract_lastname(lastname),
                organization=cls.contract_organization(organization),
                email=cls.contract_email(email),
                password=cls.contract_password(password),
                is_active=is_active,
                role=cls.contract_role(role),
                phone_number=phone_number,
                telegram=telegram,
                description=description,
                created_at=None,
                updated_at=None,
            )
        except ContractViolationError as e:
            raise DomainValidationError(e.context)


if __name__ == "__main__":
    user = UserEntityFactoryService.create_existing(
        id=1,
        firstname="Junkers",
        lastname=None,
        username="J",
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
