from typing import Any
from pydantic import BaseModel


class UpdatedEntitySchemaResponse(BaseModel):

    name: str | None

    old: Any
    new: Any
