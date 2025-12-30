from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class IdSchemaMixin(BaseModel):
    id: Annotated[int, Field(gt=0), Field(lt=65535)]


class DateTimeSchemaMixin(BaseModel):
    created_at: Annotated[datetime | None, Field(default=None)]
    updated_at: Annotated[datetime | None, Field(default=None)]