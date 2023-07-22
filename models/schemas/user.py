import datetime

from models.schemas.base import BaseSchemaModel


class UserInCreate(BaseSchemaModel):
    username: str
    password: str


class UserInUpdate(BaseSchemaModel):
    username: str | None
    password: str | None


class UserInLogin(BaseSchemaModel):
    username: str
    password: str


class UserInResponse(BaseSchemaModel):
    id: int
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None

