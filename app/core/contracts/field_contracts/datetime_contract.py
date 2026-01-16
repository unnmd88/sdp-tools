from datetime import datetime
from typing import Any

from core.contracts.exc import ContractViolationFieldError
from core.contracts.field_contracts.base import AbstractContractField


class ContractDateTimeField(AbstractContractField):
    def _validate(self, value: Any) -> Any:
        if not isinstance(value, datetime):
            raise ContractViolationFieldError(
                contract="DateTime",
                violation="Значение не является датой и временем.",
                field_name=self._name,
                value=value,
                detail=f"Нарушен контракт типа значения {value!r} на дату и время.",
            )
        return super()._validate(value)


if __name__ == "__main__":
    dt = ContractDateTimeField(
        field_name="test_datetime",
        nullable=True,
        use_cache=False,
    )

    print(dt(datetime.now()))
    print(dt(None))
