from typing import Annotated
from pydantic import BaseModel, Field

from core.constants import PassportsOwners


class PassportOwnersSchema(BaseModel):
    id: Annotated[int, Field(ge=1)]
    owner: PassportsOwners
    description: str


class PassportOwnersCreate(BaseModel):
    owner: PassportsOwners
    description: Annotated[str, Field(default='')]


class PassportOwnersPatch(BaseModel):
    owner: PassportsOwners
    description: Annotated[str, Field(default='')]