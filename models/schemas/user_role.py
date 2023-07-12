from models.schemas.base import BaseSchemaModel


class UserRoleInAssign(BaseSchemaModel):
    username: str
    role_name: str


class UserRoleInRemove(BaseSchemaModel):
    username: str
    role_name: str
