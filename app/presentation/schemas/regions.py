from pydantic import BaseModel, ConfigDict, Field


class RegionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: int = Field(
        gt=0,
        lt=65535
    )

    name: str = Field(
        min_length=2,
        max_length=32
    )


class RegionResponse(RegionCreate):
    model_config = ConfigDict(extra="ignore")

    id: int


class RegionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    new_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=32
    )

    new_code:  int | None = Field(
        default=None,
        gt=0,
        lt=65535
    )