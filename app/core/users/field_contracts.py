from core.contracts import ContractRequire
from core.contracts.field_contracts import ContractField


class ContractFieldUsername(ContractField):
    _name_by_default = "username"
    _expected_types = str
    _requires = [ContractRequire(predicate=br_username_validator)]

    __slots__ = ContractField.__slots__


class ContractFieldFirstname(ContractField):
    _name_by_default = "firstname"
    _expected_types = str
    _requires = [ContractRequire(predicate=br_first_name_validator)]

    __slots__ = ContractField.__slots__


class ContractFieldLastname(ContractField):
    _name_by_default = "lastname"
    _expected_types = str
    _requires = [ContractRequire(predicate=br_lastname_validator)]

    __slots__ = ContractField.__slots__
