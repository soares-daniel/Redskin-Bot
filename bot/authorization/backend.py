import asyncio

from aiohttp.client_exceptions import ClientConnectorError

from models.schemas.user import UserInResponse, UserInLogin
from settings import API_URL, USERNAME, PASSWORD

AUTH_URL = f"{API_URL}/authorization/login"


class LoginFailedError(Exception):
    """Exception raised when login attempts fail."""


async def login(get_http_client, set_auth_user, logger) -> None:
    """Login to API"""
    logger.info("Attempting to login to API...")
    http_client = get_http_client()()
    login_user = UserInLogin(username=USERNAME, password=PASSWORD)

    for attempt in range(3):
        try:
            user_response = await http_client.post_raw(AUTH_URL, login_user.dict())
            if user_response.get("id"):
                user = UserInResponse(
                    id=user_response.get("id"),
                    username=user_response.get('username'),
                    created_at=user_response.get('createdAt'),
                    updated_at=user_response.get('updatedAt')
                )
                set_auth_user(user)
            logger.info("Login successful")
            break
        except ClientConnectorError:
            logger.warning(f"Connection unsuccessful, API may be down! (Attempt {attempt+1}/3)")
            if attempt < 2:  # If it's not the last attempt, wait a bit before trying again
                await asyncio.sleep(5)
    else:
        logger.error("All attempts to connect to the API have failed")
        raise LoginFailedError("Unable to login after 3 attempts")
