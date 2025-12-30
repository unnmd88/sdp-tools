from typing import Any
from pydantic import BaseModel


class UpdateRecordSchemaResponse(BaseModel):

    entity_name: str | None

    old: Any
    new: Any
