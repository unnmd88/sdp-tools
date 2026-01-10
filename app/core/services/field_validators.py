
def username_validator(value: str) -> bool:
    return (
            2 < len(value) < 32
            and value.isalpha()
            or
            (value.isalnum() and not value.isnumeric())
    )

def first_name_or_lastname_validator(value: str) -> bool:
    return 3 < len(value) < 16 and value.isalpha()