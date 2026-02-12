from domain.contract2.contract_field_as_vo import DomainField
from domain.contract2.nullable_config import NullableConfig
from domain.contract2.vo_builder import BaseVoBuilder
from domain.value_objects.region_vo import RegionCodeVo


class SomeEntity:

    region_code = DomainField(
        public_field_name="region_code",
        nullable_config=NullableConfig(allow_none=False, public_message="id is required"),
        vo_builder=BaseVoBuilder(RegionCodeVo)
    )

    def __init__(self, region_code: RegionCodeVo | int):
        self.region_code = region_code

    def __repr__(self):
        return f"{self.__class__.__name__}(reg_code={self.region_code})"


if __name__ == "__main__":
    entity = SomeEntity(region_code=1)
    # for i in range(12, -1, -1):
    #     entity = SomeEntity(region_code=RegionCodeVo(value=i))
    #     print(entity)