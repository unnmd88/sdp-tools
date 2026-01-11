from core.exceptions.contract import ContractViolationBusinessRulesError
from core.services.contract.contracts import ContractRequire
from core.services.field_validators import first_name_or_lastname_validator, username_validator
from core.users.rules_messages import BusinessRulesViolationsMessages

username_pre_requires = [
    ContractRequire(
        predicate=username_validator,
        exception=ContractViolationBusinessRulesError(str(BusinessRulesViolationsMessages.username)),
    )
]

firstname_pre_requires = [
    ContractRequire(
        predicate=first_name_or_lastname_validator,
        exception=ContractViolationBusinessRulesError(str(BusinessRulesViolationsMessages.first_name)),
    )
]


lastname_pre_requires = [
    ContractRequire(
        predicate=first_name_or_lastname_validator,
        exception=ContractViolationBusinessRulesError(str(BusinessRulesViolationsMessages.last_name)),
    )
]