from bot.requests.http_client import HttpClient
from settings import API_URL
from models.schemas.role import RoleInResponse
from models.schemas.role_event_type import RoleEventTypeInResponse

ROLE_URL = f"{API_URL}/roles"


async def get_roles(
        http_client: HttpClient
) -> list[RoleInResponse]:
    """Get all roles"""
    db_roles = await http_client.get(ROLE_URL)
    db_role_list = list()
    for db_role in db_roles:  # type: ignore
        role = RoleInResponse(
            id=db_role.get("id"),
            name=db_role.get("name"),
        )
        db_role_list.append(role)

    return db_role_list


async def get_role_event_types(
        http_client: HttpClient
) -> list[RoleEventTypeInResponse]:
    """Get all role event types"""
    db_role_event_types = await http_client.get(f"{ROLE_URL}/permissions")
    db_role_event_type_list = list()
    for db_role_event_type in db_role_event_types:  # type: ignore
        role_event_type = RoleEventTypeInResponse(
            event_type_id=db_role_event_type.get("eventTypeId"),
            role_id=db_role_event_type.get("roleId"),
            can_edit=db_role_event_type.get("canEdit"),
            can_see=db_role_event_type.get("canSee"),
            can_add=db_role_event_type.get("canAdd"),
            created_at=db_role_event_type.get("createdAt"),
            updated_at=db_role_event_type.get("updatedAt"),
        )
        db_role_event_type_list.append(role_event_type)

    return db_role_event_type_list
