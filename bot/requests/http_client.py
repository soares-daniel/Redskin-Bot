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
            set_auth_user,
            logger,
    ) -> None:
        self.set_user = set_auth_user
        self.session = aiohttp.ClientSession()
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
    async def post_raw(
            self, url: str, data,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        """Only used for login because of the token potentially not stored in cookies yet"""
        self.log_request("POST", url, {}, data=data)
        async with self.session.post(url, json=data) as response:
            return await response.json()

    @handle_http_errors
    async def get(
            self, url: str,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        self.log_request("GET", url, {})
        async with self.session.get(url) as response:
            return await response.json()

    @handle_http_errors
    async def post(
            self, url: str, data,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        self.log_request("POST", url, {}, data=data)
        async with self.session.post(url, json=data) as response:
            return await response.json()

    @handle_http_errors
    async def put(
            self, url: str, data,
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        self.log_request("PUT", url, {}, data=data)
        async with self.session.put(url, json=data) as response:
            return await response.json()

    @handle_http_errors
    async def delete(
            self, url: str
    ) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        self.log_request("DELETE", url, {})
        async with self.session.delete(url) as response:
            return await response.json()

    async def close(self):
        await self.session.close()
