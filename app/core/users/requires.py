from core.exceptions.contract import ContractViolationBusinessRulesError
from core.contracts import ContractRequire
from core.contracts.validators.business_rules_validators import (
    br_username_validator,
    br_first_name_or_lastname_validator,
)
from core.users.rules_messages import BusinessRulesViolationsMessages

username_pre_requires = [
    ContractRequire(
        predicate=br_username_validator,
        exception=ContractViolationBusinessRulesError(
            str(BusinessRulesViolationsMessages.username)
        ),
    )
]

firstname_pre_requires = [
    ContractRequire(
        predicate=br_first_name_or_lastname_validator,
        exception=ContractViolationBusinessRulesError(
            str(BusinessRulesViolationsMessages.firstname)
        ),
    )
]


lastname_pre_requires = [
    ContractRequire(
        predicate=br_first_name_or_lastname_validator,
        exception=ContractViolationBusinessRulesError(
            str(BusinessRulesViolationsMessages.lastname)
        ),
    )
]
