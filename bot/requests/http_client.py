import typing

import aiohttp

from bot.authorization.backend import login


def handle_http_errors(func):
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                # Handle unauthorized error
                print("Unauthorized error, logging in...")
                await login(self, self.set_auth_user)
                return await func(self, *args, **kwargs)
            else:
                raise e
    return wrapper


class HttpClient:
    def __init__(self, get_token, set_auth_user) -> None:
        self.get_token = get_token
        self.set_auth_user = set_auth_user

    @handle_http_errors
    async def get(
            self, url: str,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        async with aiohttp.ClientSession() as session:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
# Define your headers
            async with session.get(url, headers=headers) as response:
                return await response.json()

    @handle_http_errors
    async def post(
            self, url: str, data,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        async with aiohttp.ClientSession() as session:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            async with session.post(url, json=data, headers=headers) as response:
                return await response.json()

    @handle_http_errors
    async def put(
            self, url: str, data,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        async with aiohttp.ClientSession() as session:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            async with session.put(url, json=data, headers=headers) as response:
                return await response.json()

    @handle_http_errors
    async def delete(
            self, url
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        async with aiohttp.ClientSession() as session:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            async with session.delete(url, headers=headers) as response:
                return await response.json()
