from core.exceptions.contract import ContractViolationBusinessRulesError
from core.contracts import ContractRequire
from core.contracts.validators.business_rules_validators import (
    br_username_validator,
    br_first_name_validator,
)
from core.users.rules_messages import BusinessRulesViolationsMessages

username_pre_requires = [
    ContractRequire(
        predicate=br_username_validator,
        exception=ContractViolationBusinessRulesError(),
    )
]

firstname_pre_requires = [
    ContractRequire(
        predicate=br_first_name_validator,
        exception=ContractViolationBusinessRulesError(),
    )
]


lastname_pre_requires = [
    ContractRequire(
        predicate=br_first_name_validator,
        exception=ContractViolationBusinessRulesError(),
    )
]
