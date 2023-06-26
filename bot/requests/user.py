import aiohttp

from models.schemas.role import RoleInResponse
from settings import API_URL
from models.schemas.user import UserInResponse, UserWithToken

USER_URL = f"{API_URL}/users"


async def get_users(
) -> list[UserInResponse]:
    """Get all users"""
    async with aiohttp.ClientSession() as session:
        async with session.get(USER_URL) as response:
            db_users = await response.json()
            db_user_list = list()
            for db_user in db_users:
                authorized_user = db_user.get('authorizedUser')
                if authorized_user:
                    user = UserInResponse(
                        id=db_user.get("id"),
                        authorized_user=UserWithToken(
                            token=authorized_user.get('token'),
                            username=authorized_user.get('username'),
                            created_at=authorized_user.get('createdAt'),
                            updated_at=authorized_user.get('updatedAt'),
                        ),
                    )
                    db_user_list.append(user)

    return db_user_list


async def get_user_roles(
        user_id: int,
) -> list[RoleInResponse]:
    """Get all roles from user"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{USER_URL}/{user_id}/roles") as response:
            db_roles = await response.json()
            db_role_list = list()
            for db_role in db_roles:
                role = RoleInResponse(
                    id=db_role.get("id"),
                    name=db_role.get("name"),
                )
                db_role_list.append(role)

    return db_role_list
