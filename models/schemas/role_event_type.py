import datetime

from models.schemas.base import BaseSchemaModel


class RoleEventTypeInCreate(BaseSchemaModel):
    role_id: int
    event_type_id: int
    can_edit: bool
    can_see: bool
    can_add: bool


class RoleEventTypeInUpdate(BaseSchemaModel):
    can_edit: bool | None
    can_see: bool | None
    can_add: bool | None


class RoleEventTypeInResponse(BaseSchemaModel):
    role_id: int
    event_type_id: int
    can_edit: bool
    can_see: bool
    can_add: bool
