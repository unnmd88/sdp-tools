from datetime import datetime

from core.contracts import ContractRequire
from core.contracts.contract_field_validator import FieldValidatorContract
from core.exceptions.contract import ContractViolationValueTypeError
from core.contracts.validators.domain_validators import id_validator

id_field_contract = FieldValidatorContract(
    name='id',
    nullable=False,
    expected_type_message="Ожидается 'int'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, int),
            exception=ContractViolationValueTypeError,
        ),
        ContractRequire(predicate=id_validator),
    ],
)


created_at_field_contract = FieldValidatorContract(
    name='created_at',
    nullable=True,
    expected_type_message="'datetime'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, datetime),
            exception=ContractViolationValueTypeError,
        ),
    ],
)


updated_at_field_contract = FieldValidatorContract(
    name='updated_at',
    nullable=True,
    expected_type_message="'datetime'",
    validators=[
        ContractRequire(
            predicate=lambda x: isinstance(x, datetime),
            exception=ContractViolationValueTypeError,
        ),
    ],
)
