import asyncio
from aiohttp.client_exceptions import ClientConnectorError

from models.schemas.user import UserInResponse, UserInLogin, UserWithToken
from settings import API_URL, USERNAME, PASSWORD

AUTH_URL = f"{API_URL}/authorization/login"


async def login(get_http_client, set_auth_user) -> None:
    """Login to API"""
    print("SETTING UP BACKEND CONNECTION...")

    for attempt in range(3):
        try:
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
            print("AUTHORIZATION SUCCESSFUL!")
            break
        except ClientConnectorError as e:
            print(f"CONNECTION UNSUCCESSFUL, API MAY BE DOWN! (Attempt {attempt+1}/3)")
            if attempt < 2:  # If it's not the last attempt, wait a bit before trying again
                await asyncio.sleep(5)
            else:
                raise ConnectionRefusedError("FAILED TO CONNECT TO API, SHUTTING DOWN...")
