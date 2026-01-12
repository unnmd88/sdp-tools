from core.contracts import ContractRequire
from core.contracts.field_contracts import ContractField
from core.contracts.validators.business_rules_validators import (
    br_username_validator,
    br_first_name_validator,
    br_lastname_validator,
)
from core.exceptions.contract import ContractViolationBusinessRulesError
from core.users.rules_messages import BusinessRulesViolationsMessages


class ContractFieldUsername(ContractField):
    _name_by_default = 'username'
    _expected_types = str
    _requires = [ContractRequire(predicate=br_username_validator)]

    __slots__ = ContractField.__slots__


class ContractFieldFirstname(ContractField):
    _name_by_default = 'firstname'
    _expected_types = str
    _requires = [ContractRequire(predicate=br_first_name_validator)]

    __slots__ = ContractField.__slots__


class ContractFieldLastname(ContractField):
    _name_by_default = 'lastname'
    _expected_types = str
    _requires = [ContractRequire(predicate=br_lastname_validator)]

    __slots__ = ContractField.__slots__


#
# firstname_field_contract = FieldContract(
#     name='firstname',
#     nullable=True,
#     message_expected_type_if_type_not_valid="Ожидается 'str'",
#     requires=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, str),
#             exception=ContractViolationValueTypeError,
#         ),
#         ContractRequire(
#             predicate=br_username_validator,
#             exception=ContractViolationBusinessRulesError(
#                 BusinessRulesViolationsMessages.firstname
#             ),
#         ),
#     ],
# )
#
#
# lastname_field_contract = FieldContract(
#     name='lastname',
#     nullable=True,
#     message_expected_type_if_type_not_valid="Ожидается 'str'",
#     requires=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, str),
#             exception=ContractViolationValueTypeError,
#         ),
#         ContractRequire(
#             predicate=br_username_validator,
#             exception=ContractViolationBusinessRulesError(
#                 BusinessRulesViolationsMessages.lastname
#             ),
#         ),
#     ],
# )
#
#
# organization_field_contract = FieldContract(
#     name='organization',
#     nullable=False,
#     message_expected_type_if_type_not_valid=(
#         f'Enum {Organizations.__name__!r}: {", ".join(Organizations.__members__)}'
#     ),
#     requires=[
#         ContractRequire(
#             predicate=EnumValidator(Organizations),
#             exception=ContractViolationValueTypeError,
#         ),
#     ],
#     level=ValidationLevels.strict,
# )
#
#
# email_field_contract = FieldContract(
#     name='email',
#     nullable=True,
#     message_expected_type_if_type_not_valid="Ожидается 'str'",
#     requires=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, str),
#             exception=ContractViolationValueTypeError,
#         ),
#         ContractRequire(
#             predicate=email_validator,
#             exception=ContractViolationError(DomainRulesViolationsMessages.email),
#         ),
#     ],
# )
#
#
# password_field_contract = FieldContract(
#     name='password',
#     nullable=False,
#     message_expected_type_if_type_not_valid="Ожидается 'bytes'",
#     requires=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, bytes),
#             exception=ContractViolationValueTypeError,
#         ),
#         ContractRequire(
#             predicate=password_validator,
#             exception=ContractViolationError(
#                 DomainRulesViolationsMessages.password_length
#             ),
#         ),
#     ],
#     level=ValidationLevels.strict,
# )
#
#
# is_active_field_contract = FieldContract(
#     name='is_active',
#     nullable=False,
#     message_expected_type_if_type_not_valid="Ожидается 'bool'",
#     requires=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, bool),
#             exception=ContractViolationValueTypeError,
#         ),
#     ],
#     level=ValidationLevels.strict,
# )
#
#
# role_field_contract = FieldContract(
#     name='role',
#     nullable=False,
#     message_expected_type_if_type_not_valid=f'Enum {Roles.__name__!r}: {", ".join(Roles.__members__)}',
#     requires=[
#         ContractRequire(
#             predicate=EnumValidator(Roles), exception=ContractViolationValueTypeError
#         ),
#     ],
#     level=ValidationLevels.strict,
# )
#
#
# phone_number_field_contract = FieldContract(
#     name='phone_number',
#     nullable=True,
#     message_expected_type_if_type_not_valid="Ожидается 'str'",
#     requires=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, str),
#             exception=ContractViolationValueTypeError,
#         ),
#         ContractRequire(
#             predicate=phone_number_validator,
#             exception=ContractViolationError(
#                 DomainRulesViolationsMessages.bad_phone_number
#             ),
#         ),
#     ],
#     level=ValidationLevels.soft,
# )
#
#
# telegram_field_contract = FieldContract(
#     name='telegram',
#     nullable=True,
#     message_expected_type_if_type_not_valid="Ожидается 'str'",
#     requires=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, str),
#             exception=ContractViolationValueTypeError,
#         ),
#         ContractRequire(
#             predicate=phone_number_validator,
#             exception=ContractViolationError(
#                 DomainRulesViolationsMessages.bad_telegram_username
#             ),
#         ),
#     ],
#     level=ValidationLevels.soft,
# )
#
#
# description_field_contract = FieldContract(
#     name='description',
#     nullable=False,
#     message_expected_type_if_type_not_valid="Ожидается 'str'",
#     requires=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, str),
#             exception=ContractViolationValueTypeError,
#         ),
#         ContractRequire(
#             predicate=description_validator,
#             exception=ContractViolationError(
#                 DomainRulesViolationsMessages.description_must_be_lt_255
#             ),
#         ),
#     ],
#     level=ValidationLevels.soft,
# )
