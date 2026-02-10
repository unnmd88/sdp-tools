from domain.primitives.field_type_validator import FieldTypeValidator
from domain.primitives.string_normalizer import StringNormalizer
from domain.primitives.string_validator import StringValidator

if __name__ == '__main__':

    v = FieldTypeValidator(value="1", expected_type=str, field_name='test').validate()
    normalized_string = (
        StringNormalizer.normalize_of(" Hello, World! ")
        .strip()
        .map(lambda x: x * 2)
        .get()
    )
    validated = (
        StringValidator
        .validate_of(value=normalized_string, field_name='test')
        .ensure_max_length(10)
        .ensure_min_length(1)
        .get()
    )

    print(validated)