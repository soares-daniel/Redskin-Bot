from models.schemas.base import BaseSchemaModel


class RoleInCreate(BaseSchemaModel):
    name: str


class RoleInUpdate(BaseSchemaModel):
    name: str | None


class RoleInResponse(BaseSchemaModel):
    id: int
    name: str
