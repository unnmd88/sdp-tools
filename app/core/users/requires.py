from core.contracts.exc import ContractViolationBusinessRulesError
from core.contracts import ContractRequire
from core.validators import (
    br_username_validator,
    br_first_name_validator,
)

username_pre_requires = [
    ContractRequire(
        predicate=br_username_validator,
        custom_exception=ContractViolationBusinessRulesError(),
    )
]

firstname_pre_requires = [
    ContractRequire(
        predicate=br_first_name_validator,
        custom_exception=ContractViolationBusinessRulesError(),
    )
]


lastname_pre_requires = [
    ContractRequire(
        predicate=br_first_name_validator,
        custom_exception=ContractViolationBusinessRulesError(),
    )
]
