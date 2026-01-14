from typing import Any, get_type_hints

from core.contracts.exc import ContractViolationValueTypeError


class TypeChecker:
    @classmethod
    def vector_types_check(
        cls,
        *,
        locals_args: dict[str, Any],
        annotations: dict[str, Any],
        # exception: ContractViolationValueTypeError = ContractViolationValueTypeError,
    ) -> None:
        if locals_args is None:
            return None
        locals_args.pop("self", None)
        for arg_name, arg_val in locals_args.items():
            if not isinstance(arg_val, annotations.get(arg_name, object)):
                raise ContractViolationValueTypeError(
                    field_name=arg_name, expected=annotations[arg_name].__name__
                )
        return None


# def vector_type_checker(
#     args: dict[str, Any],
#     annotations: dict[str, Any]
# ):
#     for arg_name, arg_type in args.items():
#         if not isinstance(arg_type, annotations[arg_name]):
#             raise DomainTypeValidationError(field_name=arg_name, expected=arg_type.__name__)


def foo(x: int, y: str, z=4) -> int | None:
    print(locals())
    print(get_type_hints(foo))
    print(foo.__annotations__)
    print(x, y)
    TypeChecker.vector_types_check(
        locals_args=locals(), annotations=get_type_hints(foo)
    )
    return


if __name__ == "__main__":
    foo(1, "2")
