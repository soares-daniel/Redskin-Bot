from models.schemas.user import UserInResponse, UserInLogin, UserWithToken
from settings import API_URL, USERNAME, PASSWORD

AUTH_URL = f"{API_URL}/authorization/login"


async def login(get_http_client, set_auth_user) -> None:
    """Login to API"""
    http_client = get_http_client()()
    login_user = UserInLogin(username=USERNAME, password=PASSWORD)
    user_response = await http_client.post(AUTH_URL, login_user.dict())
    auth_user = None
    authorized_user = user_response.get('authorizedUser')
    if authorized_user:
        auth_user = UserInResponse(
                    id=user_response.get("id"),
                    authorized_user=UserWithToken(
                        token=authorized_user.get('token'),
                        username=authorized_user.get('username'),
                        created_at=authorized_user.get('createdAt'),
                        updated_at=authorized_user.get('updatedAt'),
                    ),
                )
    set_auth_user(auth_user)
