from core.contracts import ContractRequire
from core.contracts.contract_field_validator import (
    FieldValidatorContract,
    ValidationLevels,
)
from core.contracts.validators.business_rules_validators import br_username_validator
from core.contracts.validators.domain_validators import (
    EnumValidator,
    email_validator,
    password_validator,
    phone_number_validator,
    description_validator,
)
from core.enums import Organizations, Roles
from core.exceptions.contract import (
    ContractViolationValueTypeError,
    ContractViolationBusinessRulesError,
    ContractViolationError,
)
from core.users.rules_messages import (
    BusinessRulesViolationsMessages,
    DomainRulesViolationsMessages,
)

username_field_contract = FieldValidatorContract(
    name='username',
    nullable=False,
    expected_type_message="Ожидается 'str'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, str),
            exception=ContractViolationValueTypeError,
        ),
        ContractRequire(
            predicate=br_username_validator,
            exception=ContractViolationBusinessRulesError(
                BusinessRulesViolationsMessages.username
            ),
        ),
    ],
    level=ValidationLevels.strict,
)


firstname_field_contract = FieldValidatorContract(
    name='firstname',
    nullable=True,
    expected_type_message="Ожидается 'str'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, str),
            exception=ContractViolationValueTypeError,
        ),
        ContractRequire(
            predicate=br_username_validator,
            exception=ContractViolationBusinessRulesError(
                BusinessRulesViolationsMessages.firstname
            ),
        ),
    ],
)


lastname_field_contract = FieldValidatorContract(
    name='lastname',
    nullable=True,
    expected_type_message="Ожидается 'str'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, str),
            exception=ContractViolationValueTypeError,
        ),
        ContractRequire(
            predicate=br_username_validator,
            exception=ContractViolationBusinessRulesError(
                BusinessRulesViolationsMessages.lastname
            ),
        ),
    ],
)


organization_field_contract = FieldValidatorContract(
    name='organization',
    nullable=False,
    expected_type_message=(
        f'Enum {Organizations.__name__!r}: {", ".join(Organizations.__members__)}'
    ),
    validators=[
        ContractRequire(
            predicate=EnumValidator(Organizations),
            exception=ContractViolationValueTypeError,
        ),
    ],
    level=ValidationLevels.strict,
)


email_field_contract = FieldValidatorContract(
    name='email',
    nullable=True,
    expected_type_message="Ожидается 'str'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, str),
            exception=ContractViolationValueTypeError,
        ),
        ContractRequire(
            predicate=email_validator,
            exception=ContractViolationError(DomainRulesViolationsMessages.email),
        ),
    ],
)


password_field_contract = FieldValidatorContract(
    name='password',
    nullable=False,
    expected_type_message="Ожидается 'bytes'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, bytes),
            exception=ContractViolationValueTypeError,
        ),
        ContractRequire(
            predicate=password_validator,
            exception=ContractViolationError(
                DomainRulesViolationsMessages.password_length
            ),
        ),
    ],
    level=ValidationLevels.strict,
)


is_active_field_contract = FieldValidatorContract(
    name='is_active',
    nullable=False,
    expected_type_message="Ожидается 'bool'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, bool),
            exception=ContractViolationValueTypeError,
        ),
    ],
    level=ValidationLevels.strict,
)


role_field_contract = FieldValidatorContract(
    name='role',
    nullable=False,
    expected_type_message=f'Enum {Roles.__name__!r}: {", ".join(Roles.__members__)}',
    validators=[
        ContractRequire(
            predicate=EnumValidator(Roles), exception=ContractViolationValueTypeError
        ),
    ],
    level=ValidationLevels.strict,
)


phone_number_field_contract = FieldValidatorContract(
    name='phone_number',
    nullable=True,
    expected_type_message="Ожидается 'str'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, str),
            exception=ContractViolationValueTypeError,
        ),
        ContractRequire(
            predicate=phone_number_validator,
            exception=ContractViolationError(
                DomainRulesViolationsMessages.bad_phone_number
            ),
        ),
    ],
    level=ValidationLevels.light,
)


telegram_field_contract = FieldValidatorContract(
    name='telegram',
    nullable=True,
    expected_type_message="Ожидается 'str'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, str),
            exception=ContractViolationValueTypeError,
        ),
        ContractRequire(
            predicate=phone_number_validator,
            exception=ContractViolationError(
                DomainRulesViolationsMessages.bad_telegram_username
            ),
        ),
    ],
    level=ValidationLevels.light,
)


description_field_contract = FieldValidatorContract(
    name='description',
    nullable=False,
    expected_type_message="Ожидается 'str'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, str),
            exception=ContractViolationValueTypeError,
        ),
        ContractRequire(
            predicate=description_validator,
            exception=ContractViolationError(
                DomainRulesViolationsMessages.description_must_be_lt_255
            ),
        ),
    ],
    level=ValidationLevels.light,
)
