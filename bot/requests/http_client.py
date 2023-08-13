import typing
from functools import wraps

import aiohttp

from bot.authorization.backend import login


def handle_http_errors(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        response = await func(self, *args, **kwargs)
        try:
            if response.status == 401:
                # Logging
                self.logger.error(f"Unauthorized error, logging in...")
                await login(lambda: self, self.set_user, self.logger)
                return await func(self, *args, **kwargs)
        except AttributeError:
            return response
    return wrapper


class HttpClient:
    def __init__(
            self,
            set_auth_user,
            logger,
    ) -> None:
        self.set_user = set_auth_user
        timeout = aiohttp.ClientTimeout(total=10)
        self.session = aiohttp.ClientSession(timeout=timeout)
        self.logger = logger
        self.headers = {"Authorization": "Bearer Undefined"}

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

    async def post_raw(self, url: str, data) -> typing.Type[typing.Dict[str, typing.Any] | typing.List[typing.Dict[str, typing.Any]]]:
        """Only used for login because of the token potentially not stored in cookies yet"""
        self.log_request("POST", url, headers={}, data=data)
        async with self.session.post(url, data=data) as response:  # Changed json to data
            return await response.json()

    @handle_http_errors
    async def get(
            self, url: str,
    ) -> aiohttp.ClientResponse:
        self.log_request("GET", url, headers=self.headers)
        async with self.session.get(url, headers=self.headers) as response:
            if response.status == 401:
                return response
            return await response.json()

    @handle_http_errors
    async def post(
            self, url: str, data,
    ) -> aiohttp.ClientResponse:
        self.log_request("POST", url, self.headers, data=data)
        async with self.session.post(url, json=data, headers=self.headers) as response:
            if response.status == 401:
                return response
            return await response.json()

    @handle_http_errors
    async def put(
            self, url: str, data,
    ) -> aiohttp.ClientResponse:
        self.log_request("PUT", url, self.headers, data=data)
        async with self.session.put(url, json=data, headers=self.headers) as response:
            if response.status == 401:
                return response
            return await response.json()

    @handle_http_errors
    async def delete(
            self, url: str
    ) -> aiohttp.ClientResponse:
        self.log_request("DELETE", url, self.headers)
        async with self.session.delete(url, headers=self.headers) as response:
            if response.status == 401:
                return response
            return await response.json()

    async def close(self):
        await self.session.close()
