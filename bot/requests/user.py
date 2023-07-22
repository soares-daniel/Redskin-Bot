from typing import List

from bot.requests.http_client import HttpClient
from models.schemas.role import RoleInResponse
from settings import API_URL
from models.schemas.user import UserInResponse

USER_URL = f"{API_URL}/users"


async def get_users(
        http_client: HttpClient
) -> List[UserInResponse]:
    """Get all users"""
    db_users = await http_client.get(USER_URL)
    db_user_list = list()
    for db_user in db_users:  # type: ignore
        user = UserInResponse(
            id=db_user.get("id"),
            username=db_user.get('username'),
            created_at=db_user.get('createdAt'),
            updated_at=db_user.get('updatedAt'),
        )
        db_user_list.append(user)

    return db_user_list


async def get_user_roles(
        http_client: HttpClient,
        user_id: int
) -> List[RoleInResponse]:
    """Get all roles from user"""
    db_roles = await http_client.get(f"{USER_URL}/user/{user_id}/roles")
    db_role_list = list()
    for db_role in db_roles:  # type: ignore
        role = RoleInResponse(
            id=db_role.get("id"),
            name=db_role.get("name"),
        )
        db_role_list.append(role)

    return db_role_list
