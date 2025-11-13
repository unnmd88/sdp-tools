from typing import Annotated

from pydantic import BaseModel, Field


class OvimPassportsFilter(BaseModel):
    owner_id: Annotated[int, Field(ge=1)]
