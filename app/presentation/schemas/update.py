from typing import Any
from pydantic import BaseModel


class UpdatedRecordSchemaResponse(BaseModel):

    old: Any
    new: Any
