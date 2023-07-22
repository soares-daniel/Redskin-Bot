import asyncio

from aiohttp.client_exceptions import ClientConnectorError

from models.schemas.user import UserInResponse, UserInLogin
from settings import API_URL, USERNAME, PASSWORD

AUTH_URL = f"{API_URL}/authorization/login"


async def login(get_http_client, set_auth_user, logger) -> None:
    """Login to API"""
    logger.info("Attempting to login to API...")

    for attempt in range(3):
        try:
            http_client = get_http_client()()
            login_user = UserInLogin(username=USERNAME, password=PASSWORD)
            user_response = await http_client.post_raw(AUTH_URL, login_user.dict())
            if user_response.get("id"):
                user = UserInResponse(
                    id=user_response.get("id"),
                    username=user_response.get('username'),
                    created_at=user_response.get('createdAt'),
                    updated_at=user_response.get('updatedAt')
                )
            else:
                raise ConnectionRefusedError(user_response)
            set_auth_user(user)
            logger.info("Login successful")
            break
        except ClientConnectorError:
            logger.error(f"Connection unsuccessful, API may be down! (Attempt {attempt+1}/3)")
            if attempt < 2:  # If it's not the last attempt, wait a bit before trying again
                await asyncio.sleep(5)
            else:
                raise ConnectionRefusedError("FAILED TO CONNECT TO API, SHUTTING DOWN...")
