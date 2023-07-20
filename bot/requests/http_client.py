import typing

import aiohttp

from bot.authorization.backend import login


def handle_http_errors(func):
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                # Logging
                self.logger.error(f"Unauthorized error, logging in...")
                await login(self, self.set_auth_user, self.get_token)
                return await func(self, *args, **kwargs)
            else:
                raise e
    return wrapper


class HttpClient:
    def __init__(
            self,
            get_token,
            set_auth_user,
            logger,
    ) -> None:
        self.get_token = get_token
        self.set_auth_user = set_auth_user
        self.logger = logger

    def log_request(self, method, url, headers, data=None, params=None):
        self.logger.debug(f"{method} {url}")

        if params:
            self.logger.debug("Params:")
            for name, value in params.items():
                self.logger.debug(f"\t{name}: {value}")

        self.logger.debug("Headers:")
        for name, value in headers.items():
            self.logger.debug(f"\t{name}: {value}")

        if data:
            self.logger.debug("Data:")
            for name, value in data.items():
                self.logger.debug(f"\t{name}: {value}")

    @handle_http_errors
    async def get(
            self, url: str,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        async with aiohttp.ClientSession() as session:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            self.log_request("GET", url, headers)
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
            self.log_request("POST", url, headers, data=data)
            async with session.post(url, json=data, headers=headers) as response:
                final = await response.json()
                return final

    @handle_http_errors
    async def put(
            self, url: str, data,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        async with aiohttp.ClientSession() as session:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            self.log_request("PUT", url, headers, data=data)
            async with session.put(url, json=data, headers=headers) as response:
                return await response.json()

    @handle_http_errors
    async def delete(
            self, url: str, data,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        async with aiohttp.ClientSession() as session:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            self.log_request("DELETE", url, headers)
            async with session.delete(url, headers=headers) as response:
                return await response.json()
