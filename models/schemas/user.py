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


class UserWithToken(BaseSchemaModel):
    token: str
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class UserInResponse(BaseSchemaModel):
    id: int
    authorized_user: UserWithToken
