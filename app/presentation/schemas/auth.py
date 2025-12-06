from pydantic import BaseModel, ConfigDict


class AuthSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra='ignore')

    username: str
    password: str
