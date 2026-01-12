from core.contracts.field_contracts_validators.common import (
    ValidationLevels,
    FieldContract,
)
from core.exceptions.contract import (
    ContractViolationValueTypeError,
)
from core.contracts.templates import ContractRequire

if __name__ == '__main__':
    o = FieldContract(
        name='test',
        # before_validators=lambda x: int(x),
        nullable=False,
        requires=[
            ContractRequire(
                predicate=lambda x: isinstance(x, int),
                exception=ContractViolationValueTypeError('Неверный тип данных'),
            ),
            ContractRequire(
                predicate=lambda x: x > 0,
                exception=ContractViolationValueTypeError('Неверное значение'),
            ),
        ],
        repair=lambda x: int(x) if isinstance(x, str) and x.strip().isdigit() else x,
        level=ValidationLevels.strict,
    )
    o(1)
    o('1')
