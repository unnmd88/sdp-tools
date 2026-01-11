from core.exceptions.base import DomainValidationError


class ContractViolationError(DomainValidationError):
    """ Ошибка нарушения контракта. """


class ContractViolationValueTypeError(ContractViolationError):
    """ Ошибка нарушения типа значения. """


class ContractViolationBusinessRulesError(ContractViolationError):
    """ Ошибка нарушения контракта бизнес-правил. """


class ContractViolationPreConditionError(ContractViolationError):
    """ Ошибка нарушения контракта предусловия. """



class ContractViolationPostConditionError(ContractViolationError):
    """ Ошибка нарушения контракта постусловия. """


class ContractViolationReturnValueError(ContractViolationError):
    """ Ошибка нарушения контракта возвращаемого значения. """


class ContractViolationInvariantError(ContractViolationError):
    """ Ошибка нарушения типа значения. """