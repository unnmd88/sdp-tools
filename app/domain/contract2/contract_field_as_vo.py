from domain.contract2.interfaces import BuilderProtocol
from domain.contract2.nullable_config import NullableConfig
from domain.kernel.enums.validation_err_messages import ErrorMessages
from domain.exceptions import DomainContractViolationError, DomainValidationError


class DomainField[T_VO, T_Primitive]:
    def __init__(
        self,
        public_field_name: str,
        nullable_config: NullableConfig,
        vo_builder: BuilderProtocol | None = None,
    ):
        self._vo_builder = vo_builder
        self._public_field_name = public_field_name
        self._nullable_config = nullable_config

    def __set_name__(self, owner, name):
        self.name = f"_{name}"
        self._entity = owner.__name__

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, instance, value):
        if value is None:
            if self._nullable_config.allow_none:
                return setattr(instance, self.name, value)
            else:
                raise DomainValidationError(
                    private_message=ErrorMessages.none_not_allowed_for_field_this_entity.format(
                        self._public_field_name, self._entity
                    ),
                    public_message=self._nullable_config.public_message,
                ).with_field(self._public_field_name).with_entity_context(entity=self._entity)

        print(f"POINT 0, value: {value}")
        if self._vo_builder.is_vo_instance(value):
            print(f"POINT 1, value: {value}")
            return setattr(instance, self.name, value)
        else:
            try:
                print("POINT 2")
                print(f"self._vo_builder: {self._vo_builder}")
                print(f"value: {value}")

                return setattr(instance, self.name, self._vo_builder(value))
            except DomainContractViolationError as e:
                e.with_field(self._public_field_name).with_entity_context(entity=self._entity)
                print("POINT EXCEPTION")
                print(e)
                print(e.to_dict())
                print("FINISH EXCEPTION")
                raise e
        raise DomainValidationError()


