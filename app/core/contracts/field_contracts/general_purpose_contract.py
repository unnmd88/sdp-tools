from core.contracts.field_contracts.base import AbstractContractField


class ContractField(AbstractContractField):
    """ Базовый класс для создания контракта полей. """


if __name__ == "__main__":
    contract_field = ContractField(
        field_name="test",
        nullable=False,
    )

    print(contract_field(()))




