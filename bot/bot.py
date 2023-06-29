import logging
from logging import handlers

import discord
from aiohttp import web
from discord import Activity, ActivityType, Intents, ApplicationCommand
from discord.ext import commands

from bot.requests.http_client import HttpClient
from bot.authorization.backend import login
from settings import SERVER_PORT, SERVER_HOST, NOTIFICATION_ENDPOINT, NOTIFICATION_CHANNEL_ID


class PRDBot(commands.Bot):
    """The PRD Discord bot."""

    def __init__(self) -> None:
        # Bot
        activity = Activity(type=ActivityType.watching, name="Kalendar")
        intents = Intents.all()
        super().__init__(activity=activity, command_prefix="!", intents=intents)
        # Logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        file_handler = handlers.TimedRotatingFileHandler(
            filename="logs/discord.log", when="midnight", backupCount=7
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)-8s - %(name)s - %(funcName)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.ERROR)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        self.file_handler = file_handler
        self.stream_handler = stream_handler
        self.logger = logger

        # Backend
        self.auth_user = None
        self.http_client: HttpClient = HttpClient(self.get_token, self.set_auth_user)

    async def on_ready(self) -> None:
        print("------")
        print("Les Peaux Rouges - Discord Bot")
        print(self.user.name)
        print("------")

        # Get auth user
        await login(self.get_http_client, self.set_auth_user)
        await self.start_server()

    async def register_command(
            self, command: ApplicationCommand, force: bool = True, guild_ids: list[int] | None = None
    ) -> None:
        pass

    def get_token(self) -> str:
        if self.auth_user is None:
            return ""
        return self.auth_user.authorized_user.token

    def set_auth_user(self, auth_user) -> None:
        self.auth_user = auth_user

    def get_http_client(self):
        return lambda: self.http_client

    async def start_server(self):
        app = web.Application()
        app.router.add_post(NOTIFICATION_ENDPOINT, self.on_event)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner=runner, host=SERVER_HOST, port=SERVER_PORT)
        await site.start()
        print(f"Server started. Awaiting events on {NOTIFICATION_ENDPOINT}")

    async def on_event(self, request):
        # Extract event data from the request
        response = await request.json()
        event_operation = response['event_operation']
        event = response['event']

        # Announce the event update in a specific channel
        channel = await self.fetch_channel(NOTIFICATION_CHANNEL_ID)
        if channel:
            await channel.send(f"Event {event_operation}:\n{event}")

        return web.Response()
